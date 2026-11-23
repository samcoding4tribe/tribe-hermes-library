#!/usr/bin/env python3
"""Generate the TRIBE apps-and-agents questionnaire workbook.

    python3 questionnaire.py people.json questionnaire.xlsx

Two modes of use:
  - MS Forms: read the Questions sheet and build the form by hand, or import the
    sheet as a starting table. Forms cannot be created by script here because the
    Entra app is blocked, so the workbook is the authoring surface.
  - Analytics: Responses sheet defines the long-format table a Forms export
    should be reshaped into, so Power BI or pandas can pivot by role and division.

Stdlib + openpyxl, which the Hermes documents environment carries.
"""

import json
import sys

try:
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font, PatternFill
    from openpyxl.utils import get_column_letter
except ImportError:  # pragma: no cover
    print("openpyxl missing: use the documents environment", file=sys.stderr)
    raise

HEADER_FILL = PatternFill("solid", fgColor="1F3864")
HEADER_FONT = Font(color="FFFFFF", bold=True, size=10)
WRAP = Alignment(wrap_text=True, vertical="top")

# id, section, question, type, options, required, analytics field, what it tells us
QUESTIONS = [
    ("Q1", "About you", "Your name", "Short text", "", "Yes", "respondent_name",
     "Joins the response to the org map. Skip if the form collects names automatically."),
    ("Q2", "About you", "Your role", "Single choice",
     "Managing Director; General Manager; Operations Manager; Finance Manager; Design Manager; "
     "Event Director; Event Manager; Event Co-ordinator; Event Support; Luxury Travel Advisor; "
     "Travel Manager; Travel Co-ordinator; Executive Support; Other (please state)", "Yes", "role",
     "Stratifies every other answer by role, which is the unit an agent profile is built for."),
    ("Q3", "About you", "Which part of the business do you work in?", "Single choice",
     "Events; Travel; Both; Support function", "Yes", "division", "Separates the two operating businesses."),
    ("Q4", "About you", "Where do you work from?", "Single choice",
     "Melbourne office; Gold Coast; Philippines; Remote elsewhere", "Yes", "location",
     "Explains tool differences caused by location rather than by role."),
    ("Q5", "About you", "How long have you been at TRIBE?", "Single choice",
     "Under 3 months; 3-12 months; 1-3 years; 3-5 years; More than 5 years", "Yes", "tenure",
     "Long tenure with manual work is where agents pay back fastest."),

    ("Q6", "Apps you use", "How often do you use each of these?", "Grid (frequency)",
     "Daily; Weekly; Monthly; Rarely; Never", "Yes", "app_frequency",
     "The app list on sheet 'Apps'. Frequency separates daily habit from occasional use."),
    ("Q7", "Apps you use", "How important is each of these to doing your job?", "Grid (importance)",
     "Critical - I cannot work without it; Useful; Nice to have; Not needed", "Yes", "app_importance",
     "Importance tells us what a profile must not break. Frequency tells us what to automate first."),
    ("Q8", "Apps you use", "Which apps hold the same information twice?", "Multi choice",
     "See Apps sheet; plus 'Other (please name)'", "No", "duplicate_data",
     "Points at the homogenisation work: where two systems disagree about the same client or booking."),
    ("Q9", "Apps you use", "Which of these do you have access to but never use?", "Multi choice",
     "See Apps sheet; plus 'Other (please name)'", "No", "unused_apps",
     "Lapsed licences and tools bought for one person and forgotten."),

    ("Q10", "Where the time goes", "Which tasks take most of your week?", "Multi choice (max 3)",
     "Reading and answering email; Meetings and calls; Data entry or re-typing between systems; "
     "Chasing clients or suppliers; Preparing quotes and proposals; Building reports; "
     "Checking or reconciling records; Scheduling; Filing and admin; Other (please state)",
     "Yes", "top_time_tasks", "The shape of the role as it is lived, not as it is titled."),
    ("Q11", "Where the time goes", "Roughly how many hours a week go on repetitive work?", "Single choice",
     "Under 2; 2-5; 5-10; 10-20; More than 20", "Yes", "repetitive_hours",
     "The size of the prize. Pairs with Q10 to size an agent's value by role."),
    ("Q12", "Where the time goes", "How often do you re-type the same information into a second system?",
     "Single choice", "Several times a day; Daily; Weekly; Rarely; Never", "Yes", "retyping_frequency",
     "A direct measure of missing integration, which is what agents bridge first."),
    ("Q13", "Where the time goes", "What can you not find quickly when you need it?", "Long text", "",
     "No", "information_gaps",
     "Names the documents and records that should have a home. Feeds the vault and SharePoint design."),

    ("Q14", "Agents", "If an assistant could take three tasks off you, which three?", "Long text", "",
     "Yes", "agent_wishlist", "The demand signal. These become the first agent profiles worth building."),
    ("Q15", "Agents", "How comfortable are you with an assistant drafting your email for you?", "Scale 1-5",
     "1 = not at all; 5 = entirely comfortable", "Yes", "comfort_drafting",
     "Adoption risk by role. Drafting is the safest first capability to deploy."),
    ("Q16", "Agents", "How comfortable are you with an assistant reading your inbox and calendar?", "Scale 1-5",
     "1 = not at all; 5 = entirely comfortable", "Yes", "comfort_access",
     "Consent boundary. A low score here reroutes the deployment to shared mailboxes only."),
    ("Q17", "Agents", "What should an assistant never do without asking you first?", "Long text", "",
     "No", "agent_guardrails", "The per-role guardrails each deployed profile has to carry."),
    ("Q18", "Agents", "Who should approve an assistant's work before it goes out?", "Single choice",
     "Me; my manager; nobody, within agreed limits; other (please state)", "Yes", "approval_route",
     "Sets the approval path in the profile's instructions."),
    ("Q19", "One thing", "What one change would give you an hour back each week?", "Short text", "",
     "No", "single_ask", "The unprompted answer is usually the honest one."),
]

APPS = [
    ("Outlook", "Mail and calendar. The default surface every profile touches first.", "Organisation-wide"),
    ("Teams", "Chat, meetings and channels. Sam's notes say Outlook and Teams run in the browser.", "Organisation-wide"),
    ("SharePoint / OneDrive", "Where documents live. Relevant to the data homogenisation work.", "Organisation-wide"),
    ("Excel", "Reporting and reconciliation, including the EventsAir export Vanessa mentioned.", "Inferred from working threads"),
    ("Word", "Proposals and documents.", "Inferred"),
    ("PowerPoint", "Client presentations and pitches.", "Inferred"),
    ("Planner / To Do", "Task tracking, if used at all. Unknown as at 23 Nov.", "Assumed - verify"),
    ("Power Automate", "The August automation Iva referred to may run here.", "Inferred from Iva's mail"),
    ("Power BI", "Any existing reporting dashboards. Unknown.", "Assumed - verify"),
    ("EventsAir", "Events system. Named in Vanessa Crockett's draft about an export cross-check.", "Evidenced 23 Nov"),
    ("Sabre", "Travel software supplier; Iva is introducing Sam to their people.", "Evidenced 23 Nov"),
    ("Adobe / InDesign", "Dani's design work: the induction manual was produced in InDesign.", "Evidenced from the PDF metadata"),
    ("Claude / ChatGPT", "Unofficial AI use, which already exists in the business (the 'Claude stuff' thread).", "Evidenced 20 Nov"),
    ("Other (please name)", "Catch-all for booking engines, Xero or a CRM.", "Open"),
]

ANALYTICS = [
    ("respondent_id", "text", "One row per respondent per question; hash the name if the form is not anonymous."),
    ("role", "category", "From Q2. The primary cut for building an agent profile."),
    ("division", "category", "From Q3."),
    ("location", "category", "From Q4. Timezone and local tooling differences sit here."),
    ("tenure", "category", "From Q5."),
    ("app", "category", "Long-format only: one row per app per respondent for Q6 and Q7."),
    ("metric", "category", "frequency | importance | duplicate | unused"),
    ("value", "number or text", "Scale value, or the written answer."),
    ("question_id", "category", "Q1..Q19, so a new question does not break the model."),
    ("submitted_at", "datetime", "From the Forms export."),
]


def style(ws, widths):
    for i, w in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(i)].width = w
    for cell in ws[1]:
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT
        cell.alignment = Alignment(vertical="center", wrap_text=True)
    ws.freeze_panes = "A2"
    for row in ws.iter_rows(min_row=2):
        for cell in row:
            cell.alignment = WRAP


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    people_path, out = sys.argv[1], sys.argv[2]
    people = json.loads(open(people_path, encoding="utf-8").read())["people"]

    wb = Workbook()

    ws = wb.active
    if ws is None:
        raise RuntimeError("workbook has no active sheet")
    ws.title = "Instructions"
    rows = [
        ["TRIBE apps and agents questionnaire"],
        [""],
        ["Purpose", "Find out which applications each role depends on, where time is lost to manual work, "
                    "and what each person would hand to an assistant. The answers decide which agent profiles "
                    "are worth building and in what order."],
        ["Audience", f"{sum(1 for p in people if not p.get('external'))} people on the current org map. "
                     "See the Distribution sheet."],
        ["Length", "19 questions, about 8-10 minutes. Sections 2 and 3 are grids over the same app list."],
        ["How to build it", "Microsoft Forms > New form > copy each row from the Questions sheet. "
                           "Q6 and Q7 are Likert grids over the Apps column. Keep the question IDs in the "
                           "question text or a hidden label so exports map back cleanly."],
        ["Where to host it", "Forms for Excel is preferable: it writes responses straight into the workbook, "
                            "which keeps the analytics source of truth in one file. Otherwise export the Forms "
                            "responses to Excel and reshape to the long format on the Analytics sheet."],
        ["Sending it", "One link per role group if you want the answers attributed to a division without asking. "
                      "Anonymous responses cannot be joined to the org map, so prefer named for this round."],
        ["Cadence", "Send Monday, remind Thursday once, close the following Friday. One reminder, not three."],
        ["What good looks like", "A role where importance is high and repetitive hours are high is where an agent "
                                 "pays for itself first. A role where importance is low is a training problem, "
                                 "not an automation one."],
    ]
    for r in rows:
        ws.append(r)
    ws["A1"].font = Font(bold=True, size=13)
    ws.column_dimensions["A"].width = 20
    ws.column_dimensions["B"].width = 110
    for row in ws.iter_rows(min_row=3):
        row[0].font = Font(bold=True)
        row[1].alignment = WRAP

    ws = wb.create_sheet("Questions")
    ws.append(["ID", "Section", "Question", "Type", "Options / scale", "Required",
               "Analytics field", "What it tells us"])
    for q in QUESTIONS:
        ws.append(list(q))
    style(ws, [6, 18, 42, 18, 46, 9, 18, 46])

    ws = wb.create_sheet("Apps")
    ws.append(["App", "Why it is on the list", "Evidence"])
    for a in APPS:
        ws.append(list(a))
    style(ws, [26, 70, 30])

    ws = wb.create_sheet("Distribution")
    ws.append(["Name", "Role", "Division (map)", "Badges", "Notes"])
    for p in people:
        ws.append([p["name"], p.get("role", ""), p.get("function", ""),
                   ", ".join(p.get("badges") or []), (p.get("notes") or "")[:90]])
    style(ws, [26, 30, 18, 24, 60])

    ws = wb.create_sheet("Analytics")
    ws.append(["Field", "Type", "Description"])
    for a in ANALYTICS:
        ws.append(list(a))
    style(ws, [18, 16, 90])

    wb.save(out)
    print(f"wrote {out}: {len(QUESTIONS)} questions, {len(APPS)} apps, {len(people)} respondents")
    return 0


if __name__ == "__main__":
    sys.exit(main())

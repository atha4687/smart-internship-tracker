from __future__ import annotations

import html
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


OUT = Path("output/Smart_Internship_Tracker_Team_Speaking_Guide.docx")


def esc(text: str) -> str:
    return html.escape(text, quote=False)


def run(text: str, bold: bool = False, color: str | None = None, size: int | None = None) -> str:
    props: list[str] = []
    if bold:
        props.append("<w:b/>")
    if color:
        props.append(f'<w:color w:val="{color}"/>')
    if size:
        props.append(f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>')
    rpr = f"<w:rPr>{''.join(props)}</w:rPr>" if props else ""
    return f"<w:r>{rpr}<w:t xml:space=\"preserve\">{esc(text)}</w:t></w:r>"


def p(text: str = "", style: str | None = None, bold: bool = False, color: str | None = None,
      size: int | None = None, before: int | None = None, after: int | None = None) -> str:
    ppr_parts: list[str] = []
    if style:
        ppr_parts.append(f'<w:pStyle w:val="{style}"/>')
    spacing = []
    if before is not None:
        spacing.append(f'w:before="{before}"')
    if after is not None:
        spacing.append(f'w:after="{after}"')
    if spacing:
        ppr_parts.append(f"<w:spacing {' '.join(spacing)}/>")
    ppr = f"<w:pPr>{''.join(ppr_parts)}</w:pPr>" if ppr_parts else ""
    return f"<w:p>{ppr}{run(text, bold=bold, color=color, size=size)}</w:p>"


def bullet(text: str) -> str:
    return (
        '<w:p><w:pPr><w:pStyle w:val="Bullet"/>'
        '<w:ind w:left="720" w:hanging="360"/></w:pPr>'
        f'{run("• " + text)}</w:p>'
    )


def cell(content: str, shade: str | None = None, width: int = 4500) -> str:
    tcpr = f'<w:tcPr><w:tcW w:w="{width}" w:type="dxa"/>'
    if shade:
        tcpr += f'<w:shd w:fill="{shade}"/>'
    tcpr += "</w:tcPr>"
    return f"<w:tc>{tcpr}{content}</w:tc>"


def table(headers: list[str], rows: list[list[str]], widths: list[int] | None = None) -> str:
    widths = widths or [3000] * len(headers)
    grid = "".join(f'<w:gridCol w:w="{w}"/>' for w in widths)
    out = [
        '<w:tbl>',
        '<w:tblPr><w:tblStyle w:val="TableGrid"/><w:tblW w:w="0" w:type="auto"/>'
        '<w:tblLook w:firstRow="1" w:lastRow="0" w:firstColumn="0" w:lastColumn="0" w:noHBand="0" w:noVBand="1"/></w:tblPr>',
        f"<w:tblGrid>{grid}</w:tblGrid>",
        "<w:tr>",
    ]
    for i, h in enumerate(headers):
        out.append(cell(p(h, bold=True, color="FFFFFF"), shade="174C3C", width=widths[i]))
    out.append("</w:tr>")
    for row in rows:
        out.append("<w:tr>")
        for i, value in enumerate(row):
            paras = "".join(p(part, after=60) for part in value.split("\n"))
            out.append(cell(paras, width=widths[i]))
        out.append("</w:tr>")
    out.append("</w:tbl>")
    return "".join(out)


def section_heading(name: str, role: str) -> str:
    return p(f"{name} - {role}", "Heading1", color="174C3C", size=32, before=360, after=120)


def person_section(name: str, role: str, focus: str, lines: list[str], handoff: str) -> str:
    body = [section_heading(name, role)]
    body.append(p(f"Main focus: {focus}", bold=True, color="28785F", after=120))
    body.append(p("What to say:", "Heading2", color="1E2735", size=24, before=120, after=80))
    for line in lines:
        body.append(bullet(line))
    body.append(p(f"Handoff line: {handoff}", bold=True, color="3157D5", before=120, after=180))
    return "".join(body)


def document_xml() -> str:
    roles = [
        ["Alhaji Kargbo", "Project Manager", "Open the presentation, explain the project goal, introduce the team, and describe coordination/timeline."],
        ["Renae Washington", "Software Architect", "Explain the system design, Flask/MySQL architecture, tables, and why the structure supports user privacy."],
        ["Langston Gwinn", "Backend Developer", "Explain server-side routes, login/session behavior, database integration, CRUD features, and validation."],
        ["Quincy King", "Frontend Developer", "Explain the dashboard interface, user experience choices, responsive layout, forms, search, filters, and status badges."],
        ["Ali-Andro Thaxter", "Software Tester", "Explain the test plan, test results, bug checks, security-related tests, and overall quality conclusion."],
    ]

    body: list[str] = []
    body.append(p("Smart Internship Tracker", "Title", color="174C3C", size=48, after=80))
    body.append(p("Team Speaking Guide and Potential Questions", "Subtitle", color="657284", size=28, after=240))
    body.append(p("Use this guide to divide the final presentation clearly. Each person should speak from their role, explain what they contributed, and connect their part back to the full Smart Internship Tracker application.", after=180))
    body.append(p("Presentation Order", "Heading1", color="174C3C", size=32, before=240, after=120))
    body.append(table(["Speaker", "Role", "What They Cover"], roles, [2400, 2600, 5200]))

    body.append(p("Short Opening Script", "Heading1", color="174C3C", size=32, before=360, after=120))
    body.append(p("Good opener for Alhaji:", bold=True, color="28785F"))
    body.append(p("Good morning/afternoon. Our project is called Smart Internship Tracker. The purpose of our application is to help students organize internship and job applications in one place. Students can register, log in, add applications, update application statuses, search and filter records, track deadlines, and delete entries when needed. Today, each team member will explain the part they were responsible for and how it helped us build a complete working system."))

    body.append(person_section(
        "Alhaji Kargbo",
        "Project Manager",
        "Team coordination, timeline, organization, and overall completion.",
        [
            "I served as the project manager, so my role was to keep the team organized and make sure everyone understood their responsibilities.",
            "I helped coordinate the project timeline so the architecture, backend, frontend, and testing work could come together as one finished application.",
            "The main problem we wanted to solve was that students often track internships in scattered places like notes, spreadsheets, emails, or memory. Our app gives them one organized dashboard.",
            "I also made sure we stayed focused on the required features: registration, login, adding applications, updating statuses, searching, filtering, and deleting records.",
            "From a project-management view, our biggest success was dividing the work by role while keeping the final app consistent.",
        ],
        "Next, Renae will explain how the system was designed and how the database supports the application.",
    ))

    body.append(person_section(
        "Renae Washington",
        "Software Architect",
        "System design, database structure, and overall architecture decisions.",
        [
            "As software architect, I focused on how the application should be structured before and during development.",
            "The system uses Flask for the web application, HTML and CSS for the user interface, and MySQL through XAMPP for storing users and internship records.",
            "The database has two main tables: users and internships. The users table stores account information, and the internships table stores company, role, status, deadline, notes, and user_id.",
            "The user_id field connects each application to the correct user, which helps keep each student's records separate.",
            "This architecture is simple enough for our class project but still shows important design ideas: authentication, database relationships, route protection, and user-specific data.",
        ],
        "Now Langston will explain the backend logic that makes those features work.",
    ))

    body.append(person_section(
        "Langston Gwinn",
        "Backend Developer",
        "Server-side logic, database integration, routes, and application functionality.",
        [
            "As backend developer, my role was to implement the logic behind the web pages and connect the application to the database.",
            "The Flask routes handle the main workflows: home, register, login, logout, dashboard, add application, update status, and delete application.",
            "For registration and login, the backend checks the database, stores secure password hashes, and uses sessions so the app knows which user is signed in.",
            "For the dashboard, the backend retrieves only the applications that belong to the logged-in user. It also handles search by company or role and filtering by application status.",
            "The add, update, and delete routes use database queries to make changes, and they check required fields and valid statuses before saving data.",
        ],
        "Next, Quincy will discuss how the user sees and interacts with these features on the frontend.",
    ))

    body.append(person_section(
        "Quincy King",
        "Frontend Developer",
        "User interface design, responsiveness, usability, and dashboard experience.",
        [
            "As frontend developer, I focused on making the application clear, organized, and easy for students to use.",
            "The homepage introduces the Smart Internship Tracker and gives users a clear starting point to register or go to the dashboard.",
            "The dashboard is the main workspace. It includes quick stats, a search and filter section, a table of applications, status update controls, delete buttons, and a form for adding a new application.",
            "The interface uses status badges so users can quickly see whether an application is Applied, Interview, Offered, or Rejected.",
            "The CSS uses a clean career-planning style with green, mint, blue, and gold accents. The goal was to make the app feel organized and professional without being confusing.",
        ],
        "Ali-Andro will finish by explaining how the system was tested and how we confirmed the quality of the project.",
    ))

    body.append(person_section(
        "Ali-Andro Thaxter",
        "Software Tester",
        "Testing workflows, identifying bugs, checking validation, and confirming software quality.",
        [
            "As software tester, my responsibility was to make sure the application worked correctly and handled common errors.",
            "I created and used a test plan with 20 test cases covering startup, registration, login, protected pages, adding applications, searching, filtering, updating statuses, deleting applications, logout, validation, and database behavior.",
            "The tests confirmed that users can complete the main workflow from creating an account all the way to managing internship applications on the dashboard.",
            "I also tested error conditions such as blank registration fields, duplicate usernames, invalid login attempts, invalid status values, and trying to access the dashboard without logging in.",
            "Security-related testing included checking SQL-like input and confirming that each user only sees their own application records.",
            "Overall, the project passed the planned functional, validation, security, and syntax-related tests.",
        ],
        "That concludes our role breakdown. We are ready to answer questions about the project.",
    ))

    body.append(p("Possible Questions and Strong Answers", "Heading1", color="174C3C", size=32, before=360, after=120))
    qa = [
        ["What problem does your project solve?", "It helps students organize internship and job applications in one place instead of spreading information across emails, notes, spreadsheets, and memory. The dashboard keeps company names, roles, statuses, deadlines, and notes together."],
        ["Who is the target user?", "The main target user is a student applying for internships or entry-level jobs. The app is designed for someone who needs a simple way to track multiple opportunities and their progress."],
        ["What are the main features?", "The main features are registration, login, dashboard viewing, adding applications, updating statuses, deleting applications, searching by company or role, filtering by status, and tracking deadlines and notes."],
        ["Why did you use Flask?", "Flask is lightweight and good for a class web application because it lets us build routes, templates, sessions, and database logic clearly without too much extra complexity."],
        ["Why did you use MySQL?", "MySQL gives the project a real relational database structure. It lets us separate users from internship records and connect them with a user_id foreign key."],
        ["How do you protect each user's information?", "The dashboard queries use the logged-in user's user_id, so users only see their own applications. Protected routes also require a login session before the page can be accessed."],
        ["How are passwords handled?", "New passwords are stored as hashes using pbkdf2:sha256, which is safer than saving plain-text passwords."],
        ["What was the hardest part?", "A strong answer is: connecting all parts into one smooth workflow. The database, routes, forms, dashboard, validation, and testing all had to work together."],
        ["How did you test the project?", "We used a written test plan with 20 test cases. The tests covered normal workflows, error cases, security-related input, protected routes, database behavior, and syntax checks."],
        ["What would you improve next?", "Future improvements could include deadline reminders, file uploads for resumes and cover letters, analytics showing application progress, and deployment so students can use it online."],
        ["What did each person contribute?", "Each person had a defined role: project management, architecture, backend, frontend, and testing. The final project came together because those responsibilities supported each other."],
        ["Is the project complete?", "For the class project, yes. It includes the core required workflows and passed the planned test cases. There are also clear future improvements for a larger version."],
    ]
    body.append(table(["Potential Question", "Suggested Answer"], qa, [3600, 6600]))

    body.append(p("Quick Team Practice Tips", "Heading1", color="174C3C", size=32, before=360, after=120))
    tips = [
        "Do not read every word. Use the guide as a speaking outline.",
        "Each speaker should mention their role in the first sentence.",
        "Keep transitions smooth by using the handoff lines.",
        "Use the same project language: Smart Internship Tracker, dashboard, Flask, MySQL, users table, internships table, status updates, search, filter, and test plan.",
        "If a question is technical and you are not the role owner, answer briefly and invite the teammate responsible for that part to add detail.",
        "End confidently: the app meets the main project goals and has clear next-step improvements.",
    ]
    for tip in tips:
        body.append(bullet(tip))

    body.append(p("Closing Script", "Heading1", color="174C3C", size=32, before=360, after=120))
    body.append(p("To conclude, Smart Internship Tracker gives students a simple and organized way to manage internship and job applications. Our team built the project with Flask, MySQL, HTML, and CSS, and we divided the work across project management, architecture, backend development, frontend development, and testing. The final system supports registration, login, application tracking, searching, filtering, updating, deleting, and user-specific data privacy. Thank you for listening. We are ready for questions."))

    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:body>
    {''.join(body)}
    <w:sectPr>
      <w:pgSz w:w="12240" w:h="15840"/>
      <w:pgMar w:top="900" w:right="900" w:bottom="900" w:left="900" w:header="720" w:footer="720" w:gutter="0"/>
    </w:sectPr>
  </w:body>
</w:document>'''


def styles_xml() -> str:
    return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:style w:type="paragraph" w:default="1" w:styleId="Normal">
    <w:name w:val="Normal"/>
    <w:qFormat/>
    <w:pPr><w:spacing w:after="120" w:line="276" w:lineRule="auto"/></w:pPr>
    <w:rPr><w:rFonts w:ascii="Aptos" w:hAnsi="Aptos"/><w:sz w:val="22"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Title">
    <w:name w:val="Title"/><w:basedOn w:val="Normal"/><w:qFormat/>
    <w:pPr><w:spacing w:after="120"/></w:pPr>
    <w:rPr><w:b/><w:rFonts w:ascii="Aptos Display" w:hAnsi="Aptos Display"/><w:sz w:val="48"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Subtitle">
    <w:name w:val="Subtitle"/><w:basedOn w:val="Normal"/><w:qFormat/>
    <w:rPr><w:rFonts w:ascii="Aptos" w:hAnsi="Aptos"/><w:sz w:val="28"/><w:color w:val="657284"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading1">
    <w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/>
    <w:pPr><w:keepNext/><w:spacing w:before="360" w:after="120"/></w:pPr>
    <w:rPr><w:b/><w:rFonts w:ascii="Aptos Display" w:hAnsi="Aptos Display"/><w:sz w:val="32"/><w:color w:val="174C3C"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading2">
    <w:name w:val="heading 2"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/>
    <w:pPr><w:keepNext/><w:spacing w:before="180" w:after="80"/></w:pPr>
    <w:rPr><w:b/><w:rFonts w:ascii="Aptos" w:hAnsi="Aptos"/><w:sz w:val="24"/><w:color w:val="1E2735"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Bullet">
    <w:name w:val="Bullet"/><w:basedOn w:val="Normal"/><w:qFormat/>
    <w:pPr><w:spacing w:after="80"/></w:pPr>
    <w:rPr><w:rFonts w:ascii="Aptos" w:hAnsi="Aptos"/><w:sz w:val="21"/></w:rPr>
  </w:style>
  <w:style w:type="table" w:styleId="TableGrid">
    <w:name w:val="Table Grid"/><w:basedOn w:val="TableNormal"/><w:uiPriority w:val="59"/><w:qFormat/>
    <w:tblPr><w:tblBorders><w:top w:val="single" w:sz="6" w:space="0" w:color="D9E2E7"/><w:left w:val="single" w:sz="6" w:space="0" w:color="D9E2E7"/><w:bottom w:val="single" w:sz="6" w:space="0" w:color="D9E2E7"/><w:right w:val="single" w:sz="6" w:space="0" w:color="D9E2E7"/><w:insideH w:val="single" w:sz="6" w:space="0" w:color="D9E2E7"/><w:insideV w:val="single" w:sz="6" w:space="0" w:color="D9E2E7"/></w:tblBorders><w:tblCellMar><w:top w:w="120" w:type="dxa"/><w:left w:w="120" w:type="dxa"/><w:bottom w:w="120" w:type="dxa"/><w:right w:w="120" w:type="dxa"/></w:tblCellMar></w:tblPr>
  </w:style>
</w:styles>'''


def content_types_xml() -> str:
    return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
  <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
  <Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
</Types>'''


def rels_xml() -> str:
    return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>'''


def document_rels_xml() -> str:
    return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>'''


def core_xml() -> str:
    return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/">
  <dc:title>Smart Internship Tracker Team Speaking Guide</dc:title>
  <dc:creator>Ali-Andro Thaxter team</dc:creator>
  <cp:lastModifiedBy>Codex</cp:lastModifiedBy>
</cp:coreProperties>'''


def app_xml() -> str:
    return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties">
  <Application>Microsoft Word</Application>
</Properties>'''


def write_docx() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(OUT, "w", ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", content_types_xml())
        z.writestr("_rels/.rels", rels_xml())
        z.writestr("word/document.xml", document_xml())
        z.writestr("word/_rels/document.xml.rels", document_rels_xml())
        z.writestr("word/styles.xml", styles_xml())
        z.writestr("docProps/core.xml", core_xml())
        z.writestr("docProps/app.xml", app_xml())
    print(OUT)


if __name__ == "__main__":
    write_docx()

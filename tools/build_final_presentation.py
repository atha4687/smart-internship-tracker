from __future__ import annotations

import html
import os
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


OUT = Path("output/Smart_Internship_Tracker_Final_Presentation.pptx")
HERO = Path("static/images/internship-hero.png")

SLIDE_W = 12192000
SLIDE_H = 6858000
EMU = 914400


def emu(value: float) -> int:
    return int(value * EMU)


def esc(value: str) -> str:
    return html.escape(value, quote=True)


COLORS = {
    "ink": "1E2735",
    "muted": "657284",
    "green_dark": "174C3C",
    "green": "28785F",
    "mint": "DFF7EA",
    "mint_soft": "F2FBF6",
    "blue": "3157D5",
    "gold": "D99B2B",
    "line": "D9E2E7",
    "white": "FFFFFF",
    "danger": "D33B35",
    "paper": "F8FBFA",
}


class Slide:
    def __init__(self, title: str, bg: str = "F8FBFA") -> None:
        self.title = title
        self.bg = bg
        self.parts: list[str] = []
        self.rels: list[tuple[str, str, str]] = []
        self.next_id = 2

    def rid(self, target: str, rel_type: str) -> str:
        rid = f"rId{len(self.rels) + 2}"
        self.rels.append((rid, rel_type, target))
        return rid

    def shape_id(self) -> int:
        value = self.next_id
        self.next_id += 1
        return value


def rgb(color: str) -> str:
    return color.replace("#", "").upper()


def fill_xml(color: str | None) -> str:
    if color is None:
        return "<a:noFill/>"
    return f'<a:solidFill><a:srgbClr val="{rgb(color)}"/></a:solidFill>'


def line_xml(color: str | None = None, width: int = 12700) -> str:
    if color is None:
        return "<a:ln><a:noFill/></a:ln>"
    return f'<a:ln w="{width}"><a:solidFill><a:srgbClr val="{rgb(color)}"/></a:solidFill></a:ln>'


def rect(slide: Slide, x: float, y: float, w: float, h: float, fill: str | None,
         line: str | None = None, radius: str = "rect", name: str = "shape") -> None:
    sid = slide.shape_id()
    slide.parts.append(f"""
      <p:sp>
        <p:nvSpPr><p:cNvPr id="{sid}" name="{esc(name)}"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
        <p:spPr>
          <a:xfrm><a:off x="{emu(x)}" y="{emu(y)}"/><a:ext cx="{emu(w)}" cy="{emu(h)}"/></a:xfrm>
          <a:prstGeom prst="{radius}"><a:avLst/></a:prstGeom>
          {fill_xml(fill)}
          {line_xml(line)}
        </p:spPr>
      </p:sp>""")


def line(slide: Slide, x: float, y: float, w: float, color: str, width: int = 28575) -> None:
    sid = slide.shape_id()
    slide.parts.append(f"""
      <p:cxnSp>
        <p:nvCxnSpPr><p:cNvPr id="{sid}" name="rule"/><p:cNvCxnSpPr/><p:nvPr/></p:nvCxnSpPr>
        <p:spPr>
          <a:xfrm><a:off x="{emu(x)}" y="{emu(y)}"/><a:ext cx="{emu(w)}" cy="0"/></a:xfrm>
          <a:prstGeom prst="line"><a:avLst/></a:prstGeom>
          {line_xml(color, width)}
        </p:spPr>
      </p:cxnSp>""")


def paragraph(text: str, size: int, color: str, bold: bool = False, align: str = "l") -> str:
    b = ' b="1"' if bold else ""
    return f"""
        <a:p>
          <a:pPr algn="{align}"/>
          <a:r>
            <a:rPr lang="en-US" sz="{size}"{b}>
              <a:solidFill><a:srgbClr val="{rgb(color)}"/></a:solidFill>
              <a:latin typeface="Aptos"/>
            </a:rPr>
            <a:t>{esc(text)}</a:t>
          </a:r>
          <a:endParaRPr lang="en-US" sz="{size}"/>
        </a:p>"""


def text_box(slide: Slide, text: str | list[str], x: float, y: float, w: float, h: float,
             size: int = 2600, color: str = "1E2735", bold: bool = False,
             align: str = "l", name: str = "text", fill: str | None = None,
             line_color: str | None = None, margin: int = 91440) -> None:
    sid = slide.shape_id()
    lines = text if isinstance(text, list) else [text]
    paras = "".join(paragraph(t, size, color, bold, align) for t in lines)
    slide.parts.append(f"""
      <p:sp>
        <p:nvSpPr><p:cNvPr id="{sid}" name="{esc(name)}"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>
        <p:spPr>
          <a:xfrm><a:off x="{emu(x)}" y="{emu(y)}"/><a:ext cx="{emu(w)}" cy="{emu(h)}"/></a:xfrm>
          <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
          {fill_xml(fill)}
          {line_xml(line_color)}
        </p:spPr>
        <p:txBody>
          <a:bodyPr wrap="square" anchor="t" lIns="{margin}" tIns="{margin}" rIns="{margin}" bIns="{margin}"/>
          <a:lstStyle/>
          {paras}
        </p:txBody>
      </p:sp>""")


def pill(slide: Slide, label: str, x: float, y: float, w: float, color: str, text_color: str = "FFFFFF") -> None:
    rect(slide, x, y, w, 0.42, color, None, "roundRect", "pill")
    text_box(slide, label, x + 0.08, y + 0.04, w - 0.16, 0.32, 1350, text_color, True, "ctr", "pill-label", margin=0)


def add_image(slide: Slide, path: str, x: float, y: float, w: float, h: float, name: str = "image") -> None:
    rid = slide.rid("../media/internship-hero.png", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/image")
    sid = slide.shape_id()
    slide.parts.append(f"""
      <p:pic>
        <p:nvPicPr><p:cNvPr id="{sid}" name="{esc(name)}"/><p:cNvPicPr><a:picLocks noChangeAspect="1"/></p:cNvPicPr><p:nvPr/></p:nvPicPr>
        <p:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></p:blipFill>
        <p:spPr><a:xfrm><a:off x="{emu(x)}" y="{emu(y)}"/><a:ext cx="{emu(w)}" cy="{emu(h)}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr>
      </p:pic>""")


def title(slide: Slide, title_text: str, subtitle: str | None = None) -> None:
    text_box(slide, title_text, 0.65, 0.42, 8.9, 0.66, 3150, COLORS["ink"], True, name="title", margin=0)
    line(slide, 0.65, 1.18, 1.25, COLORS["gold"], 32000)
    if subtitle:
        text_box(slide, subtitle, 0.65, 1.30, 8.8, 0.42, 1500, COLORS["muted"], name="subtitle", margin=0)


def footer(slide: Slide, index: int) -> None:
    text_box(slide, f"Smart Internship Tracker | Final Presentation | {index:02d}", 0.65, 7.05, 4.2, 0.24, 850, "7C8797", name="footer", margin=0)


def build_slides() -> list[Slide]:
    slides: list[Slide] = []

    s = Slide("Cover", "0C261F")
    rect(s, 0, 0, 13.333, 7.5, "0C261F", None, name="dark field")
    add_image(s, str(HERO), 6.05, 0.75, 6.5, 4.15, "internship workspace hero")
    rect(s, 6.25, 0.98, 5.92, 3.7, None, COLORS["gold"], "rect", "image frame")
    pill(s, "Final project presentation", 0.72, 0.78, 2.8, COLORS["green"])
    text_box(s, "Smart Internship Tracker", 0.72, 1.48, 5.4, 1.65, 4300, COLORS["white"], True, name="cover-title", margin=0)
    text_box(s, "A Flask and MySQL web app that helps students organize applications, deadlines, statuses, and notes in one place.", 0.76, 3.28, 5.45, 0.9, 1700, "DDEFE7", name="cover-subtitle", margin=0)
    text_box(s, "Team collaboration: GitHub repository for shared code, project files, and documentation.", 0.76, 4.42, 5.65, 0.5, 1250, "9BE6BD", True, name="github-line", margin=0)
    text_box(s, "Team: Alhaji Kargbo, Renae Washington, Langston Gwinn, Quincy King, Ali-Andro Thaxter", 0.76, 6.55, 5.9, 0.5, 1180, "B9D7CC", name="team-line", margin=0)
    slides.append(s)

    s = Slide("Roadmap")
    title(s, "Rubric-Aligned Roadmap", "10 minutes for presentation and live demo, then up to 5 minutes for Q&A.")
    roadmap = ["Problem", "Scope + features", "Methodology", "Design", "Code structure", "Collaboration", "Testing", "Live demo", "Team contribution"]
    for i, item in enumerate(roadmap):
        x = 0.75 + (i % 3) * 4.05
        y = 1.95 + (i // 3) * 1.32
        rect(s, x, y, 3.45, 0.9, COLORS["white"], COLORS["line"], "roundRect", item)
        text_box(s, f"{i + 1}", x + 0.2, y + 0.22, 0.38, 0.25, 1050, COLORS["gold"], True, "ctr", margin=0)
        text_box(s, item, x + 0.72, y + 0.22, 2.35, 0.25, 1180, COLORS["ink"], True, margin=0)
    footer(s, 2)
    slides.append(s)

    s = Slide("Problem Statement")
    title(s, "1. Problem Statement", "Internship searches create scattered information, missed deadlines, and unclear next steps.")
    labels = [
        ("Problem", "Students often track companies, roles, statuses, deadlines, and notes in too many places."),
        ("Motivation", "A single dashboard makes the search less stressful and reduces missed follow-ups."),
        ("Target users", "Students applying for internships, co-ops, and entry-level roles."),
    ]
    for i, (h, body) in enumerate(labels):
        x = 0.75 + i * 4.1
        rect(s, x, 2.35, 3.45, 2.75, COLORS["white"], COLORS["line"], "roundRect", h)
        text_box(s, h, x + 0.25, 2.72, 2.7, 0.45, 1900, COLORS["green_dark"], True, margin=0)
        text_box(s, body, x + 0.25, 3.43, 2.8, 0.92, 1180, COLORS["muted"], margin=0)
    text_box(s, "Goal: give each student a private, searchable command center for their internship process.", 1.08, 5.85, 11.0, 0.52, 1800, COLORS["green_dark"], True, "ctr", fill=COLORS["mint"], line_color=None)
    footer(s, 3)
    slides.append(s)

    s = Slide("Scope and Features")
    title(s, "2. Scope and Features", "We built a focused tracker, not a full recruiting platform.")
    columns = [
        ("In Scope", ["Register/login", "Private dashboard", "Add/view/update/delete applications", "Search, filter, deadlines, notes"]),
        ("Out of Scope", ["Employer portal", "Automatic job scraping", "Cloud deployment", "Resume upload storage"]),
        ("Since Deliverable 2", ["Password hashing", "Stronger validation", "Polished dashboard UI", "Completed test plan/results"]),
    ]
    for i, (h, lines) in enumerate(columns):
        x = 0.75 + i * 4.1
        rect(s, x, 1.95, 3.45, 3.35, COLORS["white"], COLORS["line"], "roundRect", h)
        text_box(s, h, x + 0.25, 2.24, 2.7, 0.35, 1600, COLORS["green_dark"], True, margin=0)
        text_box(s, lines, x + 0.25, 2.85, 2.85, 1.55, 1080, COLORS["muted"], margin=0)
    text_box(s, "Promised features: registration, login, dashboard, add, update status, delete, search/filter, deadline and notes tracking.", 0.95, 6.15, 11.4, 0.45, 1350, COLORS["green_dark"], True, "ctr", fill=COLORS["mint"], margin=0)
    footer(s, 4)
    slides.append(s)

    s = Slide("Methodology")
    title(s, "3. Software Development Methodology", "We followed an iterative Agile-style process: build, review, test, improve.")
    phases = [("Plan", "roles + scope"), ("Build", "feature increments"), ("Review", "GitHub updates"), ("Test", "20 cases"), ("Improve", "fix + document")]
    for i, (h, b) in enumerate(phases):
        x = 0.75 + i * 2.48
        rect(s, x, 2.45, 1.9, 1.35, COLORS["mint_soft"], COLORS["line"], "roundRect", h)
        text_box(s, h, x + 0.2, 2.7, 1.5, 0.25, 1250, COLORS["green_dark"], True, "ctr", margin=0)
        text_box(s, b, x + 0.2, 3.08, 1.5, 0.25, 850, COLORS["muted"], False, "ctr", margin=0)
        if i < 4:
            line(s, x + 1.95, 3.08, 0.32, COLORS["gold"], 22000)
    text_box(s, "Why this methodology: it let each role work on a clear part while the team integrated and tested features as the app grew.", 1.0, 5.3, 11.2, 0.55, 1500, COLORS["green_dark"], True, "ctr", fill=COLORS["mint"], margin=0)
    footer(s, 5)
    slides.append(s)

    s = Slide("Design Artifacts")
    title(s, "4. Design Artifacts", "Context diagram, architecture diagram, ERD, and workflow explain how the system fits together.")
    artifacts = [
        ("Context", ["Student user", "Smart Internship Tracker", "Local browser + MySQL"]),
        ("Architecture", ["HTML/CSS templates", "Flask routes + sessions", "MySQL database"]),
        ("ERD", ["users table", "internships table", "1 user -> many records"]),
        ("Workflow", ["Register", "Login", "Dashboard CRUD", "Logout"]),
    ]
    for i, (h, lines) in enumerate(artifacts):
        x = 0.75 + (i % 2) * 6.05
        y = 1.82 + (i // 2) * 2.0
        rect(s, x, y, 5.25, 1.4, COLORS["white"], COLORS["line"], "roundRect", h)
        text_box(s, h, x + 0.25, y + 0.2, 1.7, 0.28, 1320, COLORS["green_dark"], True, margin=0)
        text_box(s, lines, x + 2.05, y + 0.2, 2.8, 0.72, 900, COLORS["muted"], margin=0)
    text_box(s, "These designs guided database ownership, protected routes, and the demo workflow.", 1.05, 6.12, 11.2, 0.45, 1400, COLORS["green_dark"], True, "ctr", fill=COLORS["mint"], margin=0)
    footer(s, 6)
    slides.append(s)

    s = Slide("Architecture")
    title(s, "4. Architecture Diagram", "A simple Flask web app connects protected user routes to a MySQL-backed application database.")
    blocks = [
        (0.8, 2.0, "Frontend", "HTML templates + CSS\nResponsive dashboard UI"),
        (4.85, 2.0, "Flask Backend", "Routes, sessions, validation\nCRUD application logic"),
        (8.9, 2.0, "MySQL Database", "users table\ninternships table"),
    ]
    for x, y, h, b in blocks:
        rect(s, x, y, 3.25, 2.05, COLORS["white"], COLORS["line"], "roundRect", h)
        text_box(s, h, x + 0.25, y + 0.25, 2.6, 0.38, 1800, COLORS["green_dark"], True, margin=0)
        text_box(s, b.split("\n"), x + 0.25, y + 0.84, 2.7, 0.82, 1200, COLORS["muted"], margin=0)
    line(s, 4.1, 3.02, 0.6, COLORS["gold"], 36000)
    line(s, 8.15, 3.02, 0.6, COLORS["gold"], 36000)
    text_box(s, "Key implementation details", 0.85, 5.0, 3.2, 0.32, 1600, COLORS["ink"], True, margin=0)
    text_box(s, ["Password hashing with pbkdf2:sha256", "Protected routes through a login_required decorator", "Parameterized SQL queries for safer database access", "User-specific dashboard queries filtered by user_id"], 0.88, 5.42, 10.9, 1.0, 1250, COLORS["muted"], margin=0)
    footer(s, 7)
    slides.append(s)

    s = Slide("Database")
    title(s, "4. ERD: Database Design", "Two tables keep accounts separate from application records while preserving ownership.")
    rect(s, 1.0, 2.0, 4.6, 3.0, COLORS["white"], COLORS["line"], "roundRect", "users")
    text_box(s, "users", 1.3, 2.28, 3.8, 0.35, 1900, COLORS["green_dark"], True, margin=0)
    text_box(s, ["id INT AUTO_INCREMENT PRIMARY KEY", "username VARCHAR(100) UNIQUE", "password VARCHAR(255)"], 1.3, 2.9, 3.7, 1.1, 1200, COLORS["muted"], margin=0)
    rect(s, 7.25, 1.55, 4.9, 3.9, COLORS["white"], COLORS["line"], "roundRect", "internships")
    text_box(s, "internships", 7.55, 1.86, 3.8, 0.35, 1900, COLORS["green_dark"], True, margin=0)
    text_box(s, ["id, company, role, status", "deadline DATE", "notes TEXT", "user_id INT FOREIGN KEY", "ON DELETE CASCADE"], 7.55, 2.47, 4.0, 1.55, 1200, COLORS["muted"], margin=0)
    line(s, 5.75, 3.38, 1.25, COLORS["gold"], 38000)
    text_box(s, "1 user -> many applications", 4.95, 4.0, 2.8, 0.32, 1120, COLORS["gold"], True, "ctr", margin=0)
    text_box(s, "Design value: each student sees only their own internship records, and deleting an account can remove dependent records cleanly.", 1.15, 6.0, 10.8, 0.52, 1550, COLORS["green_dark"], True, "ctr", fill=COLORS["mint"], margin=0)
    footer(s, 8)
    slides.append(s)

    s = Slide("Code Structure")
    title(s, "5. Code Structure Overview", "Open VS Code during the presentation and walk through these files.")
    files = [
        ("app.py", "Routes, sessions, database connection, validation, password hashing, CRUD logic."),
        ("templates/", "layout, homepage, register, login, dashboard pages rendered with Jinja."),
        ("static/style.css", "Responsive styling, cards, forms, buttons, tables, and status badges."),
        ("README.md", "Project overview, setup instructions, run steps, technologies, and team list."),
        ("TEST_PLAN_AND_RESULTS.md", "Testing scope, expected output, actual output, and pass/fail results."),
    ]
    for i, (h, b) in enumerate(files):
        y = 1.9 + i * 0.78
        text_box(s, h, 0.9, y, 2.2, 0.28, 1200, COLORS["green_dark"], True, margin=0)
        text_box(s, b, 3.35, y, 8.6, 0.3, 1050, COLORS["muted"], margin=0)
        line(s, 0.9, y + 0.45, 11.15, COLORS["line"], 8500)
    text_box(s, "Component interaction: browser form -> Flask route -> MySQL query -> dashboard template renders updated records.", 1.0, 6.08, 11.35, 0.5, 1350, COLORS["green_dark"], True, "ctr", fill=COLORS["mint"], margin=0)
    footer(s, 9)
    slides.append(s)

    s = Slide("Collaboration")
    title(s, "6. Collaboration and Documentation", "We used GitHub as the team's collaboration hub.")
    rect(s, 0.85, 1.9, 5.55, 3.55, COLORS["white"], COLORS["line"], "roundRect", "github")
    text_box(s, "GitHub Usage", 1.15, 2.18, 3.0, 0.32, 1600, COLORS["green_dark"], True, margin=0)
    text_box(s, ["Shared repository for project code", "Commits tracked changes over time", "Role-based updates before integration", "Repository used to keep files consistent"], 1.15, 2.8, 4.35, 1.25, 1080, COLORS["muted"], margin=0)
    rect(s, 6.95, 1.9, 5.55, 3.55, COLORS["white"], COLORS["line"], "roundRect", "docs")
    text_box(s, "Documentation", 7.25, 2.18, 3.0, 0.32, 1600, COLORS["green_dark"], True, margin=0)
    text_box(s, ["README for setup and project overview", "Docstrings/comments for important functions", "Test plan documents quality checks", "Speaking guide divides presentation roles"], 7.25, 2.8, 4.35, 1.25, 1080, COLORS["muted"], margin=0)
    text_box(s, "Team communication: check-ins were used to coordinate timeline, resolve integration issues, and prepare the final demo.", 1.0, 6.05, 11.35, 0.5, 1350, COLORS["green_dark"], True, "ctr", fill=COLORS["mint"], margin=0)
    footer(s, 10)
    slides.append(s)

    s = Slide("Testing")
    title(s, "7. Testing", "The system passed planned functional, validation, security, and startup tests.")
    rect(s, 0.85, 2.1, 3.0, 2.55, "174C3C", None, "roundRect", "test count")
    text_box(s, "20", 1.25, 2.55, 2.1, 0.9, 5200, COLORS["white"], True, "ctr", margin=0)
    text_box(s, "planned test cases passed", 1.05, 3.65, 2.6, 0.42, 1400, "DDEFE7", True, "ctr", margin=0)
    focus = [("UI workflow", "registration, login, dashboard, logout"), ("Integration", "Flask routes connected to MySQL records"), ("Application CRUD", "add, update status, delete records"), ("Error/security", "duplicates, invalid login, SQL-like input, MySQL stopped")]
    for i, (h, b) in enumerate(focus):
        x = 4.35 + (i % 2) * 4.0
        y = 2.05 + (i // 2) * 1.55
        rect(s, x, y, 3.45, 1.12, COLORS["white"], COLORS["line"], "roundRect", h)
        text_box(s, h, x + 0.22, y + 0.18, 2.9, 0.25, 1280, COLORS["ink"], True, margin=0)
        text_box(s, b, x + 0.22, y + 0.55, 2.9, 0.35, 920, COLORS["muted"], margin=0)
    text_box(s, "Tools used: Safari UI checks, Flask local server, MySQL/XAMPP, manual test plan, and Python syntax check.", 1.0, 5.65, 11.4, 0.58, 1500, COLORS["green_dark"], True, "ctr", fill=COLORS["mint"], margin=0)
    footer(s, 11)
    slides.append(s)

    s = Slide("Demo")
    title(s, "8. Software Demonstration", "Show the working software live; screenshots are backup only.")
    demo_steps = [
        ("Start", "Run python3 app.py with XAMPP MySQL on."),
        ("Register/Login", "Create or use a test account."),
        ("Add", "Enter company, role, status, deadline, notes."),
        ("Search/Filter", "Search by role/company and filter by status."),
        ("Update/Delete", "Change status, save, then delete a sample."),
        ("Error Handling", "Show invalid login or protected dashboard redirect."),
    ]
    for i, (h, b) in enumerate(demo_steps):
        x = 0.65 + (i % 3) * 4.12
        y = 1.95 + (i // 3) * 1.62
        rect(s, x, y, 3.55, 1.18, COLORS["white"], COLORS["line"], "roundRect", h)
        text_box(s, f"{i + 1}. {h}", x + 0.22, y + 0.18, 2.8, 0.25, 1150, COLORS["green_dark"], True, margin=0)
        text_box(s, b, x + 0.22, y + 0.55, 2.9, 0.35, 830, COLORS["muted"], margin=0)
    text_box(s, "If an error happens: explain it calmly, show the related code or test result, and continue with the prepared demo path.", 1.0, 5.85, 11.35, 0.5, 1400, COLORS["green_dark"], True, "ctr", fill=COLORS["mint"], margin=0)
    footer(s, 12)
    slides.append(s)

    s = Slide("Security")
    title(s, "Validation and Security", "The app reduces common risk through authentication checks, scoped queries, and input validation.")
    items = [
        ("Hashed passwords", "New passwords are stored using pbkdf2:sha256 instead of plain text."),
        ("Route protection", "Dashboard, add, update, and delete actions require an active session."),
        ("SQL safety", "Parameterized queries treat SQL-like input as text."),
        ("User privacy", "Dashboard, update, and delete queries include the current user's id."),
    ]
    for i, (h, b) in enumerate(items):
        y = 1.95 + i * 1.08
        rect(s, 0.9, y, 0.42, 0.42, COLORS["gold"], None, "ellipse", "dot")
        text_box(s, h, 1.55, y - 0.02, 3.5, 0.32, 1450, COLORS["ink"], True, margin=0)
        text_box(s, b, 5.0, y - 0.02, 6.95, 0.36, 1200, COLORS["muted"], margin=0)
    rect(s, 0.9, 6.2, 11.6, 0.5, "174C3C", None, "roundRect", "security message")
    text_box(s, "Security is built into the workflow, not added as an afterthought.", 1.15, 6.31, 11.0, 0.22, 1300, COLORS["white"], True, "ctr", margin=0)
    footer(s, 13)
    slides.append(s)

    s = Slide("Team Contribution")
    title(s, "9. Team Contribution", "Each person owned a clear part of planning, design, implementation, interface, and quality.")
    people = [
        ("Alhaji Kargbo", "Project Manager", "Coordinated team timeline, scope, presentation flow, and completion."),
        ("Renae Washington", "Software Architect", "Designed system structure, database relationship, and architecture decisions."),
        ("Langston Gwinn", "Backend Developer", "Built routes, sessions, database integration, validation, and CRUD functionality."),
        ("Quincy King", "Frontend Developer", "Designed dashboard UI, responsive CSS, forms, tables, and status badges."),
        ("Ali-Andro Thaxter", "Software Tester", "Created test plan/results, checked workflows, found bugs, and confirmed quality."),
    ]
    for i, (name, role, desc) in enumerate(people):
        x = 0.7 + (i % 3) * 4.05
        y = 2.0 + (i // 3) * 2.05
        rect(s, x, y, 3.5, 1.55, COLORS["white"], COLORS["line"], "roundRect", name)
        text_box(s, name, x + 0.22, y + 0.2, 3.0, 0.28, 1220, COLORS["ink"], True, margin=0)
        text_box(s, role, x + 0.22, y + 0.55, 3.0, 0.25, 950, COLORS["green"], True, margin=0)
        text_box(s, desc, x + 0.22, y + 0.88, 2.95, 0.45, 720, COLORS["muted"], margin=0)
    footer(s, 14)
    slides.append(s)

    s = Slide("Next Steps")
    title(s, "Future Improvements", "The current version works; the next version can become more automated and career-ready.")
    items = [
        ("Deadline reminders", "Notify students before an application date arrives."),
        ("Resume and cover letter uploads", "Attach documents to each company record."),
        ("Analytics", "Show conversion rates from applied to interview and offer."),
        ("Deployment", "Host the app online with production database settings."),
    ]
    for i, (h, b) in enumerate(items):
        x = 0.8 + (i % 2) * 5.95
        y = 2.15 + (i // 2) * 1.95
        rect(s, x, y, 5.1, 1.35, COLORS["white"], COLORS["line"], "roundRect", h)
        text_box(s, h, x + 0.28, y + 0.22, 4.3, 0.28, 1450, COLORS["green_dark"], True, margin=0)
        text_box(s, b, x + 0.28, y + 0.65, 4.35, 0.38, 1050, COLORS["muted"], margin=0)
    text_box(s, "Next version theme: fewer manual reminders, more insight into the student's career pipeline.", 1.0, 6.25, 11.2, 0.44, 1450, COLORS["green_dark"], True, "ctr", fill=COLORS["mint"], margin=0)
    footer(s, 15)
    slides.append(s)

    s = Slide("Close", "174C3C")
    text_box(s, "Smart Internship Tracker", 0.95, 1.0, 7.4, 0.7, 3500, COLORS["white"], True, margin=0)
    line(s, 0.98, 1.88, 1.5, COLORS["gold"], 32000)
    text_box(s, "A focused tool for students to track applications, protect their data, and manage the internship search with confidence.", 0.98, 2.35, 8.2, 0.88, 2100, "DDEFE7", True, margin=0)
    rect(s, 1.0, 4.28, 4.95, 1.0, "0C261F", None, "roundRect", "demo")
    text_box(s, "Ready for live demo and questions", 1.25, 4.63, 4.45, 0.32, 1550, COLORS["white"], True, "ctr", margin=0)
    text_box(s, "Thank you", 8.0, 5.75, 4.0, 0.6, 2850, COLORS["white"], True, "r", margin=0)
    slides.append(s)

    return slides


def slide_xml(slide: Slide) -> str:
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
       xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
       xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld name="{esc(slide.title)}">
    <p:bg><p:bgPr>{fill_xml(slide.bg)}<a:effectLst/></p:bgPr></p:bg>
    <p:spTree>
      <p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
      <p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>
      {''.join(slide.parts)}
    </p:spTree>
  </p:cSld>
  <p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>
</p:sld>'''


def rels_xml(rels: list[tuple[str, str, str]]) -> str:
    body = "\n".join(
        f'<Relationship Id="{rid}" Type="{typ}" Target="{target}"/>'
        for rid, typ, target in rels
    )
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
{body}
</Relationships>'''


def write_deck(slides: list[Slide]) -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(OUT, "w", ZIP_DEFLATED) as z:
        slide_overrides = "\n".join(
            f'<Override PartName="/ppt/slides/slide{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>'
            for i in range(1, len(slides) + 1)
        )
        z.writestr("[Content_Types].xml", f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Default Extension="png" ContentType="image/png"/>
  <Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>
  <Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/>
  <Override PartName="/ppt/slideLayouts/slideLayout1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/>
  <Override PartName="/ppt/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>
  <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
  <Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
  {slide_overrides}
</Types>''')
        z.writestr("_rels/.rels", rels_xml([
            ("rId1", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument", "ppt/presentation.xml"),
            ("rId2", "http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties", "docProps/core.xml"),
            ("rId3", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties", "docProps/app.xml"),
        ]))
        z.writestr("docProps/core.xml", '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dc:title>Smart Internship Tracker Final Presentation</dc:title>
  <dc:creator>Ali-Andro Thaxter team</dc:creator>
  <cp:lastModifiedBy>Codex</cp:lastModifiedBy>
</cp:coreProperties>''')
        z.writestr("docProps/app.xml", f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">
  <Application>Microsoft PowerPoint</Application><Slides>{len(slides)}</Slides>
</Properties>''')
        sld_ids = "\n".join(f'<p:sldId id="{256+i}" r:id="rId{i+1}"/>' for i in range(1, len(slides) + 1))
        z.writestr("ppt/presentation.xml", f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:presentation xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rId1"/></p:sldMasterIdLst>
  <p:sldIdLst>{sld_ids}</p:sldIdLst>
  <p:sldSz cx="{SLIDE_W}" cy="{SLIDE_H}" type="wide"/>
  <p:notesSz cx="6858000" cy="9144000"/>
</p:presentation>''')
        pres_rels = [("rId1", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster", "slideMasters/slideMaster1.xml")]
        pres_rels.extend((f"rId{i+1}", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide", f"slides/slide{i}.xml") for i in range(1, len(slides) + 1))
        z.writestr("ppt/_rels/presentation.xml.rels", rels_xml(pres_rels))
        z.writestr("ppt/slideMasters/slideMaster1.xml", '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sldMaster xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr></p:spTree></p:cSld>
  <p:clrMap bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" hlink="hlink" folHlink="folHlink"/>
  <p:sldLayoutIdLst><p:sldLayoutId id="2147483649" r:id="rId1"/></p:sldLayoutIdLst>
  <p:txStyles><p:titleStyle/><p:bodyStyle/><p:otherStyle/></p:txStyles>
</p:sldMaster>''')
        z.writestr("ppt/slideMasters/_rels/slideMaster1.xml.rels", rels_xml([
            ("rId1", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout", "../slideLayouts/slideLayout1.xml"),
            ("rId2", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme", "../theme/theme1.xml"),
        ]))
        z.writestr("ppt/slideLayouts/slideLayout1.xml", '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sldLayout xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" type="blank" preserve="1">
  <p:cSld name="Blank"><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr></p:spTree></p:cSld>
  <p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>
</p:sldLayout>''')
        z.writestr("ppt/slideLayouts/_rels/slideLayout1.xml.rels", rels_xml([
            ("rId1", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster", "../slideMasters/slideMaster1.xml"),
        ]))
        z.writestr("ppt/theme/theme1.xml", '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="Smart Internship Tracker">
  <a:themeElements>
    <a:clrScheme name="Tracker"><a:dk1><a:srgbClr val="1E2735"/></a:dk1><a:lt1><a:srgbClr val="FFFFFF"/></a:lt1><a:dk2><a:srgbClr val="174C3C"/></a:dk2><a:lt2><a:srgbClr val="F8FBFA"/></a:lt2><a:accent1><a:srgbClr val="28785F"/></a:accent1><a:accent2><a:srgbClr val="3157D5"/></a:accent2><a:accent3><a:srgbClr val="D99B2B"/></a:accent3><a:accent4><a:srgbClr val="D33B35"/></a:accent4><a:accent5><a:srgbClr val="DFF7EA"/></a:accent5><a:accent6><a:srgbClr val="657284"/></a:accent6><a:hlink><a:srgbClr val="3157D5"/></a:hlink><a:folHlink><a:srgbClr val="28785F"/></a:folHlink></a:clrScheme>
    <a:fontScheme name="Aptos"><a:majorFont><a:latin typeface="Aptos Display"/></a:majorFont><a:minorFont><a:latin typeface="Aptos"/></a:minorFont></a:fontScheme>
    <a:fmtScheme name="Clean"><a:fillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:fillStyleLst><a:lnStyleLst><a:ln w="12700"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln></a:lnStyleLst><a:effectStyleLst><a:effectStyle><a:effectLst/></a:effectStyle></a:effectStyleLst><a:bgFillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:bgFillStyleLst></a:fmtScheme>
  </a:themeElements>
</a:theme>''')
        if HERO.exists():
            z.write(HERO, "ppt/media/internship-hero.png")
        for i, slide in enumerate(slides, start=1):
            z.writestr(f"ppt/slides/slide{i}.xml", slide_xml(slide))
            slide_rels = [("rId1", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout", "../slideLayouts/slideLayout1.xml")]
            slide_rels.extend(slide.rels)
            z.writestr(f"ppt/slides/_rels/slide{i}.xml.rels", rels_xml(slide_rels))


if __name__ == "__main__":
    deck_slides = build_slides()
    write_deck(deck_slides)
    print(f"Wrote {OUT} ({len(deck_slides)} slides, {os.path.getsize(OUT)} bytes)")

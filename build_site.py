#!/usr/bin/env python3
"""Build static HTML site from PTE markdown for GitHub Pages."""

import os
import re
import shutil

import markdown
from markdown.extensions.attr_list import AttrListExtension
from markdown.extensions.fenced_code import FencedCodeExtension
from markdown.extensions.tables import TableExtension
from markdown.extensions.toc import TocExtension

BASE = os.path.dirname(os.path.abspath(__file__))
SOURCE_MD = os.path.join(BASE, "PTE-HOC-TAP.md")
SOURCE_TIPS = os.path.join(BASE, "PTE-TIPS.md")
SOURCE_TEMPLATES = os.path.join(BASE, "PTE-TEMPLATES.md")
IDEA_BANKS = os.path.join(BASE, "idea_banks")
DOCS = os.path.join(BASE, "docs")
SITE_ASSETS = os.path.join(BASE, "site", "assets")
PERSONAL_SITE = os.path.abspath(
    os.path.join(BASE, "..", "..", "dunghuynhandy.github.io", "pte")
)
GITHUB_REPO = "https://github.com/dunghuynhandy/pte"


def slugify(value: str, separator: str = "-") -> str:
    value = value.strip().lower()
    value = re.sub(r"\.\s*", separator, value)
    value = re.sub(r"[^\w\s-]", "", value, flags=re.UNICODE)
    value = re.sub(r"[\s_]+", separator, value)
    value = re.sub(rf"{separator}+", separator, value)
    return value.strip(separator)


MD = markdown.Markdown(
    extensions=[
        TableExtension(),
        FencedCodeExtension(),
        AttrListExtension(),
        TocExtension(marker="", slugify=slugify),
    ]
)


def md_to_html(text: str) -> str:
    MD.reset()
    return MD.convert(text)


def page(title: str, body: str, active: str = "") -> str:
    nav = [
        ("home", "Home", "index.html"),
        ("summary", "Study Guide", "summary.html"),
        ("tips", "Tips", "tips.html"),
        ("templates", "Templates", "templates.html"),
        ("ideas", "Idea Banks", "idea_bank/index.html"),
    ]
    nav_html = "".join(
        f'<a href="{href}" class="{"active" if key == active else ""}">{label}</a>'
        for key, label, href in nav
    )
    return f"""<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} — PTE Academic Study</title>
  <link rel="stylesheet" href="assets/style.css">
</head>
<body>
  <header class="site-header">
    <div class="inner">
      <a class="logo" href="index.html">PTE <span>Academic</span></a>
      <nav>{nav_html}</nav>
    </div>
  </header>
  <main>{body}</main>
  <footer class="site-footer">
    <p>Personal study notes · <a href="{GITHUB_REPO}">GitHub</a></p>
  </footer>
</body>
</html>"""


def write(path: str, content: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def build_md_page(source: str, breadcrumb: str, active: str, out_name: str) -> None:
    with open(source, encoding="utf-8") as f:
        content = f.read()
    html = md_to_html(content)
    body = f"""
  <div class="breadcrumb"><a href="index.html">Home</a> / {breadcrumb}</div>
  <div class="content">{html}</div>
"""
    title = breadcrumb.split(" / ")[-1] if " / " in breadcrumb else breadcrumb
    write(os.path.join(DOCS, out_name), page(title, body, active=active))


def build_index() -> None:
    body = """
  <section class="hero">
    <h1>PTE Academic Study Hub</h1>
    <p>Tài liệu học PTE Academic — 22 dạng câu, chấm điểm, quy đổi IELTS, visa Úc, chiến lược ôn thi (cập nhật 2025).</p>
    <div class="hero-actions">
      <a class="btn btn-primary" href="summary.html">Study Guide</a>
      <a class="btn btn-secondary" href="tips.html">Tips</a>
      <a class="btn btn-secondary" href="templates.html">Templates</a>
      <a class="btn btn-secondary" href="idea_bank/index.html">Idea Banks</a>
    </div>
  </section>
  <h2 class="section-title">Pages</h2>
  <div class="card-grid">
    <a class="card" href="summary.html"><h3>Study Guide</h3><p>22 dạng câu · chấm điểm · visa · quy đổi IELTS</p></a>
    <a class="card" href="tips.html"><h3>Tips</h3><p>Mẹo từng dạng câu · ngày thi · lỗi thường gặp</p></a>
    <a class="card" href="templates.html"><h3>Templates</h3><p>DI · RL · Essay · SWT · SST · SGD · RTS</p></a>
    <a class="card" href="idea_bank/index.html"><h3>Idea Banks</h3><p>Essay pros &amp; cons · remote education · more topics</p></a>
  </div>
  <h2 class="section-title">Quick links</h2>
  <div class="card-grid">
    <a class="card" href="summary.html#2-cấu-trúc-bài-thi"><h3>Cấu trúc bài thi</h3><p>3 phần · 22 dạng câu</p></a>
    <a class="card" href="summary.html#9-yêu-cầu-visa--du-học-phổ-biến"><h3>Visa Úc</h3><p>50 · 65 · 79</p></a>
    <a class="card" href="tips.html#listening"><h3>Listening Tips</h3><p>WFD · SST · ghi chú khi nghe</p></a>
    <a class="card" href="tips.html#mẹo-ngày-thi"><h3>Ngày thi</h3><p>Checklist nhanh</p></a>
  </div>
"""
    write(os.path.join(DOCS, "index.html"), page("Home", body, active="home"))


def build_idea_banks() -> None:
    src = IDEA_BANKS
    dst = os.path.join(DOCS, "idea_bank")
    if not os.path.isdir(src):
        print("Skip idea banks — idea_banks/ not found")
        return
    if os.path.exists(dst):
        shutil.rmtree(dst)
    shutil.copytree(src, dst)
    print(f"Built idea banks in {dst}")


def deploy_personal_site() -> None:
    personal_root = os.path.dirname(PERSONAL_SITE)
    if not os.path.isdir(personal_root):
        print(f"Skip personal deploy — {personal_root} not found")
        return
    if os.path.exists(PERSONAL_SITE):
        shutil.rmtree(PERSONAL_SITE)
    shutil.copytree(DOCS, PERSONAL_SITE)
    print(f"Deployed to {PERSONAL_SITE}")


def main() -> None:
    if os.path.exists(DOCS):
        shutil.rmtree(DOCS)

    shutil.copytree(SITE_ASSETS, os.path.join(DOCS, "assets"))
    open(os.path.join(DOCS, ".nojekyll"), "w").close()

    build_index()
    build_md_page(SOURCE_MD, "Study Guide", "summary", "summary.html")
    build_md_page(SOURCE_TIPS, "Tips", "tips", "tips.html")
    build_md_page(SOURCE_TEMPLATES, "Templates", "templates", "templates.html")
    build_idea_banks()
    deploy_personal_site()

    print(f"Built site in {DOCS}")
    print("Live URL:   https://dunghuynhandy.github.io/pte/")
    print("Summary:    https://dunghuynhandy.github.io/pte/summary.html")
    print("Tips:       https://dunghuynhandy.github.io/pte/tips.html")
    print("Templates:  https://dunghuynhandy.github.io/pte/templates.html")
    print("Idea Banks: https://dunghuynhandy.github.io/pte/idea_bank/")
    print("Remote Ed:  https://dunghuynhandy.github.io/pte/idea_bank/remote_education/")


if __name__ == "__main__":
    main()

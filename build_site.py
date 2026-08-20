#!/usr/bin/env python3
"""Build static HTML site from PTE-HOC-TAP.md for GitHub Pages."""

import os
import re
import shutil

import markdown
from markdown.extensions.fenced_code import FencedCodeExtension
from markdown.extensions.tables import TableExtension
from markdown.extensions.toc import TocExtension

BASE = os.path.dirname(os.path.abspath(__file__))
SOURCE_MD = os.path.join(BASE, "PTE-HOC-TAP.md")
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


def build_index() -> None:
    body = """
  <section class="hero">
    <h1>PTE Academic Study Hub</h1>
    <p>Tài liệu học PTE Academic — 22 dạng câu, chấm điểm, quy đổi IELTS, visa Úc, chiến lược ôn thi (cập nhật 2025).</p>
    <div class="hero-actions">
      <a class="btn btn-primary" href="summary.html">Open Study Guide</a>
      <a class="btn btn-secondary" href="https://github.com/dunghuynhandy/pte">GitHub Repo</a>
    </div>
  </section>
  <h2 class="section-title">Contents</h2>
  <div class="card-grid">
    <a class="card" href="summary.html#1-tổng-quan"><h3>Tổng quan</h3><p>Format, thời lượng, thang điểm 10–90</p></a>
    <a class="card" href="summary.html#2-cấu-trúc-bài-thi"><h3>Cấu trúc bài thi</h3><p>3 phần · 22 dạng câu</p></a>
    <a class="card" href="summary.html#8-quy-đổi-điểm-pte--ielts"><h3>PTE ↔ IELTS</h3><p>Bảng quy đổi chính thức 2025</p></a>
    <a class="card" href="summary.html#9-yêu-cầu-visa--du-học-phổ-biến"><h3>Visa Úc</h3><p>Competent 50 · Proficient 65 · Superior 79</p></a>
    <a class="card" href="summary.html#10-chiến-lược-học--làm-bài"><h3>Chiến lược học</h3><p>Lộ trình 4–8 tuần + templates</p></a>
    <a class="card" href="summary.html#12-tài-nguyên-luyện-tập"><h3>Tài nguyên</h3><p>Pearson, ApeUni, AlfaPTE...</p></a>
  </div>
"""
    write(os.path.join(DOCS, "index.html"), page("Home", body, active="home"))


def build_summary() -> None:
    with open(SOURCE_MD, encoding="utf-8") as f:
        content = f.read()
    html = md_to_html(content)
    body = f"""
  <div class="breadcrumb"><a href="index.html">Home</a> / Study Guide</div>
  <div class="content">{html}</div>
"""
    write(os.path.join(DOCS, "summary.html"), page("Study Guide", body, active="summary"))


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
    build_summary()
    deploy_personal_site()

    print(f"Built site in {DOCS}")
    print("Live URL:  https://dunghuynhandy.github.io/pte/")
    print("Summary:   https://dunghuynhandy.github.io/pte/summary.html")


if __name__ == "__main__":
    main()

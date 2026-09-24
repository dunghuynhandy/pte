#!/usr/bin/env python3
"""Build PTE idea bank site for GitHub Pages."""

import os
import shutil

BASE = os.path.dirname(os.path.abspath(__file__))
IDEA_BANKS = os.path.join(BASE, "idea_banks")
DOCS = os.path.join(BASE, "docs")
SITE_ASSETS = os.path.join(BASE, "site", "assets")
GITHUB_REPO = "https://github.com/dunghuynhandy/pte"


def write(path: str, content: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def build_index() -> None:
    body = """
  <section class="hero">
    <h1>PTE Idea Banks</h1>
    <p>Pros &amp; cons visual maps for common PTE essay topics — use for planning Body 1 / Body 2.</p>
  </section>

  <section class="category-block" id="education">
    <h2 class="category-label">Education</h2>
    <div class="card-grid">
      <a class="card" href="idea_bank/remote_education/index.html">
        <h3>Remote Education</h3>
        <p>Flexibility · cost · access vs social · motivation · tech · cheating</p>
      </a>
      <a class="card" href="idea_bank/university_education/index.html">
        <h3>University Education</h3>
        <p>Careers · skills · access vs trades · debt · dropouts · workforce gaps</p>
      </a>
      <a class="card" href="idea_bank/homework/index.html">
        <h3>Homework</h3>
        <p>Practice · discipline · exams vs stress · balance · inequality · busy work</p>
      </a>
      <a class="card" href="idea_bank/free_university/index.html">
        <h3>Free University</h3>
        <p>Access · debt · public good vs cost · quality · taxpayers · responsibility</p>
      </a>
    </div>
  </section>

  <section class="category-block" id="technology">
    <h2 class="category-label">Technology</h2>
    <div class="card-grid">
      <a class="card" href="idea_bank/social_media/index.html">
        <h3>Social Media</h3>
        <p>Connection · info · business vs mental health · fake news · privacy · time</p>
      </a>
      <a class="card" href="idea_bank/ai_jobs/index.html">
        <h3>AI &amp; Jobs</h3>
        <p>Automation · cost · vulnerable sectors vs new roles · human skills · retraining</p>
      </a>
      <a class="card" href="idea_bank/internet_monitoring/index.html">
        <h3>Internet Monitoring</h3>
        <p>Security · crime · safety vs privacy · free speech · abuse · effectiveness</p>
      </a>
    </div>
  </section>
"""
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>PTE Idea Banks</title>
  <link rel="stylesheet" href="assets/style.css">
</head>
<body>
  <header class="site-header">
    <div class="inner">
      <a class="logo" href="index.html">PTE <span>Idea Banks</span></a>
    </div>
  </header>
  <main>{body}</main>
  <footer class="site-footer">
    <p>Personal study notes · <a href="{GITHUB_REPO}">GitHub</a></p>
  </footer>
</body>
</html>"""
    write(os.path.join(DOCS, "index.html"), html)


def build_idea_banks() -> None:
    src = IDEA_BANKS
    dst = os.path.join(DOCS, "idea_bank")
    if not os.path.isdir(src):
        print("Skip idea banks — idea_banks/ not found")
        return
    if os.path.exists(dst):
        shutil.rmtree(dst)
    shutil.copytree(src, dst)
    root_index = os.path.join(dst, "index.html")
    if os.path.exists(root_index):
        os.remove(root_index)
    print(f"Built idea banks in {dst}")


def main() -> None:
    if os.path.exists(DOCS):
        shutil.rmtree(DOCS)

    shutil.copytree(SITE_ASSETS, os.path.join(DOCS, "assets"))
    open(os.path.join(DOCS, ".nojekyll"), "w").close()

    build_index()
    build_idea_banks()

    print(f"Built site in {DOCS}")
    print("Live URL:   https://dunghuynhandy.github.io/pte/")
    print("Remote Ed:  https://dunghuynhandy.github.io/pte/idea_bank/remote_education/")
    print("University:   https://dunghuynhandy.github.io/pte/idea_bank/university_education/")
    print("Homework:     https://dunghuynhandy.github.io/pte/idea_bank/homework/")
    print("Free Uni:     https://dunghuynhandy.github.io/pte/idea_bank/free_university/")
    print("Social Media: https://dunghuynhandy.github.io/pte/idea_bank/social_media/")
    print("AI Jobs:      https://dunghuynhandy.github.io/pte/idea_bank/ai_jobs/")
    print("Monitoring:   https://dunghuynhandy.github.io/pte/idea_bank/internet_monitoring/")


if __name__ == "__main__":
    main()

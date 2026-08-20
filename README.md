# PTE Academic — Personal Study Site

Tài liệu học PTE Academic: 22 dạng câu, chấm điểm, quy đổi IELTS, visa Úc, chiến lược ôn thi.

## Live site

**https://dunghuynhandy.github.io/pte/**

Summary: **https://dunghuynhandy.github.io/pte/summary.html**

Tips: **https://dunghuynhandy.github.io/pte/tips.html**

Templates: **https://dunghuynhandy.github.io/pte/templates.html**

The site is deployed to your personal GitHub Pages repo (`dunghuynhandy.github.io/pte/`). Running `build_site.py` copies the built HTML there automatically.

## Contents

| File / Folder | Description |
|---------------|-------------|
| `PTE-HOC-TAP.md` | Source markdown — full study guide (12 sections) |
| `PTE-TIPS.md` | Tips per task type, exam day, common mistakes |
| `PTE-TEMPLATES.md` | Speaking & writing templates |
| `docs/` | Generated static website (GitHub Pages) |
| `site/assets/` | CSS styles |

## Build the website

```bash
pip3 install -r requirements.txt
python3 build_site.py
```

This regenerates all HTML in `docs/` from the markdown files.

## Enable GitHub Pages (pte repo)

1. Push this repo to GitHub: `dunghuynhandy/pte`
2. Open **Settings → Pages**: https://github.com/dunghuynhandy/pte/settings/pages
3. Under **Build and deployment → Source**, select **GitHub Actions**
4. Push any commit — the workflow deploys from `/docs`

> **Alternative:** Deploy from branch `master` → folder `/docs`

## Related

- IELTS study site: https://github.com/dunghuynhandy/ielts

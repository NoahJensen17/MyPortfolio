# Portfolio

Static HTML/CSS site showcasing application and dashboard projects. No build step — open `index.html` directly or serve the folder with any static host (GitHub Pages).

## Structure

```
index.html              Landing page — project grid ("My Developed Tools")
projects/project-N.html One case-study page per project
assets/styles.css        Shared styles
assets/img/              Redacted screenshots referenced by project pages
assets/redact-tool/       Script for redacting/watermarking screenshots before they go in assets/img
```

## Adding a project

1. Duplicate `projects/project-1.html`, rename it, update its content (title, description, role/problem/impact, tech tags).
2. Add a card linking to it in `index.html`.

## Redacting a screenshot before adding it

Never place an original, unredacted screenshot in `assets/img/`. Always run it through the redaction script first:

```
"C:\Users\Noah.Jensen\Anaconda3\python.exe" assets\redact-tool\redact.py path\to\original.png assets\img\project1-shot1.png --box 100,200,400,260 --box 50,50,300,90
```

- Each `--box left,top,right,bottom` blacks out one rectangular region (pixel coordinates from the image's top-left corner).
- The tool always flattens to a new PNG and stamps a small "Data redacted — for portfolio illustration only" watermark in the bottom-right corner.
- Only commit the output file from `assets/img/` — never the original source screenshot.

## Deploying to GitHub Pages

See the setup walkthrough provided separately. Once the repo is pushed, enable Pages in the repo Settings → Pages → set source to the `main` branch, root folder.

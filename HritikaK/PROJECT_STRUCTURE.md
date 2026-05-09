# Project Structure

```text
HritikaK/
├── index.html
├── 404.html
├── .nojekyll
├── .gitignore
├── _redirects
├── README.md
├── PROJECT_STRUCTURE.md
├── assets/
│   ├── css/
│   │   └── .gitkeep
│   ├── js/
│   │   └── .gitkeep
│   ├── images/
│   │   └── .gitkeep
│   └── docs/
│       └── .gitkeep
└── deploy/
    └── github-pages.md
```

## File Purposes

`index.html` is the live homepage. GitHub Pages looks for this file first.

`404.html` catches missing routes on GitHub Pages and sends users back to the portfolio.

`.nojekyll` tells GitHub Pages to serve files as-is instead of processing them with Jekyll.

`_redirects` is useful if you later deploy to Netlify. GitHub Pages ignores it.

`assets/css/` is for stylesheets if the single-file HTML is split later.

`assets/js/` is for JavaScript if the single-file HTML is split later.

`assets/images/` is for profile images, logos, project screenshots, and icons.

`assets/docs/` is for resume PDFs or downloadable documents.

`deploy/` stores deployment notes.


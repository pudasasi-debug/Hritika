# Deploy To GitHub Pages

Repository:

```text
https://github.com/sambriddhi28/HritikaK.git
```

## One-Time Setup

```powershell
cd "C:\Users\sambr\Downloads\www.adamhartwig.co.uk\HritikaK"
git init
git branch -M main
git remote add origin https://github.com/sambriddhi28/HritikaK.git
git add .
git commit -m "Deploy Hritika portfolio"
git push -u origin main
```

If GitHub already has files:

```powershell
git pull origin main --allow-unrelated-histories
git push -u origin main
```

## Enable Pages

1. Go to the GitHub repository.
2. Open **Settings**.
3. Open **Pages**.
4. Under **Build and deployment**, select **Deploy from a branch**.
5. Branch: `main`.
6. Folder: `/root`.
7. Click **Save**.

The site will publish at:

```text
https://sambriddhi28.github.io/HritikaK/
```


# vishnurachapudi.com

Personal portfolio site for Vishnu Rachapudi — Cloud & AI Engineer.
Static site (HTML/CSS/JS), served from the repository root.

## Structure

```
/
├── index.html                  # Homepage (the whole site is one page)
├── profile.webp                # Profile photo (LCP image + social/OG image)
├── robots.txt                  # Crawler rules (must stay at root)
├── sitemap.xml                 # Sitemap (must stay at root)
├── rss.xml                     # Blog RSS feed
├── Vishnu_Rachapudi_Resume.pdf # Résumé (linked from hero + Connect)
├── css/
│   ├── style.css               # Editable source stylesheet
│   └── style.min.css           # Minified stylesheet (linked by index.html)
├── gallery/                    # Speaker gallery images (WebP)
├── blogs/                      # Individual blog article pages
├── aws-devops-agent/           # Standalone sub-page
└── project/                    # Non-served project artifacts (deploy notes, CFP backend)
```

## Working on styles

`index.html` links `css/style.min.css`. When editing styles:

1. Edit `css/style.css` (the readable source).
2. Regenerate `css/style.min.css` (minified) before deploying.

## Images

All raster images are stored as optimized **WebP**. The gallery loads images
from `https://www.vishnurachapudi.com/gallery/` — when adding a new image,
convert it to WebP and upload it there.

## Deploy

The site is static. Publish the repository root to the host so that
`index.html`, `robots.txt`, `sitemap.xml`, `profile.webp`, and the
`gallery/`, `blogs/` folders are all served from the domain root.

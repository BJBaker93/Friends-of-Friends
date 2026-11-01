# Friends of Friends ARG website

The homepage preserves the original ARG experience and artwork. At the user's request, hotspots are now anchored to objects in image coordinates: Listen on the CD player; Socials and Contact on the computer; Tour on the bottom posters; Merch on the shirt draped over the amp. The original links, circle appearance, hover behavior and hidden SoundCloud player are preserved. Do not redesign the homepage or add SEO content to it.

SEO content lives on separate, readable pages:

- `/discover/`: a sourced listening guide with The 1975, Sam Fender, Australian alternative rock and Brisbane connections.
- `/press/`: eight verified interviews, reviews and features.

These pages have their own navigation and SEO metadata. No SEO links or content have been added to the ARG homepage. The sitemap lists the homepage and both supporting pages.

## Source and build

- `source/homepage.html` is the approved ARG homepage source, including the requested hotspot alignment.
- `scripts/build.py` copies it directly to `docs/index.html` and generates the secondary pages.
- `source/press.json` contains research and source URLs.
- `source/config.json` controls the origin and indexing policy of secondary pages.
- `docs/` is published by GitHub Pages from the `main` branch.

Run:

```sh
python3 scripts/build.py
python3 scripts/check_site.py
```

The checker verifies the homepage against the approved layout's SHA-256, then checks secondary-page links, metadata, JSON-LD and the sitemap. It intentionally does not impose SEO or markup changes on the original homepage.

Repository: https://github.com/BJBaker93/Friends-of-Friends

Preview: https://bjbaker93.github.io/Friends-of-Friends/

## Indexing and domain launch

The original homepage has its original title and no added robots directive. The separate SEO pages carry `noindex, follow` during staging. They can be enabled when the custom domain is connected. This public preview is not private access control.

The domain and DNS have not been changed. At domain cutover:

1. Preserve existing DNS/mail records, verification files and important URLs. Keep the old host available during the transition.
2. Verify domain ownership and configure the GitHub Pages custom domain before following current GitHub DNS instructions. Confirm apex/www behavior and HTTPS.
3. The homepage hard-codes `https://friendsoffriendsband.com/wp-content/uploads/2025/11/new-bg.gif`. Copy the original GIF from the local `archive/` to `docs/wp-content/uploads/2025/11/new-bg.gif` before switching that domain, so the original URL continues to resolve without changing the HTML. Mobile uses an exact local copy of the original Imgur PNG in `docs/assets/mobile-original.png` to avoid unreliable hotlink loading. A centered transparent hotspot layer tracks the background cover crop. The original portrait artwork and its separate coordinate map are used at aspect ratios of 4:3 or narrower, including portrait tablets.
4. Set `site_url` to `https://friendsoffriendsband.com/` and `indexing` to `true` in `source/config.json`; rebuild and check. This updates secondary-page canonicals, social images, metadata, sitemap and crawl policy. It does not alter the homepage.
5. Preserve `docs/CNAME` created by GitHub's custom-domain configuration. Carry forward any additional old WordPress asset paths or redirects that are needed.
6. Verify Google Search Console and Bing Webmaster Tools; submit `/sitemap.xml` and inspect the pages. The robots file in a GitHub project subdirectory is not authoritative for github.io; it becomes authoritative at the custom-domain root.

## Search and AI discovery

The secondary pages provide visible, sourced content with descriptive titles, descriptions, canonicals, social cards, MusicGroup/MusicAlbum/WebPage data and press references. Artist comparisons are grounded in actual interviews and reviews. Press is described in `subjectOf`; official artist profiles are in `sameAs`.

No ranking or AI recommendation is guaranteed. Linking to press provides useful attribution; incoming editorial links and consistent official profiles remain worthwhile. Avoid hidden keyword blocks, fabricated recommendations and mass query-variant pages. Google does not require special AI markup or `llms.txt` for AI search.

OpenAI's search crawler is allowed. Search inclusion and model-training controls are independent; the general crawl policy currently allows all crawlers.

- https://developers.google.com/search/docs/appearance/ai-features
- https://developers.google.com/search/docs/essentials/spam-policies
- https://schema.org/MusicGroup
- https://developers.openai.com/api/docs/bots
- https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site

The exact original code and full-resolution artwork are also retained in the local ignored `archive/` folder. Original media URLs, player parameters and behaviors are preserved in the published homepage, as requested.

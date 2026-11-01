# Friends of Friends website

Static GitHub Pages website. Generated HTML, CSS, a tiny background-video controller, and locally hosted artwork. No packages, build service, analytics, cookies, or runtime API credentials are required.

## Publish on GitHub Pages

In `BJBaker93/Friends-of-Friends` → Settings → Pages, select **Deploy from a branch**, branch **main**, folder **/docs**, then Save. The preview should be available at:

https://bjbaker93.github.io/Friends-of-Friends/

The preview deliberately has `noindex, follow` in the HTML, keeping it out of search results while the existing custom-domain site remains live. This is public staging, not private access control. Search optimisation goes live when indexing is enabled on the custom domain.

## Edit and preview

1. Change page content in `scripts/build.py`, press evidence in `source/press.json`, or styles in `docs/assets/site.css`.
2. Run `python3 scripts/build.py`.
3. Run `python3 scripts/check_site.py`.
4. Preview with `python3 -m http.server 8765 --directory docs`.
5. Commit the changed source and generated `docs/` files.

The copy is deliberately factual. Interviews support The 1975 and Sam Fender connections; links are included visibly. Members, current tour dates and third-party endorsements are not invented. Use a live listings link until confirmed shows can be maintained accurately. Any new event schema should represent a verified future performance with a real venue, date and ticket URL.

## Custom-domain launch — do together later

The current domain and DNS have not been changed. Before cutover:

1. Record existing DNS, mail records, Search Console verification files, and important existing URLs. Preserve mail records. Keep the old host available during the move.
2. Verify the domain for the GitHub account, then set the repository's Pages custom domain to the chosen canonical host, expected to be `friendsoffriendsband.com`.
3. Follow current GitHub Pages DNS instructions. Do not create a wildcard DNS record. Confirm both apex and www behave as intended and enable HTTPS when the certificate is ready.
4. In `source/config.json`, set `site_url` to `https://friendsoffriendsband.com/` and `indexing` to `true`. The stable `band_id` already uses this domain. Run the build and checks, then publish the updated `docs/`.
5. GitHub's branch-publishing custom-domain setup writes `docs/CNAME`; preserve it. Do not add it during staging because that could redirect the preview before the domain is ready.
6. Check the live page source for self-canonicals, `index, follow`, current domain social images, and sitemap URLs. At the domain root `/robots.txt` becomes authoritative; a project-subdirectory robots file is not authoritative for github.io.
7. Preserve any old `/wp-content/` URLs that still receive links or traffic, or establish an appropriate redirect strategy before retiring WordPress. All artwork used by the new site is already self-hosted in `docs/assets/`; it does not depend on WordPress or Imgur.
8. Verify Google Search Console and Bing Webmaster Tools, submit `/sitemap.xml`, inspect the three URLs, and monitor indexing and errors. Moving the same domain is a hosting move, not a Search Console change of address.

## Search and AI discovery

Implemented: descriptive page titles and meta descriptions; one H1 per page; accessible, visible HTML content; source-linked listening guide; press archive; stable MusicGroup identity with official `sameAs` profiles and press in `subjectOf`; MusicAlbum, WebSite, WebPage and breadcrumb structured data; canonical URLs; Open Graph/social cards; sitemap; crawl permissions; responsive layout; reduced-motion support; no hidden keyword blocks or autoplay audio.

No guaranteed position or AI recommendation is possible. Structured data describes the band; it does not guarantee a Google rich result. An outbound link to a publication is useful attribution, not an incoming backlink. Consistent official profiles and legitimate coverage that links back to the band's site are useful next steps. Do not buy fake accounts, planted recommendations or manipulative links. Do not create a Wikipedia page without independent notability and conflict-of-interest considerations.

Next useful content: firsthand song stories, recording notes, official performance videos and maintained tour pages. Add only material the band can stand behind. Keep location consistent across artist profiles: the current sources use both Gold Coast and Brisbane, so this site uses South East Queensland.

OpenAI's search crawler (`OAI-SearchBot`) is allowed. Search inclusion and model-training controls are independent; `GPTBot` can be disallowed separately if desired. The current general crawl policy allows all crawlers. No special AI markup or `llms.txt` is needed for Google AI search.

Guidance:

- https://developers.google.com/search/docs/appearance/ai-features
- https://developers.google.com/search/docs/essentials/spam-policies
- https://schema.org/MusicGroup
- https://developers.openai.com/api/docs/bots
- https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site
- https://developers.google.com/search/docs/crawling-indexing/site-move-no-url-changes

## Original code and assets

The exact pasted HTML and full-size original artwork are preserved locally in the ignored `archive/` folder. The original HTML includes an unlisted SoundCloud player token and is deliberately excluded from publication. The new site uses public music links. The original background GIF is approximately 14 MB; its MP4 rendition is approximately 125 KB. Mobile and reduced-motion visitors see a static image. The background includes historical promotional artwork; live-show links point to maintained listings.

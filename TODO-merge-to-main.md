# TODO before merging the redesign (v3-rifle-appointed) into main

main is live and has changed since this branch started. When merging:

- [ ] Prices: each of the 8 gift tag sets is **$12** (not $7). "Eight sets, $12 each". All eight bought separately cost **$96**; the Library stays **$39** (saves $57). Check index.html, main.js (deck buy label), meta/OG text.
- [ ] Footer keeps the contact email as plain visible text: `Contact: yinbo870815@gmail.com` (mailto link is fine). Needed for Creative Market review.
- [ ] Do NOT add `noindex` back to the homepage. robots.txt is `Allow: /`; homepage is in sitemap.xml.
- [ ] Keep the blog: `blog/`, `blog.css`, `img/blog/`, `tools/build_blog.py`, `tools/posts.py`, `sitemap.xml`, `robots.txt`, and the "Journal" link (`blog/`) in the homepage nav and footer.
- [ ] Under each $39 Library buy button, keep the quiet savings line (small, secondary ink colour, no red, no badge): "Save $57 vs. buying all 8 sets separately ($96)". Not under the compact masthead button.

Review round for /workspace/midnight-pages-site (keep DESIGN-v3.md rules, all copy/links). Fix:
1. Desktop hero: the tag at lower-left is clipped by the image bottom. Adjust object-position / height so the whole tag and the twine are visible at 1440x900 (try object-position 30% 80% and hero height min(82vh,720px)); text panel keeps its place on the right third, vertically centered.
2. Gift tag grid: descriptions are truncated with ellipsis; show full text (no line clamp).
3. Tag Library detail section: the library image is too dominant. Make it max 520px wide in a 6/6 split with generous whitespace, image on the right, text on the left, vertically centered.
4. Prompt Pack section: the desk image currently bleeds to the viewport left edge while everything else is contained. Contain it inside the 1280px wrapper (6/6 split, image left).
5. Mobile 390: hero image height 56svh with object-position ~35% 78% so the tag sits centered; reduce top/bottom padding of the text panel so the Buy the Library button is reachable quickly. Check all sections at 390 for anything awkward and fix it.
Run the same Chrome checks via http://localhost:8765 (server is running). Do not commit.

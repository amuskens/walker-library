# John Walker Digital Library

A dependency-free static reference app for John Walker's writings on rhetoric,
elocution, gesture, pronunciation, and the expressive voice.

Curated by Anders Muskens, with the assistance of ChatGPT.

Installed books:

- *Elements of Elocution*, Volume II (1781)
- *A Rhetorical Grammar* (1822)

## Open in VS Code

1. Unzip this project and open the folder in VS Code.
2. Install the **Live Server** extension if necessary.
3. Right-click `index.html` and select **Open with Live Server**.

There is no JavaScript build step and no database.

Johnson entries are loaded live from Johnson's Dictionary Online, so dictionary
lookup requires an internet connection. The Walker books themselves remain a
fully static site.

## Publish free with GitHub Pages

1. Create a new **public** GitHub repository.
2. Upload everything in this folder to its root.
3. Open **Settings → Pages** in the repository.
4. Select **Deploy from a branch**, then choose `main` and `/ (root)`.

The result will be available at an address like
`https://YOUR-NAME.github.io/REPOSITORY/`. All paths are relative, so it can
also be used with a custom domain or embedded into Squarespace.

## Included

- the complete supplied *Rhetorical Grammar*, including tables and figures
- the complete supplied *Elements of Elocution*, Volume II
- stable section and original-page links
- clickable entries in each book's original printed contents pages
- collapsible hierarchical contents, curated favorite indexes, and private
  reader bookmarks
- expandable quick indexes for rhetorical figures and the passions
- three linked visual explorations: an affinity-cloud map of the passions, a
  Roman architectural index of 28 rhetorical figures, and an interactive vocal
  score with eight paths through Walker's analysis of the speaking voice
- corrected chapter hierarchy for the passions and their illustrative examples
- compact-by-default Johnson lookup with an expandable live entry
- current-volume indicators in the header and navigation pane
- full-text search in the current book or the entire collection
- Walker-definition popups for figures of rhetoric
- instant Johnson's Dictionary Online popup when a word is selected or double-clicked
- on-demand Johnson loading in a compact lookup card
- multi-word quotation capture with Chicago, MLA, APA, and Oxbridge citations
- optional Johnson mode for single-click dictionary lookup
- copyable links and citations, adjustable type, and responsive navigation
- multi-book architecture and a reusable DOCX importer
- an eighteenth-century-inspired collection landing page with public-domain
  Walker portraiture and original elocution plates

## Add another Walker book

Install the importer requirement:

```bash
python3 -m pip install -r requirements.txt
```

Place the prepared DOCX in `source/`. It should use real Word Heading 1 through
Heading 4 styles as needed to preserve the book's hierarchy. Then run:

```bash
python3 tools/convert_docx.py "source/ANOTHER-BOOK.docx" \
  --output data/books.js \
  --images assets/images \
  --append \
  --slug another-book \
  --title "The Complete Historical Title" \
  --short-title "Short Display Title" \
  --author "John Walker" \
  --year 1781 \
  --edition "Edition and publication statement" \
  --description "A short catalogue description."
```

`--append` preserves existing books. Reusing a slug replaces that book. Put
each original page number in a separate square-bracketed paragraph, such as
`[253]` or `[vii]`, and the importer will create a stable page anchor.
Repeated `Contents` headings used as running heads across consecutive printed
contents pages are automatically consolidated into one section.

## Change featured passages

Edit the `featured` list at the beginning of `assets/app.js`. Titles are
matched against headings in the current book; unavailable headings are omitted.

## Structure

```text
index.html              Application shell
figures-map.html        Roman map of the rhetorical figures
voice-map.html          Interactive map of the speaking voice
passions-map.html       Affinity-cloud map of the passions
assets/app.css          Design and responsive layout
assets/app.js           Reader, search, glossary, bookmarks, lookup
assets/images/          Figures extracted from books
assets/portraits/       Public-domain landing-page portraiture and plates
data/books.js           Generated multi-book collection
source/                 Source DOCX files
tools/convert_docx.py   DOCX importer
requirements.txt        Importer dependency
```

## Image credits

The library landing page uses public-domain material from
[Wikimedia Commons](https://commons.wikimedia.org/wiki/Category:John_Walker_(lexicographer)):
John Walker by Henry Ashby (National Portrait Gallery), an engraved portrait
after T. Clerk, and two plates from the 1811 *Elements of Elocution*.

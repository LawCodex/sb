#!/usr/bin/env python3
"""Convert the SIEC legislation PDFs fetched by sb_fetch.py into Markdown.

Usage: sb_convert.py RAW_DIR OUT_DIR     (needs poppler `pdftotext`)
"""
import datetime, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sb_pdf2md  # noqa: E402

RAW, OUT = sys.argv[1], sys.argv[2]
TODAY = datetime.date.today().isoformat()

TITLES = {  # file slug on siec.gov.sb -> (directory, title, type)
    "solomon-islands-constitution": ("constitution", "The Constitution of Solomon Islands (Solomon Islands Independence Order 1978, Schedule)", "constitution"),
    "national-parliament-electoral-provisions-act": ("acts", "National Parliament Electoral Provisions Act", "act"),
    "electoral-act-2018-signed-version": ("acts", "Electoral Act 2018", "act"),
    "provincial-assemblies-and-honiara-city-council-election-regulations-2024": ("regulations", "Provincial Assemblies and Honiara City Council Election Regulations 2024", "regulation"),
    "electoral-regs-2018-gazette-notice": ("regulations", "Electoral Regulations 2018 (Gazette notice)", "regulation"),
    "electoral-amendmentregulations-2019-gazette-notice": ("regulations", "Electoral (Amendment) Regulations 2019 (Gazette notice)", "regulation"),
    "gaz-no-61-monday-8th-april-2024-liquor-ban-order-2024": ("regulations", "Liquor Ban Order 2024 (Gazette No. 61, 8 April 2024)", "order"),
}


def main():
    idx = json.load(open(os.path.join(RAW, "index.json")))
    seen, done, skipped = set(), [], []
    for d in idx:
        key = re.sub(r"^\d+_|\.pdf$|-2$", "", os.path.basename(d["file"]))
        if not d["ok"] or key not in TITLES or key in seen:
            skipped.append(d["url"])
            continue
        body, _ = sb_pdf2md.convert_plain(d["file"])
        if len(body.strip()) < 300:
            skipped.append(d["url"])
            continue
        # drop arrangement-of-sections entries (ALL-CAPS "N TITLE" lines turned into headings)
        body = "\n\n".join(b for b in body.split("\n\n")
                             if not (b.startswith("#### ") and re.sub(r"[^A-Za-z]", "", b[5:]).isupper()))
        seen.add(key)
        sub, title, typ = TITLES[key]
        fm = ["---", f'title: "{title}"', f"type: {typ}", "jurisdiction: sb", "language: en", "status: unknown",
              f'source: "{d["url"]}"', f'archived_source: "{d["archived_url"]}"',
              'publisher: "Solomon Islands Electoral Commission (siec.gov.sb)"',
              'format_note: "text extracted from the archived official PDF; layout not preserved"',
              f"retrieved: {TODAY}", "---", ""]
        p = os.path.join(OUT, sub, key + ".md")
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, "w", encoding="utf-8", newline="\n").write("\n".join(fm) + f"# {title}\n\n" + body)
        done.append(p)
    print(len(done), "written;", len(skipped), "skipped (scans/duplicates)")
    for s in skipped:
        print("  skipped", s)


if __name__ == "__main__":
    main()

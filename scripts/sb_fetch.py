#!/usr/bin/env python3
"""Fetch Solomon Islands legislation published by the Solomon Islands Electoral Commission
(siec.gov.sb, "Legislation" downloads: the Constitution and electoral laws), from Internet Archive
(Wayback Machine) captures — the live download links now redirect to the home page.

(The Acts PDFs on parliament.gov.sb, live and archived, are image-only scans and were not used.)
Usage: sb_fetch.py RAW_DIR
"""
import json, os, re, sys, time
import requests

UA = "LawCodex/1.0 (+https://github.com/LawCodex)"
CDX = ("http://web.archive.org/cdx/search/cdx?url=siec.gov.sb/download/7/legislation/&matchType=prefix"
       "&filter=statuscode:200&filter=mimetype:application/pdf&fl=original,timestamp,length")
RAW = sys.argv[1]
S = requests.Session()
S.headers["User-Agent"] = UA


def main():
    os.makedirs(os.path.join(RAW, "pdf"), exist_ok=True)
    best = {}
    for line in S.get(CDX, timeout=300).text.splitlines():
        url, ts, ln = line.split()
        if not url.endswith(".pdf"):
            continue
        if url not in best or ts > best[url][0]:
            best[url] = (ts, ln)
    out = []
    for url, (ts, ln) in sorted(best.items()):
        fn = re.sub(r"[^A-Za-z0-9._-]+", "_", url.split("/legislation/")[1])
        p = os.path.join(RAW, "pdf", fn)
        ok = os.path.exists(p)
        for a in range(5):
            if ok:
                break
            try:
                r = S.get(f"https://web.archive.org/web/{ts}id_/{url}", timeout=300)
                if r.status_code == 200 and r.content[:5] == b"%PDF-" and b"%%EOF" in r.content[-2048:]:
                    open(p, "wb").write(r.content)
                    ok = True
                    break
                print("bad", r.status_code, len(r.content), url, file=sys.stderr)
            except Exception as e:
                print("ERR", url, e, file=sys.stderr)
            time.sleep(5 * 2 ** a)
        out.append({"url": url, "timestamp": ts, "file": p, "ok": ok,
                    "archived_url": f"https://web.archive.org/web/{ts}/{url}"})
        time.sleep(2)
    json.dump(out, open(os.path.join(RAW, "index.json"), "w"), indent=1)
    print(len(out), "docs;", sum(o["ok"] for o in out), "downloaded")


if __name__ == "__main__":
    main()

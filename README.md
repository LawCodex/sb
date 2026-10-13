# LawCodex — Solomon Islands (`sb`)

A small set of Solomon Islands legislation as plain Markdown — the **Constitution** and the main
**electoral laws** — taken from Internet Archive captures of the official Solomon Islands Electoral
Commission website (`siec.gov.sb`, *Legislation* downloads).

Part of [LawCodex](https://github.com/LawCodex): the legislation of every country as Markdown in git.

Retrieved: **2026-10-13**. Status: **minimal**.

## Contents

| Directory | File | Notes |
|---|---|---|
| `constitution/` | `solomon-islands-constitution.md` | Solomon Islands Independence Order 1978 (S.I. 1978/783) with the Constitution in its Schedule — **original 1978 text as published by SIEC, not a consolidation** (later amendments, e.g. 2001, 2014, 2018, 2022, 2023, are not incorporated) |
| `acts/` | `national-parliament-electoral-provisions-act.md` | as published by SIEC |
| `acts/` | `electoral-act-2018-signed-version.md` | Electoral Act 2018, signed version |
| `regulations/` | 4 files | Provincial Assemblies and Honiara City Council Election Regulations 2024; Electoral Regulations 2018 and Electoral (Amendment) Regulations 2019 (Gazette notices); Liquor Ban Order 2024 (Gazette) |

## What is NOT covered, and why

- **The Acts of Parliament.** The National Parliament site lists 436 Acts (1981–2026) at
  <https://parliament.gov.sb/business/acts/> (JSON: `get_acts.php?year=YYYY`), but every PDF sampled —
  live and in Internet Archive captures of the older site (`files/legislation/…`,
  `sites/default/files/…`) — is an image-only scan; no OCR was performed, so none could be included.
- **A consolidated Constitution and the Revised Edition of the Laws**: the Government portal
  `solomons.gov.sb` sits behind a Sucuri bot-protection proxy, and PacLII (`paclii.org`), which hosts
  the consolidated legislation, behind a Cloudflare challenge; neither was circumvented.
- 9 further SIEC downloads (amendment Acts, 2005 regulations, the 2023 Acts) are scans.

## Sources

- Original official URLs: `https://siec.gov.sb/download/7/legislation/<id>/<name>.pdf` (the live
  links now redirect to the home page); each file records the original URL (`source`) and the
  Wayback Machine capture used (`archived_source`).
- Retrieved sequentially through the Wayback Machine with an identifying User-Agent. Text extracted
  with poppler `pdftotext`; running headers, page numbers and the arrangement of sections removed.
  Not an official version.

## Regenerate

```sh
python3 scripts/sb_fetch.py   ../_raw/sb
python3 scripts/sb_convert.py ../_raw/sb .
```

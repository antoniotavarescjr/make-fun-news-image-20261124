# Sum up 24 November's world news in one image

Entry for the make.fun contest "Sum up 24 November's world news in one image"
(https://make.fun/bounty/news-image-20261124).

- Deadline: Wednesday 25 Nov 2026, 21:00 BRT (26 Nov 00:00 UTC)
- Prize: $100 total — 1st $20, top 50 paid
- Image: `entry.png`, PNG 1024x1024, 991,620 bytes (under the 1 MiB limit)
- SHA-256 of `entry.png`:
  `8ccdee46b5e52f1cbd892cdaaea8aa2a2be09d46c425a377658c301f8fada4d8`
- Program: `main.py` (Python 3.13, standard library only, no network).
  It copies `entry.png` to `/output/entry.png` by default.
  Run it with `python3 main.py` or `python3 main.py <output-path>`.
- Determinism: `test_determinism.py` — two runs write byte-identical output.

The image is a newspaper front page ("THE WORLD — TUESDAY 24 NOVEMBER 2026")
with four verified 24 Nov stories: Riyadh (tower struck, 11 injured),
Zaporizhzhia (2 killed, 40 wounded), Gaza (Hamas security chief killed,
7 killed that day), Senegal (Africa Cup title restored by court, 1-0).

Chosen unanimously (3–0) by three independent judges, average 4.88/5.00,
from three candidates. See `../FINAL_REPORT.md` for the full report,
judging, QA (PASS) and the submission gate.

## Status — read before submitting

This folder is a ready-to-upload copy of the final package only. It does
NOT complete the submission. Before asking for submission authorisation:

1. Create the public GitHub repo in the account owner's own GitHub account
   (created after the competition opened), under this OSI-approved licence
   (MIT, in `LICENSE`), with `main.py` + `entry.png` in the root.
   The licence holder/year in `LICENSE` is a draft — change it if needed.
2. Confirm whether the AI coding-agent transcripts of the sessions that
   built this entry exist or can be recovered. None were found anywhere in
   `~/workspace/` on 24 Nov 2026 — if they cannot be recovered, that
   deliverable cannot be satisfied, and that is a decision for the owner.
3. Check the make.fun account for an existing submission for this contest
   and how much of the quota (10/day, 20 total) has been used.
4. Only then give explicit authorisation to submit. Nothing here has been
   submitted, published or uploaded.

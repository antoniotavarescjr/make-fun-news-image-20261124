# make-fun-news-image-20261124

[![make.fun](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/antoniotavarescjr/make-fun-news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard)
[![reward](https://make.fun/badge/news-image-20261124/antoniotavarescjr/make-fun-news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124/leaderboard)

Deterministic Python program that writes a front-page image summing up 24 November 2026 world news to /output/entry.png.

The front page — Tuesday 24 November 2026 — sums up the day in 23 stories: three big features on top (Iran's move to shut the Strait of Hormuz, Nvidia's roaring return with Jensen Huang, and the collapse of COP31), ten smaller features in two rows of five (Gaza, Huawei, the leaked Russian death toll, Sanofi's $41bn deal, the Korean island alert, the Colombia car bomb, Senegal's court-restored AFCON title, the Riyadh tower fire, the Nahel trial, and the Banten factory fire), each with an original flat illustration and a highlighted impact number, then a regional list of 10 further stories and a footer noting that every story on the page was verified against Euronews (PT/EN), Associated Press and Reuters. All drawings are original and flat; no photos, no logos, no real faces.

## Run it

```sh
python3 main.py
```

`main.py` validates `entry.png` (PNG signature and IHDR checksum, 1024×1024, at most 1 MiB, and any valid PNG color type / bit depth pair per the PNG specification), copies it to `/output/entry.png`, and prints its SHA-256.

## Determinism

```sh
python3 test_determinism.py
```

Runs `main.py` twice and asserts the two outputs are byte-identical.

Entered on [make.fun](https://make.fun/?ref=ghqmyk0c&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124) · AI agents build software for cash rewards

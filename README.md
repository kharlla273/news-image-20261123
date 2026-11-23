[![make.fun](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123)
[![Rank](https://make.fun/badge/news-image-20261123/kharlla273/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123)
[![Reward](https://make.fun/badge/news-image-20261123/kharlla273/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123)

# news-image-20261123

The World in One Day — Monday 23 November 2026: a newspaper front page
summing up the day's world news in one image. Lead story: the COP31
climate talks collapse without a deal, the final draft dropping any
mention of fossil fuels. Also: a blast hits a Russian ship at Benghazi
port in Libya, Mexico captures FBI most-wanted cartel boss 'El Chapo
Isidro', an AI sell-off shakes Wall Street, and dozens go missing after
an Indonesian factory fire.

## Run it

```sh
python3 draw.py   # regenerates entry.png (deterministic)
MAKEFUN_OUTPUT_DIR=out python3 main.py   # copies entry.png to out/
```

## Files

- `draw.py` — draws `entry.png` (1024×1024) with Pillow; fixed text, no
  network, no clock, so two runs are byte-identical.
- `main.py` — the graded entrypoint (standard library only): verifies and
  copies `entry.png` into the grader's output directory.
- `entry.png` — the submitted image.

---
Entered on [make.fun](https://make.fun/r/n305kcfc).

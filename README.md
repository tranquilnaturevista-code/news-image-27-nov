# The World in One Day — Friday 27 November 2026

[![News Image](https://make.fun/badge/news-image-20261127.svg)](https://make.fun/bounty/news-image-20261127)
[![Rank](https://make.fun/badge/news-image-20261127/tranquilnaturevista-code/news-image-27-nov/rank.svg)](https://make.fun/bounty/news-image-20261127)
[![Reward](https://make.fun/badge/news-image-20261127/tranquilnaturevista-code/news-image-27-nov/reward.svg)](https://make.fun/bounty/news-image-20261127)

Entry for the [make.fun bounty "Sum up 27 November's world news in one
image"](https://make.fun/bounty/news-image-20261127): a one-page newspaper
front page for **Friday 27 November 2026**, drawn programmatically with
Pillow. The lead story is the Iranian drone attack on Kuwait — falling
debris from intercepted drones killed two Italian air-defence technicians
— and the page carries five more stories: Israeli strikes killing 10 in
Gaza as the ceasefire frays, Pablo Hernández de Cos named as the next ECB
chief, the EU budget summit ending with no deal, Saudi strikes on Yemen
answered by Houthi strikes on a Saudi refinery, and the first-ever weather
postponement of the 100th Macy's Thanksgiving Day Parade, plus Bangkok and
Black Friday notes along the bottom.

## How it works

- `render_frontpage.py` draws the page (1024×1024 PNG) from the story
  list below and saves it as `entry.png`. It uses no network, no
  randomness, and no timestamps: two runs produce byte-identical output.
- `main.py` is the entry program. It checks that `entry.png` is a whole
  PNG within the competition limits (at most 1024×1024 pixels, at most
  1 MiB) and copies it byte for byte to `/output/entry.png`, so the page
  the judge sees is exactly the page laid out here. It needs only the
  Python standard library.

## Stories in the image

- **Iranian drones kill two Italians in Kuwait (lead).** Kuwait says it
  shot down several drones from Iran; falling debris killed two Italian
  air-defence technicians and injured a Kuwaiti and a Pakistani. The
  second Iranian attack on the US-allied Gulf state this month; Iran
  denies responsibility. (AP, 27 November 2026)
- **Israeli strikes kill 10 in Gaza as ceasefire frays.** Five strikes
  and a shooting killed ten Palestinians, hospitals said — among them
  Hamas deputy minister Khaled Abu Nada and his wife. (AP, BBC,
  27 November 2026)
- **Spain's Hernández de Cos named next ECB chief.** EU leaders picked
  the former Spanish central bank governor to succeed Christine Lagarde;
  formal appointment in December. (European Council, 27 November 2026)
- **EU budget summit ends with no deal after 12 hours.** Leaders left
  Brussels divided over the 2028–2034 budget, but 24 states backed a
  €45 billion loan to Ukraine. (European Council, Reuters,
  27 November 2026)
- **Saudi strikes hit Yemen as Houthis hit refinery.** The coalition said
  it destroyed 50 Houthi targets; the Houthis struck a Saudi oil refinery
  and Riyadh's financial district. (AP, 27 November 2026)
- **Also today:** the 100th Macy's Thanksgiving Day Parade is postponed
  to Saturday — the first weather delay in its history — as a storm
  brings gusts of up to 60 mph; an explosion at a Bangkok oil refinery
  injures at least nine people; some 183 million Americans are expected
  to shop over the Thanksgiving weekend, and 60% say they plan to use AI
  to help. (CNN, Reuters, NRF, 27 November 2026)

Where the day's outlets disagreed on a figure it is left out rather than
guessed: the Yemen item gives no casualty count, because coverage reported
strikes on both sides without a confirmed toll. All stories are events
that happened, or were first reported, on 27 November 2026.

## Reproduce

```sh
python3 render_frontpage.py   # writes entry.png (deterministic)
python3 main.py               # writes /output/entry.png
```

Python 3.13 and Pillow are all that is needed to render; `main.py`
itself needs only the standard library.

## Verification

Re-running `render_frontpage.py` reproduces `entry.png` byte for byte
(sha256 `4ab77ad4f859dd65bb17727eb03898c03ebab7293c400cb8880810991920cfc8`), and `main.py` refuses to deliver the page if
the PNG is oversized, malformed, or fails its own read-back check — so
what the judge receives is exactly what is stored in this repository.

<p align="center">
  <img src="docs/logo.png" width="154">
  <h1 align="center">Agenoria</h1>
  <p align="center">
    <a href="https://github.com/jiuguangw/Agenoria/blob/master/LICENSE">
      <img src="https://img.shields.io/badge/License-MIT-yellow.svg" />
    </a>
    <a href="https://github.com/jiuguangw/Agenoria/blob/master/LICENSE">
      <img src="https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg" />
    </a>
    </a>
    <a href="https://www.python.org/">
        <img src="https://img.shields.io/badge/built%20with-Python3-red.svg" />
    </a>
    <a href="https://travis-ci.com/jiuguangw/Agenoria">
    <img src="https://travis-ci.com/jiuguangw/Agenoria.svg?branch=master">
    </a>
    <a href="https://codeclimate.com/github/jiuguangw/Agenoria">
    <img src="https://img.shields.io/codeclimate/maintainability/jiuguangw/Agenoria">
    </a>
    <a href="https://codeclimate.com/github/jiuguangw/Agenoria">
    <img src="https://img.shields.io/codeclimate/issues/jiuguangw/Agenoria">
    </a>
  </p>
</p>

## Overview and etymology

Agenoria is a small utility, written in Python, for visualizing and analyzing growth data from a newborn's first year. It computes and plots statistics on feeding, diapering, sleep, and growth (such as weight, head circumference, and length), recorded in the [Glow Baby](https://glowing.com/baby) and [Hatch Baby](https://shop.hatchbaby.com/products/grow?variant=23706934597) apps.

The name Agenoria comes from the [Roman goddess](https://en.wikipedia.org/wiki/Agenoria_(mythology)) of activity, one of the deities who endows the child with a developmental capacity, such as walking, singing, reasoning, and learning to count.

## Background

When my wife and I were expecting our first child in late 2018, I came across a [post](https://www.reddit.com/r/dataisbeautiful/comments/6s0ba9/months_3_to_17_of_my_babys_sleep_and/) by Reddit user u/jitney86 in r/dataisbeautiful, with a graph visualizing his baby's sleep patterns. I was inspired to do the same and to improve upon jitney86's results (which included only sleep data, from month 3-17), by recording not just sleep, but every aspect of the baby's activities in the first year.

What started as a fun project became immensely useful in diagnosing some medical issues. Since Month 5, we've encountered significant feeding difficulties with our baby - he would often push away the bottle and refuse to eat, even when he seems hungry. We relied on accurate daily record-keeping to gauge whether or not he has had sufficient amount to eat - 1000 mL or 32 oz daily, plus pureed foods after Month 6. Despite of these efforts, while his absolute weight grew in the first nine months, his weight percentile continued to drop, from 82% at birth, to the lowest of 27% around Month 10. Several periods of slow weight gain (or even weight loss) were associated with low appetite that lasted close to a week each. But then from Month 9-10, his weight gain slowed to a crawl, even as he was eating more than ever. Mysterious low appetite, worsening feeding aversion, slow weight gain, plus frequent (few times a month) projectile vomiting, constipation, and eczema - prompted us to seek the attention of specialists, even though his pediatrician was not convinced that there were any issues at all. The result - he was diagnosed with a non-IgE mediated allergy to cow's milk, which prompted us to remove all dairy from his diet, leading to immediate weight gain from Month 11.

Agenoria was critical in visualizing the data and identifying abnormal behaviors early. In case it is helpful to another data-obsessed parent - I'm making Agenoria freely available on the web, which includes several Python scripts for statistics and visualization, as well as a dataset containing nearly 10,000 observations (2391 diaper changes, 2574 bottle feeding, 603 solid feeding, and 4203 sleep sessions). For terms of use, see the [License](#License) section below.

## Example Charts

Here are some of the visualizations that Agenoria produces.

### Daily statistics

![Daily Visualization](docs/daily.png?raw=true "Daily Visualization")

The panels include:

* Daily Volume Per Session (mL) - bottle size in mean, max, and min
* Daily Number of Feeding Sessions - total number of feeding sessions per day
* Daily Total Volume - total daily consumed formula volume, in mL
* Daily Total Solid Feeding - total daily consumed solid foods, in oz
* Daily Total Bottle + Solid - total consumed food (formula and solid), in oz
* Daily Total Naps - number of daytime (7:00-19:00) naps per day
* Daily Longest Sleep Duration - longest uninterrupted sleep session, in hours
* Daily Total Sleep - total sleep per day, in hours
* Daily Maximum Awake Duration - maximum awake time in between sleep, in hours
* Total Diapers - a cumulative count of diapers used over time
* Daily Total Pees - total number of pees
* Daily Total Poops - total number of poops

A few interesting observations:

* Max bottle size increased to about 200 mL, then plateaued
* Feed sessions stabilized to an average of 5 around March, but then due to feeding difficulties, started to fluctuate
* Average daily volume for formula was about 1000 mL, with mysterious bouts of low appetite June, July, October, November
* Solid feeding was pitful for the first 5 months, then suddenly started to increase around October
* Daily total food consumption was mostly increasing, until November
* Naps continue to stabilize over time
* Longest uninterrupted sleep improved around April, then again around October when the 10:30pm feeding was dropped. Various points of sleep regression.
* Total sleep per day mostly hovering around 13 hours
* Maximum awake time continue to increase as daytime naps stabilized.
* Used close to 2500 diapers in the first year, a whopping $500 at $0.2 each
* Gradually required less diaper changes until September (daycare requires diaper check every two hours)
* Bouts of constipation around March, April, June, September (poop = 0)

### 24-hour sleep visualization

![Sleep Visualization](docs/sleep.png?raw=true "Sleep Visualization")

A 24 hour visualization of sleep - blue is asleep, white is awake. A few interesting observations:

* Sleep was all over the place in the initial few months, but slowly settled down overnight.
* Day time sleep consolidated to two naps, then by Week 40, one nap.
* Sleep regression was present at 4 months, 10 month, and 12 month
* Several periods where we tried to enforce at 7am wake up time
* Stopping of a 10:30pm dream feed around Week 44
* Small 5 minute catnaps where he simply fell asleep in the car

### 24-hour feeding visualization

![Feeding Visualization](docs/feeding.png?raw=true "Feeding Visualization")

A 24 hour visualization of feeding.

* Stopping of overnight feedings (midnight to 7:00am) around Week 20.
* Stopping of 10:30pm dream feeds around Week 44.

### 24-hour diaper visualization

![Diaper Visualization](docs/diapers.png?raw=true "Diaper Visualization")

A 24 hour visualization of diaper changes.

* Yellow: pee / wet
* Blue: poop in yellow
* Green: poop in green
* Red: poop in an abnormal color

### Growth charts - weight, height, head circumference

![Growth Visualization](docs/growth.png?raw=true "Growth Visualization")

Plots of growth statistics.

* Weight vs age: plotted on CDC growth curves
* Weight percentile vs age: plotted linearly
* Average daily weight gain vs age: daily weight gain, averaged over a 14-day window
* Length vs age: plotted on CDC growth curves
* Head circumference vs age: plotted on CDC growth curves
* Weight vs length: plotted on CDC growth curves

## Data collection

In this section, I describe the procedure for data collection. I utilized the app [Glow Baby](https://glowing.com/baby) in recording feeding, diapering, and sleep data. For weight, I used the data recorded in the [Hatch Baby Grow](https://shop.hatchbaby.com/products/grow?variant=23706934597) scale.

### Sleep

I used Glow's sleep timer function to record sleep. This entailed starting the clock when the baby is put to bed and stop it once he wakes up. In the first six months, when he was sleeping in a [Snoo smart sleeper](https://www.happiestbaby.com/products/snoo-smart-bassinet), I cross verified the Glow data with the Snoo's own data (which is significantly less accurate)

In the first few months, the data is very accurate since waking up / cries always required intervention (diaper change, bottle, pacifier, etc.). After Month 5, when we stopped night feeding, we no longer intervened after hearing him cry, and in most cases, he went back to sleep on his own. Therefore, the sleep data is under-reporting awake time. I only stopped the clock on occasions where he cried severe enough to wake me, or if he truly required intervention (such as during sleep regressions at Month 10 and 12).

In the initial few months, I used short segments to indicate periods where he was in bed but was crying / refused to sleep. After sleep stabilized, I used a 1-minute session to indicate the time that he was put to bed, then starting another session once I verified from the baby monitor that he was indeed asleep. In computing the statistics for sleep (for example, maximum awake time), I removed these 1-minute segments.

### Feeding

The bottle and solid feeding data were both recorded in Glow, with the timestamp indicating the starting time of the feeding session.

For solid feeding, for the most part, I used a kitchen scale to measure the amount consumed, accounting for amounts that were wasted. Glow only supports a limited subset of foods. Therefore the value of "other" was used as a filler.

After he started daycare around Month 10, the data became significantly less reliable. I did my best to fact-check the daily information sheet provided by the daycare, but any records between 8:30am and 4:00pm likely contained a large margin of error. For solid feeding, I entered the data as stated by daycare - for example, the daycare specified that he ate a 3.5 oz pouch - even though the net weight of the food content was at most 3.25 oz, even without waste. I still entered 3.25 oz in my records.

### Diapering

The diaper data was recorded in Glow. At the time of the diaper change, if the front color indicator on the diaper was wet, I recorded as "pee". For poops, I recorded the color (mostly yellow or green), and texture (mostly mushy or solid).

After we started to give him a bath 30 minutes before bed time consistently, I used that diaper change as a way of recording the start of the bath (around 6:30pm - 7:30pm).

### Weight

I used the Hatch Baby Grow to take nearly daily measurements of weight. I weigh him after a fresh diaper change, then zero out the diaper and any clothing he is wearing.

Since Month 3, we've consolidated the daily weight check to the first thing in the morning, after waking up. I find this gave the most consistent results, eliminating the effects of food / poop build up.

### Vomit and Daycare

(this data is not yet available)

I recorded by hand a list of dates where he projectile vomited a significant amount. 1 indicates he vomited.

I recorded by hand all the days he attended daycare. I intend to use this to flag days were feeding and sleep data is unreliable.


## Getting Started

### Installing Anaconda Python

All perquisites are installed as a part of [Anaconda Python](https://www.anaconda.com/distribution/#download-section).

Supported Configurations:

| OS      | Python version |
| ------- | -------------- |
| MacOS   | 3.7  |
| Ubuntu  | 3.7  |
| Windows | 3.7  |


### (Optional) Create a virtual environment

I strongly recommend using a virtual environment to ensure dependencies are  installed safely. This is an optional setup, but if you have trouble running the scripts, try this first.

The instructions below assume you are using Conda, though Virtualenv is essentially interchangeable. To create a new Python 3.7 environment, run:

```bash
conda create --name agenoria python=3.7
conda activate agenoria
```

The shell should now look like `(agenoria) $`. To deactivate the environment, run:

```bash
(agenoria)$ conda deactivate
```

The prompt will return back to `$ ` or `(base)$`.

Note: Older versions of conda may use `source activate agenoria` and `source
deactivate` (`activate agenoria` and `deactivate` on Windows).


### Cloning the repo

To checkout the repo:

```bash
git clone git@github.com:jiuguangw/Agenoria.git
```

### Placing the source data

The [data](data) directory contains the raw CSV data collected from Glow Baby and Hatch Baby.

The Glow Baby data can be generated by going to "Export Report" - "CSV", choose time frame, select "All", and clicking "Export". A zip file is sent via email, which contains several CSV files:

* glow_diaper.csv - contains diaper data
* glow_feed_bottle.csv - contains feeding data for formula/bottle
* glow_feed_solid.csv - contains feeding data for solids
* glow_sleep.csv - contains sleep data
* glow_growth.csv - contains growth data such as head circumference, weight, and length

Note:

* As of late 2019, the CSV export functionality is only available via a Glow Premium subscription.
* Even with Glow Premium, the system will only generate 5000 rows of data at a time. Once you exceed this limit, you'll have to manually export multiple times to cover all the months, then merge the CSV together.
* Due to this limitation, I renamed the final, merged CSVs as described above.

The Hatch Baby data can be generated by going to "More" - "Share Hatch Baby" - "Export Your Baby's Data". It contains a single CSV file with weight and weight percentile measurements.

The columns of both the Glow and Hatch CSVs are sufficiently self explanatory. It's foreseeable that in the future, Glow might change their data format (has already changed once). If you have a different format, it should be easy to copy paste the data into the corresponding column.


### Plotting
```bash
python agenoria.py
```

By default, the charts (in PDF) are produced in a directory called "build". The PDFs are ready for printing on paper sized 17 by 11 inches (Tabloid paper).

## License

### License terms

There are two components of Agenoria, covered by two different licenses:

- The scripts in the [source](source) and [test](test) subdirectories are released under the MIT License.
- The raw data in CSV (under the [data](data) subdirectory) are released under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License (CC BY-NC-SA 4.0).

The full license details can be found in [LICENSE](LICENSE).

To recap, you are free to use or reference the scripts/code for any purpose. The data, however, is under a stricter license because it has taken me a lot of time and energy to collect.

In short, I intend to grant you every freedom in using the data if it is for personal, educational, academic research, conference/journal publication, or otherwise clearly not for profit / non-commercial purposes. All I ask for is an attribution, as required by the CC licensing terms (see the [Attribution](#Attribution) section below).

Generally, I encourage the users to self-determine if their project fits within the scope of the CC BY-NC-SA license. I'm not capable of personally examining your organization's tax-filing status or determine whether or not a financial transaction takes place. Rule of thumb - if you stand to make money by including this data/charts/images/analysis in your work, if you charge your audience for access, or if you are from a large organization - then it's highly likely it falls under commercial use.

For a commercial license, please contact me by email (contact information can be found below). An electronic invoice for the license fee will be issued by my studio and payable by credit card online. A signed copyright release is available by request.


### Attribution

If you are using the data under the Creative Commons license, an attribution  along the lines of

Jiuguang Wang (www.robo.guru), used under CC BY-NC-SA 4.0.

...would be sufficient.


## Contribute

### Technical contributions

I welcome bug fixes, feature additions, and other ways to improve the project. If you'd like to contribute your child's data, I'm happy to host it here, assuming it is in the same format and anonymized.

Please send me pull requests, issues, etc, and contact me if you'd like to be added as a collaborator to the repo.

For others without the time or skills to contribute, I'd also appreciate your help in spreading the word via Facebook, Twitter, etc.

### Donation

Please support the project by making a donation via PayPal or crypto:

[![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=N49BVZZLEXU4G&source=url)

![Bitcoin](https://img.shields.io/badge/Bitcoin-367dGyWPSfSjiP6Nh8oSmdCG9MPkMB58Ad-orange.svg?style=flat-square)
![Ethereum](https://img.shields.io/badge/Ethereum-0x4617f57f8b0e3D09Be50CcB32451A2CD20651262-orange.svg?style=flat-square)
![Bitcoin Cash](https://img.shields.io/badge/Bitcoin%20Cash-qrz4e6n3g7e2q6gqz4wetxlgk5eztskxag7tss982j-orange.svg?style=flat-square)
![Litecoin](https://img.shields.io/badge/Litecoin-MVdpa3uXnqoLkZFoarqNnGB9KHr6TL8xst-orange.svg?style=flat-square)


## Acknowledgments

* I'm grateful to Reddit user jitney86 for inspiring this project. His original post can be found [here](https://www.reddit.com/r/dataisbeautiful/comments/6s0ba9/months_3_to_17_of_my_babys_sleep_and/), and the code/data can be found [here](https://nbviewer.jupyter.org/github/jitney86/Baby-data-viz/blob/master/baby_sleep_and_feed_plot.ipynb).
* Many thanks to Brynn at Glow, Inc for providing the raw CSV data from the Glow Baby app before the CSV export functionality was included as a standard feature.
* Many thanks to the CDC for providing the growth curves data in the public domain ([source](https://www.cdc.gov/growthcharts/percentile_data_files.htm))
* The project logo is made by [Freepik](https://www.flaticon.com/authors/freepik")

## Contact

- Jiuguang Wang
- [jw@robo.guru](jw@robo.guru)
- [www.robo.guru]( www.robo.guru)

I'd love to hear what people are doing with Agenoria. Please drop me a line!



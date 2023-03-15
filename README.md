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
    <a href="https://github.com/jiuguangw/Agenoria/actions">
      <img src="https://github.com/jiuguangw/Agenoria/actions/workflows/test.yml/badge.svg">
    </a>
    <br />
    <a href="https://codeclimate.com/github/jiuguangw/Agenoria">
      <img src="https://img.shields.io/codeclimate/maintainability/jiuguangw/Agenoria">
    </a>
    <a href="https://codeclimate.com/github/jiuguangw/Agenoria/issues">
      <img src="https://img.shields.io/codeclimate/issues/jiuguangw/Agenoria">
    </a>
    <a href="https://codecov.io/gh/jiuguangw/Agenoria">
      <img src="https://codecov.io/gh/jiuguangw/Agenoria/branch/main/graph/badge.svg?token=UU0KQ94PAQ" />
    </a>
    <a href="https://github.com/jiuguangw/Agenoria/actions">
      <img src="https://img.shields.io/badge/linting-pylint-yellowgreen" />
    </a>
  </p>
  <p align="center">
    <a href="https://github.com/codespaces/new?hide_repo_select=true&ref=main&repo=222033385&machine=standardLinux32gb&devcontainer_path=.devcontainer%2Fdevcontainer.json&location=EastUs">
      <img src="https://github.com/codespaces/badge.svg" />
    </a>
  </p>
</p>

## Overview and etymology

Agenoria is a small utility, written in Python, for visualizing and analyzing growth data from a newborn's first year. It computes and plots statistics on feeding, diapering, sleep, and growth (such as weight, head circumference, and length), recorded in the [Glow Baby](https://glowing.com/baby) and [Hatch Baby](https://shop.hatchbaby.com/products/grow?variant=23706934597) apps.

The name Agenoria comes from the [Roman goddess](https://en.wikipedia.org/wiki/Agenoria_(mythology)) of activity, one of the deities who endows the child with a developmental capacity, such as walking, singing, reasoning, and learning to count.

## Background

When my wife and I were expecting our first child in late 2018, I came across a [post](https://www.reddit.com/r/dataisbeautiful/comments/6s0ba9/months_3_to_17_of_my_babys_sleep_and/) by Reddit user u/jitney86 in r/dataisbeautiful, with a graph visualizing his baby's sleep patterns. I was inspired to do the same and to improve upon jitney86's results (which included only sleep data, from month 3-17), by recording not just sleep, but every aspect of the baby's activities in the first year.

What started as a fun project became immensely useful in diagnosing some medical issues. Since Month 5, we've encountered significant feeding difficulties with our baby - he would often push away the bottle and refuse to eat, even when he seems hungry. We relied on accurate daily record-keeping to gauge whether or not he has had sufficient amount to eat - 1000 mL or 32 oz daily, plus pureed foods after Month 6. Despite of these efforts, while his absolute weight grew in the first nine months, his weight percentile continued to drop, from 82% at birth, to the lowest of 27% around Month 10. Several periods of slow weight gain (or even weight loss) were associated with low appetite that lasted close to a week each. But then from Month 9-10, his weight gain slowed to a crawl, even as he was eating more than ever. Mysterious low appetite, worsening feeding aversion, slow weight gain, plus frequent (few times a month) projectile vomiting, constipation, and eczema - prompted us to seek the attention of specialists, even though his pediatrician was not convinced that there were any issues at all. The result - he was diagnosed with a non-IgE mediated allergy to cow's milk, which prompted us to remove all dairy from his diet, leading to immediate weight gain from Month 11.

Agenoria was critical in visualizing the data and identifying abnormal behaviors early. In case it is helpful to another data-obsessed parent - I'm making Agenoria freely available on the web, which includes several Python scripts for statistics and visualization, as well as a dataset containing nearly 23,000+ observations (Baby 1 with 3371 diaper changes, 2929 bottle feeding, 1158 solid feeding, and 5140 sleep sessions; Baby 2 with 2431 diaper changes, 3614 bottle feeding, 113 solid feeding, and 4541 sleep sessions). For terms of use, see the [License](#License) section below.

## Gallery

Here are some of the visualizations that Agenoria produces.

### Daily statistics

Baby 1 - Feeding          |  Baby 2 - Feeding
:-------------------------:|:-------------------------:
![Daily Feeding Statistics](docs/zyw_daily_feeding_stats.png?raw=true "Daily Feeding Statistics")  |  ![Daily Feeding Statistics](docs/zlw_daily_feeding_stats.png?raw=true "Daily Feeding Statistics")

Baby 1 - Sleep          |  Baby 2 - Sleep
:-------------------------:|:-------------------------:
![Daily Sleep Statistics](docs/zyw_daily_sleep_stats.png?raw=true "Daily Sleep Statistics")  |  ![Daily Sleep Statistics](docs/zlw_daily_sleep_stats.png?raw=true "Daily Sleep Statistics")

Baby 1 - Diapers          |  Baby 2 - Diapers
:-------------------------:|:-------------------------:
![Daily Diaper Statistics](docs/zyw_daily_diaper.png?raw=true "Daily Diaper Statistics")  |  ![Daily Diaper Statistics](docs/zlw_daily_diaper.png?raw=true "Daily Diaper Statistics")


### 24-hour visualizations

Baby 1 - Sleep          |  Baby 2 - Sleep
:-------------------------:|:-------------------------:
![Sleep Visualization](docs/zyw_sleep.png?raw=true "Sleep Visualization")  |  ![Sleep Visualization](docs/zlw_sleep.png?raw=true "Sleep Visualization")

Baby 1 - Feeding           |  Baby 2 - Feeding
:-------------------------:|:-------------------------:
![Feeding Visualization](docs/zyw_feeding.png?raw=true "Feeding Visualization")  |  ![Feeding Visualization](docs/zlw_feeding.png?raw=true "Feeding Visualization")

Baby 1 - Diapers         |  Baby 2 - Diapers
:-------------------------:|:-------------------------:
![Diaper Visualization](docs/zyw_diapers.png?raw=true "Diaper Visualization")  |  ![Diaper Visualization](docs/zlw_diapers.png?raw=true "Diaper Visualization")

### Growth charts - weight, height, head circumference

Baby 1           |  Baby 2
:-------------------------:|:-------------------------:
![Growth Visualization](docs/zyw_growth.png?raw=true "Growth Visualization")  |  ![Growth Visualization](docs/zlw_growth.png?raw=true "Growth Visualization")

### Misc charts

Baby 1           |  Baby 2
:-------------------------:|:-------------------------:
![Medical Issues Visualization](docs/zyw_medical.png?raw=true "Medical Issues Visualization")  |  ![Medical Issues Visualization](docs/zlw_medical.png?raw=true "Medical Issues Visualization")

## Data collection

In this section, I describe the procedure for data collection.

I utilized the app [Glow Baby](https://glowing.com/baby) in recording feeding, diapering, and sleep data. For weight, I used the data recorded in the [Hatch Baby Grow](https://shop.hatchbaby.com/products/grow?variant=23706934597) scale.

<details><summary>Click for details...</summary>

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

I recorded by hand a list of dates where he projectile vomited a significant amount. 1 indicates he vomited.

I recorded by hand all the days he attended daycare. I intend to use this to flag days were feeding and sleep data is unreliable.

</details>

## Getting Started

### Installing Anaconda Python (Recommended)

All perquisites are installed as a part of [Anaconda Python](https://www.anaconda.com/distribution/#download-section).

Supported Configurations:

| OS      | Python version |
| ------- | -------------- |
| macOS   | 3.10  |
| Ubuntu  | 3.10  |


### (Optional) Create a virtual environment

I strongly recommend using a virtual environment to ensure dependencies are  installed safely. This is an optional setup, but if you have trouble running the scripts, try this first.

The instructions below assume you are using Conda, though Virtualenv is essentially interchangeable. To create a new Python environment, run:

```bash
conda create --name agenoria python=3.10
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

* `glow_diaper.csv` - contains diaper data
* `glow_feed_bottle.csv` - contains feeding data for formula/bottle
* `glow_feed_solid.csv` - contains feeding data for solids
* `glow_sleep.csv` - contains sleep data
* `glow_growth.csv` - contains growth data such as head circumference, weight, and length

The `config/*.toml` configuration files (imported via `__init__.py`) specifies the locations of the data files. It also requires the user to enter two values - gender and birthday.

Note:

* As of early 2023, the Glow app's export to CSV function has a bug that prevents the export of solid feeding data. You must email customer support to obtain this data.
* As of late 2019, the CSV export functionality is only available via a Glow Premium subscription.
* Even with Glow Premium, the system will only generate 5000 rows of data at a time. Once you exceed this limit, you'll have to manually export multiple times to cover all the months, then merge the CSV together.
* Due to this limitation, I renamed the final, merged CSVs as described above.

The Hatch Baby data can be generated by going to "More" - "Share Hatch Baby" - "Export Your Baby's Data". It contains a single CSV file with weight and weight percentile measurements.

The columns of both the Glow and Hatch CSVs are sufficiently self explanatory. It's foreseeable that in the future, Glow might change their data format (has already changed once). If you have a different format, it should be easy to copy paste the data into the corresponding column.

### Installing the Agenoria package

Install Agenoria by running
```bash
(agenoria)$ pip install .
```
To install the required packages.

### Plotting
```bash
# Pass in the configuration file in .toml
(agenoria)$ agenoria config/config_zyw.toml
```
If for some reason you'd rather skip `setuptools`, you can launch the module directly with
```bash
# Pass in the configuration file in .toml
(agenoria)$ python -m agenoria config/config_zyw.toml
```
If no configuration file is supplied, `config_zyw.toml` is used by default.

By default, the charts (in PDF) are produced in a directory called "build". The PDFs are ready for printing on paper sized 17 by 11 inches (Tabloid paper).

### Development
The following linting tools are used for the project:
* yapf: autoformatter
* isort: imports sorting
* pylint: linting
* mypy: type checking
Install these extra development dependencies by running
```bash
(agenoria)$ pip install '.[dev]'
```
Please note that the single quotes are necessary in `zsh` shell.

You can then run the linters via a single command using pre-commit:
```bash
pre-commit run --all-files
```
Alternatively, you can also run the linters separately:
```bash
yapf -i -r .
isort .
pylint ./agenoria
mypy ./agenoria
```

The unit tests can be run by:
```bash
(agenoria)$ pytest
```

## License

### License terms

There are two components of Agenoria, covered by two different licenses:

- The scripts in the [agenoria](agenoria) and [test](test) subdirectories are released under the MIT License.
- The raw data in CSV (under the [data/zw](data/zw) subdirectory) and the associated charts/images are released under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License (CC BY-NC-SA 4.0).

The full license details can be found in [LICENSE](LICENSE).

To recap, you are free to use or reference the scripts/code for any purpose. The data and any visualizations/graphs/images based on the data, however, is under a stricter license because it has taken me a lot of time and energy to collect.

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
- [jw@robo.guru](mailto:jw@robo.guru?subject=Agenoria)
- [www.robo.guru](https://www.robo.guru)

I'd love to hear what people are doing with Agenoria. Please drop me a line!

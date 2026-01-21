# COVID-19 Data Analysis

Comprehensive analysis of global COVID-19 data to identify trends, high-risk countries, and calculate per-capita metrics.

## 📊 Project Overview

This project analyzes COVID-19 data from [Kaggle's COVID-19 Dataset](https://www.kaggle.com/datasets/imdevskp/corona-virus-report) to:

- Clean and process global COVID-19 data
- Identify high-risk countries based on per-capita metrics
- Calculate country-level aggregations and trends
- Generate actionable insights from the data

## Status

**In Development**

- [x] Project setup
- [ ] Data loading and cleaning
- [ ] Country-level aggregation
- [ ] Risk metric calculations
- [ ] Visualizations
- [ ] Documentation

## Tech Stack

- **Python 3.9+**
- **Pandas** - Data manipulation and analysis
- **NumPy** - Numerical operations
- **Matplotlib** - Visualizations

## Project Structure

```
covid19-analysis/
├── data/               # Data files (not committed)
├── src/                # Source code
│   ├── __init__.py
│   └── analysis.py     # Main analysis script
├── outputs/            # Analysis results
├── .gitignore          # Git ignore rules
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Setup

### Prerequisites

- Python 3.9 or higher
- pip package manager

### Installation

1. **Clone the repository**

```bash
   git clone https://github.com/perlathebian/covid19-analysis.git
   cd covid19-analysis
```

2. **Install dependencies**

```bash
   pip install -r requirements.txt
```

3. **Download the dataset**
   - Download from [Kaggle COVID-19 Dataset](https://www.kaggle.com/datasets/imdevskp/corona-virus-report)
   - Extract `covid_19_clean_complete.csv`
   - Place in `data/` folder and rename to `covid19.csv`

### Usage

```bash
# Run analysis (once implemented)
python src/analysis.py
```

## Planned Features

- **Data Cleaning:** Handle missing values and duplicates
- **Country Aggregation:** Total cases, deaths, recoveries per country
- **Risk Assessment:** Calculate cases/deaths per million
- **Time Series Analysis:** Track trends over time
- **Visualizations:** Charts and graphs for key metrics
- **Export Results:** Save analysis to CSV for further use

## Expected Outputs

Results will be saved to `outputs/`:

- `country_summary.csv` - Country-level statistics
- `risk_analysis.csv` - Per-capita risk metrics
- `visualizations/` - Charts and graphs

## Goals

This project demonstrates:

- Data cleaning and preprocessing
- Pandas operations (filtering, grouping, aggregation)
- Statistical analysis
- Data visualization
- Professional code structure

## Data Source

Dataset: [COVID-19 Dataset by Devakanta](https://www.kaggle.com/datasets/imdevskp/corona-virus-report)

**Columns:**

- Province/State
- Country/Region
- Date
- Confirmed
- Deaths
- Recovered
- Active

## Author

**Perla Thebian**

- GitHub: [@perlathebian](https://github.com/perlathebian)
- LinkedIn: [Perla Thebian](https://www.linkedin.com/in/perla-thebian-43a1ab21b/)

## Acknowledgments

- Dataset provided by [Devakumar K. P. on Kaggle](https://www.kaggle.com/imdevskp)

---

**Note:** This is a learning project for data analysis practice. Data is for educational purposes only.

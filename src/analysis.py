"""
COVID-19 Data Analysis
Analyzes global COVID-19 data to identify trends and high-risk countries.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys


# ===== PATH SETUP =====
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
DATA_DIR = PROJECT_ROOT / "data"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"

# Create outputs directory if it doesn't exist
OUTPUTS_DIR.mkdir(exist_ok=True)


# ===== STEP 1: DATA LOADING & CLEANING =====

def load_data(filename: str = "covid19.csv") -> pd.DataFrame:
    """
    Load COVID-19 dataset from CSV file.
    
    Args:
        filename: Name of CSV file in data directory
        
    Returns:
        DataFrame containing COVID-19 data
        
    Raises:
        FileNotFoundError: If file doesn't exist
        
    Example:
        >>> df = load_data('covid19.csv')
        >>> print(df.shape)
        (100000, 8)
    """
    filepath = DATA_DIR / filename
    
    # Check if file exists
    if not filepath.exists():
        print(f"Error: File not found at {filepath}")
        print(f"\nAvailable files in data directory:")
        for file in DATA_DIR.iterdir():
            print(f"  - {file.name}")
        raise FileNotFoundError(f"File not found: {filepath}")
    
    # Load data
    try:
        df = pd.read_csv(filepath)
        print(f"Data loaded successfully")
        print(f"   Shape: {df.shape[0]:,} rows × {df.shape[1]} columns")
        print(f"   Columns: {list(df.columns)[:5]}...")
        return df
    except Exception as e:
        print(f"Error loading file: {e}")
        raise


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean dataset by handling missing values and duplicates.
    
    Args:
        df: Raw COVID-19 DataFrame
        
    Returns:
        Cleaned DataFrame with missing values filled and duplicates removed
    """
    print("\n--- Cleaning Data ---")
    
    # Show initial missing values
    missing_before = df.isna().sum()
    print(f"Missing values before cleaning:\n{missing_before[missing_before > 0]}\n")
    
    # Handle missing values
    # Fill numeric columns with 0
    numeric_cols = ['Confirmed', 'Deaths', 'Recovered', 'Active']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = df[col].fillna(0)
    
    # Fill categorical columns with 'Unknown'
    if 'Province/State' in df.columns:
        df['Province/State'] = df['Province/State'].fillna('Unknown')
    
    # Remove duplicates
    initial_rows = len(df)
    df = df.drop_duplicates()
    duplicates_removed = initial_rows - len(df)
    
    print(f"Duplicates removed: {duplicates_removed:,}")
    print(f"Missing values filled: {missing_before.sum():,}")
    print(f"Final shape: {df.shape[0]:,} rows x {df.shape[1]} columns\n")
    
    return df

# ===== STEP 2: FILTERING =====

def filter_country(df: pd.DataFrame, country: str) -> pd.DataFrame:
    """
    Filter data for a specific country.
    
    Args:
        df: COVID-19 DataFrame
        country: Country name to filter (e.g., 'India', 'US')
        
    Returns:
        DataFrame containing only specified country's data
        
    Example:
        >>> india_df = filter_country(df, 'India')
        >>> print(len(india_df))
        365
    """
    # Handle different country column names
    country_col = 'Country/Region' if 'Country/Region' in df.columns else 'Country'
    
    country_df = df[df[country_col] == country].copy()
    
    if len(country_df) == 0:
        print(f"Warning: No records found for '{country}'")
        print(f"    Available countries: {df[country_col].unique()[:10].tolist()}...")
    else:
        print(f"{country}: {len(country_df):,} records found")
        print(f"   Date range: {country_df['Date'].min()} to {country_df['Date'].max()}")
        print(f"   Total confirmed: {country_df['Confirmed'].sum():,}")
    
    return country_df


def filter_high_cases(df: pd.DataFrame, threshold: int = 10000) -> pd.DataFrame:
    """
    Filter rows where confirmed cases exceed threshold.
    
    Args:
        df: COVID-19 DataFrame
        threshold: Minimum number of confirmed cases (default: 10,000)
        
    Returns:
        DataFrame with only high-case records
        
    Example:
        >>> high_cases = filter_high_cases(df, 10000)
        >>> print(len(high_cases))
        5432
    """
    high_cases_df = df[df['Confirmed'] > threshold].copy()
    
    num_records = len(high_cases_df)
    num_countries = high_cases_df['Country/Region'].nunique() if 'Country/Region' in df.columns else 0
    
    print(f"High cases filter (>{threshold:,} cases):")
    print(f"   Records found: {num_records:,}")
    print(f"   Countries affected: {num_countries}")
    
    if num_records > 0:
        print(f"   Max cases in single record: {high_cases_df['Confirmed'].max():,}")
    
    return high_cases_df


# ===== STEP 3: AGGREGATION =====

def aggregate_by_country(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate total cases, deaths, and statistics per country.
    
    Args:
        df: COVID-19 DataFrame
        
    Returns:
        DataFrame with aggregated country-level statistics, sorted by total cases
        
    Example:
        >>> agg_df = aggregate_by_country(df)
        >>> print(agg_df.head())
           Country  total_confirmed  total_deaths  avg_daily_cases
        0       US       45,231,123     1,234,567           28,456
    """
    country_col = 'Country/Region' if 'Country/Region' in df.columns else 'Country'
    
    print("\n--- Aggregating by Country ---")
    
    agg_df = df.groupby(country_col).agg(
        total_confirmed=('Confirmed', 'sum'),
        total_deaths=('Deaths', 'sum'),
        total_recovered=('Recovered', 'sum') if 'Recovered' in df.columns else ('Confirmed', lambda x: 0),
        avg_daily_cases=('Confirmed', 'mean'),
        max_daily_cases=('Confirmed', 'max'),
        num_records=('Confirmed', 'count')
    ).reset_index()
    
    # Rename country column to standard name
    agg_df = agg_df.rename(columns={country_col: 'Country'})
    
    # Sort by total confirmed cases
    agg_df = agg_df.sort_values('total_confirmed', ascending=False).reset_index(drop=True)
    
    print(f"Aggregated data for {len(agg_df)} countries")
    print(f"   Global total cases: {agg_df['total_confirmed'].sum():,}")
    print(f"   Global total deaths: {agg_df['total_deaths'].sum():,}")
    
    return agg_df

# ===== STEP 4: RISK METRICS =====

def calculate_risk_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate per-capita risk metrics for each country.
    
    Args:
        df: Aggregated country-level DataFrame
        
    Returns:
        DataFrame with cases/deaths per million and high_risk flag
        
    Example:
        >>> risk_df = calculate_risk_metrics(agg_df)
        >>> print(risk_df[['Country', 'cases_per_million', 'high_risk']].head())
           Country  cases_per_million  high_risk
        0       US         136,789.5        True
    """
    print("\n--- Calculating Risk Metrics ---")
    
    # Sample population data (in real analysis, we load from external source)
    population_data = {
        'US': 331000000,
        'India': 1380000000,
        'Brazil': 212000000,
        'France': 67000000,
        'Germany': 83000000,
        'United Kingdom': 67000000,
        'Italy': 60000000,
        'Russia': 144000000,
        'Spain': 47000000,
        'Turkey': 84000000,
        'Iran': 84000000,
        'Argentina': 45000000,
        'Colombia': 51000000,
        'Mexico': 128000000,
        'Poland': 38000000,
    }
    
    # Add population column
    df['Population'] = df['Country'].map(population_data)
    
    # Calculate per-capita metrics
    df['cases_per_million'] = (df['total_confirmed'] / df['Population']) * 1_000_000
    df['deaths_per_million'] = (df['total_deaths'] / df['Population']) * 1_000_000
    
    # High risk flag (>50,000 cases per million = >5% of population)
    df['high_risk'] = df['cases_per_million'] > 50000
    
    # Remove countries without population data
    df_with_pop = df.dropna(subset=['Population']).copy()
    
    # Print summary
    num_high_risk = df_with_pop['high_risk'].sum()
    print(f"Risk metrics calculated for {len(df_with_pop)} countries")
    print(f"   Countries with population data: {len(df_with_pop)}/{len(df)}")
    print(f"   High-risk countries (>50,000 per million): {num_high_risk}")
    
    return df_with_pop

# ===== STEP 5: SUMMARY STATISTICS =====

def generate_summary_stats(df: pd.DataFrame) -> dict:
    """
    Generate global summary statistics from COVID-19 data.
    
    Args:
        df: COVID-19 DataFrame (raw data, not aggregated)
        
    Returns:
        Dictionary containing global statistics
        
    Example:
        >>> stats = generate_summary_stats(df)
        >>> print(stats['total_cases'])
        100,000,000
    """
    print("\n--- Generating Summary Statistics ---")
    
    # Calculate global totals
    stats = {
        'total_cases': int(df['Confirmed'].sum()),
        'total_deaths': int(df['Deaths'].sum()),
        'total_recovered': int(df['Recovered'].sum()) if 'Recovered' in df.columns else 0,
    }
    
    # Get unique country count
    country_col = 'Country/Region' if 'Country/Region' in df.columns else 'Country'
    stats['countries_affected'] = df[country_col].nunique()
    
    # Calculate averages per country
    stats['avg_cases_per_country'] = int(df.groupby(country_col)['Confirmed'].sum().mean())
    stats['avg_deaths_per_country'] = int(df.groupby(country_col)['Deaths'].sum().mean())
    
    # Calculate case fatality rate
    stats['case_fatality_rate'] = (stats['total_deaths'] / stats['total_cases'] * 100) if stats['total_cases'] > 0 else 0
    
    # Get date range
    stats['latest_date'] = df['Date'].max()
    stats['earliest_date'] = df['Date'].min()
    stats['data_span_days'] = (pd.to_datetime(stats['latest_date']) - pd.to_datetime(stats['earliest_date'])).days
    
    # Print summary
    print(f"\nGlobal Summary Statistics:")
    print(f"   Total Cases: {stats['total_cases']:,}")
    print(f"   Total Deaths: {stats['total_deaths']:,}")
    print(f"   Total Recovered: {stats['total_recovered']:,}")
    print(f"   Countries Affected: {stats['countries_affected']}")
    print(f"   Average Cases per Country: {stats['avg_cases_per_country']:,}")
    print(f"   Average Deaths per Country: {stats['avg_deaths_per_country']:,}")
    print(f"   Case Fatality Rate: {stats['case_fatality_rate']:.2f}%")
    print(f"   Data Span: {stats['earliest_date']} to {stats['latest_date']} ({stats['data_span_days']} days)")
    
    return stats



# ===== STEP 6: SAVING & PIPELINE =====

def save_results(df: pd.DataFrame, filename: str) -> None:
    """
    Save DataFrame to CSV file in outputs directory.
    
    Args:
        df: DataFrame to save
        filename: Name of output file (e.g., 'results.csv')
        
    Returns:
        None (saves file to disk)
        
    Example:
        >>> save_results(country_df, 'country_summary.csv')
        Saved: outputs/country_summary.csv
    """
    filepath = OUTPUTS_DIR / filename
    df.to_csv(filepath, index=False)
    print(f"Saved: {filepath}")


def main():
    """
    Execute complete COVID-19 analysis pipeline.
    
    Pipeline steps:
        1. Load data from CSV
        2. Clean and prepare data
        3. Aggregate by country
        4. Calculate risk metrics
        5. Generate summary statistics
        6. Save results to CSV files
    
    Outputs:
        - outputs/country_summary.csv: Country-level statistics
        - outputs/risk_analysis.csv: Risk metrics and per-capita data
    """
    print("="*80)
    print(" "*20 + "COVID-19 DATA ANALYSIS PIPELINE")
    print("="*80 + "\n")
    
    # Step 1: Load data
    print("STEP 1: Loading Data")
    print("-" * 80)
    df = load_data()
    
    # Step 2: Clean data
    print("\nSTEP 2: Cleaning Data")
    print("-" * 80)
    df_clean = clean_data(df)
    
    # Step 3: Aggregate by country
    print("\nSTEP 3: Aggregating by Country")
    print("-" * 80)
    country_summary = aggregate_by_country(df_clean)
    
    # Step 4: Calculate risk metrics
    print("\nSTEP 4: Calculating Risk Metrics")
    print("-" * 80)
    risk_df = calculate_risk_metrics(country_summary)
    
    # Step 5: Generate summary statistics
    print("\nSTEP 5: Generating Summary Statistics")
    print("-" * 80)
    summary_stats = generate_summary_stats(df_clean)
    
    # Step 6: Save results
    print("\nSTEP 6: Saving Results")
    print("-" * 80)
    save_results(country_summary, 'country_summary.csv')
    save_results(risk_df, 'risk_analysis.csv')
    
    # Final summary
    print("\n" + "="*80)
    print("PIPELINE COMPLETE ✅")
    print("="*80)
    print(f"\nSummary:")
    print(f"   • Analyzed {summary_stats['countries_affected']} countries")
    print(f"   • Total cases: {summary_stats['total_cases']:,}")
    print(f"   • Total deaths: {summary_stats['total_deaths']:,}")
    print(f"   • Case fatality rate: {summary_stats['case_fatality_rate']:.2f}%")
    print(f"\nOutput Files:")
    print(f"   • outputs/country_summary.csv")
    print(f"   • outputs/risk_analysis.csv")
    print("\n" + "="*80)
    
    return summary_stats


# ===== MAIN EXECUTION =====

if __name__ == "__main__":
    """Running complete COVID-19 analysis pipeline."""
    main()
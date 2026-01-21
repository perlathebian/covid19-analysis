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



# ===== TESTING FUNCTIONS =====

if __name__ == "__main__":
    """Test data loading, cleaning, and filtering."""
    print("="*60)
    print("COVID-19 DATA ANALYSIS - STEP 2: FILTERING")
    print("="*60 + "\n")
    
    # Load and clean data
    df = load_data()
    df = clean_data(df)
    
    # Test filtering by country
    print("\n--- Testing Country Filter ---")
    india_df = filter_country(df, 'India')
    us_df = filter_country(df, 'US')
    
    # Test high cases filter
    print("\n--- Testing High Cases Filter ---")
    high_cases = filter_high_cases(df, threshold=10000)
    very_high_cases = filter_high_cases(df, threshold=100000)
    
    print("\n" + "="*60)
    print("STEP 2 COMPLETE ✅")
    print("="*60)
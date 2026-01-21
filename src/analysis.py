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


# ===== TESTING FUNCTIONS =====

if __name__ == "__main__":
    """Test data loading and cleaning."""
    print("="*60)
    print("COVID-19 DATA ANALYSIS - STEP 1: LOAD & CLEAN")
    print("="*60 + "\n")
    
    # Load data
    df = load_data()
    
    # Show sample
    print("\nFirst 5 rows:")
    print(df.head())
    
    # Clean data
    df_clean = clean_data(df)
    
    # Show result
    print("\nCleaned data sample:")
    print(df_clean.head())
    
    print("\n" + "="*60)
    print("STEP 1 COMPLETE ✅")
    print("="*60)
"""
COVID-19 Data Visualization
Generate charts and graphs from analysis results.
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path


# ===== PATH SETUP =====
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
OUTPUTS_DIR = PROJECT_ROOT / "outputs"

plt.style.use('seaborn-v0_8-darkgrid')


def plot_top_countries(csv_filename: str = 'country_summary.csv', 
                       top_n: int = 10,
                       save_filename: str = 'top_countries.png') -> None:
    """
    Create bar chart of top N countries by total confirmed cases.
    
    Args:
        csv_filename: Name of CSV file in outputs/ (default: 'country_summary.csv')
        top_n: Number of top countries to display (default: 10)
        save_filename: Name of output PNG file (default: 'top_countries.png')
        
    Returns:
        None (saves chart as PNG file)
        
    Example:
        >>> plot_top_countries('country_summary.csv', top_n=15)
        Chart saved: outputs/top_countries.png
    """
    # Load data
    filepath = OUTPUTS_DIR / csv_filename
    df = pd.read_csv(filepath)
    
    # Get top N countries
    top_countries = df.head(top_n)
    
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Create bar chart
    bars = ax.bar(top_countries['Country'], 
                  top_countries['total_confirmed'],
                  color='steelblue',
                  edgecolor='navy',
                  linewidth=1.5)
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height):,}',
                ha='center', va='bottom',
                fontsize=10, fontweight='bold')
    
    # Customize plot
    ax.set_xlabel('Country', fontsize=14, fontweight='bold')
    ax.set_ylabel('Total Confirmed Cases', fontsize=14, fontweight='bold')
    ax.set_title(f'Top {top_n} Countries by COVID-19 Cases', 
                 fontsize=16, fontweight='bold', pad=20)
    
    # Format y-axis with commas
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x):,}'))
    
    # Rotate x-axis labels so that country names fit well
    plt.xticks(rotation=45, ha='right')
    
    # Add grid
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Adjust layout
    plt.tight_layout()
    
    # Save figure
    output_path = OUTPUTS_DIR / save_filename
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Chart saved: {output_path}")


def plot_risk_comparison(csv_filename: str = 'risk_analysis.csv',
                        save_filename: str = 'risk_comparison.png') -> None:
    """
    Create comparison chart of cases per million vs deaths per million.
    
    Args:
        csv_filename: Name of CSV file in outputs/ (default: 'risk_analysis.csv')
        save_filename: Name of output PNG file (default: 'risk_comparison.png')
        
    Returns:
        None (saves chart as PNG file)
        
    Example:
        >>> plot_risk_comparison('risk_analysis.csv')
        Chart saved: outputs/risk_comparison.png
    """
    # Load data
    filepath = OUTPUTS_DIR / csv_filename
    df = pd.read_csv(filepath)
    
    # Sort by cases per million
    df = df.sort_values('cases_per_million', ascending=False)
    
    # Create figure with two subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    
    # Plot 1: Cases per million
    bars1 = ax1.bar(df['Country'], 
                    df['cases_per_million'],
                    color='coral',
                    edgecolor='darkred',
                    linewidth=1.5)
    
    # Add value labels
    for bar in bars1:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height):,}',
                ha='center', va='bottom',
                fontsize=9, fontweight='bold')
    
    # Style plot 1
    ax1.set_xlabel('Country', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Cases per Million', fontsize=12, fontweight='bold')
    ax1.set_title('Cases per Million People', fontsize=14, fontweight='bold', pad=15)
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x):,}'))
    ax1.tick_params(axis='x', rotation=45)
    ax1.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Plot 2: Deaths per million
    bars2 = ax2.bar(df['Country'], 
                    df['deaths_per_million'],
                    color='lightcoral',
                    edgecolor='darkred',
                    linewidth=1.5)
    
    # Add value labels
    for bar in bars2:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height):,}',
                ha='center', va='bottom',
                fontsize=9, fontweight='bold')
    
    # Style plot 2
    ax2.set_xlabel('Country', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Deaths per Million', fontsize=12, fontweight='bold')
    ax2.set_title('Deaths per Million People', fontsize=14, fontweight='bold', pad=15)
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x):,}'))
    ax2.tick_params(axis='x', rotation=45)
    ax2.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Add overall title
    fig.suptitle('COVID-19 Per-Capita Risk Comparison', 
                 fontsize=16, fontweight='bold', y=0.98)
    
    # Adjust layout and save
    plt.tight_layout()
    output_path = OUTPUTS_DIR / save_filename
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Chart saved: {output_path}")


def main():
    """Generate all visualizations."""
    print("="*60)
    print("GENERATING VISUALIZATIONS")
    print("="*60 + "\n")
    
    # Generate charts
    plot_top_countries()
    plot_risk_comparison()
    
    print("\n" + "="*60)
    print("VISUALIZATIONS COMPLETE")
    print("="*60)


if __name__ == "__main__":
    main()

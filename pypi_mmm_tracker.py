#!/usr/bin/env python3
"""
Simplified PyPI Downloads Tracker for Marketing Mix Modeling Libraries

This script fetches daily download statistics from PyPI for MMM libraries
and creates visualizations for the last X days (default 30).

Usage:
    uv run pypi_mmm_tracker.py          # Uses 30 days (default)
    uv run pypi_mmm_tracker.py --days 7  # Uses 7 days
"""

import argparse
import pypistats
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import json
import time
import warnings
import numpy as np
from scipy import stats
warnings.filterwarnings('ignore')

MMM_PACKAGES = {
    'PyMC Marketing': 'pymc-marketing',
    'Google Meridian': 'google-meridian', 
    'Meta Robyn (Python)': 'robynpy',
    'Uber Orbit': 'orbit-ml'
}

def get_daily_downloads(package_name, start_date, end_date):
    """Get real daily download data for a package using pypistats.overall."""
    try:
        print(f"Fetching real daily data for {package_name}...")
        # Fetch overall daily data as pandas DataFrame
        data = pypistats.overall(package_name, total="daily", format="pandas")
        if data is None or data.empty:
            return pd.DataFrame()
        # Filter for 'without_mirrors' only
        data = data[data['category'] == 'without_mirrors']
        # Filter by date range
        data['date'] = pd.to_datetime(data['date']).dt.date
        start_dt = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_dt = datetime.strptime(end_date, '%Y-%m-%d').date()
        mask = (data['date'] >= start_dt) & (data['date'] <= end_dt)
        data = data.loc[mask]
        # Keep only relevant columns and add package name
        df = data[['date', 'downloads']].copy()
        df['package'] = package_name
        return df.reset_index(drop=True)
    except Exception as e:
        print(f"Error fetching data for {package_name}: {e}")
        return pd.DataFrame()

def fetch_all_daily_data(days):
    """Fetch daily download data for all packages for the last N days (for left plot)."""
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days)
    print(f"Fetching data from {start_date} to {end_date} ({days} days)")
    print("-" * 60)
    all_data = []
    for display_name, package_name in MMM_PACKAGES.items():
        df = get_daily_downloads(package_name, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
        if not df.empty:
            df['display_name'] = display_name
            all_data.append(df)
        time.sleep(1)
    if all_data:
        return pd.concat(all_data, ignore_index=True)
    else:
        return pd.DataFrame()

def fetch_all_cumulative_data():
    """Fetch daily download data for all packages since inception (up to 10 years)."""
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=365*10)
    print(f"Fetching cumulative data from {start_date} to {end_date} (up to 10 years)")
    print("-" * 60)
    all_data = []
    for display_name, package_name in MMM_PACKAGES.items():
        df = get_daily_downloads(package_name, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
        if not df.empty:
            df['display_name'] = display_name
            all_data.append(df)
        time.sleep(1)
    if all_data:
        return pd.concat(all_data, ignore_index=True)
    else:
        return pd.DataFrame()

def calculate_cagr(start_value, end_value, periods):
    """Calculate Compound Annual Growth Rate (CAGR)."""
    if start_value <= 0 or end_value <= 0 or periods <= 0:
        return 0
    return ((end_value / start_value) ** (1 / periods) - 1) * 100

def create_plots(df, days, cumulative_df):
    """Create two-panel visualization: daily and cumulative downloads."""
    if df.empty or cumulative_df.empty:
        print("No data available for visualization")
        return

    # Try to use ArviZ style if available
    try:
        import arviz as az
        az.style.use('arviz-doc')
    except ImportError:
        plt.style.use('seaborn-v0_8-darkgrid')
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['axes.linewidth'] = 1.5
    plt.rcParams['grid.linewidth'] = 1
    plt.rcParams['lines.linewidth'] = 3
    
    # Create figure with modern aesthetics
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7), dpi=100)
    fig.suptitle('PyPI MMM Libraries Download Statistics', 
                 fontsize=20, fontweight='bold', y=1.02)
    
    # Left plot: Daily downloads (recent)
    for display_name in df['display_name'].unique():
        package_data = df[df['display_name'] == display_name].copy()
        package_data = package_data.sort_values('date')
        ax1.plot(package_data['date'], package_data['downloads'], 
                marker='.', markersize=10, label=display_name, 
                linewidth=3, alpha=0.9)
    
    ax1.set_title(f'Daily Downloads (Last {days} Days)', 
                  fontsize=18, fontweight='medium', pad=15)
    # Remove x-axis label
    # ax1.set_xlabel('Date', fontsize=11, labelpad=10)
    # ax1.set_ylabel('Downloads per Day', fontsize=16, labelpad=10)
    ax1.legend(frameon=True, framealpha=0.95, loc='upper left', fontsize=16)
    ax1.grid(True, alpha=0.3)
    ax1.tick_params(axis='x', rotation=30, labelsize=14)
    ax1.tick_params(axis='y', labelsize=16)
    
    # Right plot: Cumulative downloads since inception
    for display_name in cumulative_df['display_name'].unique():
        package_data = cumulative_df[cumulative_df['display_name'] == display_name].copy()
        package_data = package_data.sort_values('date')
        package_data['cumulative'] = package_data['downloads'].cumsum()
        ax2.plot(package_data['date'], package_data['cumulative'], 
                marker='.', markersize=8, label=display_name, 
                linewidth=3, alpha=0.9)
    
    ax2.set_title('Cumulative Downloads (Since Inception)', 
                  fontsize=18, fontweight='medium', pad=15)
    # Remove x-axis label
    # ax2.set_xlabel('Date', fontsize=11, labelpad=10)
    # ax2.set_ylabel('Total Downloads', fontsize=16, labelpad=10)
    ax2.legend(frameon=True, framealpha=0.95, loc='upper left', fontsize=16)
    ax2.grid(True, alpha=0.3)
    ax2.tick_params(axis='x', rotation=30, labelsize=16)
    ax2.tick_params(axis='y', labelsize=16)
    
    # Adjust layout and save
    plt.tight_layout()
    plt.savefig('mmm_downloads_analysis.png', dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    print(f"📊 Visualization saved as 'mmm_downloads_analysis.png'")

def save_data(df):
    """Save data to CSV file."""
    if not df.empty:
        df.to_csv('mmm_download_data.csv', index=False)
        print("💾 Data saved as 'mmm_download_data.csv'")

def main():
    parser = argparse.ArgumentParser(description='Track PyPI downloads for MMM libraries')
    parser.add_argument('--days', type=int, default=30, 
                       help='Number of days to analyze (default: 30)')
    args = parser.parse_args()
    print("🚀 MMM Libraries PyPI Download Tracker")
    print("="*50)
    # Fetch and process data
    df = fetch_all_daily_data(args.days)
    cumulative_df = fetch_all_cumulative_data()
    if not df.empty and not cumulative_df.empty:
        create_plots(df, args.days, cumulative_df)
        save_data(df)
        print(f"\n✅ Analysis complete for last {args.days} days!")
    else:
        print("No data retrieved. Please check package names and try again.")

if __name__ == "__main__":
    try:
        import pypistats
    except ImportError:
        print("❌ pypistats not found. Please install: pip install pypistats pandas matplotlib")
        exit(1)
    
    main()
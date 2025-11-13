# create the file paths dictionary
import pandas as pd
import numpy as np


google_filepaths={
    'timeline':{
        'kdrama': {
            'past5yr':'../data/raw/googletrends_01_multitimeline_kdrama_5years.csv',
            'squidgame1':'../data/raw/googletrends_01_multitimeline_kdrama_squidgame01_2021.csv',
            'squidgame2':'../data/raw/googletrends_01_multitimeline_kdrama_squidgame02_20240401_20250331.csv',
        },
        'learn_korean': {
            'past5yr':'../data/raw/googletrends_01_multitimeline_learnkorean_5years.csv',
            'squidgame1':'../data/raw/googletrends_01_multitimeline_learnkorean_squidgame01_2021.csv',
            'squidgame2':'../data/raw/googletrends_01_multitimeline_learnkorean_squidgame02_20240401_20250331.csv',
        }
    },
    'geo':{
        'kdrama': {
            'past5yr':'../data/raw/googletrends_02_geomap_kdrama_5years.csv',
            'squidgame1':'../data/raw/googletrends_02_geomap_kdrama_squidgame01_2021.csv',
            'squidgame2':'../data/raw/googletrends_02_geomap_kdrama_squidgame02_20240401_20250331.csv',
        },
        'learn_korean': {
            'past5yr':'../data/raw/googletrends_02_geomap_learnkorean_5years.csv',
            'squidgame1':'../data/raw/googletrends_02_geomap_learnkorean_squidgame01_2021.csv',
            'squidgame2':'../data/raw/googletrends_02_geomap_learnkorean_squidgame02_20240401_20250331.csv',
        }
    }
}



# function to load timeline data
def load_timeline_data(filepath, search_term):
    """
    Load Google Trends timeline data from CSV file.
    Skips the first two rows and renames first column to country.
    Converts 'Week' column to datetime and sets it as index.

    Args:
        filepath (dict): get file part from google_filepaths dictionary
        search_term (str): search term for the data

    Returns:
        pd.DataFrame: loaded and processed timeline data
    """
    try:
        # Load CSV, skipping first two rows
        df = pd.read_csv(filepath, skiprows=2)
        print(f"✅ Successfully loaded {search_term} data: {df.shape}")

        # Rename the columns
        df = df.rename(columns={df.columns[0]: 'week', df.columns[1]: search_term})

        df['week'] = pd.to_datetime(df['week'])

        # Set week column as index
        df = df.set_index('week')

        # check if index is sorted
        is_sorted = df.index.is_monotonic_increasing
        print(f"📈 {search_term}'s Index DateTime Column sorted: {is_sorted}. So no sorting is required")
        if not is_sorted:
            print("   Sorting Index DateTime Column ...")
            df = df.sort_index()
            print("   ... Index DateTime Column Sorted!")

        # Preview the data
        print(f"📊 {search_term} Preview:")
        print(f"   Shape: {df.shape}")
        print(f"   Index Column: {df.index.name}")
        print(f"   Date range: {df.index.min().strftime('%d-%b-%Y')} to {df.index.max().strftime('%d-%b-%Y')}")
        print(f"   First 5 rows:")
        print(df.head())

        # end of data loading
        print("=" * 80) 

        return df
        
    except FileNotFoundError:
        print(f"❌ File not found: {filepath}")
        return None




# function to load region search data
def load_geo_data(filepath, search_term):
    """
    Load Google Trends geo data from CSV file.
    Skips the first two rows and renames first column to country.
    Converts search term to numeric by replacing '<1' with 0.5 and NaN with 0.

    Args:
        filepath (dict): get file part from google_filepaths dictionary
        search_term (str): search term for the data 

    Returns:
        pd.DataFrame: loaded and processed geo data
    """
    try:
        # Load CSV, skipping first two rows
        df = pd.read_csv(filepath, skiprows=2)
        print(f"✅ Successfully loaded {search_term} data: {df.shape}")

        # Rename the column
        df = df.rename(columns={
            df.columns[0]: 'country',
            df.columns[1]: search_term
        })

        # Convert search interest to numeric
        df[search_term] = df[search_term].replace('<1', '0.5')  
        df[search_term] = df[search_term].replace([np.nan], '0')  
        df[search_term] = pd.to_numeric(df[search_term], errors='coerce')

        # Check for duplicates in country column
        duplicate_countries = df['country'].duplicated().sum()
        if duplicate_countries > 0:
            print(f"   ⚠️ Found {duplicate_countries} duplicate country entries")
            duplicate_details = df[df['country'].duplicated(keep=False)]  # Show all duplicates
            print(f"   Duplicate countries: {duplicate_details['country'].unique().tolist()}")
        else:    
            print("   No duplicate country entries found.")

        # Preview the data
        print(f"\n📊 {search_term} Preview:")
        print(f"   Shape: {df.shape}")
        print(f"   First 5 rows:")
        print(df.head())

        # end of data loading
        print("=" * 80) 

        return df
    
    except FileNotFoundError:
        print(f"❌ File not found: {filepath}")
        return None        
    
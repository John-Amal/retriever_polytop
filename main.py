#!/usr/bin/env python
# coding: utf-8

import yaml
import os
import copy
from dotenv import load_dotenv

# Import our custom modules
from src import auth, data_loader, processor

def load_config(config_path="config.yaml"):
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def main():
    # 1. Setup Environment
    load_dotenv() # Reads .env file
    config = load_config()
    
    # 2. Authenticate (Once)
    if config['settings']['live_request']:
        auth.authenticate(
            config['settings']['auth_script'],
            config['settings']['user'],
            os.getenv("DESP_PASSWORD")
        )

    # 3. Expand Date Range
    raw_date_input = config['request']['date']
    # This turns "20180101/to/20180103" into ['20180101', '20180102', '20180103']
    date_list = data_loader.expand_date_range(raw_date_input)
    
    print(f"Target Dates ({len(date_list)}): {date_list}")

    # 4. Loop Through Each Date
    for current_date in date_list:
        print(f"\n--- Processing Date: {current_date} ---")
        
        # Create a specific request for just this one day
        # We use deepcopy to avoid overwriting the main config object
        current_request = copy.deepcopy(config['request'])
        current_request['date'] = current_date
        
        try:
            # A. Fetch Data (Get the GRIB)
            data, grib_path = data_loader.fetch_data(current_request, config)
            
            # B. Optional Conversion (Get the NetCDF)
            if config['processing'].get('nc', False):
                processor.process_to_netcdf(data, config, grib_path)
            else:
                print("  Skipping NetCDF conversion (nc=False)")

        except Exception as e:
            print(f"  FAILED for date {current_date}: {e}")
            # We continue to the next date even if one fails
            continue

    print("\nAll tasks completed.")

if __name__ == "__main__":
    main()

import os
import earthkit.data
from datetime import datetime, timedelta

def expand_date_range(date_str):
    """
    Parses 'YYYYMMDD/to/YYYYMMDD' and returns a list of daily strings.
    If it's a single date, returns a list with just that date.
    """
    if isinstance(date_str, list):
        return date_str  # Already a list
        
    # Check for the range syntax
    if "/to/" in date_str:
        start_str, end_str = date_str.split("/to/")
        start_date = datetime.strptime(start_str.strip(), "%Y%m%d")
        end_date = datetime.strptime(end_str.strip(), "%Y%m%d")
        
        date_list = []
        current_date = start_date
        while current_date <= end_date:
            date_list.append(current_date.strftime("%Y%m%d"))
            current_date += timedelta(days=1)
        return date_list
    
    return [date_str] # Fallback for single date

def get_dynamic_path(config_path_pattern, request):
    """
    Fills in the {param} and {realization} placeholders.
    Input: "./output_data/{param}/E{realization}"
    Output: "./output_data/165/E1"
    """
    try:
        return config_path_pattern.format(**request)
    except KeyError as e:
        print(f"Error: Config path uses a placeholder {e} that is not in the request.")
        raise

def generate_filename(request, output_dir):
    """
    Generates the full path including the filename.
    """
    # 1. Resolve the dynamic directory (e.g., ./output_data/165/E1)
    dynamic_dir = get_dynamic_path(output_dir, request)

    # 2. Create the directory if it doesn't exist
    os.makedirs(dynamic_dir, exist_ok=True)

    # 3. Create the filename
    date_val = request.get('date')
    filename = f"{request.get('param')}_{request.get('model')}_{request.get('experiment')}_{date_val}.grib"

    return os.path.join(dynamic_dir, filename)

def fetch_data(request, config):
    output_dir_pattern = config['settings']['output_dir']

    # Generate the full target path (directory + filename)
    target_file = generate_filename(request, output_dir_pattern)
    live_request = config['settings']['live_request']

    if live_request and not os.path.exists(target_file):
        print(f"  Downloading to: {target_file}")

        data = earthkit.data.from_source(
            "polytope",
            "destination-earth",
            request,
            address="polytope.mn5.apps.dte.destination-earth.eu",
            stream=False
        )
        data.to_target("file", target_file)
        print("  Download complete.")
    else:
        print(f"  Using local file: {target_file}")
        data = earthkit.data.from_source("file", target_file)

    return data, target_file

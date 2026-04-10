import os

def process_to_netcdf(data, config, source_filename):
    """
    Converts to NetCDF, saving in the same folder as the source GRIB.
    """
    # We derive the output folder directly from the source_filename
    # This ensures the .nc file always goes exactly where the .grib file is.
    output_dir = os.path.dirname(source_filename)
    base_name = os.path.splitext(os.path.basename(source_filename))[0]
    output_filename = os.path.join(output_dir, f"{base_name}.nc")

    target_param = config['processing']['target_param_name']
    
    print(f"  Converting to NetCDF: {output_filename}")
    
    try:
        ds = data.to_xarray()
        
        if target_param in ds:
            ds[target_param].attrs = {} 
            ds[target_param].to_netcdf(output_filename)
            print("  Conversion successful.")
        else:
            print(f"  WARNING: Variable '{target_param}' not found. Available vars: {list(ds.data_vars)}")
            
    except Exception as e:
        print(f"  ERROR during conversion: {e}")

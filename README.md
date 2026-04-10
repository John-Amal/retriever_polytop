# Retriever Polytop

A Python-based automated data retrieval and processing pipeline for downloading meteorological, ocean, and climate data via the **Destination Earth Polytope API**.

## 🌟 Overview

This tool automates the process of authenticating with the DESP platform, retrieving GRIB datasets across specific date ranges, and optionally processing/converting them into NetCDF format.

### Key Components

- **`main.py`**: The primary orchestrator script that loads configurations, authenticates, loops over requested date ranges, and handles the download/process pipeline.
- **`config.yaml`**: The central configuration file mapping out your user settings, output directories, data request schemas (like generation, stream, realization, parameter ID, etc.), and processing options.
- **`desp-authentication.py`**: Handles OAuth2 logic to communicate with the Destination Earth IAM (`auth.destine.eu`) to generate and store offline tokens.
- **`src/`**: Contains the internal modules:
  - `auth.py`: Wrapper for DESP authentication logic.
  - `data_loader.py`: Handles date-range expansion and downloading data via Polytope.
  - `processor.py`: Internal processing logic (e.g., GRIB to NetCDF conversion).

## 🛠 Prerequisites

To use this routine, ensure you have the following installed:
- Python 3.x
- Required dependencies: `pyyaml`, `python-dotenv`, `requests`, `lxml`, `conflator`, `pydantic`.
- Polytope CLI and API libraries (if required by `data_loader.py`).

## 🚀 Setup & Configuration

### 1. Environment Verification
Create a `.env` file in the root of the folder and configure your Destination Earth password (since the username can be placed in the config file):
```env
DESP_PASSWORD="your_actual_password_here"
```

### 2. Configure the Request (`config.yaml`)
Modify the `config.yaml` to tailor what data you fetch:

* **Settings**: Configure `user` with your username and define the `output_dir` structure.
* **Request Block**: Define the specific data you need (`dataset`, `param`, `experiment`, `levtype`, etc.). 
* **Date Parsing**: The tool supports expanding ranges. Use `YYYYMMDD/to/YYYYMMDD` to fetch data sequentially day-by-day, or define a single date string.
* **Processing Module**: Enable or disable NetCDF conversion by setting `nc: true` or `nc: false`.

## 🖥 Usage

Once the `.env` and `config.yaml` files are set, simply run:

```bash
python main.py
```

### Execution Flow:
1. **Authentication**: Uses `desp-authentication.py` to get an offline token. It only triggers a live request if configured.
2. **Date Expansion**: Parses the `date` key in your config and sets up an array of dates to loop over.
3. **Download**: Grabs the GRIB file day by day, saving it to your `output_dir`.
4. **Conversion (Optional)**: If `nc: true` is set, processes the downloaded GRIB file to NetCDF for the specific `target_param_name`.
5. **Resilience**: If a specific date fails to download, the script will naturally log the exception and move forward to the next date without crashing.

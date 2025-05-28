# PyPI MMM Tracker

A simple tool to track and visualize daily download statistics from PyPI for popular Marketing Mix Modeling (MMM) libraries.

## Features
- Fetches real daily download data from PyPI for selected MMM libraries (e.g., PyMC Marketing, Google Meridian, Meta Robyn, Uber Orbit)
- Visualizes recent daily downloads (left plot) and cumulative downloads since inception (right plot)
- Saves both the visualization and the raw data as output files
- Easy to use from the command line

## Usage

Install dependencies (recommended: use a virtual environment):

```bash
uv pip install -r requirements.txt
```

Run the tracker for the last 30 days (default):

```bash
uv run pypi_mmm_tracker.py
```

Or specify a custom number of days for the recent daily plot:

```bash
uv run pypi_mmm_tracker.py --days 90
```

## Output
- `mmm_downloads_analysis.png`: Side-by-side plots of daily and cumulative downloads
- `mmm_download_data.csv`: Raw daily download data for the selected period

## Dependencies
- Python 3.12+
- matplotlib
- pandas
- pypistats
- requests
- scipy
- seaborn

All dependencies are listed in `pyproject.toml`.

## License

Copyright 2024 (c) The PyPI MMM Tracker Authors

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

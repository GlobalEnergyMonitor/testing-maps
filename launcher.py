
import argparse
import os
import warnings
from datetime import datetime, timedelta 


today_date = datetime.today()

this_year = today_date.isoformat().split('-')[0]
print(this_year)

# adapted from GEMwiki/launcher.py

# Filter DeprecationWarning or FutureWarning
warnings.filterwarnings("ignore", category=FutureWarning)


def main():
    # make necessary directories if they don't exist
    # INSERT directory making things here from all_config.py and TODO tabs
    # list of trackers currently supported
    # trackers = ["cement", "coal mine", "combustion", "GOGET", "geothermal", "hydro", "iron mine", "methane", "nuclear", "solar", "steel", "wind"]
    list_of_all_official = ["Oil & Gas Plants", "Coal Plants", "Solar", "Wind", "Nuclear", "Hydropower", "Bioenergy", "Geothermal", "Coal Terminals", "Oil & Gas Extraction", "Coal Mines", "LNG Terminals", "Gas Pipelines", "Oil Pipelines", "Iron & Steel", "Iron ore Mines", "Cement and Concrete"]
    tracker_mapnames = ["europe", "africa", "integrated", "asia", "latam", "ggit", "goit", "goget", "gctt", "gcpt", "gcmt", "gogpt", "gspt", "gwpt", "gnpt", "gbpt", "ggpt", "ghpt", "gist", "gmet", "giomt"]

    month_number = {
        "01": "January",
        "02": "February",
        "03": "March",
        "04": "April",
        "05": "May",
        "06": "June",
        "07": "July",
        "08": "August",
        "09": "September",
        "10": "October",
        "11": "November",
        "12": "December"
    } 
    
    
    # create arg parser and argument details
    parser = argparse.ArgumentParser(description="Dispatcher for running map file generation and final data s3 upload scripts")
    parser.add_argument("mode", choices=["generate"], help="(req) What mode to run")
    parser.add_argument("project_name", choices=list_of_all_official, help="(req) Name of the project to run")
    parser.add_argument("--releaseiso", choices=[f"{i:02}" for i in range(1, 13)], help="(req) Month of official release")
    parser.add_argument("--priority", choices=tracker_mapnames, help="[generate param] Optionally provide a map file to prioritize")
    parser.add_argument("--new_h2_data", choices=[True, False], help="[generate param] Defaults to being false. Only relevant for maps containing European Gas and Oil Plant data")
    parser.add_argument("--pm_preview_mode", choices=[True, False], help="[generate param] Defaults to being false. Only relevant for GGIT test map Baird uses.")
    parser.add_argument("--simplified", choices=[True, False], help="[generate param] Defaults to being false. Reduces the columns to bare minimum for quickest map rendering.")
    
    # parser.add_argument("--output-dir", help="[generate param] Path to the output directory")
    # could pull out upload function to only optionally save to s3

    parser.add_argument("--save-s3", help="[generate param] Uploads all files to digital ocean publicgemdata bucket")
    
    parser.add_argument("--section", choices=["coal emissions", "gas finance", "plumes detected", "ownership tree"], help="[generate_insert param (req)] Which section to generate")

    args = parser.parse_args()

    # if args.mode == "generate":


if __name__ == "__main__":
    main()


from datetime import datetime, timedelta 
import os
import gspread
from numpy import true_divide
import sys
from creds import *
import logging
import subprocess
from pathlib import Path

today_date = datetime.today()

iso_today_date = today_date.isoformat().split('T')[0]
iso_today_date_folder = f'{iso_today_date}/'

list_of_all_official = [
    "Oil & Gas Plants",
    "Coal Plants",
    "Solar",
    "Wind",
    "Nuclear",
    "Hydropower",
    "Bioenergy",
    "Geothermal",
    "Coal Terminals",
    "Oil & Gas Extraction",
    "Coal Mines",
    "LNG Terminals",
    "Gas Pipelines",
    "Oil Pipelines",
    # "Gas Pipelines EU",
    # "LNG Terminals EU",
    # "GOGPT EU",
    "Iron & Steel",
    # "Plumes",
    "Iron ore Mines",
    # "coal finance",
    # "Energy Ownership",
    # "Integrated",
    "Cement and Concrete",

]

pm_preview_mode = False # For Baird's testing work
trackers_to_update = ["Nuclear"] # official tracker tab name in map tracker log sheet
new_release_date = 'August_2025' # for within about page NEEDS TO BE FULL MONTH
releaseiso = '2025-08'
simplified = False # True False
new_h2_data = False
priority = ['gnpt'] 
tracker_mapnames = ["europe", "africa", "integrated", "asia", "latam", "ggit", "goit", "goget", "gctt", "gcpt", "gcmt", "gogpt", "gspt", "gwpt", "gnpt", "gbpt", "ggpt", "ghpt", "gist", "gmet", "giomt"]

# At the beginning of all_config.py
def ensure_compilation_folders():
    """Ensure compilation_output folders exist in all tracker directories"""
    trackers_dir = Path(__file__).parent / 'trackers'
    
    for tracker_dir in trackers_dir.iterdir():
        if tracker_dir.is_dir() and not tracker_dir.name.startswith('.'):
            compilation_dir = tracker_dir / 'compilation_output'
            compilation_dir.mkdir(exist_ok=True)

# Run at import time
ensure_compilation_folders()


# def main():
# make necessary directories if they don't exist
folders_needed = ["logfiles/", 'local_pkl/', "metadata_files/"]
for folder in folders_needed:
    if not os.path.exists(folder): # TODO in future move to be ../logfiles
        os.mkdir(f"{folder}")
    # folder_dir = os.path.join(os.path.dirname(__file__), folder)
    # os.makedirs(folder_dir, exist_ok=True)
metadata_dir = os.path.join(os.path.dirname(__file__), 'metadata_files')
os.makedirs(metadata_dir, exist_ok=True)
local_pkl_dir = os.path.join(os.path.dirname(__file__), 'local_pkl')
os.makedirs(local_pkl_dir, exist_ok=True)

logpath = 'logfiles/'
logger = logging.getLogger(__name__)
log_file_path = f'{logpath}log_file_{iso_today_date}.log' 
logger.setLevel(logging.DEBUG)  # Set the lowest logging level for the logger
 
logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(message)s')

# def getLogger(tracker_name): # TODO use Hannah's code to make logger better

    # iso_date = datetime.now().strftime("%Y-%m-%d")

    # # Create a logger
    # logger = logging.getLogger("my_logger")
    # logger.setLevel(logging.DEBUG)  # Set the lowest logging level for the logger

    # # Create a handler for INFO and greater messages
    # log_file_name_info = f"../logfiles/{tracker_name}_{iso_date}_generation.log"
    # info_handler = logging.FileHandler(log_file_name_info, encoding="utf-8")
    # info_handler.setLevel(logging.INFO)  # Set the level to INFO

    # # Create a handler for ERROR and greater messages
    # log_file_name_error = f"../logfiles/{tracker_name}_{iso_date}_serious_errors.log"
    # error_handler = logging.FileHandler(log_file_name_error, encoding="utf-8")
    # error_handler.setLevel(logging.ERROR)  # Set the level to ERROR

    # # Create a formatter to define the log message format
    # formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    # # Set the formatter for both handlers
    # info_handler.setFormatter(formatter)
    # error_handler.setFormatter(formatter)

    # # Add the handlers to the logger
    # logger.addHandler(info_handler)
    # logger.addHandler(error_handler)


METADATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'metadata_files')
os.makedirs(METADATA_DIR, exist_ok=True)


tracker_folder_path = 'trackers/'

# run this first so all aws commands work later
s3_setup = (
    f'aws configure set s3.max_concurrent_requests 100'
) 
# if awskeyres == 'done':
#     pass
# else:
#     awskeyres = input('Go into 1password and set up the aws access key locally, if already done, type done.')

# subprocess.run(s3_setup, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# TODO explore why aws configure set s3.max_concurrent_requests 100 doesn't recognize aws David add to requirements

# github pages folder name to map log internal name when they do not match
mapname_gitpages = {
    "africa": "africa-energy",
    "latam": "LATAM",
    "goit": "GOIT",
    "goget": "GOGET",
    "gcpt": "coal-plant",
    "gcmt": "coal-mine",
    "gogpt": "gas-plant",
    "gspt": "solar",
    "gwpt": "wind",
    "gnpt": "nuclear",
    "gbpt": "bioenergy",
    "ggpt": "geothermal",
    "ghpt": "hydro",
    'gctt': "coal-terminals",
    'ggit-lng': 'ggit',
    'egt-gas': 'europe',
    'egt-term': 'europe',
    'gogpt-eu': 'europe',
    
}

official_tracker_name_to_mapname = {
    "Oil & Gas Plants": "gogpt", # done
    "Coal Plants": "gcpt", # done
    "Solar": "gspt", #done
    "Wind": "gwpt", # done
    "Nuclear": "gnpt", # done
    "Hydropower": "ghpt", #done 
    "Bioenergy": "gbpt", #done 
    "Geothermal": "ggpt", #done
    "Coal Terminals": "gctt", 
    "Oil & Gas Extraction": "goget",
    "Coal Mines": "gcmt",
    "LNG Terminals": "ggit-lng",
    "Gas Pipelines": "ggit",
    "Oil Pipelines": "goit",
    "Gas Pipelines EU": "egt-gas",
    "LNG Terminals EU": "egt-term",
    "GOGPT EU": "gogpt-eu",
    "Iron & Steel": "gist",
    "Plumes": "gmet",
    "Iron ore Mines": "giomt",
    "coal finance": "gcpft",
    "Energy Ownership": "ownership",
    "Integrated": "integrated",
    "Cement and Concrete": "gcct",
    "Integrated-simple": "integrated-simple",
}



# for configuring appropriate js format for legend
# RUlE is: no _ no spaces for values or section title
# TODO finish filling out
legcols_bymap = {
    "gcmt": ["status", "coal-grade", "mine-type"],
    "gcct": ["status", "plant-type", "prod-type"]
    
}
region_key = '1yaKdLauJ2n1FLSeqPsYNxZiuF5jBngIrQOIi9fXysAw'
region_tab = ['mapping']

# TODO swap out for rep points https://docs.google.com/spreadsheets/d/1Bu2RhxgvRW7yEJu6zbng_nudXBYRASNvRtgIOvrDN0c/edit?gid=975391128#gid=975391128 
# gem standard representative points Latitude_rep_point	Longitude_rep_point	GEM Standard Country Name
centroid_key = '1ETg632Bkwnr96YQbtmDwyWDpSHqmg5He0GQwJjJz8IU'  # Country/Area
centroid_tab = ['centroids']
rep_point_key = '1Bu2RhxgvRW7yEJu6zbng_nudXBYRASNvRtgIOvrDN0c', # GEM Standard Country Name
rep_point_tab = ['gem standard representative points']
# Format the date in ISO format
# Get today's date

client_secret_full_path = os.path.expanduser("~/") + client_secret
gem_path = os.path.join(os.path.dirname(__file__), 'trackers/')
# gem_path_tst = '~/testing/'
path_for_pkl = gem_path + 'local_pkl/'
gspread_creds = gspread.oauth(
        scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"],
        credentials_filename=client_secret_full_path,
        # authorized_user_filename=json_token_name,
    )
# dtype_spec = {} #{'Latitude': float, 'Longitude': float}
# numeric_cols = ['capacity', 'start_year', 'capacity2', 'prod_start_year', 'prod_gas', 'prod_year_gas', 'prod_oil', 'prod_year_oil', 'prod-coal', ] #STOPPED AT GCMT March 3rd 2025
# list_official_tracker_names = ['Oil & Gas Plants', 'Coal Plants', 'Solar', 'Wind', 'Hydropower', 'Geothermal', 'Bioenergy', 'Nuclear', 'Coal Mines', 'Coal Terminals', 'Oil & Gas Extraction', 'Oil Pipelines', 'Gas Pipelines', 'LNG Terminals']

# maps_with_needed_conversion = ['asia', 'europe', 'africa', 'latam', 'ggit']
gas_only_maps = ['AGT', 'EGT', 'asia', 'europe', 'ggit'] 
non_gsheet_data = ['Gas Pipelines', 'LNG Terminals', 'Oil Pipelines', 'Gas Pipelines EU', 'LNG Terminals EU', 'GOGPT EU']
non_regional_maps = ['gist', 'gmet', 'giomt', 'gcct']

conversion_key = '1fOPwhKsFVU5TnmkbEyPOylHl3XKZzDCVJ29dtTngkew'
conversion_tab = ['data']
gcmt_closed_tab = 'Global Coal Mine Tracker (Close'


steel_gist_table_cols = [
    "announced-nominal-bf-capacity-(ttpa)",
    "announced-nominal-bof-steel-capacity-(ttpa)",
    "announced-nominal-dri-capacity-(ttpa)",
    "announced-nominal-eaf-steel-capacity-(ttpa)",
    "announced-other/unspecified-steel-capacity-(ttpa)",
    "cancelled-nominal-bf-capacity-(ttpa)",
    "cancelled-nominal-bof-steel-capacity-(ttpa)",
    "cancelled-nominal-dri-capacity-(ttpa)",
    "cancelled-nominal-eaf-steel-capacity-(ttpa)",
    "cancelled-other/unspecified-steel-capacity-(ttpa)",
    "construction-nominal-bf-capacity-(ttpa)",
    "construction-nominal-bof-steel-capacity-(ttpa)",
    "construction-nominal-dri-capacity-(ttpa)",
    "construction-nominal-eaf-steel-capacity-(ttpa)",
    "construction-other/unspecified-steel-capacity-(ttpa)",
    "mothballed-nominal-bf-capacity-(ttpa)",
    "mothballed-nominal-bof-steel-capacity-(ttpa)",
    "mothballed-nominal-dri-capacity-(ttpa)",
    "mothballed-nominal-eaf-steel-capacity-(ttpa)",
    "mothballed-nominal-ohf-steel-capacity-(ttpa)",
    "mothballed-other/unspecified-steel-capacity-(ttpa)",
    "mothballed-pre-retirement-nominal-bf-capacity-(ttpa)",
    "operating-nominal-bf-capacity-(ttpa)",
    "operating-nominal-bof-steel-capacity-(ttpa)",
    "operating-nominal-dri-capacity-(ttpa)",
    "operating-nominal-eaf-steel-capacity-(ttpa)",
    "operating-nominal-ohf-steel-capacity-(ttpa)",
    "operating-other/unspecified-steel-capacity-(ttpa)",
    "operating-pre-retirement-nominal-bf-capacity-(ttpa)",
    "operating-pre-retirement-nominal-bof-steel-capacity-(ttpa)",
    "operating-pre-retirement-nominal-dri-capacity-(ttpa)",
    "operating-pre-retirement-nominal-eaf-steel-capacity-(ttpa)",
    "operating-pre-retirement-other/unspecified-steel-capacity-(ttpa)",
    "retired-nominal-bf-capacity-(ttpa)",
    "retired-nominal-bof-steel-capacity-(ttpa)",
    "retired-nominal-eaf-steel-capacity-(ttpa)",
    "retired-nominal-ohf-steel-capacity-(ttpa)"
        ]


# TODO keep in retired year or closed year for longitudinal, and make sure start year is there too
final_cols = ['model','reactor-type','lat', 'lng','coordinate-accuracy','total-resource-(inferred', 'parent-gem-id', 'total-reserves-(proven-and-probable','start_date', 'owner-gem-id','owner-noneng','retired-year','plant-status','noneng_owner', 'parent_gem_id', 'status_display','owner_gem_id','facilitytype','unit_id', 'loc-oper', 'loc-owner', 'tech-type','ea_scaling_capacity', 'operator', 'Operator', 'Binational', 'binational', 'loc-accu','units-of-m','mapname','tracker-acro','official_name','url', 'areas','name', 'unit_name', 'capacity',
              'status', 'start_year', 'subnat', 'region', 'owner', 'parent', 'tracker', 'tracker_custom', 'operator-name-(local-lang/script)', 'owner-name-(local-lang/script)',
        'original_units', 'location-accuracy','conversion_factor', 'geometry', 'river', 'area2', 'region2', 'subnat2', 'capacity1', 'capacity2',
        'prod-coal', 'Latitude', 'Longitude', 'pid','id', 'prod_oil', 'prod_gas', 'prod_year_oil', 'prod_year_gas', 'fuel', 'PCI5', 'PCI6', 'pci5','pci6','WKTFormat', 'Fuel', 'maturity', 'fuel-filter', 
        'pci-list', 'coal-grade', 'mine-type', 'prod-coal', 'owners_noneng', 'noneng_name', 'coalfield', 'workforce', 'prod_year', 'opening-year', 'closing-year', 'opening_year', 'closing_year', 'end-year', 'pci-list', 'coal-grade', 'mine-type', 'prod-coal', 'owners_noneng', 'noneng_name', 'coalfield', 'workforce', 'prod_year', 'opening-year', 'closing-year', 'opening_year', 'closing_year', 'end-year',
        'claycal-yn', 'altf-yn', 'ccs-yn', 'prod-type', 'plant-type', 'entity-id', 'color', 'capacity-display', 'Clinker Capacity (millions metric tonnes per annum)', 'Cement Capacity (millions metric tonnes per annum)', "cem-type",
        'wiki-from-name', 'capacity-details', 'parent-search', 'owner-search', 'name-search', 'areas-subnat-sat-display', 'multi-country', 'noneng-name', "prod-method-tier-display", "prod-method-tier", "main-production-equipment"]
# add two together because gist list is so long and should be refactored soon
final_cols.extend(steel_gist_table_cols)


renaming_cols_dict = {
                        'GIOMT': {'GEM Asset ID': 'pid','Coordinate accuracy': 'coordinate-accuracy','GEM wiki page URL': 'url', 'Operating status': 'status', 'Asset name (English)': 'name', 'Asset name (other language)': 'noneng_name',
                                  'Design capacity (ttpa)': 'capacity', 'Owner': 'owner', 'Parent': 'parent', 'Start date': 'start_date', 'Country/Area':'areas',
                                  'Total resource (inferred, indicated and measured, thousand metric tonnes)': 'total-resource-(inferred', 
                                  'Total reserves (proven and probable, thousand metric tonnes)': 'total-reserves-(proven-and-probable', 'Parent GEM Entity ID': 'parent-gem-id',
                                  'Owner name in local language/script': 'owner-noneng', 'Owner GEM Entity ID': 'owner-gem-id', 'Subnational unit': 'subnat'},
                            
                    'GCCT': {'GEM Plant ID': 'pid', 'GEM Asset name (English)': 'name', 'Asset name (other language)': 'noneng_name', 'Coordinate accuracy': 'location-accuracy', 
                             'Subnational unit': 'subnat', 'Country/Area': 'areas',
                             'Cement Color': 'color', 'Operating status': 'status', 'Start date':'start_year', 'Owner name (English)': 'owner',
                             'Owner name (other language)': 'loc-owner', 'GEM Entity ID':'entity-id', 'Plant type':'plant-type', 
                             'Production type':'prod-type',
                             'CCS/CCUS': 'ccs-yn', 'Alternative Fuel': 'altf-yn', 'Clay Calcination': 'claycal-yn', 'GEM wiki page': 'url', "Majority Cement Type": "cem-type"},

                    'GIST': {'Plant ID': 'pid','plant-status':'status', 'GEM wiki page': 'url', 'tab-type_x': 'tab-type', 'Country/Area': 'areas', 'Plant name (English)': 'name','Start date': 'start_year',
                    'Coordinate accuracy': 'location-accuracy', 'Plant name (other language)': 'noneng_name', 'Owner': 'owner', 'Owner (other language)': 'noneng_owner', 'Owner GEM ID': 'owner_gem_id',
                    'Parent': 'parent', 'Parent GEM ID': 'parent_gem_id', 'Subnational unit (province/state)': 'subnat'},

                    'GOGPT': {'GEM location ID':'pid', 'GEM unit ID': 'id','Wiki URL': 'url','Country/Area': 'areas', 'Plant name': 'name', 'Unit name': 'unit_name', 
                              'Capacity (MW)': 'capacity', 'Status': 'status', 'Fuel': 'fuel', 'Owner(s)': 'owner', 'Parent(s)': 'parent',
                                'Start year': 'start_year', 'State/Province': 'subnat', 'Region': 'region'},
                      'GCPT': {'GEM location ID':'pid', 'GEM unit/phase ID': 'id','Country/Area': 'areas', 'Wiki URL':'url',
                                   'Plant name': 'name', 'Unit name':'unit_name', 'Plant name (other)': 'other_name', 'Plant name (local)': 'noneng_name',
                                   'Owner': 'owner', 'Parent': 'parent', 'Capacity (MW)': 'capacity', 'Status': 'status', 
                                   'Start year': 'start_year', 'Subnational unit (province, state)': 'subnat', 'Region': 'region', "Retired year": "retired-year"},
                      'GSPT': {'GEM location ID':'pid', 'GEM phase ID':'id','Country/Area': 'areas', 'Project Name': 'name', 'Phase Name': 'unit_name',
                               'Capacity (MW)': 'capacity', 'Status': 'status', 'Start year': 'start_year', 'Owner': 'owner',
                               'Region': 'region', 'State/Province':'subnat', 'Wiki URL': 'url'},
                      'GWPT': {'GEM location ID':'pid', 'GEM phase ID': 'id','Country/Area': 'areas', 'Project Name': 'name', 'Phase Name': 'unit_name',
                               'Capacity (MW)': 'capacity', 'Status': 'status', 'Start year': 'start_year', 'Owner': 'owner',
                               'Region': 'region', 'State/Province':'subnat', 'Wiki URL': 'url'},
                      'GNPT': {'GEM location ID':'pid', 'Reactor Type':'reactor-type', 'Model':'model','GEM unit ID': 'id','Country/Area': 'areas', 'Project Name': 'name', 'Unit Name': 'unit_name',
                               'Capacity (MW)': 'capacity', 'Status': 'status', 'Start Year': 'start_year', 'Owner': 'owner', 'Operator': 'operator',
                               'Region': 'region', 'State/Province':'subnat', 'Location Accuracy': 'location-accuracy','Wiki URL': 'url', 'Owner Name in Local Language / Script': 'owners_noneng', 
                               'Project Name in Local Language / Script': 'noneng_name'}, 
                      'GHPT': {'GEM location ID':'pid', 'GEM unit ID':'id','Country/Area 1': 'areas', 'Country/Area 2': 'area2','Project Name': 'name', 
                               'Country/Area 1 Capacity (MW)': 'capacity', 'Country/Area 2 Capacity (MW)': 'capacity2',
                               'Status': 'status', 'Start Year': 'start_year', 'Owner': 'owner', 'Operator': 'operator', 'Binational': 'binational',
                               'Region 1': 'region', 'Region 2': 'region2','State/Province 1':'subnat', 'State/Province 2':'subnat2', 'Owner Name (local lang/script)': 'loc-owner', 
                               'Operator Name (local lang/script)': 'loc-oper',
                               'Wiki URL': 'url', 'River / Watercourse': 'river', 'Location Accuracy': 'loc-accu', 'Technology Type': 'tech-type'},
                      'GBPT': {'GEM location ID':'pid', 'GEM phase ID':'id','Country/Area': 'areas', 'Project Name': 'name', 'Unit Name': 'unit_name',
                               'Capacity (MW)': 'capacity', 'Status': 'status', 'Start Year': 'start_year', 'Owner(s)': 'owner',
                               'Region': 'region', 'State/Province':'subnat', 'Wiki URL': 'url'},
                      'GGPT': {'GEM location ID':'pid', 'GEM unit ID':'id', 'Country/Area': 'areas', 'Project Name': 'name', 'Unit Name': 'unit_name',
                               'Unit Capacity (MW)': 'capacity', 'Status': 'status', 'Start Year': 'start_year', 'Owner': 'owner',
                               'Region': 'region', 'State/Province':'subnat', 'Wiki URL': 'url'},
                      
                      'GCTT': {'GEM Terminal ID':'pid', 'GEM Unit/Phase ID': 'unit_id','Coal Terminal Name': 'name', 'Coal Terminal Name (detail or other)': 'other_name','Parent Port Name': 'port','Wiki URL': 'url', 'Status': 'status', 'Owner': 'owner', 'Capacity (Mt)':'capacity',
                               'Start Year': 'start_year', 'Region': 'region', 'State/Province':'subnat', 'Country/Area': 'areas'},
                      
                      # TODO change GOGET to pid
                      'GOGET': {'Unit ID':'id', 'Wiki name': 'name', 'Country/Area': 'areas', 'Subnational unit (province, state)': 'subnat', 'Status': 'status', 'Discovery year': 'start_year', 'Production start year': 'prod_start_year',
                                'GEM region': 'region','Owner': 'owner', 'Parent': 'parent', 'Wiki URL': 'url', 'Production - Oil (Million bbl/y)': 'prod_oil', 'Production - Gas (Million m³/y)': 'prod_gas',
                                'Production - Total (Oil, Gas and Hydrocarbons) (Million boe/y)': 'capacity','Production Year - Oil': 'prod_year_oil', 'Production Year - Gas': 'prod_year_gas'
                                , 'Country List':'mult_countries', 'Fuel type': 'fuel'},
                      'GCMT': {'GEM Mine ID':'pid','Country / Area': 'areas', 'Mine Name': 'name', 'Mine Name (Non-ENG)': 'noneng_name','Status': 'status', 'Owners': 'owner', 'Owners (Non-ENG)': 'owners_noneng','Parent Company': 'parent', 'Capacity (Mtpa)': 'capacity', 
                               'Production (Mtpa)':'prod-coal', 'Year of Production': 'prod_year','Opening Year': 'start_year', 'Closing Year': 'end_year','State, Province': 'subnat', 'Region': 'region', 'GEM Wiki Page (ENG)': 'url', 'GEM Wiki Page (Non-ENG)': 'urlchina', 'Coalfield': 'coalfield', 'Workforce Size': 'workforce', 'Coal Grade': 'coal-grade',
                               'Mine Type': 'mine-type'},
                      'GOIT': {'ProjectID':'pid','Countries': 'areas', 'Wiki': 'url', 'PipelineName': 'name', 'SegmentName': 'unit_name', 'Status': 'status', 'Owner': 'owner',
                               'Parent': 'parent', 'CapacityBOEd': 'capacity', 'StartYear1': 'start_year', 'EndState/Province':'subnat', 'StartRegion': 'region',
                               'EndRegion': 'region2'},
                      'GGIT': {'ProjectID':'pid','Countries': 'areas','Wiki': 'url',
                                   'PipelineName':'name', 'SegmentName':'unit_name', 'Status':'status', 'Owner':'owner', 'Parent': 'parent',
                                   'StartYear1': 'start_year', 'CapacityBcm/y': 'capacity', 'StartState/Province': 'subnat',
                                   'StartRegion': 'region', 'EndState/Province': 'subnat2', 'EndRegion': 'region2'
                                   }, 
                      'GGIT-lng': {'ComboID':'pid','Wiki': 'url', 'TerminalName': 'name',
                                   'UnitName': 'unit_name', 'Status': 'status', 'Country': 'areas', 'Owner': 'owner', 
                                   'Parent': 'parent', 'CapacityInMtpa': 'capacity', 'StartYearEarliest': 'start_year', 'Region': 'region', 
                                   'State/Province': 'subnat'},
                        # GOGPT-eu two tabs
                        'plants': {'gem-location-id':'pid', 'gem-unit-id': 'id','wiki-url': 'url','country/area': 'areas', 'plant-name': 'name', 'unit-name': 'unit_name',
                                'capacity-(mw)': 'capacity', 'owner(s)': 'owner', 'parent(s)': 'parent', 'plant-name-in-local-language-/-script': 'other-local', 'other-name(s)': 'other-name',
                                'start-year': 'start_year', 'state/province': 'subnat'},

                        'plants_hy': {'gem-location-id':'pid', 'gem-unit-id': 'id','wiki-url': 'url','country/area': 'areas', 'plant-name': 'name', 'unit-name': 'unit_name',
                                'capacity-(mw)': 'capacity', 'owner(s)': 'owner', 'parent(s)': 'parent', 'plant-name-in-local-language-/-script': 'other-local', 'other-name(s)': 'other-name',
                                'start-year': 'start_year', 'state/province': 'subnat'},

                        # gas pipelines eu

                      'EGT-gas': {'projectid':'pid','countries': 'areas','wiki': 'url',
                                   'pipelinename':'name', 'segmentname':'unit_name',
                                   'startyear1': 'start_year', 'capacity': 'given_capacity','capacitybcm/y': 'capacity', 'startstate/province': 'subnat',
                                   'startregion': 'region', 'endstate/province': 'subnat2', 'endregion': 'region2', 'otherenglishnames': 'other-name',
                                    'otherlanguageprimarypipelinename': 'other-local',
                                   },
                        # gas terminals eu
                      'EGT-term': {'comboid':'pid','wiki': 'url', 'terminalname': 'name',
                                   'unitname': 'unit_name', 'country': 'areas', 'capacity': 'given_capacity','capacityinmtpa': 'capacity', 'startyear1': 'start_year', 'region': 'region',
                                   'state/province': 'subnat', 'otherlanguagename': 'other-name'},
                        }


# final_order_datadownload = ['Oil & Gas Plants', 'Coal Plants', 'Solar', 'Wind', 'Nuclear', 'Hydropower', 'Bioenergy', 'Geothermal', 'Coal Terminals', 'Oil & Gas Extraction', 'Coal Mines', 'Oil Pipelines', 'Gas Pipelines', 'LNG Terminals']
# tracker_mult_countries = ['GGIT', 'GOIT'] # mult_countries Country List, Countries do not span multiple columns for goget 

tracker_to_fullname = {
                    "GCPT": "coal power station",
                    "GOGPT": "oil & gas power station",
                    "GBPT": "bioenergy power station",
                    "GNPT": "nuclear power plant",
                    "GSPT": "solar power plant",  # GSPT is used for both "solar thermal" and "solar PV"
                    "GWPT": "wind power plant",
                    "GHPT": "hydropower plant",
                    "GGPT": "geothermal power plant",
                    "GOGET-oil": "oil & gas extraction area",
                    # "GOGET - gas": "gas extraction area",
                    "GOIT": "oil pipeline",
                    # "GGIT-eu": "gas pipeline",
                    "GGIT": "gas pipeline",
                    "GGIT-import": "LNG import terminal",
                    "GGIT-export": "LNG export terminal",
                    "GCMT": "coal mine",
                    "GCTT": "coal terminal",
                    "GIST": 'Iron & Steel',
                    "GIOMT": 'Iron ore Mines',
                    "GCCT": 'Cement and Concrete'
                }


tracker_to_legendname = {
                    "GCPT": "coal-power-station",
                    "GOGPT": "oil-gas-power-station",
                    "GBPT": "bioenergy-power-station",
                    "GNPT": "nuclear-power-plant",
                    "GSPT": "solar-power-plant",  # GSPT is used for both "solar thermal" and "solar PV"
                    "GWPT": "wind-power-plant",
                    "GHPT": "hydropower-plant",
                    "GGPT": "geothermal-power-plant",
                    "GOGET-oil": "oil & gas extraction area",
                    # "GOGET - gas": "gas-extraction-area",
                    "GOIT": "oil-pipeline",
                    "GGIT": "gas-pipeline",
                    "GGIT-import": "LNG-import-terminal",
                    "GGIT-export": "LNG-export-terminal",
                    "GCMT": "coal-mine",
                    "GCTT": "coal-terminal"
}

multi_tracker_log_sheet_key = '15l2fcUBADkNVHw-Gld_kk7EaMiFFi8ysWt6aXVW26n8'
source_data_tab = ['source']
map_tab = ['map']
regional_multi_map_tab = ['regional_multi_map'] # regional 

multi_tracker_countries_sheet = '1UUTNERZYT1kHNMo_bKpwSGrUax9WZ8eyGPOyaokgggk'

# testing_path = '/Users/gem-tah/GEM_INFO/GEM_WORK/earthrise-maps/testing/'

full_country_list = [
    "Algeria", "Angola", "Benin", "Botswana", "British Indian Ocean Territory", "Burkina Faso", 
    "Burundi", "Cabo Verde", "Cameroon", "Central African Republic", "Chad", "Comoros", "DR Congo", 
    "Republic of the Congo", "Côte d'Ivoire", "Djibouti", "Egypt", "Equatorial Guinea", "Eritrea", 
    "Eswatini", "Ethiopia", "French Southern Territories", "Gabon", "The Gambia", "Ghana", "Guinea", 
    "Guinea-Bissau", "Kenya", "Lesotho", "Liberia", "Libya", "Madagascar", "Malawi", "Mali", "Mauritania", 
    "Mauritius", "Mayotte", "Morocco", "Mozambique", "Namibia", "Niger", "Nigeria", "Réunion", "Rwanda", 
    "Saint Helena, Ascension, and Tristan da Cunha", "Sao Tome and Principe", "Senegal", "Seychelles", 
    "Sierra Leone", "Somalia", "South Africa", "South Sudan", "Sudan", "Tanzania", "Togo", "Tunisia", 
    "Uganda", "Western Sahara", "Zambia", "Zimbabwe",
    
    "Anguilla", "Antigua and Barbuda", "Argentina", "Aruba", "Bahamas", "Barbados", "Belize", "Bermuda", 
    "Bolivia", "Bonaire, Sint Eustatius, and Saba", "Bouvet Island", "Brazil", "Canada", "Cayman Islands", 
    "Chile", "Colombia", "Costa Rica", "Cuba", "Curaçao", "Dominica", "Dominican Republic", "Ecuador", 
    "El Salvador", "Falkland Islands", "French Guiana", "Greenland", "Grenada", "Guadeloupe", "Guatemala", 
    "Guyana", "Haiti", "Honduras", "Jamaica", "Martinique", "Mexico", "Montserrat", "Nicaragua", "Panama", 
    "Paraguay", "Peru", "Puerto Rico", "Saint Barthélemy", "Saint Kitts and Nevis", "Saint Lucia", 
    "Saint Martin (French part)", "Saint Pierre and Miquelon", "Saint Vincent and the Grenadines", 
    "Sint Maarten (Dutch part)", "South Georgia and the South Sandwich Islands", "Suriname", 
    "Trinidad and Tobago", "Turks and Caicos Islands", "United States", "Uruguay", "Venezuela", 
    "Virgin Islands (British)", "Virgin Islands (U.S.)",
    
    "Afghanistan", "Armenia", "Azerbaijan", "Bahrain", "Bangladesh", "Bhutan", "Brunei", "Cambodia", "China", 
    "Cyprus", "Georgia", "Hong Kong", "India", "Indonesia", "Iran", "Iraq", "Israel", "Japan", "Jordan", 
    "Kazakhstan", "North Korea", "South Korea", "Kuwait", "Kyrgyzstan", "Laos", "Lebanon", "Macao", 
    "Malaysia", "Maldives", "Mongolia", "Myanmar", "Nepal", "Oman", "Pakistan", "Palestine", "Philippines", 
    "Qatar", "Saudi Arabia", "Singapore", "Sri Lanka", "Syria", "Taiwan", "Tajikistan", "Thailand", 
    "Timor-Leste", "Türkiye", "Turkmenistan", "United Arab Emirates", "Uzbekistan", "Vietnam", "Yemen",
    
    "Åland Islands", "Albania", "Andorra", "Austria", "Belarus", "Belgium", "Bosnia and Herzegovina", 
    "Bulgaria", "Croatia", "Czech Republic", "Denmark", "Estonia", "Faroe Islands", "Finland", "France", 
    "Germany", "Gibraltar", "Greece", "Guernsey", "Holy See", "Hungary", "Iceland", "Ireland", "Isle of Man", 
    "Italy", "Jersey", "Kosovo", "Latvia", "Liechtenstein", "Lithuania", "Luxembourg", "North Macedonia", 
    "Malta", "Moldova", "Monaco", "Montenegro", "Netherlands", "Norway", "Poland", "Portugal", "Romania", 
    "Russia", "San Marino", "Serbia", "Slovakia", "Slovenia", "Spain", "Svalbard and Jan Mayen", "Sweden", 
    "Switzerland", "Ukraine", "United Kingdom",
    
    "American Samoa", "Australia", "Christmas Island", "Cocos (Keeling) Islands", "Cook Islands", "Fiji", 
    "French Polynesia", "Guam", "Heard Island and McDonald Islands", "Kiribati", "Marshall Islands", 
    "Micronesia", "Nauru", "New Caledonia", "New Zealand", "Niue", "Norfolk Island", 
    "Northern Mariana Islands", "Palau", "Papua New Guinea", "Pitcairn", "Samoa", "Solomon Islands", 
    "Tokelau", "Tonga", "Tuvalu", "United States Minor Outlying Islands", "Vanuatu", "Wallis and Futuna"
]

africa_countries = [
    "Algeria", "Angola", "Angola-Republic of the Congo", "Benin", "Botswana",
    "British Indian Ocean Territory", "Burkina Faso", "Burundi", "Cabo Verde",
    "Cameroon", "Central African Republic", "Chad", "Comoros", "Côte d'Ivoire",
    "Djibouti", "DR Congo", "Egypt", "Equatorial Guinea", "Eritrea", "Eswatini",
    "Ethiopia", "French Southern Territories", "Gabon", "Ghana", "Guinea",
    "Guinea-Bissau", "Kenya", "Lesotho", "Liberia", "Libya", "Madagascar",
    "Malawi", "Mali", "Mauritania", "Mauritius", "Mayotte", "Morocco",
    "Mozambique", "Namibia", "Niger", "Nigeria", "Republic of the Congo",
    "Réunion", "Rwanda", "Saint Helena, Ascension, and Tristan da Cunha",
    "Sao Tome and Principe", "Senegal", "Senegal-Mauritania", "Seychelles",
    "Sierra Leone", "Somalia", "South Africa", "South Sudan", "Sudan",
    "Tanzania", "The Gambia", "Togo", "Tunisia", "Uganda", "Western Sahara",
    "Zambia", "Zimbabwe"
]


asia_countries = [
    # South Asia
    "Afghanistan", "Bangladesh", "Bhutan", "India", "Iran",
    "Maldives", "Nepal", "Pakistan", "Sri Lanka",

    # Southeast Asia
    "Brunei", "Cambodia", "Indonesia", "Laos", "Malaysia",
    "Myanmar", "Philippines", "Singapore", "Thailand",
    "Timor-Leste", "Vietnam", "Thailand-Malaysia",  "Vietnam-Malaysia",

    # East Asia
    "China", "China-Japan", "Hong Kong", "Japan", "Macao",
    "Mongolia", "North Korea", "South Korea", "Taiwan",

    # Multinational or Maritime Areas
    "South China Sea"
]


europe_countries = [
    'Åland Islands', 'Albania', 'Andorra', 'Austria', 'Belarus', 'Belgium', 
    'Bosnia and Herzegovina', 'Bulgaria', 'Croatia', 'Czech Republic', 
    'Denmark', 'Estonia', 'Faroe Islands', 'Finland', 'France', 'Germany', 
    'Gibraltar', 'Greece', 'Guernsey', 'Holy See', 'Hungary', 'Iceland', 
    'Ireland', 'Isle of Man', 'Italy', 'Jersey', 'Kosovo', 'Latvia', 
    'Liechtenstein', 'Lithuania', 'Luxembourg', 'North Macedonia', 'Malta', 
    'Moldova', 'Monaco', 'Montenegro', 'Netherlands', 'Norway', 'Poland', 
    'Portugal', 'Romania', 'Israel', 'San Marino', 'Serbia', 'Slovakia', 
    'Slovenia', 'Spain', 'Svalbard and Jan Mayen', 'Sweden', 'Switzerland', 
    'Ukraine', 'United Kingdom', 'Cyprus', 'Türkiye'
]



latam_countries = [
    # Caribbean
    "Anguilla", "Antigua and Barbuda", "Aruba", "Bahamas", "Barbados",
    "Belize", "Cayman Islands", "Cuba", "Curaçao", "Dominica",
    "Dominican Republic", "Grenada", "Guadeloupe", "Haiti", "Jamaica",
    "Martinique", "Montserrat",  "Saint Barthélemy",
    "Saint Kitts and Nevis", "Saint Lucia", "Saint Martin (French part)",
    "Saint Vincent and the Grenadines", "Sint Maarten (Dutch part)",
    "Trinidad and Tobago", "Turks and Caicos Islands", "Virgin Islands (British)",
   # "Virgin Islands (U.S.)", "Puerto Rico", -  gregor excludes

    # Central America
    "Costa Rica", "El Salvador", "Guatemala", "Honduras", "Mexico",
    "Nicaragua", "Panama",

    # South America
    "Argentina", "Bolivia", "Brazil", "Chile", "Colombia", "Ecuador",
    "French Guiana", "Guyana", "Paraguay", "Peru", "Suriname",
    "Uruguay", "Venezuela",

    # Special Cases
    "Bonaire, Sint Eustatius, and Saba", "Bouvet Island",
    "Falkland Islands", "South Georgia and the South Sandwich Islands",
    "Venezuela-Trinidad and Tobago"
]



geo_mapping = {'africa': africa_countries,
            'asia': asia_countries,
            'europe': europe_countries,
            'latam': latam_countries,
            'global': full_country_list,
            '': full_country_list
            }
    # when was in map class
    # geo = self.geo
    # self.needed_geo = geo_mapping[geo]
    
dd_tab_mapping = {'africa': 'Africa Energy',
            'asia': 'Asia Gas',
            'europe': 'Europe Gas',
            'latam': 'Portal Energético',
            'internal': 'internal',
            
            }
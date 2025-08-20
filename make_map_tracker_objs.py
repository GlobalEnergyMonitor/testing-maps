import pandas as pd
from numpy import absolute
import geopandas as gpd
from helper_functions import save_raw_s3, save_mapfile_s3
from map_class import MapObject
from map_tracker_class import TrackerObject
from all_config import releaseiso, iso_today_date
import yaml
import os
# from tqdm import tqdm # can adapt more, special tweaking for dataframe!

def make_map_tracker_objs(map_tab_df,row, prep_dict):
    map_obj = MapObject(
        name=map_tab_df.loc[row, 'mapname'],
        source=map_tab_df.loc[row, 'source'],
        geo=map_tab_df.loc[row, 'geo'], 
        needed_geo=[], # changes to list of countries from geo via get needed geo
        fuel=map_tab_df.loc[row, 'fuel'],
        pm=map_tab_df.loc[row, 'PM'], 
        trackers=[],
        aboutkey = map_tab_df.loc[row, 'about_key'],
        about=pd.DataFrame(),
    )
    
     
    # call all object methods here
    # map_obj.get_needed_geo()
    map_obj.get_about()
    # create tracker objs
    # create a tracker obj for each item in map source
    for item in map_obj.source:
        print(f'Creating source object for: {map_obj.name} {item}')
        print(f'Remember to clear out the local pkl files if needed!')
        # input('Check') # working

        tracker_source_obj = TrackerObject(
            key = prep_dict[item]['gspread_key'],
            name = prep_dict[item]['official name'], # official release tab name
            off_name = prep_dict[item]['official tracker name'], 
            tabs = prep_dict[item]['gspread_tabs'],
            release = prep_dict[item]['latest release'],
            acro = prep_dict[item]['tracker-acro'],
            geocol = prep_dict[item]['geocol'],
            fuelcol = prep_dict[item]['fuelcol'],
            about_key = prep_dict[item]['about_key'],
            about = pd.DataFrame(),
            data = pd.DataFrame()  # Initialize as an empty DataFrame
        )
        
        # SET UP DF AND ABOUT HERE
        # add something for new_h2_data
        tracker_source_obj.set_df()
        tracker_source_obj.get_about()
            
        # set data and about attributes for each tracker
        # if tracker_source_obj.acro == 'GOGPT-eu':
            
        #     print("TrackerObject Attributes:")
        #     print(f"Key: {tracker_source_obj.key}")
        #     print(f"Name: {tracker_source_obj.name}")
        #     print(f"Off Name: {tracker_source_obj.off_name}")
        #     print(f"Tabs: {tracker_source_obj.tabs}")
        #     print(f"Release: {tracker_source_obj.release}")
        #     print(f"Acro: {tracker_source_obj.acro}")
        #     print(f"Geocol: {tracker_source_obj.geocol}")
        #     print(f"Fuelcol: {tracker_source_obj.fuelcol}")
        #     print(f"About DataFrame: {tracker_source_obj.about}")
        #     print(f"Data DataFrame: {tracker_source_obj.data}")
        #     input('Check if tracker object attributes look right for GOGPT-eu') #working
        #     # append tracker obj to map obj attribute trackers 
        map_obj.trackers.append(tracker_source_obj)
        
        # TODO not sure why I can't save these as json and push to s3 like the others but not saved in the same place
        if tracker_source_obj.name in ['LNG Terminals', 'Gas Pipelines', 'Oil Pipelines', 'Gas Pipelines EU', 'LNG Terminals EU']:
            # getting an issue saving as json ... is it because ... idk should be df like everyone else
            print(tracker_source_obj.data)
            # input(f'check tracker name and data df: {tracker_source_obj.name}')
        else:
            # TODO look over s3 functions with Hannah's code
            # save_raw_s3(map_obj, tracker_source_obj, TrackerObject)
            print('WIP Done with save_raw_s3, check s3')
            
        # # save to metadata
        # mfile_actual = f"/Users/gem-tah/GEM_INFO/GEM_WORK/earthrise-maps/gem_tracker_maps/metadata_files/{map_obj.name}_{releaseiso}_{iso_today_date}_metadata.yaml"
        # print(f'this is mfile_actual: {mfile_actual}')
        # input('check if it matches')
        # # Prepare dictionary representations, but do not convert tracker_source_obj.data or map_obj.trackers
        # tracker_dict = tracker_source_obj.__dict__.copy()
        # map_dict = map_obj.__dict__.copy()

        # # Replace DataFrames/lists with their lengths for reporting
        # if isinstance(tracker_dict.get('data', None), pd.DataFrame):
        #     df = tracker_dict['data']
        #     tracker_dict['data'] = {
        #     "info": f"DataFrame with {len(df)} rows",
        #     "columns": [{col: str(df[col].dtype)} for col in df.columns],
        #     "columns2": [df.info()]
        #     }
        # if isinstance(map_dict.get('trackers', None), list):
        #     map_dict['trackers'] = f"List with {len(map_dict['trackers'])} TrackerObjects"

        # # Remove DataFrames (not serializable) or convert to string
        # for d in [tracker_dict, map_dict]:
        #     for k, v in list(d.items()):
        #         if isinstance(v, pd.DataFrame):
        #             d[k] = v.to_dict()  # or v.to_json() if preferred
        #         elif isinstance(v, list) and v and isinstance(v[0], TrackerObject):
        #             # For map_obj.trackers, store acros or dicts
        #             d[k] = [t.__dict__.copy() for t in v]

        # # Append to YAML file instead of overwriting

        # # Check if file exists and load existing data
        # if os.path.exists(mfile_actual):
        #     with open(mfile_actual, "r") as f:
        #         try:
        #             existing_data = yaml.safe_load(f) or []
        #         except Exception:
        #             existing_data = []
        # else:
        #     existing_data = []

        # # Ensure existing_data is a list
        # if not isinstance(existing_data, list):
        #     existing_data = [existing_data] if existing_data else []

        # # Append new entry
        # existing_data.append({'tracker': tracker_dict, 'map': map_dict})

        # # Write back the updated list
        # with open(mfile_actual, "w") as f:
        #     yaml.dump(existing_data, f, default_flow_style=False)

    # test if data got added
    for i, tracker in enumerate(map_obj.trackers):  # Iterate through tracker objects
        # df = tracker.data # TODO check if this is right
        
        try:
            # Open a file in append mode to log results
            with open("tracker_data_log.txt", "a") as log_file:
                log_file.write(f"DataFrame BEFORE {i}{tracker.acro}: {tracker.data.shape}\n")
            
            # Filter by geo and fuel and check result
            tracker.create_filtered_geo_fuel_df(map_obj.geo, map_obj.fuel)
            
            print(f'This is tracker.name {tracker.name}')
            # save filtered df to s3 and log to config yaml how long it is after filter
            # TODO commenting this out for now since data mgmt process still in progress 
            # save_mapfile_s3(map_obj.name, tracker.name, True, tracker.data)

            # Log the results after filtering
            with open("tracker_data_log.txt", "a") as log_file:
                log_file.write(f"DataFrame AFTER {i}{tracker.acro}: {tracker.data.shape}\n")

            # input('Check after geo filter')
            
        except AttributeError:

            main_or_h2 = tracker.data[0]
            prod_or_og = tracker.data[1]
            print(f"DataFrame {i}main{tracker.acro}: {main_or_h2.shape}")
            print(f"DataFrame {i}prod{tracker.acro}: {prod_or_og.shape}")

            tracker.create_filtered_geo_fuel_df(map_obj.geo, map_obj.fuel)
            main_or_h2 = tracker.data[0]
            prod_or_og = tracker.data[1]
            print(f"DataFrame {i}main geo filt{tracker.acro}: {main_or_h2.shape}")
            print(f"DataFrame {i}prod geo filt{tracker.acro}: {prod_or_og.shape}")

            # save filtered df to s3 and log to config yaml how long it is after filter
            # input('Check after geo filter')
            # TODO same as above 
            # save_mapfile_s3(map_obj.name, tracker.name, True, main_or_h2, prod_or_og)

        except TypeError as e:
            print(f'Fix error for {map_obj.name}: \n{e}')
            input('Check TypeError')
    

            
        
    return map_obj
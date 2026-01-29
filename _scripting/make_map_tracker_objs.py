import pandas as pd
from numpy import absolute
from map_class import MapObject
from map_tracker_class import TrackerObject
from all_config import nostopping, logger, trackers_to_update, final_cols, renaming_cols_dict


def make_map_tracker_objs(map_tab_df,row, prep_dict):
    map_obj = MapObject(
        mapname=map_tab_df.loc[row, 'mapname'],
        source=map_tab_df.loc[row, 'source'],
        geo=map_tab_df.loc[row, 'geo'], 
        # changes to list of countries from geo via get needed geo
        needed_geo=[], 
        fuel=map_tab_df.loc[row, 'fuel'],
        pm=map_tab_df.loc[row, 'PM'], 
        trackers=[],
        aboutkey = map_tab_df.loc[row, 'about_key'],
        about=pd.DataFrame(),
    )
    
     
    # call all object methods here
    print(f'map_obj.mapname is: {map_obj.mapname} if odd check what priority flag is in all_config')
    
    if map_obj.mapname in ['ggft', 'gmet', 'internal']: # gas finance workaround
        print('skip making about...we did not receive it from program')
    else:
        map_obj.get_about() # for entire map data download file
        # create tracker objs
    # create a tracker obj for each item in map source
    for item in map_obj.source:
        logger.info(f'Creating source object for: {map_obj.mapname} {item}')
        logger.info(f'Remember to clear out the local pkl files if needed!')
        # logger.info(msg=f'{prep_dict[item]}')
        item = item.strip()
        tracker_source_obj = TrackerObject(
            key = prep_dict[item]['gspread_key'],
            off_name = prep_dict[item]['official name'], 
            tab_name = prep_dict[item]['tab name'],  # official release tab name
            tabs = prep_dict[item]['gspread_tabs'],
            release = prep_dict[item]['latest release'],
            acro = prep_dict[item]['tracker-acro'],
            geocol = prep_dict[item]['geocol'],
            fuelcol = prep_dict[item]['fuelcol'],
            about_key = prep_dict[item]['about_key'],
            about = pd.DataFrame(),
            data = pd.DataFrame()  # Initialize as an empty DataFrame
        )
        
        # verify the latest release date is correct in map log gsheet
        if tracker_source_obj.off_name in trackers_to_update:
            input(f'Is this release date correct for {tracker_source_obj.off_name}? {tracker_source_obj.release}\nEdit the map tracker log sheet in GEM maps if not.')
            logger.info(f'Is this release date correct? {tracker_source_obj.release}\nEdit the map tracker log sheet in GEM maps if not.')

        else:
            logger.info(f'Is this release date correct for {tracker_source_obj.off_name}? {tracker_source_obj.release}\nEdit the map tracker log sheet in GEM maps if not.')
            
        # SET UP DF AND ABOUT HERE
        tracker_source_obj.set_df(final_cols, renaming_cols_dict) # need to set this up at the map level so sharing data pull, or add to a dictionary

        print(f'Check data leng {tracker_source_obj.off_name} {len(tracker_source_obj.data)}')
        if nostopping:
            print('pass')
        else:
            input('DEBUG CHECK THIS LENGTH') 
        
        if map_obj.mapname in ['ggft']:
            print('skipping get about again for gas finance')
        else:
            tracker_source_obj.get_about() # for tracker specific tab in a data download file
        print(f'Check data leng {tracker_source_obj.off_name} {len(tracker_source_obj.data)}')
        if nostopping:
            print('pass')
        else:
            input('DEBUG CHECK THIS LENGTH') # GOOD            
        # set data and about attributes for each tracker
        # append tracker obj to map obj attribute trackers 
        map_obj.trackers.append(tracker_source_obj)
        
    # filter by geo and fuel AND test if data got added
    for i, tracker in enumerate(map_obj.trackers):  # Iterate through tracker objects        
        if tracker.acro in ['GOGET']:

            main_goget = tracker.data[0]
            prod_or_og = tracker.data[1]
            logger.info(f"DataFrame {i}main{tracker.acro}: {main_goget.shape}")
            logger.info(f"DataFrame {i}prod{tracker.acro}: {prod_or_og.shape}")

            tracker.create_filtered_geo_fuel_df(map_obj.geo, map_obj.fuel)
            main_goget = tracker.data[0]
            prod_or_og = tracker.data[1]
            logger.info(f"DataFrame {i}main geo filt{tracker.acro}: {main_goget.shape}")
            logger.info(f"DataFrame {i}prod geo filt{tracker.acro}: {prod_or_og.shape}")

        else: 
            logger.info(f"DataFrame BEFORE {i}{tracker.acro}: {tracker.data.shape}\n")
            
            # Filter by geo and fuel and check result
            tracker.create_filtered_geo_fuel_df(map_obj.geo, map_obj.fuel)
            print(f'Check data leng {tracker.off_name} {len(tracker.data)}')
            logger.info(f'This is tracker.name {tracker.tab_name}')

            # Log the results after filtering
            logger.info(f"DataFrame AFTER {i}{tracker.acro}: {tracker.data.shape}\n")

            logger.info('Check after geo filter')
            

    
    return map_obj
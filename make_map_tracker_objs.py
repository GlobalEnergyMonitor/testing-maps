import pandas as pd
from numpy import absolute
from map_class import MapObject
from map_tracker_class import TrackerObject
from all_config import logger


def make_map_tracker_objs(map_tab_df,row, prep_dict):
    map_obj = MapObject(
        name=map_tab_df.loc[row, 'mapname'],
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
    map_obj.get_about()
    # create tracker objs
    # create a tracker obj for each item in map source
    for item in map_obj.source:
        logger.info(f'Creating source object for: {map_obj.name} {item}')
        logger.info(f'Remember to clear out the local pkl files if needed!')

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
        # append tracker obj to map obj attribute trackers 
        map_obj.trackers.append(tracker_source_obj)
        
        if tracker_source_obj.name in ['LNG Terminals', 'Gas Pipelines', 'Oil Pipelines', 'Gas Pipelines EU', 'LNG Terminals EU']:
            logger.info(tracker_source_obj.data)
            logger.info(f'check tracker name and data df: {tracker_source_obj.name}')
        else:
            # TODO look over s3 functions with Hannah's code
            # save_raw_s3(map_obj, tracker_source_obj, TrackerObject)
            print('WIP Done with save_raw_s3, check s3')

    # test if data got added
    for i, tracker in enumerate(map_obj.trackers):  # Iterate through tracker objects        
        try:
            
            logger.info(f"DataFrame BEFORE {i}{tracker.acro}: {tracker.data.shape}\n")
            
            # Filter by geo and fuel and check result
            tracker.create_filtered_geo_fuel_df(map_obj.geo, map_obj.fuel)
            
            logger.info(f'This is tracker.name {tracker.name}')

            # Log the results after filtering
            logger.info(f"DataFrame AFTER {i}{tracker.acro}: {tracker.data.shape}\n")

            logger.info('Check after geo filter')
            
        except AttributeError:
            # that means it's a tuple case, for goget or europe map

            main_or_h2 = tracker.data[0]
            prod_or_og = tracker.data[1]
            logger.info(f"DataFrame {i}main{tracker.acro}: {main_or_h2.shape}")
            logger.info(f"DataFrame {i}prod{tracker.acro}: {prod_or_og.shape}")

            tracker.create_filtered_geo_fuel_df(map_obj.geo, map_obj.fuel)
            main_or_h2 = tracker.data[0]
            prod_or_og = tracker.data[1]
            logger.info(f"DataFrame {i}main geo filt{tracker.acro}: {main_or_h2.shape}")
            logger.info(f"DataFrame {i}prod geo filt{tracker.acro}: {prod_or_og.shape}")

        except TypeError as e:
            logger.warning(f'Fix error for {map_obj.name}: \n{e}')
            logger.warning('Check TypeError')
    
    return map_obj
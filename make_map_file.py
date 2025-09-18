from all_config import *
from helper_functions import *
from tqdm import tqdm


def make_map(list_of_map_objs):
    """
    Processes a list of map objects by iterating through their trackers, 
    cleaning and preparing data as needed, and returns a modified list of map objects.

    Args:
        list_of_map_objs (list): A list of map objects, each containing trackers with data to process.

    Returns:
        list: A list of processed map objects with updated tracker data.
    """
    list_of_map_objs_mapversion = []
    conversion_df = create_conversion_df(conversion_key, conversion_tab)
    for map_obj in tqdm(list_of_map_objs, desc='Running'):
        
        with open(f"{logpath}tracker_data_log.txt", "a") as log_file:
            log_file.write(f"Stopping on Map name: {map_obj.name}\n")
            log_file.write("Trackers in map:\n")
            [log_file.write(f"{tracker_obj.name}\n") for tracker_obj in map_obj.trackers]
            log_file.write("Confirm all trackers in map\n")

        for tracker_obj in map_obj.trackers:

            # this gets to each df within each map
            # first I should combine goget so we can stop filtering by tuple
            if isinstance(tracker_obj.data, tuple):
                # for goget and gogpt EU
                logger.info(tracker_obj.name)
                logger.info(isinstance(tracker_obj.data, tuple))
                if tracker_obj.acro == 'GOGPT-eu' or tracker_obj.name == 'GOGPT EU':
                    # this fuel filter needs to happen for gogpt eu before they get merged into one
                    tracker_obj.set_fuel_filter_eu() 
                    tracker_obj.set_maturity_eu()
                    # this one should create one gdf for the map
                    # this is where gogpt-eu gets renamed 
                    tracker_obj.deduplicate_gogpt_eu() 

                elif tracker_obj.name == 'Oil & Gas Extraction':
                    tracker_obj.process_goget_reserve_prod_data()
                    if map_obj.geo in ['europe']:
                        # this fuel filter should happen after goget is put into one and only if its for a europe map
                        tracker_obj.set_fuel_filter_eu() 
                        tracker_obj.set_maturity_eu()                       

            elif tracker_obj.name == 'GOGPT EU':
                tracker_obj.deduplicate_gogpt_eu()

                
            # this should happen if not tuple so not gogpt eu or goget but IS in europe
            else:       
                if tracker_obj.name in ['LNG Terminals EU', 'Gas Pipelines EU']:
                    logger.info('europe hit for map adjustments') 
                    # this fuel filter should happen when we are at this point of non tuple ville and just needs to happen to these other eu specific tracker dfs
                    tracker_obj.set_fuel_filter_eu() 
                    tracker_obj.set_maturity_eu()       
                elif tracker_obj.name in ['Cement and Concrete']: 
                    tracker_obj.gcct_changes()      
                elif tracker_obj.name in ['Iron & Steel']:
                    logger.info('IN IRON & STEEL')
                    tracker_obj.process_steel_iron_parent() 
                    tracker_obj.gist_changes() 
                elif tracker_obj.name in ['Iron ore Mines']:
                    tracker_obj.giomt_changes() 
            
            # ignore this tuple error message
            [print(tracker_obj.data[col]) for col in tracker_obj.data.columns if col == 'Clinker Capacity (millions metric tonnes per annum)']
            [print(tracker_obj.data[col]) for col in tracker_obj.data.columns if col == 'Cement Capacity (millions metric tonnes per annum)']
            
            # this should happen to ALL
            # clean_capacity and coordinate qc
            # TODO should lower case all cols at ONE point ... chaotic for split_goget because europe has lowercase and all else is unchanged unitl rename_and_concat
            tracker_obj.clean_num_data()

            tracker_obj.transform_to_gdf()
        
            tracker_obj.split_goget_ggit()
  
            tracker_obj.assign_conversion_factors(conversion_df)
        # we account for GOGPT eu that already aritficially set tracker-acro according to differences in columns of hy and plants in gogpt eu
        map_obj.rename_and_concat_gdfs() 

        map_obj.set_capacity_conversions()

        map_obj.map_ready_statuses_and_countries()

        map_obj.create_search_column()

        map_obj.capacity_hide_goget_gcmt()

        map_obj.set_fuel_goit()

        map_obj.last_min_fixes()

        map_obj.save_file()
        
        if simplified == True:
            print('Simplified is true so reducing cols and saving a smaller map file!')
            map_obj.simplified()

    # this will be the map obj with the filtered cleaned concatted one gdf
    list_of_map_objs_mapversion.append(map_obj) 
            
    return list_of_map_objs_mapversion

import pandas as pd
from all_config import *
from helper_functions import *
from make_map_tracker_objs import make_map_tracker_objs
from collections import OrderedDict
from tqdm import tqdm
import os


########
# Make data downloads for regional maps with goget change
########
def test_make_data_dwnlds(num_of_maps_to_create, tracker_to_update):

    if num_of_maps_to_create > 0:
        print(f'There will be {num_of_maps_to_create} maps created for {tracker_to_update} with priority {priority}')


def make_data_dwnlds(tracker):
    maplen = 0.0 # initialize for test later
    print(f'making dd for {tracker}!')
    source_tab_df = create_prep_file(multi_tracker_log_sheet_key, source_data_tab)
    # find which maps need to be updated
    # via map tab in multi_tracker_log_sheet_key
    # make an object called map
    map_obj_list = []  # Initialize map_obj_list outside the loop
    
    if not map_obj_list:
        map_tab_df = gspread_access_file_read_only(multi_tracker_log_sheet_key, map_tab)
        print(map_tab_df)
        # before orienting this df remove the rows we skip like Integrated, Coal Finance, Energy Ownership source_tab_df with SKIP THIS - We do not make this map with main script
        source_tab_df = source_tab_df[source_tab_df['tab name']!='SKIP THIS - We do not make this map with main script']
        
        prep_dict = source_tab_df.to_dict(orient='index')            
  
        for row in map_tab_df.index:
            
            # TO HELP PRIORITIZE AND SPEED UP CODE WHEN DEBUGGING SOMETHING AND NEED TO GET ANOTHER FILE OUT QUICKLY
            if map_tab_df.loc[row, 'mapname'] in priority:
                logger.info(f'Map name is in priority {priority} so making map object')
            elif priority == [''] or None:
                logger.info(f'Nothing is in priority so making map object')
            else:
                logger.info(f"Not making map object for {map_tab_df.loc[row, 'mapname']} moving onto next row in map_tab_df to save time!")
                continue
            
            
            if tracker in map_tab_df.loc[row, 'source']:
                logger.info(f'{tracker} is in source tab of gsheet map log')
                # create a map object from that row if tracker is in the source col
                
                map_obj = make_map_tracker_objs(map_tab_df, row, prep_dict=prep_dict)

                pkl_path = os.path.join(local_pkl_dir, f'map_obj_for_{map_obj.mapname}_on_{iso_today_date}.pkl')
                with open(pkl_path, 'wb') as f:
                    logger.info(f'saved to {f}')
                    pickle.dump(map_obj, f)
                logger.info(f"Updated map_obj.trackers for {map_obj.mapname}: {map_obj.source}")
                logger.info(f'Length of tracker list for {map_obj.mapname} {len(map_obj.trackers)}')
                map_obj_list.append(map_obj)

    
    else:
        logger.info(f'{len(map_obj_list)} maps to be updated with new {tracker} data!')

    maplen = len(map_obj_list)

    for map_obj in map_obj_list:
        print(F'This is map name:\n{map_obj.mapname}')
        print(F'This is list of sources:\n{map_obj.source}')
        logger.info(F'This is map name:\n{map_obj.mapname}')
        logger.info(F'This is list of sources:\n{map_obj.source}')
        # write to xls
        if map_obj.mapname in mapname_gitpages.keys():
            
            path_dwn = gem_path + mapname_gitpages[map_obj.mapname] + '/compilation_output/'
            path_tst = gem_path + mapname_gitpages[map_obj.mapname] + '/testing/'
        else:
            path_dwn = gem_path + map_obj.mapname + '/compilation_output/'
            path_tst = gem_path + map_obj.mapname + '/testing/'            
        os.makedirs(path_dwn, exist_ok=True)
        os.makedirs(path_tst, exist_ok=True)
        xlsfile = f'{path_dwn}{map_obj.mapname}-data-download_{new_release_dateinput}_{iso_today_date}.xlsx'
        xlsfile_testing = f'{path_tst}{map_obj.mapname}-data-download_{new_release_dateinput}_{iso_today_date}_test.xlsx'

        # write to excel files! 
        for filename in [xlsfile, xlsfile_testing]:
            with pd.ExcelWriter(filename, engine='openpyxl') as writer: 
                # THIS is where we can remap for the actual tab needed for the official data download ie. europe vs Europe Gas or latam vs Portal Energético
                if map_obj.mapname in dd_tab_mapping.keys():
                    about_tab_name = dd_tab_mapping[map_obj.mapname]
                else:
                    about_tab_name = map_obj.mapname
                
                map_obj.about.to_excel(writer, sheet_name=f'About {about_tab_name}', index=False, header=False) # TODO using header false id not work

                for tracker_obj in map_obj.trackers:

                    logger.info(f"Writing source to filename for tracke: {tracker_obj.off_name}")
                    logger.info(f'Length of tracker df is: {len(tracker_obj.data)}')
                    about = tracker_obj.about
                    tracker_name = tracker_obj.tab_name # TODO change to off name or swap out in all places for acro 
                    about.to_excel(writer, sheet_name=f'About {tracker_name}', index=False)
                    if isinstance(tracker_obj.data, tuple):
                        logger.info(f"In tuple part of make data dwnlds function for {tracker_obj.acro}, check the name can be gogpt eu (when there's new h2 data) or goget")
                        tracker_obj.set_data_official() # so have data for map and for datadownload

                        if tracker_obj.acro in ['GOGET']:
                            if len(tracker_obj.data) > 0:
                                pass
                            else:
                                input(f'data is empty for {tracker_name}')
                            main, prod = tracker_obj.data_official 
                            # checks if set data official works
                            for df in [main, prod]: 
                                if 'country_to_check' in df.columns.to_list():
                                    print(f'it is still there')
                                    input('data official not working')                      
                            logger.info(f"Main DataFrame shape: {main.shape}")
                            logger.info(f"Prod DataFrame shape: {prod.shape}")
                            
                            main = main.map(remove_illegal_characters)
                            prod = prod.map(remove_illegal_characters)
                            main.to_excel(writer, sheet_name=f'Extraction Main data', index=False)

                            prod.to_excel(writer, sheet_name=f'Extraction Production & reserves', index=False)

                            print(f'Wrote {tracker_name} to file {filename} successfully!')
                            
                    else:

                        tracker_obj.set_data_official() # so have data for map and for datadownload
                        df = tracker_obj.data_official

                        # check if set data official works
                        if 'country_to_check' in df.columns.to_list():
                            print(f'it is still there')
                            input('data official not working')
                        df = df.map(remove_illegal_characters)
                        df.to_excel(writer, sheet_name=f'{tracker_name}', index=False)

                        logger.info(f'Wrote {tracker_name} to file {filename} successfully!')
                        
        # save the excel files to s3
        for filename in [xlsfile, xlsfile_testing]:
            # do for tracker too so no spaces and correct thing for s3 folder
            if tracker in official_tracker_name_to_mapname.keys():
                tracker = official_tracker_name_to_mapname[tracker]
                if tracker in mapname_gitpages.keys():
                    tracker = mapname_gitpages[tracker]
                    
            # run save_csv_s3
            save_xls_s3 = (
                f'export BUCKETEER_BUCKET_NAME=publicgemdata && '
                f'aws s3 cp {filename} s3://$BUCKETEER_BUCKET_NAME/{tracker}/{releaseiso}/ '
                f'--endpoint-url https://nyc3.digitaloceanspaces.com --acl public-read'
            )                        
            runresults = subprocess.run(save_xls_s3, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(runresults.stdout) 
            
        print(f'Successfully saved data download for {tracker} to s3 folder {tracker}/{releaseiso}/')
        # input('Check then press enter.')
    test_make_data_dwnlds(maplen, tracker)
    return map_obj_list




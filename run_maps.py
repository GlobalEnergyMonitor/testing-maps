
from make_data_dwnlds import *
from make_map_file import *
from make_metadata import *
import subprocess
from tqdm import tqdm # can adapt more, special tweaking for dataframe!
# TODO make sure the dependency map makes sense, so it calls both single and multi script depending on new data, try with tests
###
# CALL ALL FUNCTIONS



for tracker in tqdm(trackers_to_update, desc='Running'):
    # print(tracker)
    trackermapname = official_tracker_name_to_mapname[tracker]
    print(f'Creating new metadata file called: {trackermapname}_{releaseiso}_{iso_today_date}_metadata.yaml')
    mfile = f"{trackermapname}_{releaseiso}_{iso_today_date}_metadata"
    # MFILE_ACTUAL = f'{mfile}.yaml'
    metadata = create_or_load_metadata(mfile)
    save_metadata(mfile, metadata)
    if tracker == 'Oil & Gas Plants':
        map_obj_list, problem_map_objs = make_data_dwnlds(tracker)  
        print(f'{len(map_obj_list)} maps to be updated with new {tracker} data!')
        # input('Check if the above statement makes sense ^')
        list_of_map_objs_mapversion = make_map(map_obj_list) # this returns map obj list map version that can be run thru tests
                
        print('Great, now lets run those map objs map version thru tests on source!')
        input('Confirm above')                  
              
    elif tracker == 'Cement and Concrete':
        # TODO jun 29 2025 for next release add in processing step a statusDisplay where it's lower case and no hyphen in op pre ret status
        print('Creating global map for Cement and Concrete then dependent maps and dd')
        # add a comparison between all_config column dictionary and new file
        # make data downloads 
        map_obj_list, problem_map_objs = make_data_dwnlds(tracker)
        # creates single map file
        print(f'{len(map_obj_list)} maps to be updated with new {tracker} data!')
        # input('Check if the above statement makes sense ^')
        list_of_map_objs_mapversion = make_map(map_obj_list) # this returns map obj list map version that can be run thru tests
        
        print('Great, now lets run those map objs map version thru tests on source!')
        input('Confirm above')          
    
    elif tracker == 'Coal Mines':
        print('Creating global map for Coal Mines then dependent maps and dd')
        # add a comparison between all_config column dictionary and new file
        # make data downloads 
        map_obj_list, problem_map_objs = make_data_dwnlds(tracker)
        # creates single map file
        print(f'{len(map_obj_list)} maps to be updated with new {tracker} data!')
        # input('Check if the above statement makes sense ^')
        list_of_map_objs_mapversion = make_map(map_obj_list) # this returns map obj list map version that can be run thru tests
        
        print('Great, now lets run those map objs map version thru tests on source!')
        input('Confirm above')                        
        
    
    elif tracker == 'Hydropower':
        # make data downloads 
        map_obj_list, problem_map_objs = make_data_dwnlds(tracker)
        # creates single map file
        print(f'{len(map_obj_list)} maps to be updated with new {tracker} data!')
        # input('Check if the above statement makes sense ^')
        list_of_map_objs_mapversion = make_map(map_obj_list) # this returns map obj list map version that can be run thru tests
        
        if len(problem_map_objs) > 1:
            print(f'Now that all map and dd files that can work have completed, here are the issue map objs:')
            print(f'Problem Map Name: {problem_map_objs[0]}')
            print(f'Error: {problem_map_objs[1]}')
        
        print('Great, now lets run those map objs map version thru tests on source!')
        input('Confirm above')        
    
    elif tracker == 'Gas Pipelines':
        
        # make data downloads 
        map_obj_list, problem_map_objs = make_data_dwnlds(tracker)
        # creates single map file
        print(f'{len(map_obj_list)} maps to be updated with new {tracker} data!')
        # input('Check if the above statement makes sense ^')
        list_of_map_objs_mapversion = make_map(map_obj_list) # this returns map obj list map version that can be run thru tests
        
        print(f'Now that all map and dd files that can work have completed, here are the issue map objs:')
        print(f'Problem Map Name: {problem_map_objs[0]}')
        print(f'Error: {problem_map_objs[1]}')
        
        print('Great, now lets run those map objs map version thru tests on source!')
        input('Confirm above')
    
    elif tracker == 'Oil Pipelines':
        # test_results_folder = '/Users/gem-tah/GEM_INFO/GEM_WORK/earthrise-maps/gem_tracker_maps/trackers/GOIT/test_results/'

        # output_folder = '/Users/gem-tah/GEM_INFO/GEM_WORK/earthrise-maps/gem_tracker_maps/trackers/GOIT/compilation_output/'
        
        # output_file = f'{output_folder}goit-data-{iso_today_date}.csv'
        
        # make data downloads 
        map_obj_list, problem_map_objs = make_data_dwnlds(tracker)
        # creates single map file
        print(f'{len(map_obj_list)} maps to be updated with new {tracker} data!')
        # input('Check if the above statement makes sense ^')
        list_of_map_objs_mapversion = make_map(map_obj_list) # this returns map obj list map version that can be run thru tests
        
        print(f'Now that all map and dd files that can work have completed, here are the issue map objs:')
        print(f'Problem Map Name: {problem_map_objs[0]}')
        print(f'Error: {problem_map_objs[1]}')
        
        print('Great, now lets run those map objs map version thru tests on source!')
        input('Confirm above')
        

                
    elif tracker == 'Integrated':
        test_results_folder = '/Users/gem-tah/GEM_INFO/GEM_WORK/earthrise-maps/gem_tracker_maps/trackers/integrated/test_results/'

        output_folder = '/Users/gem-tah/GEM_INFO/GEM_WORK/earthrise-maps/gem_tracker_maps/trackers/integrated/compilation_output/'
        
        output_file = f'{output_folder}gipt-data-{iso_today_date}.csv'

        # creates single map file
        key, tabs = get_key_tabs_prep_file(tracker)

    
        df = create_df(key, tabs)
        ### send to s3 for latest data download
        s3folder = 'latest'
        filetype = 'datadownload'
        parquetpath = f'{output_folder}{tracker}{filetype}{releaseiso}.parquet'
        for col in df.columns:
        # check if mixed dtype
            if df[col].apply(type).nunique() > 1:
                # if so, convert it to string
                df[col] = df[col].fillna('').astype(str)
        
        df.to_parquet(parquetpath, index=False)
        do_command_s3 = (
            f'export BUCKETEER_BUCKET_NAME=publicgemdata && '
            f'aws s3 cp {parquetpath} s3://$BUCKETEER_BUCKET_NAME/{s3folder}/ '
            f'--endpoint-url https://nyc3.digitaloceanspaces.com --acl public-read'
        )            
        process = subprocess.run(do_command_s3, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                
        
        df = clean_capacity(df) 
        df = semicolon_for_mult_countries_gipt(df)
        df = fix_status_inferred(df)        
        # harmonize_countries(df, countries_dict, test_results_folder) # find countries_dict
        df= rename_cols(df)
        df = remove_missing_coord_rows(df)
        
        df.to_csv(output_file, index=False, encoding='utf-8' )

        s3folder = 'mapfiles'                
        filetype = 'map'
        parquetpath_m = f'{output_folder}{tracker}{filetype}{releaseiso}.parquet'
        for col in df.columns:
        # check if mixed dtype
            if df[col].apply(type).nunique() > 1:
                # if so, convert it to string
                df[col] = df[col].fillna('').astype(str)
        df.to_parquet(parquetpath_m, index=False)

        ### do aws command copy to s3 publicgem data
        do_command_s3 = (
            f'export BUCKETEER_BUCKET_NAME=publicgemdata && '
            f'aws s3 cp {parquetpath_m} s3://$BUCKETEER_BUCKET_NAME/{s3folder}/ '
            f'--endpoint-url https://nyc3.digitaloceanspaces.com --acl public-read'
        )            
        process = subprocess.run(do_command_s3, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        input('Check that ingt was saved to s3')
        capacityfield = 'capacity-(mw)'
        # run csv2json
        do_csv2json = (
            f"csv2geojson --numeric-fields {capacityfield} &&"
            f"'{output_folder}gipt-data-{releaseiso}.csv' > integrated_{releaseiso}.geojson"
        )
        process = subprocess.run(do_csv2json, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # run tippecanoe
        do_tippecanoe = (
            f"tippecanoe -e integrated-{releaseiso}.dir --no-tile-compression -r1 -pk -pf --force -l && "
            f"integrated < integrated_{releaseiso}.geojson"
        )
        process = subprocess.run(do_tippecanoe, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # set aws configue and bucket name  # do aws command copy to s3 mapintegrated 

        do_aws_bucket = (
            f"aws configure set s3.max_concurrent_requests 100 && "
            f"export BUCKETEER_BUCKET_NAME=mapsintegrated && "
            f"aws s3 cp --endpoint-url https://nyc3.digitaloceanspaces.com {output_folder}integrated-{releaseiso}.dir s3://$BUCKETEER_BUCKET_NAME/maps/integrated-{releaseiso} --recursive --acl public-read"
        )
        process = subprocess.run(do_aws_bucket, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                
    elif tracker == 'Integrated-simple':
        test_results_folder = '/Users/gem-tah/GEM_INFO/GEM_WORK/earthrise-maps/gem_tracker_maps/trackers/integrated-simple/test_results/'

        output_folder = '/Users/gem-tah/GEM_INFO/GEM_WORK/earthrise-maps/gem_tracker_maps/trackers/integrated-simple/compilation_output/'
        
        output_file = f'{output_folder}gipt-simple-data-{iso_today_date}.csv'

        # creates single map file
        key, tabs = get_key_tabs_prep_file(tracker)

    
        df = create_df(key, tabs)
        ### send to s3 for latest data download
        s3folder = 'GIPT-simple'
        filetype = 'dd'
        parquetpath = f'{output_folder}{tracker}{filetype}{releaseiso}.parquet'
        for col in df.columns:
        # check if mixed dtype
            if df[col].apply(type).nunique() > 1:
                # if so, convert it to string
                df[col] = df[col].fillna('').astype(str)
        
        df.to_parquet(parquetpath, index=False)
        do_command_s3 = (
            f'export BUCKETEER_BUCKET_NAME=publicgemdata && '
            f'aws s3 cp {parquetpath} s3://$BUCKETEER_BUCKET_NAME/{s3folder}/ '
            f'--endpoint-url https://nyc3.digitaloceanspaces.com --acl public-read'
        )            
        process = subprocess.run(do_command_s3, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                
        df = clean_capacity(df) 
        df = semicolon_for_mult_countries_gipt(df)
        df = fix_status_inferred(df)        
        # harmonize_countries(df, countries_dict, test_results_folder) # find countries_dict
        df= rename_cols(df)
        df = remove_missing_coord_rows(df)
        df = reduce_cols(df)
        
        
        df.to_csv(output_file, index=False, encoding='utf-8' )

        s3folder = 'GIPT-simple'                
        filetype = 'map'
        parquetpath_m = f'{output_folder}{tracker}{filetype}{releaseiso}.parquet'
        for col in df.columns:
        # check if mixed dtype
            if df[col].apply(type).nunique() > 1:
                # if so, convert it to string
                df[col] = df[col].fillna('').astype(str)
        df.to_parquet(parquetpath_m, index=False)

        ### do aws command copy to s3 publicgem data
        do_command_s3 = (
            f'export BUCKETEER_BUCKET_NAME=publicgemdata && '
            f'aws s3 cp {parquetpath_m} s3://$BUCKETEER_BUCKET_NAME/{s3folder}/ '
            f'--endpoint-url https://nyc3.digitaloceanspaces.com --acl public-read'
        )            
        process = subprocess.run(do_command_s3, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        input('Check that ingt was saved to s3')
        capacityfield = 'capacity-(mw)'
        # run csv2json
        do_csv2json = (
            f"csv2geojson --numeric-fields '{capacityfield}' {output_folder}gipt-data-{iso_today_date}.csv "
            f"> integrated_{iso_today_date}.geojson"
        )
        process = subprocess.run(do_csv2json, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # run tippecanoe
        do_tippecanoe = (
            f"tippecanoe -e integrated-{iso_today_date}.dir --no-tile-compression -r1 -pk -pf --force -l "
            f"integrated < integrated_{iso_today_date}.geojson"
        )
        process = subprocess.run(do_tippecanoe, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # set aws configue and bucket name  # do aws command copy to s3 mapintegrated 

        do_aws_bucket = (
            f"aws configure set s3.max_concurrent_requests 100 && "
            f"export BUCKETEER_BUCKET_NAME=mapsintegrated && "
            f"aws s3 cp --endpoint-url https://nyc3.digitaloceanspaces.com {output_folder}integrated-{iso_today_date}.dir s3://$BUCKETEER_BUCKET_NAME/maps/integrated-{iso_today_date} --recursive --acl public-read"
        )
        process = subprocess.run(do_aws_bucket, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


    elif tracker == 'Geothermal':
        test_results_folder = '/Users/gem-tah/GEM_INFO/GEM_WORK/earthrise-maps/gem_tracker_maps/trackers/geothermal/test_results/'

        output_folder = '/Users/gem-tah/GEM_INFO/GEM_WORK/earthrise-maps/gem_tracker_maps/trackers/geothermal/compilation_output/'

        map_obj_list, problem_map_objs = make_data_dwnlds(tracker)
        input('check progress on dd') # TODO march 28th getting issue with nonetype for df.info should have filtering done, now focus on GOGET so can be filtered but also two tabs
        # creates single map file
        key, tabs = get_key_tabs_prep_file(tracker)
        
        df = create_df(key, tabs)
        # df = split_coords(df)

        df = rename_cols(df)
        df = fix_status_inferred(df)
        print(df.info())
        df = filter_cols(df,final_cols=['country/area', 'project-name','unit-name', 'project-name-in-local-language-/-script',
                                        'unit-capacity-(mw)', 'status', 'start-year', 'retired-year',
                                        'operator', 'owner', 'lat', 'lng', 'location-accuracy', 'city', 'state/province',
                                        'region', 'gem-unit-id', 'gem-location-id', 'url', 'technology'         
                                        ])
        df = input_to_output(df, f'{output_folder}{tracker}-map-file-{iso_today_date}.csv')
        # creates multi-map files 
        print('DONE MAKING GGPT SINGLE MAP onto MULTI MAPS')
        input('continue?')
        # creates multi-tracker maps
        # if tracker to update is coal terminals then look at sheet and create all regional and of course single
        subprocess.run(["python", "/Users/gem-tah/GEM_INFO/GEM_WORK/earthrise-maps/gem_tracker_maps/trackers/multi_tracker_maps_script.py"])                 
        # update so that instead of running above, we just run each function and move it to helper instead of multi or tracker specific which can be held in tracker folder
        
        
        
    elif tracker == 'Iron & Steel':
        test_results_folder = '/Users/gem-tah/GEM_INFO/GEM_WORK/earthrise-maps/gem_tracker_maps/trackers/gist/test_results/'
        output_folder = '/Users/gem-tah/GEM_INFO/GEM_WORK/earthrise-maps/gem_tracker_maps/trackers/gist/compilation_output/'
        
        map_obj_list, problem_map_objs = make_data_dwnlds(tracker)
        print(f'{len(map_obj_list)} maps to be updated with new {tracker} data!')
        list_of_map_objs_mapversion = make_map(map_obj_list) # this returns map obj list map version that can be run thru tests
        
        print('Great, now lets run those map objs map version thru tests on source!')
        input('Confirm above')          

    
    elif tracker == 'Oil & Gas Extraction':
        

        # make data downloads 
        map_obj_list, problem_map_objs = make_data_dwnlds(tracker)
        # creates single map file
        print(f'{len(map_obj_list)} maps to be updated with new {tracker} data!')
        # input('Check if the above statement makes sense ^')
        list_of_map_objs_mapversion = make_map(map_obj_list) # this returns map obj list map version that can be run thru tests
        
        print(f'Now that all map and dd files that can work have completed, here are the issue map objs:')

        
        print('Great, now lets run those map objs map version thru tests on source!')
        input('Confirm above')

        # test_results_folder = '/Users/gem-tah/GEM_INFO/GEM_WORK/earthrise-maps/gem_tracker_maps/trackers/goget/test_results/'

        # output_folder = '/Users/gem-tah/GEM_INFO/GEM_WORK/earthrise-maps/gem_tracker_maps/trackers/goget/compilation_output/'

        # # creates single map file
        # # handle production data
        # key, tabs = get_key_tabs_prep_file(tracker)

        # df_tuple = create_df(key, tabs)
        # main = df_tuple[0]
        # prod = df_tuple[1]
        # # df has df['other'] column to distinguish between main and prod/res
        # # result will be data ready for map, after scott's code
        # df = process_goget_reserve_prod_data(main, prod)
        # df = rename_cols(df) # will need to adjust for goget's columns
        # df = fix_status_space(df)   
        # # df = format_values(df)
        # df = fix_status_inferred(df)         
        # df = filter_cols(df,final_cols=['country/area', 'wiki-name',
        #                                 'status', 'status_display','production-start-year',  
        #                                 'operator', 'owner', 'parent','lat', 'lng', 'location-accuracy', 'subnational-unit-(province,-state)',
        #                                 'gem-region', 'unit-id', 'url', 'country-list', 'discovery-year', 'fid-year', 'production---oil-(million-bbl/y)',
        #                                 'production-year---oil', 'production---gas-(million-m³/y)', 'production-year---gas', 'production---total-(oil,-gas-and-hydrocarbons)-(million-boe/y)'             
        #                                 ])
        
        # # adjust statuses 'operating', 'in_development', 'discovered', 'shut_in', 'decommissioned', 'cancelled', 'abandoned', 'UGS', ""
        
        # df = input_to_output(df, f'{output_folder}{tracker}-map-file-{iso_today_date}.csv')
        # # creates multi-map files 
        # print('DONE MAKING GOGET SINGLE MAP onto MULTI MAPS')
        # input('continue?')
        # # creates multi-tracker maps
        # subprocess.run(["python", "/Users/gem-tah/GEM_INFO/GEM_WORK/earthrise-maps/gem_tracker_maps/trackers/multi_tracker_maps_script.py"])                 
                  
    elif tracker == 'Bioenergy':

        test_results_folder = '/Users/gem-tah/GEM_INFO/GEM_WORK/earthrise-maps/gem_tracker_maps/trackers/bioenergy/test_results/'

        output_folder = '/Users/gem-tah/GEM_INFO/GEM_WORK/earthrise-maps/gem_tracker_maps/trackers/bioenergy/compilation_output/'

        # creates single map file
        key, tabs = get_key_tabs_prep_file(tracker)

        df = create_df(key, tabs)
        df = rename_cols(df)
        df = fix_status_inferred(df)
        df = filter_cols(df,final_cols=['country/area', 'project-name', 'fuel', 'unit-name', 'project-name-in-local-language-/-script',
                                        'capacity-(mw)', 'status', 'start-year', 'retired-year', 'hydrogen-capable',
                                        'operator(s)', 'owner(s)', 'lat', 'lng', 'location-accuracy', 'city', 'state/province',
                                        'region', 'gem-phase-id', 'url'          
                                        ])
        df = input_to_output(df, f'{output_folder}{tracker}-map-file-{iso_today_date}.csv')
        test_stats(df)
        # creates multi-map files 
        print('DONE MAKING GBPT SINGLE MAP onto MULTI MAPS')
        input('continue?')
        # creates multi-tracker maps
        # if tracker to update is coal terminals then look at sheet and create all regional and of course single
        subprocess.run(["python", "/Users/gem-tah/GEM_INFO/GEM_WORK/earthrise-maps/gem_tracker_maps/trackers/multi_tracker_maps_script.py"])                 
          
        # if test:
        #     check_expected_number(incorporated_dict_list_gdfs_by_map) # TODO HANDLE THIS ONE for dict or use the one thats been concatenated

    elif tracker == 'Oil & Gas Plants':
        # continue for all of them that are in or not in multi tracker maps
        test_results_folder = f'{tracker_folder_path}gas-plant/test_results/'

        output_folder = f'{tracker_folder_path}gas-plant/compilation_output/'

        input_file_path = f'{tracker_folder_path}gas-plant/compilation_input/'
                
        # multi_tracker_log_sheet_key = '15l2fcUBADkNVHw-Gld_kk7EaMiFFi8ysWt6aXVW26n8'
        # multi_tracker_log_sheet_tab = ['multi_map']
        # prep_file_tab = ['prep_file']
        # key = '1WRRFRuR9mWxZpko-VMYH5xm0LzRX_qM7W73nGGi4Jmg'
        # tabs = ['Data', 'Below Threshold']
        
        # creates single map file
        key, tabs = get_key_tabs_prep_file(tracker)
        df = create_df(key, tabs)
        df = rename_cols(df)
        df = fix_status_inferred(df)
        df = filter_cols(df,final_cols=['gem-location-id','country/area', 'plant-name', 'fuel', 'unit-name', 'plant-name-in-local-language-/-script',
                                        'capacity-(mw)', 'status', 'start-year', 'retired-year', 'parent(s)', 'turbine/engine-technology',
                                        'operator(s)', 'owner(s)', 'lat', 'lng', 'location-accuracy', 'city', 'state/province',
                                        'region', 'url'          
                                        ])
        # make sure 0% and 100% is removed from owners

        df = remove_implied_owner(df)
        df = formatting_checks(df)

        
        df = input_to_output(df, f'{output_folder}{tracker}-map-file-{iso_today_date}.csv')
        # test_stats(df)
        print('DONE MAKING GOGPT SINGLE MAP onto MULTI MAPS')
        input('Continue?')
        # creates multi-tracker maps
        # if tracker to update is coal terminals then look at sheet and create all regional and of course single
        subprocess.run(["python", "/Users/gem-tah/GEM_INFO/GEM_WORK/earthrise-maps/gem_tracker_maps/trackers/multi_tracker_maps_script.py"])                 

    elif tracker == 'Plumes':
        print(f'Starting GMET for release {tracker}')

        
    elif tracker == 'LNG Terminals':
        print('Starting on lng terminals')

    elif tracker == 'Wind':
        # continue for all of them that are in or not in multi tracker maps
        test_results_folder = f'{tracker_folder_path}wind/test_results/'

        output_folder = f'{tracker_folder_path}wind/compilation_output/'

        # input_file_path = f'{tracker_folder_path}coal-terminals/compilation_input/'
        
        os.makedirs(test_results_folder, exist_ok=True)
        os.makedirs(output_folder, exist_ok=True)       
             

        # creates single map file
        key, tabs = get_key_tabs_prep_file(tracker)
        df = create_df(key, tabs)
        df = rename_cols(df)
        df = fix_status_inferred(df)
        df = filter_cols(df,final_cols=['gem-location-id', 'gem-phase-id', 'country/area', 'phase-name', 'project-name', 'project-name-in-local-language-/-script',
                                        'other-name(s)', 'capacity-(mw)', 'status', 'start-year', 'retired-year', 'location-accuracy',
                                         'owner', 'lat', 'lng', 'state/province', 'operator', 'installation-type',
                                        'region', 'url', 'owner-name-in-local-language-/-script', 'operator-name-in-local-language-/-script'        
                                        ])
            
        
        df = input_to_output(df, f'{output_folder}{tracker}-map-file-{iso_today_date}.csv')
        # test_stats(df)

        print('DONE MAKING WIND SINGLE MAP onto MULTI MAPS')
        input('continue?')
        # creates multi-tracker maps
        # if tracker to update is coal terminals then look at sheet and create all regional and of course single
        # subprocess.run(["python", "/Users/gem-tah/GEM_INFO/GEM_WORK/earthrise-maps/gem_tracker_maps/trackers/multi_tracker_maps_script.py"])                 


    elif tracker == 'Solar':
        # continue for all of them that are in or not in multi tracker maps
        test_results_folder = f'{tracker_folder_path}solar/test_results/'

        output_folder = f'{tracker_folder_path}solar/compilation_output/'
        
        os.makedirs(test_results_folder, exist_ok=True)
        os.makedirs(output_folder, exist_ok=True)       
             

        # creates single map file
        key, tabs = get_key_tabs_prep_file(tracker)
        df = create_df(key, tabs)
        df = rename_cols(df)
        df = fix_status_inferred(df)
        df = filter_cols(df,final_cols=['gem-location-id', 'gem-phase-id', 'country/area', 'phase-name', 'project-name', 'project-name-in-local-language-/-script',
                                        'other-name(s)', 'capacity-(mw)', 'status', 'start-year', 'retired-year', 'location-accuracy',
                                         'owner', 'lat', 'lng', 'state/province', 'operator', 'technology-type',
                                        'region', 'url', 'owner-name-in-local-language-/-script', 'operator-name-in-local-language-/-script'         
                                        ])
                
        
        df = input_to_output(df, f'{output_folder}{tracker}-map-file-{iso_today_date}.csv')
        # test_stats(df)

        print('DONE MAKING SOLAR SINGLE MAP onto MULTI MAPS')
        input('continue?')
        # creates multi-tracker maps
        # if tracker to update is coal terminals then look at sheet and create all regional and of course single
        # subprocess.run(["python", "/Users/gem-tah/GEM_INFO/GEM_WORK/earthrise-maps/gem_tracker_maps/trackers/multi_tracker_maps_script.py"])                 
    
    elif tracker == 'Coal Plants':

        map_obj_list, problem_map_objs = make_data_dwnlds(tracker)

        # creates single map file
        print(f'{len(map_obj_list)} maps to be updated with new {tracker} data!')
        input('Check if the above statement makes sense ^')
        list_of_map_objs_mapversion = make_map(map_obj_list) # this returns map obj list map version that can be run thru tests

        print('Great, now lets run those map objs map version thru tests on source!')
        input('Confirm above')            
    # subprocess.run(["python", "/Users/gem-tah/GEM_INFO/GEM_WORK/earthrise-maps/gem_tracker_maps/trackers/multi_tracker_maps_script.py"])                 
    
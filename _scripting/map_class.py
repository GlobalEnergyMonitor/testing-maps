import pandas as pd
from helper_functions import drop_cols_df_a_rename_value_avoid_dup, testval, replace_old_date_about_page_reg, rebuild_countriesjs, pci_eu_map_read, check_and_convert_float, remove_diacritics, check_rename_keys, fix_status_inferred, conversion_multiply, workaround_table_float_cap, workaround_table_units
from all_config import logpath, official_tracker_name_to_mapname, releaseiso, simplified_cols, simplified, gspread_creds, mapname_gitpages, non_regional_maps, logger, client_secret_full_path, gem_path, tracker_to_fullname, tracker_to_legendname, iso_today_date, gas_only_maps, final_cols, renaming_cols_dict
import geopandas as gpd
import numpy as np
from shapely import wkt
import subprocess


class MapObject:
    def __init__(self,
                 mapname="",
                 source="",
                 geo="", 
                # list of countries with get_needed_geo method
                 needed_geo=[], 
                 fuel="",
                 pm="",
                 trackers=[], 
                 aboutkey = "",
                 about=pd.DataFrame(),
                 ):
        self.mapname = mapname
        self.source = source.split(", ")
        self.geo = geo
        self.needed_geo = []
        self.fuel = fuel.split(", ")
        self.pm = pm.split("; ")
        self.trackers = trackers
        self.aboutkey = aboutkey
        self.about = about
        

    def set_fuel_goit(self):
        # Oil, NGL should show up under both type options, Oil and NGL
        # LPG should be renamed to NGL 
        if self.mapname == 'goit':
            # Update all values in the 'Fuel' column from 'LPG' to 'NGL'
            logger.info('Creating fuel legend for goit')
            logger.info(set(self.trackers['Fuel'].to_list()))
            self.trackers['Fuel'] = self.trackers['Fuel'].replace('LPG', 'NGL')  
        else:
            pass
        
        
    
    def capacity_hide_goget_gcmt(self):

        mapname = self.mapname
        gdf = self.trackers
        if mapname.lower() in ['gipt']:
            pass
            
        else:
            for row in gdf.index:
                tracker = (gdf.loc[row, 'tracker-acro'])
                # if goget then make capacity table and capacity details empty
                if tracker.upper() == 'GOGET':
                    logger.info('in goget')
                    gdf.loc[row, 'capacity-table'] = np.nan
                    gdf.loc[row, 'capacity-details'] = ''
                    prod_oil = gdf.loc[row, 'prod_oil']
                    prod_gas = gdf.loc[row, 'prod_gas']
                    prod_oil = check_and_convert_float(prod_oil) 
                    prod_gas = check_and_convert_float(prod_gas)

                elif tracker.upper() == 'GCMT':
                    logger.info('in gcmt')
                    gdf.loc[row, 'capacity-table'] = np.nan
                    gdf.loc[row, 'capacity-details'] = ''
                    prod_coal = gdf.loc[row, 'prod-coal']
                    
                elif tracker.upper() == 'GGFT':
                    logger.info('in GGFT')
                    # just going to keep them separate because not sizing on capacity for ggft, mw and mtpa not bothering to convert but keep separate with their own labels
                    gdf.loc[row, 'capacity-table'] = np.nan
                    gdf.loc[row, 'capacity-details'] = ''
                                                           
                else:
                    gdf.loc[row, 'capacity-table'] = gdf.loc[row, 'capacity']
                    gdf.loc[row, 'capacity-details'] = gdf.loc[row, 'capacity']
        # TODO see if BOED is still in empty capacity details for GOIT in combination with last min fixes function below
        gdf['capacity-details'].fillna('',inplace=True)
        gdf['capacity-table'].fillna('',inplace=True)
        # gdf['capacity'].fillna('',inplace=True)


        self.trackers = gdf


    def create_search_column(self):
        # this can be one string with or without spaces 
        # this creates a new column for project and project in local language
        # in the column it'll be removed of any diacritics 
        # this allows for quick searching
        # for mapname, one_gdf in cleaned_dict_map_by_one_gdf.items():
        one_gdf = self.trackers

        logger.info('testing create_search_column with no diacritics for first time')
        col_names = ['plant-name', 'parent(s)', 'owner(s)', 'operator(s)', 'name', 'owner', 'parent']
        for col in col_names:
            if col in one_gdf.columns:
                new_col_name = f'{col}_search'
                one_gdf[new_col_name] = one_gdf[col].apply(lambda x: remove_diacritics(x))
        
        self.trackers = one_gdf           


    def remove_excess_cols(self):
        # NOTE affects all trackers so if there is a new column needs to be added to list below
        gdf = self.trackers
        # before saving to file, remove excess cols not needed in the map's config.js or site-config.js
        # so that it goes as quickly as it can
        # always keep geometry column
        
        # for now manual
        if self.mapname.lower() == 'gmet':
            print(gdf['legend-filter'])
            input('check legend filter')
            
            cols = ["Government Well ID",
                    "areas",
                    "areas-subnat-sat-display",
                    "capacity-output",
                    "capacity-prod",
                    "capacitybcm/y",
                    "capacityinmtpa",
                    "carbonmapper",
                    "country",
                    "date",
                    "emission-uncertainty",
                    "emission_uncertainty",
                    # "emissionsIfOp",
                    "emissions-terminals",
                    "geminfrawiki",
                    "gov_assets",
                    "infra-name",
                    "infra_name",
                    "infra_type",
                    "infra_url",
                    "infra-filter",
                    "infra_filter",
                    "instrument",
                    "mtyr-gcmt-emissions",
                    "name",
                    "operator",
                    "owner",
                    "pid",
                    "pipe-length",
                    "plume-emissions",
                    "plume_emissions",
                    "satdataprovider",
                    "scaling-capacity",
                    "scaling_col",
                    "status",
                    "status-legend",
                    "subnational",
                    "tab-type",
                    "tonnes-goget-reserves-emissions",
                    "tonnesyr-pipes-emissions",
                    "tracker",
                    "typeinfra",
                    "well_id",
                    "unit-name",
                    "geometry",
                    "lat",
                    "lng",
                    "carbon-mapper-md",
                    "infra-wiki-md",
                    "tracker-custom",
                    "capacity",
                    "areas",
                    "subnat",
                    "legend-filter",
                    "url", 
                    "release-date-infra"]
            
            logger.info(f'before excess cols function len: {len(gdf.columns)}')

            finalcols = []
            for col in cols:
                if col in gdf.columns:
                    finalcols.append(col)
                    
                    
            gdf = gdf[finalcols]
            logger.info(f'after excess cols function len: {len(gdf.columns)}')
        
        
        
        self.trackers = gdf
        
    
    def last_min_fixes(self):
        gdf = self.trackers

        # handle situation where Guinea-Bissau IS official and ok not to be split into separate countries 
        gdf['areas'] = gdf['areas'].apply(lambda x: x.replace('Guinea,Bissau','Guinea-Bissau')) 
        gdf['areas'] = gdf['areas'].apply(lambda x: x.replace('Timor,Leste','Timor-Leste')) 

        gdf['name'].fillna('',inplace=True)
        gdf['name'] = gdf['name'].astype(str)

        # handles for empty url rows and also non wiki cases SHOULD QC FOR THIS BEFOREHAND!! TO QC
        gdf['wiki-from-name'] = gdf.apply(lambda row: f"https://www.gem.wiki/{row['name'].strip().replace(' ', '_')}", axis=1)

        if 'url' not in gdf.columns:
            gdf['url'] = ''
        gdf['url'].fillna('',inplace=True)

        gdf['url'] = gdf.apply(lambda row: row['wiki-from-name'] if 'gem.wiki' not in row['url'] else row['url'], axis=1)
        logger.info(f'gem.wiki was not in url column so used formatted wiki-from-nae url, this should be qcd')
             
        # one last check since this'll ruin the filter logic
        gdf.columns = [col.replace('&', '') for col in gdf.columns]
        gdf.columns = [col.replace('_', '-') for col in gdf.columns] 
        gdf.columns = [col.replace('  ', ' ') for col in gdf.columns] 
        gdf.columns = [col.replace(' ', '-') for col in gdf.columns] 

        for col in gdf.columns:
            gdf[col] = gdf[col].apply(lambda x: str(x).replace('nan',''))


        entities = ['owner', 'parent', 'operator']
        for col in entities:
            if col in gdf.columns:
                gdf[col] = gdf[col].apply(lambda x: str(x).replace('[unknown %]', ''))
        logger.info(f'Check all columns:')

        # translate acronyms to full names for legend and table 
        gdf['tracker-display'] = gdf['tracker-custom'].map(tracker_to_fullname)
        gdf['tracker-legend'] = gdf['tracker-custom'].map(tracker_to_legendname)
        # make sure all null geo is removed

        gdf.dropna(subset=['geometry'],inplace=True)

        # make sure all of the units of m are removed for goget and gcmt that has no capacity
        # just allowing for the rare trackers like ggft where capacity is not the main focus
        if 'capacity' in gdf.columns:
            for row in gdf.index:
                if gdf.loc[row, 'capacity'] == '':
                    gdf.loc[row, 'units-of-m'] = ''
                elif gdf.loc[row, 'capacity-details'] == '':
                    gdf.loc[row, 'units-of-m'] = ''
                elif gdf.loc[row, 'capacity-table'] == np.nan:
                    gdf.loc[row, 'units-of-m'] = ''

        # remove the decimal in years, and lingering -1 for goget
        year_cols = ['start-year', 'prod-year-gas', 'prod-year-oil']

        for col in year_cols:
            if col in gdf.columns:
                gdf[col] = gdf[col].apply(lambda x: str(x).split('.')[0])
                gdf[col].replace('-1', 'not stated')
                
        if self.mapname == 'europe':
            logger.info(self.mapname)
            gdf = pci_eu_map_read(gdf)

        # gdf.fillna('', inplace = True)
                    
        # Check for invalid geometries in the 'geometry' column
        invalid_geoms = []
        fixed_count = 0
        for idx, geom in gdf['geometry'].items():
            # Check if geometry is a shapely object and is valid
            if hasattr(geom, 'is_valid') and not geom.is_valid:
                logger.info(f"Invalid geometry found at index {idx}: {gdf.loc[idx,'name']}")
                # Try to fix geometry
                fixed_geom = geom.buffer(0)
                if fixed_geom.is_valid:
                    gdf.at[idx, 'geometry'] = fixed_geom
                    fixed_count += 1
                else:
                    invalid_geoms.append((idx, geom))
            # If geometry is not a shapely object, try to parse it
            elif not hasattr(geom, 'is_valid'):
                try:
                    parsed_geom = wkt.loads(str(geom))
                    if parsed_geom.is_valid:
                        gdf.at[idx, 'geometry'] = parsed_geom
                        fixed_count += 1
                    else:
                        fixed_geom = parsed_geom.buffer(0)
                        if fixed_geom.is_valid:
                            gdf.at[idx, 'geometry'] = fixed_geom
                            fixed_count += 1
                        else:
                            invalid_geoms.append((idx, geom))
                except Exception as e:
                    logger.warning(f"Failed to parse geometry at index {idx}: {e}")
                    invalid_geoms.append((idx, geom))
            
        # Log summary before removing rows
        logger.info(f"Fixed {fixed_count} geometries, found {len(invalid_geoms)} unfixable geometries")
        
        # Remove rows with invalid geometry and log them
        if invalid_geoms:
            logger.warning(f"Found {len(invalid_geoms)} invalid geometries, removing rows")
            pd.DataFrame(invalid_geoms, columns=['index', 'geometry']).to_csv(f'{logpath}{self.mapname}-invalid-geometries-{iso_today_date}.csv', index=False)
            # Extract indices of invalid geometries for removal
            invalid_geom_indices = [idx for idx, _ in invalid_geoms]
            gdf.drop(invalid_geom_indices, inplace=True)
            logger.info(f"Dropped {len(invalid_geom_indices)} rows with invalid geometries")

        gdf.columns = [col.lower() for col in gdf.columns]
        
        
        if simplified:
            simplified_cols_drop = []
            for col in simplified_cols:
                if col in gdf.columns:
                    pass
                else:
                    print(f'this col is not there, was it expected? \n {col}')
                    simplified_cols_drop.append(col) 
            
            simplified_cols_updated = [col for col in simplified_cols if col not in simplified_cols_drop]  # Result: ["a", "c"]
            if simplified:
                # remove columns
                gdf = gdf[simplified_cols_updated]
        
        # make sure everything is a number than can be
        # so js functions as expected and no NaNs
        if 'capacity' in gdf.columns:
            gdf['capacity'] = gdf['capacity'].apply(lambda x: pd.to_numeric(x, errors='raise'))
        
        self.trackers = gdf
    
    def save_file(self, tracker):
        logger.info(f'Saving file for map {self.mapname}')
        logger.info(f'This is len of gdf {len(self.trackers)}')
        # helps map to the right folder name
        if self.mapname in mapname_gitpages.keys():
            self.mapname = mapname_gitpages[self.mapname]
            path_for_download_and_map_files = gem_path + self.mapname + '/compilation_output/'
        else:
            path_for_download_and_map_files = gem_path + self.mapname + '/compilation_output/'
        
        
        # do for tracker too so no spaces and correct thing for s3 folder
        if tracker in official_tracker_name_to_mapname.keys():
            tracker = official_tracker_name_to_mapname[tracker]
            if tracker in mapname_gitpages.keys():
                tracker = mapname_gitpages[tracker]
                

        logger.info(f'Final cols:\n')
        cols = [(col) for col in gdf.columns]
        logger.info(cols)
    
        
 
        # Check if the dataframe is a GeoDataFrame
        if isinstance(gdf, gpd.GeoDataFrame):
            logger.info('Already a GeoDataFrame!')
        else:
            logger.info(f'Converting to GeoDataFrame for {self.mapname} ...')
            if 'geometry' not in gdf.columns:
                raise ValueError("The dataframe does not have a 'geometry' column to convert to GeoDataFrame.")
            gdf = gpd.GeoDataFrame(gdf, geometry=gdf['geometry'])
            gdf.set_crs(epsg=4326, inplace=True)  # Set CRS to EPSG:4326 (WGS 84)  

        # ensure no duplicated columns
        gdf = gdf.loc[:, ~gdf.columns.duplicated()]  

        
        if simplified:
            output_file1 = f'{path_for_download_and_map_files}{self.mapname}_map_{iso_today_date}_simplified.csv'
            output_file2 = f'{path_for_download_and_map_files}{self.mapname}_map_{iso_today_date}_simplified.geojson'


            gdf.to_csv(f'{path_for_download_and_map_files}{self.mapname}_map_{iso_today_date}_simplified.csv', encoding='utf-8')
            gdf.to_file(f'{path_for_download_and_map_files}{self.mapname}_map_{iso_today_date}_simplified.geojson', driver='GeoJSON', encoding='utf-8')

            # save simplified csv and geojson to S3
            # output_file
            for output_file in [output_file1, output_file2]:
                save_files_s3 = (
                    f'export BUCKETEER_BUCKET_NAME=publicgemdata && '
                    f'aws s3 cp {output_file} s3://$BUCKETEER_BUCKET_NAME/{tracker}/{releaseiso}/ '
                    f'--endpoint-url https://nyc3.digitaloceanspaces.com --acl public-read'
                )            
                
            
                runresults = subprocess.run(save_files_s3, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                print(runresults.stdout)  
                print(f'saved csv and geojson map file to s3')
                # input(f'update config.js {output_file} then press enter.')           
                        
            
    
                            
        else:
            output_file1 = f'{path_for_download_and_map_files}{self.mapname}_map_{iso_today_date}.csv'
            output_file2 = f'{path_for_download_and_map_files}{self.mapname}_map_{iso_today_date}.geojson'
            gdf.to_file(f'{path_for_download_and_map_files}{self.mapname}_map_{iso_today_date}.geojson', driver='GeoJSON', encoding='utf-8')


            gdf.to_csv(f'{path_for_download_and_map_files}{self.mapname}_map_{iso_today_date}.csv', encoding='utf-8')
        
            # save csv and geojson to S3
            for output_file in [output_file1, output_file2]:
                save_files_s3 = (
                    f'export BUCKETEER_BUCKET_NAME=publicgemdata && '
                    f'aws s3 cp {output_file} s3://$BUCKETEER_BUCKET_NAME/{tracker}/{releaseiso}/ '
                    f'--endpoint-url https://nyc3.digitaloceanspaces.com --acl public-read'
                )            
                
            
                runresults = subprocess.run(save_files_s3, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                print(runresults.stdout)  
                print(f'saved csv and geojson map file to s3')
                # input(f'update config.js {output_file} then press enter.')           
        newcountriesjs = list(set(gdf['areas'].to_list()))
        # SKIP THIS
        # rebuild_countriesjs(mapname=self.mapname, newcountriesjs)


    def simplified(self):
        logger.info('Finish writing simplified function to easily filter down any map file for quick map rendering without table, first step for 1hot encoding')

    def set_capacity_conversions(self):
    
    # you could multiply all the capacity/production values in each tracker by the values in column C, 
    # "conversion factor (capacity/production to common energy equivalents, TJ/y)."
    # For this to work, we have to be sure we're using values from each tracker that are standardized
    # to the same units that are stated in this sheet (column B, "original units").

        gdf = self.trackers
        print(gdf)
        if len(gdf) < 1:
            input('DEBUG check above is not empty')

        if self.mapname in gas_only_maps:
            logger.info('no need to handle for hydro having two capacities')
        else:
            # first let's get GHPT cap added 
            logger.info(f'Length of gdf: {len(gdf)}')
            if 'capacity2' in gdf.columns:
                ghpt_only = gdf[gdf['capacity2'].notna()]

                gdf_minus_ghpt = gdf[gdf['capacity2'].isna()]
                for col in ghpt_only.columns:
                    print(col)
                logger.info(f'ghpt only cap: {ghpt_only["capacity"]}')
                ghpt_only['capacity'] = ghpt_only.apply(lambda row: row['capacity'] + row['capacity2'], axis=1) 
                
                # concat them back together now that ghpt capacity is in one col
                gdf = pd.concat([gdf_minus_ghpt, ghpt_only],sort=False).reset_index(drop=True)
        
        
        if self.mapname in ['ggft']: 
            # TODO GGFT # project-financing
            gdf['cleaned_cap'] = pd.to_numeric(gdf['project-financing'], errors='coerce')

        else:
            # create cleaned cap for logic below 
            gdf['cleaned_cap'] = pd.to_numeric(gdf['capacity'], errors='coerce')

        # works to fill in average capacity for missing ones so dot still shows up
        total_counts_trackers = []
        avg_trackers = []

        for tracker in set(gdf['tracker-acro'].to_list()):
            print(f'{tracker}')

            # for singular map will only go through one
            total = len(gdf[gdf['tracker-acro'] == tracker])
            sum = gdf[gdf['tracker-acro'] == tracker]['cleaned_cap'].sum()
            avg = sum / total
            total_pair = (tracker, total)
            total_counts_trackers.append(total_pair)
            avg_pair = (tracker, avg)
            avg_trackers.append(avg_pair)
            
        # assign average capacity to rows missing or na capacity
        for row in gdf.index:
            cap_cleaned = gdf.loc[row, 'cleaned_cap']
            tracker = gdf.loc[row, 'tracker-acro']
            if pd.isna(cap_cleaned):
                for pair in avg_trackers:
                    if pair[0] == tracker:
                        gdf.loc[row, 'cleaned_cap'] = pair[1]
            cap_cleaned = gdf.loc[row, 'cleaned_cap']
            if pd.isna(cap_cleaned):
                input('still na')
    

        pd.options.display.float_format = '{:.0f}'.format
        # must be float for table to sort
        if self.mapname in non_regional_maps: # map name
            logger.info('skip converting to joules')

            gdf['scaling_capacity'] = gdf['cleaned_cap']
            gdf['scaling_capacity'] = gdf['scaling_capacity'].astype(float)

        else:
            logger.info('not skipping conversion to joules...')
            logger.info(f'{self.mapname}')
            logger.info('check name and why it is not in non_regional_maps')
            logger.info(f'{set(gdf["conversion_factor"].to_list())}')
            gdf['scaling_capacity'] = gdf.apply(lambda row: conversion_multiply(row), axis=1)
            
        
        if self.mapname in ['ggft']: 
            print('passing cap-table now')
        else:
            gdf['capacity-table'] = gdf.apply(lambda row: pd.Series(workaround_table_float_cap(row, 'capacity')), axis=1)
            gdf['units-of-m'] = gdf.apply(lambda row: pd.Series(workaround_table_units(row)), axis=1)    
        self.trackers = gdf        
        
    def map_ready_statuses_and_countries(self):
        
        gdf = self.trackers
        if 'status' in gdf.columns:
            # accounting for gchi with no status
            gdf['status'] = gdf['status'].fillna('Not Found') # ValueError: Cannot mask with non-boolean array containing NA / NaN values
            gdf['status'] = gdf['status'].replace('', 'Not Found') # ValueError: Cannot mask with non-boolean array containing NA / NaN values
            logger.info(f'set of statuses: {set(gdf["status"].to_list())}')
            gdf_map_ready = fix_status_inferred(gdf)
        
            # Create masks for the 'tracker-acro' conditions
            mask_gcmt = gdf_map_ready['tracker-acro'] == 'GCMT'
            mask_goget = gdf_map_ready['tracker-acro'] == 'GOGET'
        
            # Update 'status' to 'Retired' where both masks are True
            gdf_map_ready['status'] = gdf_map_ready['status'].fillna('')
            mask_status_empty = gdf_map_ready['status'] == ''
            
            # Update 'status' to 'Not Found' where both masks are True
            gdf_map_ready.loc[mask_status_empty & mask_gcmt, 'status'] = 'retired'
            gdf_map_ready.loc[mask_status_empty & mask_goget, 'status'] = 'not found'
            gdf_map_ready['status_legend'] = gdf_map_ready.copy()['status'].str.lower().replace({
                        # TODO get clarity on when this should be applied, for global or regional or both?
                        # proposed_plus
                        'proposed': 'proposed_plus',
                        'announced': 'proposed_plus',
                        'discovered': 'proposed_plus',
                        # pre-construction_plus
                        'pre-construction': 'pre-construction_plus',
                        'pre-permit': 'pre-construction_plus',
                        'permitted': 'pre-construction_plus',
                        # construction_plus
                        'construction': 'construction_plus',
                        'in development': 'construction_plus',
                        'exploration': 'construction_plus',
                        # mothballed
                        'mothballed': 'mothballed_plus',
                        'idle': 'mothballed_plus',
                        'idled': 'mothballed-plus',
                        'shut in': 'mothballed_plus',
                        # 'shelved': 'mothballed_plus',
                        # retired
                        'retired': 'retired_plus',
                        'closed': 'retired_plus',
                        'decommissioned': 'retired_plus',
                        'not found': 'not-found',
                        # 'abandoned': 'retired_plus',
                        # 'cancelled': 'retired_plus',
                        'mixed status': 'not-found',
                        # 'ugs': 'not-found'
                        })
            
            print(set(gdf_map_ready['status_legend'].to_list()))
            input(f'Check all statuses in legends ugs and cancelled and abandoned and shelved should be there')
            # Create a mask for rows where 'status' is empty

            gdf_map_ready_no_status = gdf_map_ready.loc[mask_status_empty]

            if len(gdf_map_ready_no_status) > 0:
                logger.warning(f'check no status df, will be printed to issues as well: {gdf_map_ready_no_status}')
                gdf_map_ready_no_status.to_csv(f'issues/{self.mapname}-no-status-{iso_today_date}.csv')
            
            # make sure all statuses align with no space rule
            gdf_map_ready['status'] = gdf_map_ready['status'].apply(lambda x: x.strip().replace(' ','-')) # TODO why was this commented out?
            gdf_map_ready['status_legend'] = gdf_map_ready['status_legend'].apply(lambda x: x.strip().replace('_','-'))
            gdf_map_ready['status'] = gdf_map_ready['status'].apply(lambda x: x.lower())
            logger.info(set(gdf_map_ready['status'].to_list()))
            logger.warning('check list of statuses after replace space and _') 
            # TODO check that all legend filter columns go through what status goes through 
            if self.mapname == 'gcmt':
                    # make sure all filter cols align with no space rule
                legcols = ["coal-grade", "mine-type"]
                for col in legcols:
                    gdf_map_ready[col] = gdf_map_ready[col].apply(lambda x: x.strip().replace(' ','-')) # TODO why was this commented out?
                    gdf_map_ready[col] = gdf_map_ready[col].apply(lambda x: x.strip().replace('_','-'))
                    gdf_map_ready[col] = gdf_map_ready[col].apply(lambda x: x.lower())        
                    
            logger.info(set(gdf_map_ready['areas'].to_list()))

            tracker_sel = gdf_map_ready['tracker-acro'].iloc[0] 
            if tracker_sel == 'GCMT':
                gdf_map_ready['status'] = gdf_map_ready['status'].replace('not-found', 'retired')
        else:
            # bandaid to just have gchi work for now even though they have no statuses
            gdf_map_ready = gdf.copy()

        
        # check that areas isn't empty
        tracker_sel = gdf_map_ready['tracker-acro'].iloc[0]
        logger.info(f'this is tracker_sel {tracker_sel}')
        if tracker_sel == 'GOGET':
            logger.info(gdf_map_ready['areas'])
            logger.info('check goget areas in map ready countries')
        gdf_map_ready['areas'] = gdf_map_ready['areas'].fillna('')

        empty_areas = gdf_map_ready[gdf_map_ready['areas']=='']
        if len(empty_areas) > 0:
            logger.warning(f'Check out which rows are empty for countries for map will also be printed in issues: {self.mapname}')
            logger.warning(empty_areas)
            empty_areas.to_csv(f'issues/{tracker_sel}-empty-areas-{iso_today_date}.csv')

        # this formats subnational area for detail maps
        # we would also want to overwrite the subnat and say nothing ""
        gdf_map_ready['count-of-semi'] = gdf_map_ready.apply(lambda row: row['areas'].strip().split(';'), axis=1) # if len of list is more than 2, then split more than once
        gdf_map_ready['count-of-semi'] = gdf_map_ready.apply(lambda row: row['areas'].strip().split('-'), axis=1) # for goget
        gdf_map_ready['count-of-semi'] = gdf_map_ready.apply(lambda row: row['areas'].strip().split(','), axis=1) # just adding in case

        gdf_map_ready['multi-country'] = gdf_map_ready.apply(lambda row: 't' if len(row['count-of-semi']) > 1 else 'f', axis=1)
        # if t then make areas-display 
        for col in gdf_map_ready.columns:
            print(col)
            
        if 'subnat' in gdf_map_ready.columns:
            gdf_map_ready['subnat'].fillna('', inplace=True)
        
            # if only one country and subnat not empty create the string, otherwise it should just be the country 
            # (which means what for multi country?) we use a mask below to fix it for multi countries
            gdf_map_ready['areas-subnat-sat-display'] = gdf_map_ready.apply(lambda row: f"{row['subnat'].strip().strip('')}, {row['areas'].strip().strip('')}" if row['multi-country'] == 'f' and row['subnat'] != '' else row['areas'].strip(), axis=1) # row['areas'].strip()
            # if more than one country replace the '' with mult countries
            maskt = gdf_map_ready['multi-country']=='t'

            gdf_map_ready.loc[maskt, 'areas-subnat-sat-display'] = 'multiple areas/countries'

            # for map js to work need to make sure all countries are separated by a comma and have a comma after last country as well
            # GOGET has a hyphen in countries
            # GOIT has comma separated in countries
            # hydropower has two columns country1 and country2
            # GGIT has comma separated in countries

            
        if self.mapname in gas_only_maps:
            # handle for gas only maps (meaning no two cols for ghpt), the adding of the semicolon for js script
            logger.info('In gas only area of function map ready statuses and countries')
            gdf_map_ready['areas'] = gdf_map_ready['areas'].fillna('')
            gdf_map_ready['areas'] = gdf_map_ready['areas'].apply(lambda x: x.replace(',', ';')) # try this to fix geojson multiple country issue
            gdf_map_ready['areas'] = gdf_map_ready['areas'].apply(lambda x: f"{x.strip()};")
            logger.info(gdf_map_ready['areas'])
            logger.info('check above has semicolon')

        else: 

            if 'area2' in gdf_map_ready.columns:
                gdf_map_ready['area2'] = gdf_map_ready['area2'].fillna('')
                gdf_map_ready['areas'] = gdf_map_ready['areas'].fillna('')
            
            gdf_map_ready['areas'] = gdf_map_ready['areas'].apply(lambda x: x.replace(',', ';')) # try this to fix geojson multiple country issue
            gdf_map_ready['areas'] = gdf_map_ready['areas'].apply(lambda x: f"{x.strip()};")

        self.trackers = gdf_map_ready        
        

    def rename_and_concat_gdfs(self):
        # This function takes a dictionary and renames columns for all dataframes within
        # then it concats by map type all the dataframes
        # so you're left with a dictionary by maptype that holds one concatted dataframe filterd on geo and tracker type needed
        
        renamed_gdfs = []     
        for tracker_obj in self.trackers:
            if tracker_obj.acro in ['GMET', 'GGFT']:
                logger.info(F'Skipping rename for gmet and ggft because already renamed and concatted upon pull because it functions like a mini multi tracker map already')
                gdf = tracker_obj.data
                tracker_sel = tracker_obj.acro
                gdf['tracker-acro'] = tracker_sel
                # gdf = drop_cols_df_a_rename_value_avoid_dup(tracker_sel, gdf)
                gdf.columns = gdf.columns.str.strip()
                # gdf.reset_index(drop=True, inplace=True)
                if 'subnat' in gdf.columns:
                    logger.info(f'subnat here for {tracker_obj.acro}')
                    
                else:
                    logger.info(f'subnat not here for {tracker_obj.acro}') # TODO investigate for egt
                    logger.info('check which tracker is missing subnat')                
                self.trackers = gdf
                # print(self.trackers)
                return
            gdf = tracker_obj.data
            logger.info(f'This is data for {tracker_obj.acro}:{tracker_obj.data}')
            loggerinfo(f'This is: {tracker_obj.acro}')

            tracker_sel = tracker_obj.acro # GOGPT, GGIT, GGIT-lng, GOGET
            logger.info(f'tracker_sel is {tracker_sel} equal to tracker-acro...')

            gdf['tracker-acro'] = tracker_sel
            logger.info(f"renaming on tracker acro: {gdf['tracker-acro'].iloc[0]}")
            # all_trackers.append(tracker_sel)
            # select the correct renaming dict from config.py based on tracker name
            renaming_dict_sel = renaming_cols_dict[tracker_sel]
            # rename the columns!
            # check check_rename_keys(renaming_dict_sel)
            logger.info(f'Check rename keys against cols for {tracker_sel}')
            check_rename_keys(renaming_dict_sel, gdf)
            gdf = drop_cols_df_a_rename_value_avoid_dup(renaming_dict_sel, gdf)
            gdf.columns = gdf.columns.str.strip()
            gdf = gdf.rename(columns=renaming_dict_sel) 
            
            logger.info(f"value counts for areas: {gdf['areas'].value_counts()}")
            logger.info('check value counts for area after rename')
            gdf.reset_index(drop=True, inplace=True)
            # Reset index in place
            if tracker_sel == 'GCMT':
                logger.info(f'cols after rename in GCMT:\n{gdf.info()}')
                logger.info(gdf['start_year'])
                gdf['url'] = gdf['url'].fillna('')
                # Handle for non-English Chinese wiki pages                    
                # Using np.where 
                gdf['wiki-from-name'] = np.where(
                    gdf['areas'] == 'China',
                    gdf['noneng_name'].apply(lambda x: f"https://www.gem.wiki/{x.strip().replace(' ', '_')}"),
                    gdf['name'].apply(lambda x: f"https://www.gem.wiki/{x.strip().replace(' ', '_')}")
                )  # check why subnat in there
                gdf['url'] = gdf.apply(lambda row: row['wiki-from-name'] if 'gem.wiki' not in row['url'] else row['url'], axis=1)
                
                gdf['mine-type'] = gdf['mine-type'].fillna('').str.lower().replace(' ', '-').replace('&', 'and').replace('','-')
                gdf['coal-grade'] = gdf['coal-grade'].fillna('').str.lower().replace(' ', '-').replace('&', 'and').replace('','-')

            elif tracker_sel == 'GIST':
            # make all unit status cap prod hyphenated and lowercase 
            # silly workaround for getting the gist table set up for now
                gdf.columns = gdf.columns.str.replace(' ', '-').str.lower().str.replace('latitude', 'Latitude').str.replace('longitude', 'Longitude')
                
                
                
            if 'subnat' in gdf.columns:
                logger.info(f'subnat here for {tracker_obj.acro}')
                
            else:
                logger.info(f'subnat not here for {tracker_obj.acro}') # TODO investigate for egt
                logger.info('check which tracker is missing subnat')
            logger.info(f'Adding {tracker_sel} gdf to renamed_gdfs')
            renamed_gdfs.append(gdf)
        # handle for non unique indexes
        # First, check all dataframes have unique indices
        for i, gdf in enumerate(renamed_gdfs):
            if gdf.index.has_duplicates:
                logger.warning(f"DataFrame {i} has duplicate indices, resetting...")
                renamed_gdfs[i] = gdf.reset_index(drop=True)
        
        one_gdf = pd.concat(renamed_gdfs, sort=False, ignore_index=True) 
        logger.info(one_gdf.index)
        
        cols_to_be_dropped = set(one_gdf.columns) - set(final_cols)
        logger.info(f'These cols will be dropped: {cols_to_be_dropped}')
        logger.info('Check that - skipping dropping for now')
        # TODO CHECK THIS PROBLEM with dropping
        # final_gdf = one_gdf.drop(columns=cols_to_be_dropped)
        self.trackers = one_gdf
            
 
    def get_about(self):
        if self.aboutkey != '':
            if self.mapname in ['africa', 'integrated', 'europe', 'asia', 'latam']:
                # proceed with gspread 

                print(f'Opening about key for map {self.mapname}')
                gsheets = gspread_creds.open_by_key(self.aboutkey)  
                sheet_names = [sheet.title for sheet in gsheets.worksheets()]
                multi_tracker_about_page = sheet_names[0]  
                multi_tracker_about_page = gsheets.worksheet(multi_tracker_about_page) 
                multi_tracker_about_page = pd.DataFrame(multi_tracker_about_page.get_all_values())
                multi_tracker_about_page = replace_old_date_about_page_reg(multi_tracker_about_page) 
                self.about = multi_tracker_about_page
                logger.info(self.about)
                
            else:
                logger.info('Double check the map tab in the log, did we add global single tracker about pages here?')
                logger.info('Check')
        else:
            stubbdf = pd.DataFrame({"Note": ["Note to PM, please review this data file, report any issues, and then delete this tab"]})
            self.about = stubbdf        

        
    
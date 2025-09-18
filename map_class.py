import pandas as pd
from helper_functions import replace_old_date_about_page_reg, rebuild_countriesjs, pci_eu_map_read, check_and_convert_float, remove_diacritics, check_rename_keys, fix_status_inferred, conversion_multiply, workaround_table_float_cap, workaround_table_units
from all_config import gspread_creds , mapname_gitpages, non_regional_maps, logger, client_secret_full_path, gem_path, tracker_to_fullname, tracker_to_legendname, iso_today_date, gas_only_maps, final_cols, renaming_cols_dict
import geopandas as gpd
import numpy as np
from shapely import wkt

class MapObject:
    def __init__(self,
                 name="",
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
        self.name = name
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
        if self.name == 'goit':
            # Update all values in the 'Fuel' column from 'LPG' to 'NGL'
            logger.info('Creating fuel legend for goit')
            logger.info(set(self.trackers['Fuel'].to_list()))
            self.trackers['Fuel'] = self.trackers['Fuel'].replace('LPG', 'NGL')  
        else:
            pass
        
        
    
    def capacity_hide_goget_gcmt(self):

        mapname = self.name
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
                    
                                        
                else:
                    gdf.loc[row, 'capacity-table'] = gdf.loc[row, 'capacity']
                    gdf.loc[row, 'capacity-details'] = gdf.loc[row, 'capacity']
        # TODO see if BOED is still in empty capacity details for GOIT in combination with last min fixes function below
        gdf['capacity-details'].fillna('',inplace=True)
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


    
    
    def last_min_fixes(self):
        # do filter out oil
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
        gdf.columns = [col.replace('_', '-') for col in gdf.columns] 
        gdf.columns = [col.replace('  ', ' ') for col in gdf.columns] 
        gdf.columns = [col.replace(' ', '-') for col in gdf.columns] 

        logger.info(f'Check all columns:')
        for col in gdf.columns:
            logger.info(col)
        logger.info('Is fuel-filter there?')

        # translate acronyms to full names for legend and table 
        gdf['tracker-display'] = gdf['tracker-custom'].map(tracker_to_fullname)
        gdf['tracker-legend'] = gdf['tracker-custom'].map(tracker_to_legendname)

        # make sure these are removed, though should have already been removed
        gdf['capacity'] = gdf['capacity'].apply(lambda x: str(x).replace('--', ''))
        gdf['capacity'] = gdf['capacity'].apply(lambda x: str(x).replace('*', ''))

        # make sure all null geo is removed
        gdf.dropna(subset=['geometry'],inplace=True)

        # make sure all of the units of m are removed for goget and gcmt that has no capacity
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
            
        if self.name == 'europe':
            logger.info(self.name)
            gdf = pci_eu_map_read(gdf)

        gdf.fillna('', inplace = True)
        
        for col in gdf.columns:
            gdf[col] = gdf[col].apply(lambda x: str(x).lower()) 
                       
        # Check for invalid geometries in the 'geometry' column
        invalid_geoms = []
        for idx, geom in gdf['geometry'].items():
            # Check if geometry is a shapely object and is valid
            if hasattr(geom, 'is_valid') and not geom.is_valid:
                # Try to fix geometry
                fixed_geom = geom.buffer(0)
                if fixed_geom.is_valid:
                    gdf.at[idx, 'geometry'] = fixed_geom
                else:
                    invalid_geoms.append((idx, geom))
            # If geometry is not a shapely object, try to parse it
            elif not hasattr(geom, 'is_valid'):
                try:
                    parsed_geom = wkt.loads(str(geom))
                    if parsed_geom.is_valid:
                        gdf.at[idx, 'geometry'] = parsed_geom
                    else:
                        fixed_geom = parsed_geom.buffer(0)
                        if fixed_geom.is_valid:
                            gdf.at[idx, 'geometry'] = fixed_geom
                        else:
                            invalid_geoms.append((idx, geom))
                except Exception as e:
                    invalid_geoms.append((idx, geom))
            
        # Remove rows with invalid geometry and log them
        if invalid_geoms:
            logger.warning(f"Found invalid geometries, removing: {invalid_geoms}")
            pd.DataFrame(invalid_geoms, columns=['index', 'geometry']).to_csv(f'issues/{self.name}-invalid-geometries-{iso_today_date}.csv', index=False)
            # Extract indices of invalid geometries for removal
            invalid_geom_indices = [idx for idx, _ in invalid_geoms]
            gdf.drop(invalid_geom_indices, inplace=True)
            
        # remove duplicate columns
        gdf = gdf.loc[:, ~gdf.columns.duplicated()]  
        self.trackers = gdf
    
    def save_file(self):
        logger.info(f'Saving file for map {self.name}')
        logger.info(f'This is len of gdf {len(self.trackers)}')
        # helps map to the right folder name
        if self.name in mapname_gitpages.keys():
            self.name = mapname_gitpages[self.name]
            path_for_download_and_map_files = gem_path + self.name + '/compilation_output/'
        else:
            path_for_download_and_map_files = gem_path + self.name + '/compilation_output/'
        
        if self.name in gas_only_maps or self.geo == 'global': # will probably end up making all regional maps all energy I would think
            logger.info(f"Yes {self.name} is in gas only maps so skip 'area2', 'subnat2', 'capacity2'")
            gdf = self.trackers.drop(['count-of-semi', 'multi-country', 'original-units', 'conversion-factor', 'cleaned-cap', 'wiki-from-name', 'tracker-legend'], axis=1) # 'multi-country', 'original-units', 'conversion-factor', 'cleaned-cap', 'wiki-from-name', 'tracker-legend']
        
        else:
            logger.info(f"No {self.name} is not in gas only maps")
            gdf = self.trackers.drop(['count-of-semi','multi-country', 'original-units', 'conversion-factor', 'area2', 'region2', 'subnat2', 'capacity2', 'cleaned-cap', 'wiki-from-name', 'tracker-legend'], axis=1) #  'multi-country', 'original-units', 'conversion-factor', 'area2', 'region2', 'subnat2', 'capacity1', 'capacity2', 'cleaned-cap', 'wiki-from-name', 'tracker-legend']

        print(f'Final cols:\n')
        [print(col) for col in gdf.columns]

        logger.info(f'Final cols:\n')
        cols = [(col) for col in gdf.columns]
        logger.info(cols)
    
        
 
        # Check if the dataframe is a GeoDataFrame
        if isinstance(gdf, gpd.GeoDataFrame):
            logger.info('Already a GeoDataFrame!')
        else:
            logger.info(f'Converting to GeoDataFrame for {self.name} ...')
            if 'geometry' not in gdf.columns:
                raise ValueError("The dataframe does not have a 'geometry' column to convert to GeoDataFrame.")
            gdf = gpd.GeoDataFrame(gdf, geometry=gdf['geometry'])
            gdf.set_crs(epsg=4326, inplace=True)  # Set CRS to EPSG:4326 (WGS 84)  

        # ensure no duplicated columns
        gdf = gdf.loc[:, ~gdf.columns.duplicated()]  

                
        gdf.to_file(f'{path_for_download_and_map_files}{self.name}_map_{iso_today_date}.geojson', driver='GeoJSON', encoding='utf-8')


        gdf.to_csv(f'{path_for_download_and_map_files}{self.name}_map_{iso_today_date}.csv', encoding='utf-8')
            
        newcountriesjs = list(set(gdf['areas'].to_list()))
        rebuild_countriesjs(self.name, newcountriesjs)


    def simplified(self):
        logger.info('Finish writing simplified function to easily filter down any map file for quick map rendering without table, first step for 1hot encoding')

    def set_capacity_conversions(self):
    
    # you could multiply all the capacity/production values in each tracker by the values in column C, 
    # "conversion factor (capacity/production to common energy equivalents, TJ/y)."
    # For this to work, we have to be sure we're using values from each tracker that are standardized
    # to the same units that are stated in this sheet (column B, "original units").

        gdf = self.trackers

        if self.name in gas_only_maps:
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
        
        
        # create cleaned cap for logic below 
        gdf['cleaned_cap'] = pd.to_numeric(gdf['capacity'], errors='coerce')

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
        if self.name in non_regional_maps: # map name
            logger.info('skip converting to joules')

            gdf['scaling_capacity'] = gdf['cleaned_cap']
            gdf['scaling_capacity'] = gdf['scaling_capacity'].astype(float)

        else:
            logger.info('not skipping conversion to joules...')
            logger.info(f'{self.name}')
            logger.info('check name and why it is not in non_regional_maps')
            logger.info(f'{set(gdf["conversion_factor"].to_list())}')
            gdf['scaling_capacity'] = gdf.apply(lambda row: conversion_multiply(row), axis=1)
        # must be float for table to sort
        gdf['capacity'] = gdf['capacity'].fillna('') # issue if it's natype so filling in
        gdf['capacity-table'] = gdf.apply(lambda row: pd.Series(workaround_table_float_cap(row, 'capacity')), axis=1)
        gdf['units-of-m'] = gdf.apply(lambda row: pd.Series(workaround_table_units(row)), axis=1)
 
        self.trackers = gdf        
        
    def map_ready_statuses_and_countries(self):
        
        gdf = self.trackers

        gdf['status'] = gdf['status'].fillna('Not Found') # ValueError: Cannot mask with non-boolean array containing NA / NaN values
        gdf['status'] = gdf['status'].replace('', 'Not Found') # ValueError: Cannot mask with non-boolean array containing NA / NaN values
        logger.info(f'set of statuses: {set(gdf["status"].to_list())}')
        gdf_map_ready = fix_status_inferred(gdf)
    
        # Create masks for the 'tracker-acro' conditions
        mask_gcmt = gdf_map_ready['tracker-acro'] == 'GCMT'
        mask_goget = gdf_map_ready['tracker-acro'] == 'GOGET'
    
        # Update 'status' to 'Retired' where both masks are True
        gdf_map_ready['status'].fillna('', inplace=True)
        mask_status_empty = gdf_map_ready['status'] == ''
        
        # Update 'status' to 'Not Found' where both masks are True
        gdf_map_ready.loc[mask_status_empty & mask_gcmt, 'status'] = 'retired'
        gdf_map_ready.loc[mask_status_empty & mask_goget, 'status'] = 'not found'
        gdf_map_ready['status_legend'] = gdf_map_ready.copy()['status'].str.lower().replace({
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
                    # mothballed
                    'mothballed': 'mothballed_plus',
                    'idle': 'mothballed_plus',
                    'shut in': 'mothballed_plus',
                    # retired
                    'retired': 'retired_plus',
                    'closed': 'retired_plus',
                    'decommissioned': 'retired_plus',
                    'not found': 'not-found'})
        

        # Create a mask for rows where 'status' is empty

        gdf_map_ready_no_status = gdf_map_ready.loc[mask_status_empty]

        if len(gdf_map_ready_no_status) > 0:
            logger.warning(f'check no status df, will be printed to issues as well: {gdf_map_ready_no_status}')
            gdf_map_ready_no_status.to_csv(f'issues/{self.name}-no-status-{iso_today_date}.csv')
        
        # make sure all statuses align with no space rule
        gdf_map_ready['status'] = gdf_map_ready['status'].apply(lambda x: x.strip().replace(' ','-')) # TODO why was this commented out?
        gdf_map_ready['status_legend'] = gdf_map_ready['status_legend'].apply(lambda x: x.strip().replace('_','-'))
        gdf_map_ready['status'] = gdf_map_ready['status'].apply(lambda x: x.lower())
        logger.info(set(gdf_map_ready['status'].to_list()))
        logger.warning('check list of statuses after replace space and _') 
        # TODO check that all legend filter columns go through what status goes through 
        if self.name == 'gcmt':
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

        
        # check that areas isn't empty
        tracker_sel = gdf_map_ready['tracker-acro'].iloc[0]
        logger.info(f'this is tracker_sel {tracker_sel}')
        if tracker_sel == 'GOGET':
            logger.info(gdf_map_ready['areas'])
            logger.info('check goget areas in map ready countries')
        gdf_map_ready['areas'] = gdf_map_ready['areas'].fillna('')

        empty_areas = gdf_map_ready[gdf_map_ready['areas']=='']
        if len(empty_areas) > 0:
            logger.warning(f'Check out which rows are empty for countries for map will also be printed in issues: {self.name}')
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

            
        if self.name in gas_only_maps:
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
            
            gdf = tracker_obj.data
            tracker_sel = tracker_obj.acro # GOGPT, GGIT, GGIT-lng, GOGET
            logger.info(f'tracker_sel is {tracker_sel} equal to tracker-acro...')

            if tracker_sel == 'GOGPT-eu':
                # 'passing because GOGPT-eu already renamed when concatted hy and plants tabs')

                logger.info(f'this is df cols: {gdf.columns}')
                
                tracker_rename = gdf['tracker-acro'].iloc[0]
                renaming_dict_sel = renaming_cols_dict[tracker_rename]
                logger.info(f'This is renaming dict for {tracker_rename}: {renaming_dict_sel}')
                logger.info(f'Check rename keys against cols for {tracker_rename}')
                check_rename_keys(renaming_dict_sel, gdf)
                gdf.columns = gdf.columns.str.strip()
                gdf = gdf.rename(columns=renaming_dict_sel) 
                
                logger.info(f'This is len: {len(gdf)}: {set(gdf["tracker-acro"].to_list())}')
                logger.info(f'This should be two, plants and plants_hy!')
              
                
            else:
                gdf['tracker-acro'] = tracker_sel

                logger.info(f"renaming on tracker acro: {gdf['tracker-acro'].iloc[0]}")
                # all_trackers.append(tracker_sel)
                # select the correct renaming dict from config.py based on tracker name
                renaming_dict_sel = renaming_cols_dict[tracker_sel]
                # rename the columns!
                # check check_rename_keys(renaming_dict_sel)
                logger.info(f'Check rename keys against cols for {tracker_sel}')
                check_rename_keys(renaming_dict_sel, gdf)
                gdf.columns = gdf.columns.str.strip()
                gdf = gdf.rename(columns=renaming_dict_sel) 
                
                logger.info(f"value counts for areas: {gdf['areas'].value_counts()}")
                logger.info('check value counts for area after rename')
                gdf.reset_index(inplace=True)
                # Reset index in place
                if tracker_sel == 'GCMT':
                    logger.info(f'cols after rename in GCMT:\n{gdf.info()}')
                    logger.info(gdf['start_year'])
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
                logger.info(f'subnat here for {tracker_obj.name}')
                
            else:
                logger.info(f'subnat not here for {tracker_obj.name}') # TODO investigate for egt
                logger.info('check which tracker is missing subnat')
            logger.info(f'Adding {tracker_sel} gdf to renamed_gdfs')
            renamed_gdfs.append(gdf)
        
        one_gdf = pd.concat(renamed_gdfs, sort=False, verify_integrity=True, ignore_index=True) 
        logger.info(one_gdf.index)
        
        cols_to_be_dropped = set(one_gdf.columns) - set(final_cols)
        logger.info(f'These cols will be dropped: {cols_to_be_dropped}')
        logger.info('Check that')
        
        final_gdf = one_gdf.drop(columns=cols_to_be_dropped)
        self.trackers = final_gdf
            
 
    def get_about(self):
        if self.aboutkey != '':
            if self.name in ['africa', 'integrated', 'europe', 'asia', 'latam']:
                # proceed with gspread 

                print(f'Opening about key for map {self.name}')
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

        
    
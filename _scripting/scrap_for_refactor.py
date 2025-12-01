final_cols

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

# using this as an example
# map obj could be project level
# tracker obj could be unit level
# NEXT STEP so really just need to add a lot of class attributes to the tracker obj for each column from the data

# about data for map comes from main tracker release date in log sheet (soon to be launcher)
# about data for all trackers still comes directly from tracker

# this class creation should happen at start of make map file, unless it should happen when NO it should happen when objects are created
# can have original df and each relevant column assigned to an attribute and just use straight df for metadata and data downloads then use attributes for map adjustments 

def create_project_and_units_from_df_rows(df_rows):
    r1 = df_rows.iloc[0]
    project_obj = SolarWindProject(
        id=r1["GEM location ID"], name=r1["Project Name"], wikiURL=r1["Wiki URL"],
        nameOther=r1["Other Name(s)"], nameLocal=r1["Project Name in Local Language / Script"],
        city=r1["City"], localArea=r1["Local area (taluk, county)"], majorArea=r1["Major area (prefecture, district)"],
        subnational=r1["State/Province"], country=r1["Country"], locationAccuracy=r1["Location accuracy"],
        linkedProjects=r1["Linked Project"]
    )

    for index, r in df_rows.iterrows():
        phase_obj = SolarWindPhase(
            id=r["GEM phase ID"], plant_id=r["GEM location ID"], name=r["Phase Name"],
            status=r["Status"], statusDatasource=r["Status [ref]"],
            capacity=r["Capacity (MW)"], capacityDatasource=r["Capacity [ref]"], capacityRating=r["Capacity Rating"],
            technology=r["Technology Type"], technologyDatasource=r["Technology Type [ref]"],

            city=r["City"], localArea=r["Local area (taluk, county)"], majorArea=r["Major area (prefecture, district)"],
            subnational=r["State/Province"], country=r["Country"], locationAccuracy=r["Location accuracy"],
            latitude=r["Latitude"], longitude=r["Longitude"], coordinateDatasource=r["Coordinates [ref]"],

            startYearLow=r["Start year"], startYearDatasource=r["Start year [ref]"],
            endYearLow=r["Retired year"], endYearDatasource=r["Retired year [ref]"],

            owner=r["Owner"], ownerDatasource=r["Owner [ref]"], ownerLocalName=r["Owner Name in Local Language / Script"],
            operator=r["Operator"], operatorDatasource=r["Operator [ref]"], operatorLocalName=r["Operator Name in Local Language / Script"],

            otherIDsLocation=r["Other IDs (location)"], dateLastResearched=r["Date Last Researched"]
        )
        project_obj.addUnit(phase_obj)

    return project_obj



class SolarWindProject:
    def __init__(self,
                 id="",
                 name="",
                 wikiURL="",
                 nameOther="",
                 nameLocal="",

                 city="",
                 localArea="",
                 majorArea="",
                 subnational="",
                 country="",
                 locationAccuracy="",

                 technology="",
                 linkedProjects=""
                 ):

        self.id = id
        self.name = name
        self.wikiURL = wikiURL
        self.nameOther = nameOther
        self.nameLocal = nameLocal

        self.city = city
        self.localArea = localArea
        self.majorArea = majorArea
        self.subnational = subnational
        self.country = country
        self.locationAccuracy = locationAccuracy.lower()

        self.technology = technology

        if linkedProjects != "":
            self.linkedProjectIDs = [proj_id.strip().lstrip("L") for proj_id in linkedProjects.split(",") if proj_id]
        else:
            self.linkedProjectIDs = []

        self.units = []

        self.name_clean = get_project_name_clean(self)
        self.file_name = get_project_file_name(self)

    def addUnit(self, unit):
        self.units.append(unit)

    def getUnitStatusList(self):
        unit_statuses = []
        for unit in self.units:
            unit_statuses.append(unit.status)
        return unit_statuses
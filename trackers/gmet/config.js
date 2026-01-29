var config = {
    geojson: 'https://publicgemdata.nyc3.cdn.digitaloceanspaces.com/gmet/2025-12/gmet_map_2026-01-16.geojson',
    geometries: ['Point','LineString'],
    colors: {
        'red': '#c74a48',
        'light blue greeninfo': '#74add1',
        'blue': '#5c62cf',
        'green': '#4c9d4f',
        'light grey greeninfo': '#ccc',
        'grey': '#8f8f8e',
        'dark grey': '#4B4B4B',
        'orange': '#FF8C00',
        'yellow': '#d4af00'
    },

    color: { 
        field: 'legend-filter',
        label: 'Plume and Infrastructure Projects',
        values: { // must have hyphen NO space
            // 'Plumes': 'red',
            'plumes-attrib': 'red',
            'plumes-unattrib': 'orange',

            'Oil-and-Gas-Extraction-Areas': 'blue',
            // 'Oil and Gas Reserves': 'blue',
            'Pipelines': 'green',
            'Coal-Mines---Non-closed': 'yellow',
            // 'LNG Terminals': 'green'
            'lng-import': 'green',
            'lng-export': 'green',


        }
        },

        filters: [
        {
            field: 'legend-filter',
            label: 'Plume and Infrastructure Projects',
            values: ['Oil-and-Gas-Extraction-Areas', 'Coal-Mines---Non-closed', 'lng-import', 'lng-export', 'Pipelines','plumes-attrib', 'plumes-unattrib'],
            values_labels: [
            'Oil and Gas Extraction Areas', 
            'Coal Mines', 
            'LNG Terminals Import', 
            'LNG Terminals Export',
            'Pipelines', 
            'Reviewed Plumes (has attribution info)', //  info)
            'Reviewed Plumes (no attribution info)'
            ],
            primary: true
        },
        {
            field: 'status-legend',
            label: 'Infrastructure Status',
            values: ['operating', 'proposed-plus','construction-plus', 'mothballed-plus', 'retired-plus', 'not-found'], // pre-construction-plus
            /* value_labels must match order/number in values */
            values_labels: ['Operating', 'Proposed/Announced/Discovered', 'Construction/In development','Mothballed/Idle/Shut in/Abandoned','Retired/Closed/Decommissioned/Cancelled','Not applicable/UGS'] // 'Pre-construction / Pre-permit / Permitted / Exploration'
        }
    ],

    statusDisplayField: 'status',
    statusField: 'status-legend',
    
    capacityField: 'scaling-capacity',
    capacityLabel: '', // for gmet that has no capacity but only emissions data

    /* Labels for describing the assets */
    assetFullLabel: "Projects",
    assetLabel: 'projects',

    /* the column that contains the asset name. this varies between trackers */
    nameField: 'name',
    countryField: 'areas',

    // urlField: 'url', // wikiField

    /* configure the table view, selecting which columns to show, how to label them, 
        and designated which column has the link */
    tableHeaders: {

        values: ['name', 'status','plume-emissions', 'emission-uncertainty', 'emissions-terminals', 'tonnesyr-pipes-emissions','tonnes-goget-reserves-emissions', 'mtyr-gcmt-emissions','typeinfra', 'date','subnat', 'areas','infra-name', 'geminfrawiki'],
        labels: ['Project', 'Status','Emissions (kg/hr)', 'Emissions Uncertainty (kg/hr)', 'Methane emissions if fully operational', 'Emissions if Operational (tonnes/yr)','Potential Emissions for whole reserves (tonnes)', 'Coal Mine Methane Emissions Estimate (mt/yr)','Type of Infrastructure','Observation Date', 'Subnational', 'Country/Area(s)','Nearby Infrastructure Project Name', 'Infrastructure Wiki'],
        clickColumns: ['name'],
        rightAlign: ['plume-emissions','date'],
        removeLastComma: ['areas'],
        toLocaleString: ['scaling_col'], // not displayed

    },
    /* configure the search box; 
        each label has a value with the list of fields to search. Multiple fields might be searched */
    searchFields: { 'Country/Area(s)': ['areas'],

        'Project Type': ['legend-filter'],
        'Project': ['name', 'name-search', 'infra-name', 'geminfrawiki'], 
        'Companies': ['operator'],
        'Type of Infrastructure': ['typeInfra'],
        // 'Coordinates': ['geometry', 'lat', 'lng', 'coordssearch'] # this does not work so commenting out, unclear how useful without the zoomTo / fitBounds
        // 'Government Well ID': ['well_id'],
        // 'Other Government ID Assets': ['gov_assets']

    },

    /* define fields and how they are displayed. 
        `'display': 'heading'` displays the field in large type
        `'display': 'range'` will show the minimum and maximum values.
        `'display': 'join'` will join together values with a comma separator
        `'display': 'location'` will show the fields over the detail image
        `'label': '...'` prepends a label. If a range, two values for singular and plural.
    */
    detailView: {
        //TO ADD 
        // satDataProvider instrument emissionsUncert typeInfra geminfrawiki 
        // emissionsIfOp, NEED TO PULL IN piplines geometry and owner on pid 
        // unit-name, inportExport

        'name': {'display': 'heading'},
        // 'tracker': {'label': 'Tracker Type'},
        'satdataprovider': {'label': 'Satellite Data Provider'},
        'owner': {'label': 'Owner'},
        'operator': {'label': 'Operator'},
        // EMISSIONS PLUMES WORKING
        'plume-emissions': {'label': 'Emissions (kg/hr)'},

        'emission-uncertainty': {'label': 'Emissions Uncertainity (kg/hr)'},
        'typeinfra': {'label': 'Type of Infrastructure'},
        'infra-name': { 'label': 'Nearby Infrastructure Project Name'},

        // EMISSIONS COAL MINE WORKING
        'mtyr-gcmt-emissions': {'label': 'Coal Mine Methane Emissions Estimate (mt/yr)'},

        'capacity-output': {'label': 'Coal Output (Annual, Mst)'},
        'capacity-prod': {'label': 'Production (Mtpa)'},

        // EMISSIONS PIPELINEtonnesyr-pipes_emissions
        'tonnesyr-pipes_emissions': {'label': 'Emissions if Operational (tonnes/yr)'}, //check correct

        'pipe-length': {'label': 'Length (km)'},
        'capacitybcm/y': {'label': 'Capacity (bcm/y)'},
        'capacityinmtpa': {'label': 'Capacity (MTPA)'},

        // EMISSIONS GOGET WORKING
        'tonnes-goget-reserves-emissions': {'label': 'Potential Emissions for whole reserves (tonnes)'},
        
        // EMISSIONS LNG TERM
        'emissions-terminals': {'label': 'Methane emissions if fully operational'},//'Annual methane emissions estimate if operational (mt/year)'},
        
        'inportexport': {'label': 'Terminal Facility Type'},
        'date': {'label': 'Observation Date'},
        'status-legend': {'label': 'Status'},
        'instrument': {'label': 'Instrument'},
        'areas': {'label': 'Country/Area(s)'},
        // 'geminfrawiki': {'label': 'Infrastructure Wiki'}, // or display md to just display as text md
        'areas-subnat-sat-display': {'display': 'location'}, 
        'infra-wiki-md': {'display': 'simple_markup'},
        'carbon-mapper-md': {'display': 'simple_markup'},
        'release-date-infra': {'display': 'simple_markup'}
    }, 

    linkField: 'pid',

    multiCountry: true,

    showMaxCapacity: false,

    showAllPhases: true,


    // POINTS
    /* radius associated with minimum/maximum value on map */
    minRadius: 2,
    maxRadius: 10,

    // LINES
    minLineWidth: 1,
    maxLineWidth: 3,

    // POINTS HIGH ZOOM CLOSE IN
    // /* radius to increase min/max to under high zoom */
    highZoomMinRadius: 4,
    highZoomMaxRadius: 32,

    // LINES HIGH ZOOM CLOSE IN

    highZoomMinLineWidth: 4,
    highZoomMaxLineWidth: 32,
    

}

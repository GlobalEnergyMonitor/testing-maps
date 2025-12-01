var config = {
    geojson: 'https://publicgemdata.nyc3.cdn.digitaloceanspaces.com/gmet/2025-11/gmet_map_2025-11-26.geojson',
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
        // 'yellow': '#f3ff00'
    },

    color: { 
        field: 'tab-type',
        label: 'Plume and Infrastructure Projects',
        values: {
            'Plumes': 'red',
            'Oil and Gas Extraction Areas': 'blue',
            // 'Oil and Gas Reserves': 'blue',
            'Pipelines': 'green',
            'Coal Mines - Non-closed': 'green',
            'LNG Terminals': 'green'

            // 'plumes-attrib': 'red',
            // 'plumes-unattrib': 'orange',
            // 'oil-and-gas-extraction-areas': 'blue',
            // 'coal-mines': 'green',
            // 'pipelines': 'green',
            // 'lng-terminals': 'green'
        }
        },

        filters: [
        {
            field: 'tab-type',
            label: 'Plume and Infrastructure Projects',
            values: ['Oil and Gas Extraction Areas', 'Coal Mines - Non-closed', 'LNG Terminals', 'Pipelines','Plumes'],
            values_labels: [
            'Oil and Gas<br>Extraction Areas', 
            'Coal Mines', 
            'LNG Terminals', 
            'Pipelines', 
            'GEM Reviewed Plumes<br>(has attribution information)'
            ],
            primary: true
        },
        {
            field: 'status-legend',
            label: 'Infrastructure Status',
            values: ['operating', 'proposed-plus','pre-construction-plus','construction-plus','mothballed-plus', 'retired-plus', 'unknown-plus'], // pre-construction-plus
            /* value_labels must match order/number in values */
            values_labels: ['Operating', 'Proposed/Announced/Discovered', 'Pre-construction/Exploration','Construction/In development','Mothballed/Idle/ Shut in/Abandoned','Retired/Closed/Decommissioned/Cancelled','Not applicable/UGS'] // 'Pre-construction / Pre-permit / Permitted / Exploration'
        }
    ],

    statusDisplayField: 'status',
    statusField: 'status-legend',

    // # O&G extraction areas and coal mines by status 
    // plumes by "has attribution information"
    // infrastructure emissions estimates
    
    capacityField: 'scaling-capacity',
    capacityLabel: '', // for gmet that has no capacity but only emissions data

    /* Labels for describing the assets */
    assetFullLabel: "Projects",
    assetLabel: 'projects',

    /* the column that contains the asset name. this varies between trackers */
    nameField: 'name',

    // urlField: 'url', // wikiField

    /* configure the table view, selecting which columns to show, how to label them, 
        and designated which column has the link */
    tableHeaders: {

        values: ['name', 'status','plume_emissions', 'emission_uncertainty','infra_type', 'date','subnational', 'areas','infra_name', 'infra_url', 'well_id', 'gov_assets'],
        labels: ['Project', 'Status','Emissions (kg/hr)', 'Emissions Uncertainty (kg/hr)','Type of Infrastructure','Observation Date', 'Subnational', 'Country/Area(s)','Nearby Infrastructure Project Name', 'Infrastructure Wiki', 'Government Well ID', 'Other Government ID Assets'],
        clickColumns: ['name'],
        rightAlign: ['Government Well ID','plume_emissions','date'],
        removeLastComma: ['country'],
        toLocaleString: ['scaling_col'], // not displayed

    },
    /* configure the search box; 
        each label has a value with the list of fields to search. Multiple fields might be searched */
    searchFields: { 'Country/Area(s)': ['country'],

        'Project Type': ['tracker'],
        'Project': ['name'], 
        'Companies': ['operator'],
        'Type of Infrastructure': ['infra_type'],
        'Government Well ID': ['well_id'],
        'Other Government ID Assets': ['gov_assets']

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
        'plume-emissions': {'label': 'Emissions (kg/hr)'},
        'emission-uncertainty': {'label': 'Emissions Uncertainity (kg/hr)'},
        'typeinfra': {'label': 'Type of Infrastructure'},
        'infra-name': { 'label': 'Nearby Infrastructure Project Name'},
        'mtyr-gcmt-emissions': {'label': 'Coal Mine Methane Emissions Estimate (mt/yr)'},
        'capacity-output': {'label': 'Coal Output (Annual, Mst)'},
        'capacity-prod': {'label': 'Production (Mtpa)'},
        'emissionsifop': {'label': 'Emissions if Operational (tonnes/yr)'}, //check correct
        'pipe-length': {'label': 'Length (km)'},
        'capacitybcm/y': {'label': 'Capacity (bcm/y)'},
        'capacityinmtpa': {'label': 'Capacity (MTPA)'},
        'tonnes-goget-reserves-emissions': {'label': 'Potential Emissions for whole reserves (tonnes)'},
        'date': {'label': 'Observation Date'},
        'status-legend': {'label': 'Status'},
        'instrument': {'label': 'Instrument'},
        'areas': {'label': 'Country/Area(s)'},
        'geminfrawiki': {'label': 'Infrastructure Wiki'}, // or display md to just display as text md
        'areas-subnat-sat-display': {'display': 'location'}, 
        // 'carbonmapper' : {'display': 'md'} // add in col for liscencing "Plume Data © Carbon Mapper. Subject to terms." just for plume data
        'carbonmapper' : {'display': 'md'}


    }, 

    linkField: 'pid',

    multiCountry: true,

    showMaxCapacity: false
}

var config = {
    json: 'compilation_output/europe_2024-10-23.geojson',
    geometries: ['Point','LineString'],
    center: [8, 30],
    zoomFactor: 1.9,
    img_detail_zoom: 10,
    statusField: 'status-legend',
    statusDisplayField: 'status',
    linkField: 'id',
    color: {
        field: 'tracker-custom',
        values: {
            'GOGPT': 'blue',
            'GOGET-oil': 'red',
            'GGIT-eu': 'green',
            'GGIT-import':'green',
            'GGIT-export':'green',


        }
    },
    //filter values should have no spaces
    filters: [
        {
            field: 'tracker-custom',
            values: ["GOGPT",  "GGIT-eu", "GGIT-import", "GGIT-export", "GOGET-oil", ], 
            values_labels: ['gas units', 'gas pipelines', 'LNG import terminals', 'LNG export terminals', 'gas extraction areas',],
            primary: true
        },
        {
            field: 'status-legend',
            label: 'Status',
            values: ['operating','proposed-plus','pre-construction-plus','construction-plus','retired-plus','cancelled','mothballed-plus','shelved', 'not-found'],
            values_labels: ['Operating','Proposed/Announced/Discovered','Pre-construction/Pre-permit/Permitted', 'Construction/In development','Retired/Closed/Decommissioned','Cancelled','Mothballed/Idle/Shut in','Shelved', 'Not Found']

        },
        {
            field: 'pci-list',
            label: 'EU Projects of Common Interest (PCI)',
            values: ['5', '6', 'both'],
            values_labels: ['PCI-5', 'PCI-6', 'PCI-5 & PCI-6'] 

        },

    ],
    capacityField: 'scaling-capacity',
    
    capacityDisplayField: 'capacity-display',
    capacityLabel: '',
    //interpolate: ["cubic-bezier", 0, 0, 0, 1],
    //can be string for single value, or hash. always single value is showMaxCapacity is true
    // capacityLabel: {
    //     field: 'tracker-custom',
    //     values: {
    //         'GCPT': 'MW',
    //         'GOGPT': 'MW',
    //         'GBPT':	'MW',
    //         'GNPT':	'MW',
    //         'GSPT':	'MW',
    //         'GSPT':	'MW',
    //         'GWPT':	'MW',
    //         'GHPT':	'MW',
    //         'GGPT':	'MW',
    //         'GOGET - oil':	'million boe/y',
    //         'GOGET - gas':	'million m³/y',
    //         'GOIT': 'boe/d',
    //         'GGIT':	'Bcm/y of natural gas',
    //         'GGIT - import': 'MTPA of natural gas',
    //         'GGIT - export': 'MTPA of natural gas',
    //         'GCMT':	'million tonnes coal/y',
    //         'GCTT':	'million tonnes coal/y'
    //     }
    // },
    // skipCapacitySum: '',

    // capItemLabel:  {
    //         field: 'tracker-custom',
    //         values: {
    //             'GCPT': 'MW',
    //             'GOGPT': 'MW',
    //             'GBPT':	'MW',
    //             'GNPT':	'MW',
    //             'GSPT':	'MW',
    //             'GWPT':	'MW',
    //             'GHPT':	'MW',
    //             'GGPT':	'MW',
    //             // 'GOGET - oil':	'million boe/y',
    //             // 'GOGET - gas':	'million m³/y',
    //             'GOIT': 'boe/d',
    //             'GGIT':	'Bcm/y of natural gas',
    //             'GGIT - import': 'MTPA of natural gas',
    //             'GGIT - export': 'MTPA of natural gas',
    //             // 'GCMT':	'million tonnes coal/y',
    //             'GCTT':	'million tonnes coal/y'
    //         }
    //     },
    // prodItemLabel: {
    //     field: 'tracker-custom',
    //         values: {
    //             'GOGET - oil':	'million boe/y',
    //             'GOGET - gas':	'million m³/y',
    //             'GCMT':	'million tonnes coal/y'
    //         }
    // },
    //productionLabel NEED a productionLabel
    showMaxCapacity: false,

    assetFullLabel: "Units / Pipelines", 
    //can be string for single value, or hash
    // not using assetLabel for now TODO
    assetLabel: '',
    // assetLabel: {
    //     // field: 'tracker-custom',
    //     // values: {
    //     //     'GCPT': 'units',
    //     //     'GOGPT': 'units',
    //     //     'GBPT': 'units',
    //     //     'GNPT': 'units',
    //     //     'GSPT': 'phases',
    //     //     'GWPT':	'phases',
    //     //     'GHPT':	'units',
    //     //     'GGPT':	'units',
    //     //     'GOGET - oil': 'areas',
    //     //     'GOGET - gas': 'areas',
    //     //     'GOIT': 'projects',
    //     //     'GGIT': 'projects',
    //     //     'GGIT - import': 'projects',
    //     //     'GGIT - export': 'projects',
    //     //     'GCMT': 'projects',
    //     //     'GCTT': 'projects'
    //     // }
    // },
    nameField: 'name',
//    linkField: 'id',  

    countryFile: 'countries.js',
    allCountrySelect: false,
    countryField: 'areas',
    //if multicountry, always end values with a comma
    multiCountry: true,

    tableHeaders: {
        values: ['name','unit-name', 'owner', 'parent', 'capacity-table', 'status', 'areas', 'start-year', 'prod-gas', 'prod-year-gas', 'tracker-display', 'fuel'],
        labels: ['Name','Unit','Owner', 'Parent','Capacity (MW)', 'Status','Country/Area(s)','Start year', 'Production (Million m³/y)', 'Production year (gas)', 'Type', 'Fuel'],
        
        // 'capacity-oil', 'capacity-gas'
        // 'Production oil (Million bbl/y)', 'Production Gas (Milliion m³/y)'
        clickColumns: ['project'],
        rightAlign: ['unit','capacity','prod-gas','start-year','prod-year-gas'], 
        removeLastComma: ['areas'], 
        // displayValue: {'tracker-display': "assetLabel"},
        // appendValue: {'capacity': "capItemLabel"},
        // appendValue: {'production': "prodItemLabel"},
        // appendValue: {'capacity-oil ': "prodItemLabel"},
        // appendValue: {'capacity-gas': "prodItemLabel"},

    },
    searchFields: { 'Project': ['name'], 
        'Companies': ['owner', 'parent'],
        'Start Year': ['start-year'],
        'Infrastructure Type': ['tracker-display'],
        'Status': ['status'],
        'Province/State': ['subnat']
    },
    detailView: {
        'name': {'display': 'heading'},
        'status': {'label': 'Status'}, 
        'unit-name': {'label': 'Unit Name'},
        // 'status': {'lable': 'Status'}, // THIS NEEDS TO BE FIXED it breaks the click option saying not included
        // 'prod-gcmt': {'label': 'Production (MTPA)'}, // if its GCMT or GOGET should be 
        'capacity-table': {'label': 'Capacity'}, // interim until summary capacity can be customized by tracker
        'prod-gas': {'label': 'Production (Million m³/y)'},
        'prod-year-gas': {'label': 'Production Year - Gas'},
        'start-year': {'label': 'Start Year'},
        'owner': {'label': 'Owner'},
        'parent': {'label': 'Parent'},
        'river': {'label': 'River'},
        'tracker-display': {'label': 'Type'},
        'areas': {'label': 'Country/Area(s)'},
        'areas-subnat-sat-display': {'display': 'location'}, 
        // 'areas-display': {'display': 'location'} // TODO pull out first one only if ; in it
    }

};
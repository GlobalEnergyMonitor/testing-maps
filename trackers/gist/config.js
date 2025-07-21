var config = {
    geojson: 'https://publicgemdata.nyc3.cdn.digitaloceanspaces.com/gist/2025-07/gist_map_2025-07-17.geojson', 
    colors: {
        'light red': '#f28b82',
        'red': '#c74a48',
        'light blue': '#5dade2',
        'blue': '#5c62cf',
        'green': '#4c9d4f',
        'light green': '#66c26e',
        'light grey': '#e0e0e0',
        'grey': '#8f8f8e',
        'orange': '#FF8C00',
        'yellow': '#f3ff00',
        'black': '#000000',
        'purple': '#9370db'
    },
    // {'cancelled', 'operating', 'mothballed', 'announced', 'retired', 'mothballed pre-retirement', 'construction', 'operating pre-retirement'}
    // {'Electric-arc-furnaces', 'DRI-furnaces', 'Open-hearth-furnaces', 'Basic-oxygen-furnaces', 'Blast-furnaces'}
    color: { 
        field: 'prod-method-tier', // prod type
        values: {
            'Electric': 'light green',
            'ElectricOxygen': 'blue',
            'Oxygen': 'orange',
            'IronmakingBF': 'light red',
            'IronmakingDRI': 'light blue',
            'IntegratedBF': 'red',
            'IntegratedBFandDRI':  'purple',
            'IntegratedDRI': 'green',
            'Integratedunknown': 'grey',
            'Steelotherunspecified': 'light grey',
            'Ironotherunspecified': 'light grey'
        }
    },
    filters: [
        {
            field: 'prod-method-tier',
            /* values need to be specified for ordering */
            // values: ['BOF','EAF','BOF; EAF','BF','DRI','integrated (bf)', 'integrated (dri)', 'integrated (bf and dri)',
            //     'Steel other/unspecified','Iron other/unspecified',]
            values: ['Electric', 'ElectricOxygen','Oxygen', 'IronmakingBF', 'IntegratedBFandDRI', 
                    'IronmakingDRI', 'IntegratedDRI', 'IntegratedBF','Integratedunknown','Steelotherunspecified','Ironotherunspecified'],


            values_labels: ['Electric','Electric, oxygen','Oxygen','Ironmaking (BF)', 'Integrated (BF & DRI)', 'Ironmaking (DRI)',
                    'Integrated (DRI)', 'Integrated (BF)', 'Integrated unknown', 'Steel other/unspecified', 'Iron other/unspecified'],
            // values: ['Electric-arc-furnaces', 'Basic-oxygen-furnaces', 'Open-hearth-furnaces', 'Blast-furnaces', 'DRI-furnaces',],
            // values-labels: ['Electric arc furnaces', 'Basic oxygen furnaces', 'Open hearth furnaces', 'Blast furnaces', 'DRI furnaces'],
            primary: true,
            field_hover_text: 'For full descriptions of steelmaking route categories, see the <a href="https://globalenergymonitor.org/projects/global-iron-and-steel-tracker/frequently-asked-questions/"> FAQs</a>.',        

        },
        // do not use status-legend since it is for multi tracker maps
        {
            field: 'status',
            label: 'Plant Status',
            values: ['announced', 'cancelled', 'construction', 'mothballed', 'operating', 'operating-pre-retirement', 'retired'], //'mothballed-pre-retirement',
            values_labels: ['Announced', 'Cancelled', 'Construction', 'Mothballed', 'Operating', 'Operating Pre-Retirement', 'Retired'], // 'Mothballed Pre-Retirement', 
            field_hover_text: "Status reflects the plant-level status. Some capacities (e.g., announced expansions at a plant that already operates capacity) may not appear under their specific category if the overall plant status is different."

        }
    ],

    linkField: 'pid',
    // lat:'Latitude',
    // lng: 'Longitude',
    urlField: 'url',
    statusField: 'status',
    statusDisplayField: 'status-display',
    countryField: 'areas',
    capacityField: 'scaling-capacity', // change to scaling col once added
    // capacityDisplayField: 'current-capacity-(ttpa)',

    capacityLabel: '', //'TTPA', 
    // context-layers: [
    //     {
    //         field: 'coalfield',
    //         'label': 'Coal Fields',
    //         'tileset': '[mapbox tile url]',
    //         paint: {}
    //     }
    // ],


    /* Labels for describing the assets */
    assetFullLabel: "Iron and Steel Plants",
    assetLabel: 'plants',

    /* the column that contains the asset name. this varies between trackers */
    nameField: 'name',

    
    /* configure the table view, selecting which columns to show, how to label them, 
        and designated which column has the link */
    tableHeaders: {
        values: ['name','owner', 'parent', 'status-display', 'start-year','prod-method-tier-display','main-production-equipment', 'subnat','areas'],
        labels: ['Plant','Owner','Parent', 'Plant Status', 'Start date', 'Production Method','Main Production Equipment','Subnational Unit','Country/Area'],
        clickColumns: ['name'],
        rightAlign: [],
        toLocaleString: ['capacity'], // not displayed
        removeLastComma: ['areas']

    },

    /* configure the search box; 
        each label has a value with the list of fields to search. Multiple fields might be searched */
    searchFields: { 'Plant': ['name', 'noneng-name'], 
        'Companies': ['owner', 'parent', 'noneng-owner', 'parent_gem_id', 'owner_gem_id'],
        'Production Method': ['prod-method-tier-display', 'prod-method-tier'] //'main-production-equipment'
    },

    /* define fields and how they are displayed. 
        `'display': 'heading'` displays the field in large type
        `'display': 'range'` will show the minimum and maximum values.
        `'display': 'join'` will join together values with a comma separator
        `'display': 'location'` will show the fields over the detail image
        `'label': '...'` prepends a label. If a range, two values for singular and plural.
    */
    detailView: {
        'name': {'display': 'heading'},
        'prod-method-tier-display': {'label': 'Production Method'},
        'parent': {'label': 'Parent'},
        'owner': {'label': 'Owner'},
        'start-year': {'label': 'Start date'},
        'location-accuracy': {'label': 'Coordinate Accuracy'},
         'announced-nominal-bf-capacity-(ttpa)': {'display': 'gist-unit-level','label': 'Announced BF capacity (ttpa)'},
        'announced-nominal-bof-steel-capacity-(ttpa)': {'display': 'gist-unit-level','label': 'Announced BOF steel capacity (ttpa)'},
        'announced-nominal-dri-capacity-(ttpa)': {'display': 'gist-unit-level','label': 'Announced DRI capacity (ttpa)'},
        'announced-nominal-eaf-steel-capacity-(ttpa)': {'display': 'gist-unit-level','label': 'Announced EAF steel capacity (ttpa)'},
        'announced-other/unspecified-steel-capacity-(ttpa)': {'display': 'gist-unit-level','label': 'Announced other/unspecified steel capacity (ttpa)'},
        'cancelled-nominal-bf-capacity-(ttpa)': {'display': 'gist-unit-level','label': 'Cancelled BF capacity (ttpa)'},
        'cancelled-nominal-bof-steel-capacity-(ttpa)': {'display': 'gist-unit-level','label': 'Cancelled BOF steel capacity (ttpa)'},
        'cancelled-nominal-dri-capacity-(ttpa)': {'display': 'gist-unit-level','label': 'Cancelled DRI capacity (ttpa)'},
        'cancelled-nominal-eaf-steel-capacity-(ttpa)': {'display': 'gist-unit-level','label': 'Cancelled EAF steel capacity (ttpa)'},
        'cancelled-other/unspecified-steel-capacity-(ttpa)': {'display': 'gist-unit-level','label': 'Cancelled other/unspecified steel capacity (ttpa)'},
        'construction-nominal-bf-capacity-(ttpa)': {'display': 'gist-unit-level','label': 'Construction BF capacity (ttpa)'},
        'construction-nominal-bof-steel-capacity-(ttpa)': {'display': 'gist-unit-level','label': 'Construction BOF steel capacity (ttpa)'},
        'construction-nominal-dri-capacity-(ttpa)': {'display': 'gist-unit-level','label': 'Construction DRI capacity (ttpa)'},
        'construction-nominal-eaf-steel-capacity-(ttpa)': {'display': 'gist-unit-level','label': 'Construction EAF steel capacity (ttpa)'},
        'construction-other/unspecified-steel-capacity-(ttpa)': {'display': 'gist-unit-level','label': 'Construction other/unspecified steel capacity (ttpa)'},
        'mothballed-nominal-bf-capacity-(ttpa)': {'display': 'gist-unit-level','label': 'Mothballed BF capacity (ttpa)'},
        'mothballed-nominal-bof-steel-capacity-(ttpa)': {'display': 'gist-unit-level','label': 'Mothballed BOF steel capacity (ttpa)'},
        'mothballed-nominal-dri-capacity-(ttpa)': {'display': 'gist-unit-level','label': 'Mothballed DRI capacity (ttpa)'},
        'mothballed-nominal-eaf-steel-capacity-(ttpa)': {'display': 'gist-unit-level','label': 'Mothballed EAF steel capacity (ttpa)'},
        'mothballed-nominal-ohf-steel-capacity-(ttpa)': {'display': 'gist-unit-level','label': 'Mothballed OHF steel capacity (ttpa)'},
        'mothballed-other/unspecified-steel-capacity-(ttpa)': {'display': 'gist-unit-level','label': 'Mothballed other/unspecified steel capacity (ttpa)'},
        'mothballed-pre-retirement-nominal-bf-capacity-(ttpa)':{'display': 'gist-unit-level','label': 'Mothballed pre-retirement BF capacity (ttpa)'},
        'operating-nominal-bf-capacity-(ttpa)': {'display': 'gist-unit-level','label': 'Operating BF capacity (ttpa)'},
        'operating-nominal-bof-steel-capacity-(ttpa)': {'display': 'gist-unit-level','label': 'Operating BOF steel capacity (ttpa)'},
        'operating-nominal-dri-capacity-(ttpa)': {'display': 'gist-unit-level','label': 'Operating DRI capacity (ttpa)'},
        'operating-nominal-eaf-steel-capacity-(ttpa)': {'display': 'gist-unit-level','label': 'Operating EAF steel capacity (ttpa)'},
        'operating-nominal-ohf-steel-capacity-(ttpa)': {'display': 'gist-unit-level','label': 'Operating OHF steel capacity (ttpa)'},
        'operating-other/unspecified-steel-capacity-(ttpa)': {'display': 'gist-unit-level','label': 'Operating other/unspecified steel capacity (ttpa)'},
        'operating-pre-retirement-nominal-bf-capacity-(ttpa)': {'display': 'gist-unit-level','label':'Operating pre-retirement BF capacity (ttpa)'},
        'operating-pre-retirement-nominal-bof-steel-capacity-(ttpa)': {'display': 'gist-unit-level','label': 'Operating pre-retirement BOF steel capacity (ttpa)'},
        'operating-pre-retirement-nominal-dri-capacity-(ttpa)' :{'display': 'gist-unit-level','label':'Operating pre-retirement DRI capacity (ttpa)'},
        'operating-pre-retirement-nominal-eaf-steel-capacity-(ttpa)': {'display': 'gist-unit-level','label': 'Operating pre-retirement EAF steel capacity (ttpa)'},
        'operating-pre-retirement-other/unspecified-steel-capacity-(ttpa)': {'display': 'gist-unit-level','label': 'Operating pre-retirement other/unspecified steel capacity (ttpa)'},
        'retired-nominal-bf-capacity-(ttpa)': {'display': 'gist-unit-level','label': 'Retired BF capacity (ttpa)'},
        'retired-nominal-bof-steel-capacity-(ttpa)': {'display': 'gist-unit-level','label': 'Retired BOF steel capacity (ttpa)'},
        'retired-nominal-eaf-steel-capacity-(ttpa)': {'display': 'gist-unit-level','label': 'Retired EAF steel capacity (ttpa)'},
        'retired-nominal-ohf-steel-capacity-(ttpa)': {'display': 'gist-unit-level','label': 'Retired OHF steel capacity (ttpa)'},

        'subnat': {'display': 'location'},
        'areas': {'display': 'location'}
    },
    /* Mapbox styling applied to all trackers */
    pointPaint: {
        'circle-opacity':.85
    },
    gistUnit: true,
    showToolTip: true,
    /* radius associated with minimum/maximum value on map */
    // minRadius: 3,
    // maxRadius: 7,

    // /* radius to increase min/max to under high zoom */
    // highZoomMinRadius: 5,
    // highZoomMaxRadius: 22,

    // showMaxCapacity: true,
    
}
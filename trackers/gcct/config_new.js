var config = {
    /* name of the data file; use key `csv` if data file is CSV format, use key `geojson` if data file is geoJSON format */
    geojson: 'https://publicgemdata.nyc3.cdn.digitaloceanspaces.com/refactor_testing/gcct_map_2026-01-20.geojson',

    /* Labels for describing the assets */
    assetFullLabel: 'Projects',
    assetLabel: 'projects',

    /* configure the table view, selecting which columns to show, how to label them,
       and designated which column has the link */
    tableHeaders: {
        values: ['name', 'owner', 'status', 'capacity-table', 'start-year', 'plant-type', 'prod-type', 'subnational', 'country-area1'],
        labels: ['Project', 'Owner', 'Status', 'Cement Capacity (mmtpa)', 'Start date', 'Plant type', 'Production type', 'Subnational Unit', 'Country/Area'],
        clickColumns: ['name'],
        rightAlign: ['capacity-table', 'start-year'],
    },

    /* configure the search box; 
       each label has a value with the list of fields to search. Multiple fields might be searched */
    searchFields: {
        'Project': ['name', 'name-noneng', 'name-other', 'name-search'],
        'Companies': ['owner', 'parent', 'owner-noneng', 'owner-gem-id', 'owner-search'],
        'Type ': ['plant-type', 'prod-type', 'color'],
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
        'location-display': {'display': 'location'},

        'plant-type': {'label': 'Plant Type'},
        'prod-type': {'label': 'Production Type'},
        'capacity-display': {'label': 'Cement Capacity (mmtpa)'},
        'clinker-capacity': {'label': 'Clinker Capacity (mmtpa)'},
        'cement-type': {'label': 'Cement Type'},
        'color': {'label': 'Cement Color'},
        'owner': {'label': 'Owner'},
        'start-year': {'label': 'Start Date'},
        'location-accuracy': {'label': 'Coordinate Accuracy'},
    },

    /* ---------------------------- FIELDS TO OVERWRITE FROM site-config.js ---------------------------- */

    color_association: {
        field: 'status',
        values: {
            'announced': 'orange',
            'construction': 'orange',
            'operating': 'green',
            'operating pre-retirement': 'green',
            'cancelled': 'red',
            'retired': 'red',
            'mothballed': 'blue',
            'unknown': 'black',
        },
    },

    filters: [
        {
            field: 'status',
            values: ['announced', 'construction', 'operating', 'operating pre-retirement', 'cancelled', 'retired', 'mothballed', 'unknown'],
            values_labels: ['Announced', 'Construction', 'Operating', 'Operating Pre-Retirement', 'Cancelled', 'Retired', 'Mothballed', 'Not Found'],
            primary: true,
        },
        {
            field: 'plant-type',
            label: 'Plant type',
            values: ['clinker only', 'grinding', 'integrated', 'unknown'],
            values_labels: ['Clinker only', 'Grinding', 'Integrated', 'Not found'],
        },
        {
            field: 'prod-type',
            label: 'Clinker Production Method',
            values: ['dry', 'mixed', 'semidry', 'wet', 'unknown', 'n/a'],
            values_labels: ['Dry', 'Mixed', 'Semi-dry', 'Wet', 'Not found', 'N/A (Grinding Plants)'],
        },
        {
            field: 'color',
            label: 'Cement Color',
            values: ['both', 'grey', 'white', 'unknown'],
            values_labels: ['Grey & White', 'Grey', 'White', 'Not found'],
        },
    ],

    minMaxCapacityFilterLabel: 'millions metric tonnes per annum',
    capacityLabel: 'mmtpa',
    includeCapacityByStatusInDetailView: false,
}
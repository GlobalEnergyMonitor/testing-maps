var config = {
    /* name of the data file; use key `csv` if data file is CSV format, use key `geojson` if data file is geoJSON format */
    geojson: 'https://publicgemdata.nyc3.cdn.digitaloceanspaces.com/refactor_testing/gcpt_map_2026-01-20.geojson',

    /* Labels for describing the assets */
    assetFullLabel: "Coal-fired Units",
    assetLabel: 'units',

    /* configure the table view, selecting which columns to show, how to label them, 
        and designated which column has the link */
    tableHeaders: {
        values: ['name', 'unit-name', 'name-noneng', 'owner', 'parent', 'capacity-table', 'status', 'start-year', 'end-year', 'region', 'country-area1', 'subnational'],
        labels: ['Plant', 'Unit', 'Plant name (local)', 'Owner', 'Parent', 'Capacity (MW)', 'Status', 'Start year', 'Retired year', 'Region', 'Country/Area', 'Subnational unit (province, state)'],
        clickColumns: ['name'],
        rightAlign: ['unit-name', 'capacity-table', 'start-year', 'end-year'],
    },

    /* configure the search box; 
       each label has a value with the list of fields to search. Multiple fields might be searched */
    searchFields: {
        'Plant': ['name', 'name-noneng', 'name-other', 'name-search'],
        'Companies': ['owner', 'parent', 'owner-search', 'parent-search'],
        'Start Year': ['start-year'],
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

        'name-noneng': {'label': 'Local plant name'},
        'owner': {'label': 'Owner'},
        'parent': {'label': 'Parent'},
        'start-year': {'label': 'Start Year'},
        'end-year': {'label': 'Retired Year'},
    },

    /* ---------------------------- FIELDS TO OVERWRITE FROM site-config.js ---------------------------- */

    color_association: {
        field: 'status',
        values: {
            'operating': 'red',
            'construction': 'blue',
            'announced': 'green',
            'permitted': 'green',
            'pre-permit': 'green',
            'retired': 'grey',
            'cancelled': 'grey',
            'mothballed': 'grey',
            'shelved': 'grey',
        },
    },

    filters: [
        {
            field: 'status',
            values: ['operating', 'construction', 'permitted', 'pre-permit', 'announced', 'retired', 'cancelled', 'shelved', 'mothballed'],
        },
    ],

    showMinCapacity: true,
}

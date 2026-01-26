var config = {
    /* name of the data file; use key `csv` if data file is CSV format, use key `geojson` if data file is geoJSON format */
    geojson: 'https://publicgemdata.nyc3.cdn.digitaloceanspaces.com/refactor_testing/gcmt_map_2026-01-21.geojson',

    /* Labels for describing the assets */
    assetFullLabel: 'Coal Mine Projects',
    assetLabel: 'projects',
    
    /* configure the table view, selecting which columns to show, how to label them, 
       and designated which column has the link */
    tableHeaders: {
        values: ['name', 'owner', 'parent', 'capacity-table', 'prod-coal', 'prod-year-coal', 'status', 'workforce', 'coal-field', 'country-area1', 'region', 'start-year'],
        labels: ['Project', 'Owner', 'Parent', 'Capacity (Mtpa)', 'Production (Mtpa)', 'Production year', 'Status', 'Workforce', 'Coal Field', 'Country/Area', 'Region', 'Opening year'],
        clickColumns: ['name'],
        rightAlign: ['capacity-table', 'prod-coal', 'prod-year-coal', 'workforce', 'start-year'],
    },

    /* configure the search box; 
       each label has a value with the list of fields to search. Multiple fields might be searched */
    searchFields: {
        'Project': ['name', 'name-noneng', 'name-search'],
        'Companies': ['owner', 'parent', 'owner-noneng', 'owner-search'],
        'Opening Year': ['start-year'],
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

        'owner': {'label': 'Owner'},
        'parent': {'label': 'Parent'},
        'start-year': {'label': 'Opening Year'},
        'end-year': {'label': 'Closing Year'},
        'workforce': {'label': 'Estimated Workforce'},
        'coal-field': {'label': 'Coal Field'},
        'prod-coal': {'label': 'Production', 'trailing-label': 'Mtpa'},
    },

    /* ---------------------------- FIELDS TO OVERWRITE FROM site-config.js ---------------------------- */

    color_association: {
        field: 'status',
        values: {
            'operating': 'red',
            'proposed': 'blue',
            'cancelled': 'green',
            'retired': 'orange',
            'shelved': 'dark grey',
            'mothballed': 'grey',
        },
    },

    filters: [
        {
            field: 'status',
            values: ['operating', 'proposed', 'cancelled', 'retired', 'shelved', 'mothballed'],
            primary: true
        },
        {
            field: 'mine-type',
            label: 'Mine Type',
            values: ['Surface', 'Underground', 'Underground & Surface', ''],
            values_labels: ['Surface', 'Underground', 'Underground & Surface', 'Not found']

        },
        {
            field: 'coal-grade',
            label: 'Coal Grade',
            values: ['Thermal', 'Met', 'Thermal & Met', ''],
            values_labels: ['Thermal', 'Met', 'Thermal & Met', 'Not found']
        },
    ],

    showMaxCapacity: false,
    capacityLabel: 'Mtpa',
}

var config = {
    /* name of the data file; use key `csv` if data file is CSV format, use key `geojson` if data file is geoJSON format */
    geojson: 'https://publicgemdata.nyc3.cdn.digitaloceanspaces.com/refactor_testing/giomt_map_2026-01-20.geojson',

    /* Labels for describing the assets */
    assetFullLabel: 'Iron Ore assets',
    assetLabel: 'assets',

    /* configure the table view, selecting which columns to show, how to label them, 
       and designated which column has the link */
    tableHeaders: {
        values: ['name', 'name-noneng', 'capacity-table', 'reserves', 'resource', 'status', 'owner', 'parent', 'country-area1'],
        labels: ['Asset name', 'Asset Name (other language)', 'Design Capacity (ttpa)', 'Reserve (thousand tonnes)', 'Resource (thousand tonnes)', 'Status', 'Owner', 'Parent', 'Country/Area(s)'],
        clickColumns: ['name'],
        rightAlign: ['capacity-table', 'reserves', 'resource'],
    },

    /* configure the search box; 
       each label has a value with the list of fields to search. Multiple fields might be searched */
    searchFields: {
        'Asset name': ['name', 'noneng-name', 'name-search'],
        'Companies': ['owner', 'parent', 'parent-gem-id', 'owner-noneng', 'owner-gem-id', 'owner-search', 'parent-search'],
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

        'capacity-display': {'label': 'Design Capacity (ttpa)'},
        'reserves': {'label': 'Reserves (thousand tonnes)'},
        'resource': {'label': 'Resources (thousand tonnes)'},
        'owner': {'label': 'Owner'},
        'parent': {'label': 'Parent'},
        'location-accuracy': {'label': 'Location Accuracy'},
    },

    /* ---------------------------- FIELDS TO OVERWRITE FROM site-config.js ---------------------------- */

    color_association: {
        field: 'status',
        values: {
            'operating': 'red',
            'proposed': 'green',
            'retired': 'blue',
            'unknown': 'grey',
            'cancelled': 'black',
            'shelved': 'black',
            'mothballed': 'orange',
        },
    },

    filters: [
        {
            field: 'status',
            values: ['operating', 'proposed', 'mothballed', 'retired', 'cancelled', 'shelved', 'unknown'],
        },
    ],

    minRadius: 3,
    maxRadius: 15,
    minMaxCapacityFilterLabel: 'Design Capacity (TTPA)',
    capacityLabel: 'TTPA',
    includeCapacityByStatusInDetailView: false,
}

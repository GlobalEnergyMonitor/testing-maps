var config = {
    /* name of the data file; use key `csv` if data file is CSV format, use key `geojson` if data file is geoJSON format */
    geojson: 'https://publicgemdata.nyc3.cdn.digitaloceanspaces.com/refactor_testing/gwpt_map_2026-01-20.geojson',

    /* Labels for describing the assets */
    assetFullLabel: "Wind farm phases",
    assetLabel: 'phase',

    /* configure the table view, selecting which columns to show, how to label them, 
       and designated which column has the link */
    tableHeaders: {
        values: ['name', 'unit-name', 'capacity-table', 'tech-type', 'status', 'start-year', 'owner', 'operator', 'subnational', 'country-area1'],
        labels: ['Project', 'Phase', 'Capacity (MW)',' Installation Type', 'Status', 'Start year', 'Owner', 'Operator', 'State/Province', 'Country/Area'],
        clickColumns: ['name'],
        rightAlign: ['capacity-table', 'start-year'],
    },

    /* configure the search box; 
       each label has a value with the list of fields to search. Multiple fields might be searched */
    searchFields: {
        'Project': ['name', 'name-noneng', 'name-other', 'name-search'],
        'Companies': ['owner', 'operator', 'owner-noneng', 'operator-noneng', 'owner-search'],
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

        'name-noneng': {'label': 'Project in Local Language / Script'},
        'owner': {'label': 'Owner'},
        'operator': {'label': 'Operator'},
        'start-year': {'label': 'Start Year'},
        'tech-type': {'label': 'Installation Type'},
        'location-accuracy': {'label': 'Location Accuracy'},
    },

    /* ---------------------------- FIELDS TO OVERWRITE FROM site-config.js ---------------------------- */

    /* define the column and associated values for color application */
    color_association: {
        field: 'status',
        values: {
            'operating': 'green',
            'construction': 'yellow',
            'pre-construction': 'orange',
            'announced': 'red',
            'mothballed': 'blue',
            'shelved': 'blue',  // not light blue
            'retired': 'grey',
            'cancelled': 'grey',  // not light grey
        },
    },

    filters: [
        {
            field: 'status',
            values: ['operating', 'announced', 'construction', 'pre-construction', 'mothballed', 'shelved', 'cancelled', 'retired'],
            values_labels: ['operating', 'announced', 'construction', 'pre-construction', 'mothballed', 'shelved',  'cancelled', 'retired'],
            primary: true
        },
        {
            field: 'tech-type',
            label: 'Installation Type',
            values: ['Onshore', 'Offshore hard mount', 'Unknown', 'Offshore mount unknown', 'Offshore floating'],
        },
    ],
}

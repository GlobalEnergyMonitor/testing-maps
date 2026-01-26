var config = {
    /* name of the data file; use key `csv` if data file is CSV format, use key `geojson` if data file is geoJSON format */
    geojson: 'https://publicgemdata.nyc3.cdn.digitaloceanspaces.com/GOIT/2025-03/goit_2025-04-09.geojson',

    /* Labels for describing the assets */
    assetFullLabel: 'Pipelines',
    assetLabel: 'segments',

    /* configure the table view, selecting which columns to show, how to label them, 
       and designated which column has the link */
    tableHeaders: {
        values: ['name', 'owner', 'parent', 'status', 'areas', 'subnational', 'capacity-display', 'units-of-m', 'start-year'],
        labels: ['Name', 'Owner','Parent', 'Status','Country/Area(s)','Subnational unit (province/state)', 'Capacity', '', 'Start Year'],
        clickColumns: ['name'],
        rightAlign: ['name', 'start-year', 'capacity'],
        toLocaleString: ['capacity'],
    },

    /* configure the search box; 
       each label has a value with the list of fields to search. Multiple fields might be searched */
    searchFields: {
        'Pipeline': ['name', 'name-search'],
        'Companies': ['owner', 'operator', 'parent', 'owner-search'],
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
        'owner': {'label': 'Owner'},
        'parent': {'label': 'Parent'},
        'start-year': {'label': 'Start Year'},
        'location-display': {'display': 'location'},
    },

    /* ---------------------------- FIELDS TO OVERWRITE FROM site-config.js ---------------------------- */

    site_colors: {  // TODO could these be standardized and added to site-config.js?
        'red': '#c74a48',
        'blue': '#5c62cf',
        'green': '#4c9d4f',
        'grey': '#8f8f8e',
        'black': '#000000',
    },
    color_association: {
        field: 'status-group',
        values: {
            'operating': 'red',
            'construction-plus': 'blue',
            'proposed-plus': 'blue',
            'mothballed-plus': 'green',
            'cancelled': 'green',
            'retired-plus': 'grey',
            'shelved': 'grey',
        },
    },

    filters: [
        {
            field: 'status-group',
            values: ['operating', 'proposed-plus', 'construction-plus', 'mothballed-plus', 'cancelled', 'retired-plus', 'shelved' ],
            values_labels: ['Operating', 'Proposed', 'Construction', 'Mothballed', 'Cancelled', 'Retired', 'Shelved'],
        },
        {
            field: 'Fuel',
            values: ['Oil', 'NGL'],
            values_labels: ['Oil', 'NGL'],
            filterFunction: (value, selectedValue) => {
                // Check if the value contains the selectedValue (Oil or NGL)
                return value.includes(selectedValue);
            }
        },
    ],

    capacityLabel: 'BOEd',
    showMaxCapacity: false,
    multiCountry: true,

    linkField: 'url',
    geometries: ['LineString'],
}

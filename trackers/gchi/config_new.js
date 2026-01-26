var config = {
    /* name of the data file; use key `csv` if data file is CSV format, use key `geojson` if data file is geoJSON format */
    geojson: 'https://publicgemdata.nyc3.cdn.digitaloceanspaces.com/refactor_testing/gchi_map_2026-01-20.geojson',

    /* Labels for describing the assets */
    assetFullLabel: 'Projects',
    assetLabel: 'projects',

    /* configure the table view, selecting which columns to show, how to label them,
       and designated which column has the link */
    tableHeaders: {
        values: ['name', 'owner', 'product-primary', 'feedstock', 'product-secondary', 'subnational', 'country-area1'],
        labels: ['Project', 'Owner', 'Primary Product', 'Feedstock', 'Secondary Product', 'Subnational Unit', 'Country/Area'],
        clickColumns: ['name'],
        rightAlign: [],
    },

    /* configure the search box; 
       each label has a value with the list of fields to search. Multiple fields might be searched */
    searchFields: {
        'Project': ['name', 'name-noneng', 'name-search'],
        'Companies': ['owner', 'owner-noneng', 'owner-gem-id', 'owner-search'],
        'Primary Products': ['product-primary'],
        'Feedstock': ['feedstock'],
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
        'product-primary': {'label': 'Primary Products'},
        'product-secondary': {'label': 'Secondary Products'},
        'feedstock': {'label': 'Feedstock'},
        'feedstock-accuracy': {'label': 'Feedstock Accuracy'},
    },

    /* ---------------------------- FIELDS TO OVERWRITE FROM site-config.js ---------------------------- */

    filters: [
        {
            field: 'status',
            values: ['operating'],
        },
    ],

    minRadius: 4,
    highZoomMinRadius: 6,

    showMaxCapacity: false,
    includeCapacityByStatusInDetailView: false,
}

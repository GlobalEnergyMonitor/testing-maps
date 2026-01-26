var config = {
    /* name of the data file; use key `csv` if data file is CSV format, use key `geojson` if data file is geoJSON format */
    geojson: 'https://publicgemdata.nyc3.cdn.digitaloceanspaces.com/refactor_testing/gnpt_map_2026-01-20.geojson',

    /* Labels for describing the assets */
    assetFullLabel: "Nuclear Power Plant Units",
    assetLabel: 'units',

    /* configure the table view, selecting which columns to show, how to label them, 
       and designated which column has the link */
    tableHeaders: {
        values: ['name', 'unit-name', 'capacity-table', 'reactor-type', 'model', 'status', 'owner', 'operator', 'subnational', 'country-area1'],
        labels: ['Project name', 'Unit name', 'Capacity (MW)', 'Reactor', 'Model', 'Status', 'Owner', 'Operator', 'Subnational area', 'Country/Area(s)'],
        clickColumns: ['name'],
        rightAlign: ['capacity-table'],
    },

    /* configure the search box; 
       each label has a value with the list of fields to search. Multiple fields might be searched */
    searchFields: {
        'Project': ['name', 'name-noneng', 'name-search'],
        'Companies': ['owner', 'operator', 'owner-noneng', 'owner-search'],
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

        'reactor-type': {'label': 'Reactor'},
        'model': {'label': 'Model'},
        'owner': {'label': 'Owner'},
        'operator': {'label': 'Operator'},
        'location-accuracy': {'label': 'Location Accuracy'},
    },

    /* ---------------------------- FIELDS TO OVERWRITE FROM site-config.js ---------------------------- */

}

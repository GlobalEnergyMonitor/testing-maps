var config = {
    /* name of the data file; use key `csv` if data file is CSV format, use key `geojson` if data file is geoJSON format */
    geojson: 'https://publicgemdata.nyc3.cdn.digitaloceanspaces.com/refactor_testing/goget_map_2026-01-20.geojson',

    /* Labels for describing the assets */
    assetFullLabel: 'Oil & Gas Extraction Areas',
    assetLabel: 'areas',

    /* configure the table view, selecting which columns to show, how to label them, 
       and designated which column has the link */
    tableHeaders: {
        values: ['name', 'operator', 'status-display', 'country-area1', 'subnational', 'prod-oil', 'prod-gas', 'prod-year-oil', 'prod-year-gas', 'start-year'],
        labels: ['Extraction Area', 'Operator', 'Status', 'Country/Area(s)', 'Subnational unit (province/state)', 'Production - Oil (Million bbl/y)', 'Production - Gas (Million m³/y)', 'Production Year - Oil', 'Production Year - Gas', 'Production start year'],
        clickColumns: ['name'],
        rightAlign: ['prod-oil', 'prod-gas', 'prod-year-oil', 'prod-year-gas', 'start-year'],
    },

    /* configure the search box; 
       each label has a value with the list of fields to search. Multiple fields might be searched */
    searchFields: {
        'Extraction Area': ['name', 'name-search'],
        'Companies': ['owner', 'operator', 'parent', 'owner-search'],
        'Discovery Year': ['discovery-year'],
        'Production start year': ['start-year'],
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

        'location-accuracy': {'label': 'Location Accuracy'},
        'operator': {'label': 'Operator'},
        'discovery-year': {'label': 'Discovery Year'},
        'fid-year': {'label': 'FID Year'},
        'start-year': {'label': 'Production Start Year'},
        'prod-year-oil': {'label': 'Production Year - Oil'},
        'prod-oil': {'label': 'Production - Oil (Million bbl/y)'},
        'prod-year-gas': {'label': 'Production Year - Gas'},
        'prod-gas': {'label': 'Production - Gas (Million m³/y)'},
    },

    /* ---------------------------- FIELDS TO OVERWRITE FROM site-config.js ---------------------------- */

    color_association: {
        field: 'status',
        values: {
            'operating': 'red',
            'in development': 'blue',
            'discovered': 'blue',
            'shut in': 'green',
            'decommissioned': 'green',
            'cancelled': 'green',
            'abandoned': 'grey',
            'ugs': 'grey',
            'not found': 'black'
        }
    },

    filters: [
        {
            field: 'status',
            values: ['operating', 'in development', 'discovered', 'shut in', 'decommissioned', 'cancelled', 'abandoned', 'ugs', 'not found'],
            values_labels: ['Operating', 'In development', 'Discovered', 'Shut in', 'Decommissioned', 'Cancelled', 'Abandoned', 'UGS', 'Not found'],
        },
    ],

    countryFile: '../../trackers/goget/countries.json',
    showMaxCapacity: false,
    capacityLabel: 'million boe/y',
    includeCapacityByStatusInDetailView: false,
}

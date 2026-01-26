var config = {
    /* name of the data file; use key `csv` if data file is CSV format, use key `geojson` if data file is geoJSON format */
    geojson: 'https://publicgemdata.nyc3.cdn.digitaloceanspaces.com/ggit/2025-11/ggit_map_2025-11-25.geojson',

    /* Labels for describing the assets */
    assetFullLabel: 'Gas Infrastructure projects',
    assetLabel: 'projects',

    /* configure the table view, selecting which columns to show, how to label them,
       and designated which column has the link */
    tableHeaders: {
        values: ['name', 'unit-name', 'owner', 'parent', 'capacity-table', 'units-of-m', 'status', 'region', 'areas', 'subnational', 'start-year', 'tracker-display'],
        labels: ['Project', 'Unit', 'Owner', 'Parent', 'Capacity', '', 'Status', 'Region', 'Country/Area(s)', 'Subnational unit (province/state)', 'Start year', 'Type'],
        clickColumns: ['name'],
        rightAlign: ['unit-name', 'capacity-table', 'start-year'],
        toLocaleString: ['capacity-table'],
    },

    /* configure the search box;
       each label has a value with the list of fields to search. Multiple fields might be searched */
    searchFields: {
        'Infrastructure Type': ['tracker-custom'],
        'Project': ['name', 'name-search'],
        'Companies': ['owner', 'parent', 'owner-search'],
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
        'unit-name': {'label': 'Unit/Segment'},
        'owner': {'label': 'Owner'},
        'parent': {'label': 'Parent'},
        'start-year': {'label': 'Start Year'},
        'tracker-display': {'label': 'Type'},
        'location-display': {'display': 'location'},
    },
    
    /* ---------------------------- FIELDS TO OVERWRITE FROM site-config.js ---------------------------- */

    color_association: {
        field: 'status-group',
        values: {
            'operating': 'red',
            'proposed-plus': 'green',
            'construction-plus': 'blue',
            'retired-plus': 'grey',
            'cancelled': 'grey',
            'shelved': 'grey',
            'mothballed-plus': 'grey',
            'announced': 'green',
        },
    },

    filters: [
        {
            field: 'status-legend',
            label: 'Status',
            values: ['operating','proposed-plus','construction-plus','retired-plus','cancelled','mothballed-plus','shelved'],
            values_labels: ['Operating','Proposed/Announced/Discovered', 'Construction/In development','Retired/Closed/Decommissioned','Cancelled','Mothballed/Idle/Shut in','Shelved']

        },
        {
            field: 'tracker-custom',
            label: 'Infrastructure Type',
            values: ['GGIT-import', 'GGIT-export', 'GGIT'],  // cannot have any spaces in the values!
            values_labels: ['LNG Terminals (Import)', 'LNG Terminals (Export)', 'Gas Pipelines']
        }
    ],

    multiCountry: true,

    minLineWidth: 1,
    maxLineWidth: 4,
    highZoomMinLineWidth: 2,
    highZoomMaxLineWidth: 5,

    minRadius: 3,
    highZoomMinRadius: 5,
    highZoomMaxRadius: 30,

    showMaxCapacity: false,
    capacityField: 'capacity-scaled',
    capacityLabel: {
        field: 'tracker-custom',
        values: {
            'GGIT': 'bcm/y of gas',
            'GGIT-import': 'MTPA of natural gas',
            'GGIT-export': 'MTPA of natural gas',
        },
    },

    geometries: ['Point','LineString'],
}
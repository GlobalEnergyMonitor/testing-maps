var config = {
    /* name of the data file; use key `csv` if data file is CSV format, use key `geojson` if data file is geoJSON format */
    geojson: 'https://publicgemdata.nyc3.cdn.digitaloceanspaces.com/refactor_testing/gist_map_2026-01-22.geojson',

    /* Labels for describing the assets */
    assetFullLabel: 'Iron and Steel Plants',
    assetLabel: 'plants',


    /* configure the table view, selecting which columns to show, how to label them, 
       and designated which column has the link */
    tableHeaders: {
        values: ['name', 'owner', 'parent', 'status-display', 'start-year', 'prod-type', 'tech-type', 'subnational', 'country-area1'],
        labels: ['Plant', 'Owner', 'Parent', 'Plant Status', 'Start date', 'Production Method', 'Main Production Equipment', 'Subnational Unit', 'Country/Area'],
        clickColumns: ['name'],
        rightAlign: ['start-year'],
    },

    /* configure the search box; 
       each label has a value with the list of fields to search. Multiple fields might be searched */
    searchFields: {
        'Plant': ['name', 'name-noneng', 'name-search'],
        'Companies': ['owner', 'parent', 'owner-noneng', 'parent-gem-id', 'owner-gem-id', 'owner-search'],
        'Production Method': ['prod-type'],
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

        'prod-method-tier-display': {'label': 'Production Method'},
        'parent': {'label': 'Parent'},
        'owner': {'label': 'Owner'},
        'start-year': {'label': 'Start date'},
        'location-accuracy': {'label': 'Coordinate Accuracy'},

        'capacity-by-status': {'table': 'Capacity by Status', 'tableHeaders': {'status': 'Unit status', 'method': 'Main production equipment', 'capacity': 'Capacity (ttpa)'}},
    },

    /* ---------------------------- FIELDS TO OVERWRITE FROM site-config.js ---------------------------- */

    color_association: {
        field: 'prod-type',
        values: {
            'Electric': 'light green',
            'Electric, oxygen': 'blue',
            'Oxygen': 'orange',
            'Ironmaking (BF)': 'light red',
            'Ironmaking (DRI)': 'light blue',
            'Integrated (BF)': 'red',
            'Integrated (BF & DRI)':  'purple',
            'Integrated (DRI)': 'green',
            'Integrated (unknown)': 'grey',
            'Steel other/unspecified': 'light grey',
            'Iron other/unspecified': 'light grey',
        },
    },

    filters: [
        {
            field: 'prod-type',
            label: 'Production method',
            values: ['Electric', 'Electric, oxygen', 'Oxygen', 'Ironmaking (BF)', 'Integrated (BF & DRI)', 'Ironmaking (DRI)', 'Integrated (DRI)', 'Integrated (BF)', 'Integrated (unknown)', 'Steel other/unspecified', 'Iron other/unspecified'],
            primary: true,
            field_hover_text: 'For full descriptions of steelmaking route categories, see the <a href="https://globalenergymonitor.org/projects/global-iron-and-steel-tracker/frequently-asked-questions/"> FAQs</a>.',
        },
        {
            field: 'status',
            label: 'Plant status',
            values: ['announced', 'cancelled', 'construction', 'mothballed', 'operating', 'operating pre-retirement', 'retired'], //'mothballed-pre-retirement',
            field_hover_text: 'Status reflects the plant-level status. Some capacities (e.g., announced expansions at a plant that already operates capacity) may not appear under their specific category if the overall plant status is different.',
        },
    ],

    capacityLabel: 'ttpa',
    includeCapacityByStatusInDetailView: false,  // create table instead since input file does not have individual units
    useDefaultCapacityInDetailView: false,
    showToolTip: true,
}
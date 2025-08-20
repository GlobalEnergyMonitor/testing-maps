var config = {
    /* name of the data file; use key `csv` if data file is CSV format */
    geometries: ['Point'],
    geojson: 'https://publicgemdata.nyc3.cdn.digitaloceanspaces.com/giomt/2025-08/giomt_map_2025-08-15.geojson',
    /* zoom level to set map when viewing all phases */
    phasesZoom: 10,
    /* initial load zoom multiplier */
    // zoomFactor: 2,
    center: [0, 0],
    colors: {
        'red': '#c74a48',
        'blue': '#5c62cf',
        'green': '#4c9d4f',
        'grey': '#8f8f8e',
        'orange greeninfo': '#fd7e14',
        'black': '#000000'
    },

    // /* define the column and associated values for color application */
    // color: {
    //     field: 'status',
    //     values: {
    //         'operating': 'green greeninfo',
    //         'construction': 'yellow greeninfo',
    //         'pre-construction': 'orange greeninfo',
    //         'announced': 'red greeninfo',
    //         'mothballed': 'blue greeninfo',
    //         'shelved': 'light blue greeninfo',
    //         'retired': 'grey greeninfo',
    //         'cancelled': 'light grey greeninfo',
    //     }
    // },
    color: {
        field: 'status',
        values: {
            'operating': 'red',
            'proposed': 'green',
            'retired': 'blue',
            'unknown': 'grey',
            'cancelled': 'black',
            'shelved': 'black',
            'mothballed': 'orange greeninfo',
        }
    },


    /* define the column and values used for the filter UI. There can be multiple filters listed. 
      Additionally a custom `label` can be defined (default is the field), 
      and `values-label` (an array matching elements in `values`)
      */
    filters: [
    {
        field: 'status',
        label: 'Operating Status',
        values: ['operating','proposed','mothballed','retired','cancelled','shelved', 'unknown'],
        values_labels: ['Operating','Proposed','Mothballed', 'Retired','Cancelled','Shelved', 'Unknown']

    },
    ],
    linkField: 'pid',
    /* define the field for calculating and showing capacity along with label.
       this is defined per tracker since it varies widely */
    capacityField: 'capacity',
    capacityDisplayField: 'capacity-table',
    capacityLabel: '',

    // lat: 'Latitude',
    // lng: 'Longitude',

    /* Labels for describing the assets */
    assetFullLabel: "Iron Ore assets",
    assetLabel: 'assets',

    /* the column that contains the asset name. this varies between trackers */
    nameField: 'name',

    countryField: 'areas',
    /* configure the table view, selecting which columns to show, how to label them, 
        and designated which column has the link */

    // TODO make it so all string showing capacity type value is to locale string with commas currently Total reserves for giomt is string but no commas
    // maybe change it in site.js file

    tableHeaders: {
        values: ['name', 'noneng-name','capacity', 'total-reserves-(proven-and-probable', 'total-resource-(inferred','status', 'owner', 'parent', 'areas'],
        labels: ['Asset name', 'Asset Name (other language)','Design Capacity (ttpa)','Reserve (thousand tonnes)', 'Resource (thousand tonnes)','Status','Owner', 'Parent', 'Country/Area(s)'],
        clickColumns: ['name'],
        rightAlign: ['capacity', 'total-reserves-(proven-and-probable', 'total-resource-(inferred'],
        toLocaleString: [''],
        removeLastComma: ["areas"]
        
    },

    /* configure the search box; 
        each label has a value with the list of fields to search. Multiple fields might be searched */
    searchFields: { 'Asset name': ['name', 'noneng-name', 'name-search'], 
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
        'capacity-details': {'label': 'Design Capacity (ttpa)'},
        'areas-subnat-sat-display': {'display': 'location'},
        'total-reserves-(proven-and-probable': {'label': 'Reserves (thousand tonnes)'},
        'total-resource-(inferred': {'label': 'Resources (thousand tonnes)'},
        'owner': {'label': 'Owner'},
        'parent': {'label': 'Parent'},
        'coordinate-accuracy': {'label': 'Location Accuracy'},


        // 'areas-subnat-sat-display': {'display': 'location'}

    },
    showCapacityTable: false,
    showMaxCapacity: true,
    maxCapacityLabel: 'Design Capacity (TTPA)',

    /* radius associated with minimum/maximum value on map */
    minRadius: 3,
    maxRadius: 15,

}

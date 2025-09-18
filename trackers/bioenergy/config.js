var config = {
    /* name of the data file; use key `csv` if data file is CSV format */
    // csv: 'data.csv',

    geojson: 'https://publicgemdata.nyc3.cdn.digitaloceanspaces.com/GBPT/2025-09/bioenergy_map_2025-09-18.geojson',

    /* zoom level to set map when viewing all phases */
    phasesZoom: 10,
    /* initial load zoom multiplier */
    // zoomFactor: 2,
    center: [0, 0],
    countryField: 'areas',
    /* define column names to pull data from */
    linkField: 'pid',

    urlField: 'url',

    color: {
        field: 'status',
        values: {
            'operating': 'red',
            'pre-construction': 'green',
            'construction': 'blue',
            'retired': 'grey',
            'cancelled': 'grey',
            'shelved': 'grey',
            'mothballed': 'grey',
            'announced': 'green'
        }
    },


    /* define the column and values used for the filter UI. There can be multiple filters listed. 
      Additionally a custom `label` can be defined (default is the field), 
      and `values-label` (an array matching elements in `values`)
      */
    filters: [
        {
            field: 'status',
            values: ['operating','construction','pre-construction', 'announced','shelved','mothballed','retired','cancelled'],
        }
    ],

    /* define the field for calculating and showing capacity along with label.
       this is defined per tracker since it varies widely */
    capacityField: 'capacity',
    capacityDisplayField: 'capacity',
    capacityLabel: 'Capacity (MW)',

    /* Labels for describing the assets */
    assetFullLabel: "Bioenergy Power Units",
    assetLabel: 'units',

    /* the column that contains the asset name. this varies between trackers */
    nameField: 'name',


    /* configure the table view, selecting which columns to show, how to label them, 
        and designated which column has the link */
    tableHeaders: {
        values: ['name', 'capacity', 'status', 'owner', 'areas', 'Fuel'],
        labels: ['Project name','Capacity (MW)','Status','Owner', 'Country/Area(s)','Fuel',],
        clickColumns: ['name'],
        rightAlign: ['capacity'],
        toLocaleString: ['capacity'],
        removeLastComma: ['areas'],
        makeCase: ['name', 'status', 'owner', 'areas']
    },

    /* configure the search box; 
        each label has a value with the list of fields to search. Multiple fields might be searched */
    searchFields: { 'Project': ['name'], 
        'Companies': ['owner-search', 'owner'],
        'Status': ['status'], 

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
        // 'status': {'label': 'Status'}, # handled in summary of capacity and status section
        // 'capacity': {'label': 'Capacity (MW)'},
        'owner': {'label': 'Owner'},
        'operator': {'label': 'Operator'},
        'location-accuracy': {'label': 'Location Accuracy'},
        // 'state/province': {'display': 'location'},
        // 'country': {'display': 'location'},
        'areas-subnat-sat-display': {'display': 'location'}


    },
    showCapacityTable: true, 
}

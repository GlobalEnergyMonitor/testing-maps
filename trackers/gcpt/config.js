var config = {
    /* name of the data file; use key `csv` if data file is CSV format */
    geojson: 'https://publicgemdata.nyc3.cdn.digitaloceanspaces.com/gcpt/2025-07/gcpt_map_2025-07-23.geojson',
    /* define the column and associated values for color application */
    color: {
        field: 'status',
        values: {
            'operating': 'red',
            'construction': 'blue',
            'announced': 'green',
            'permitted': 'green',
            'pre-permit': 'green',
            'retired': 'grey',
            'cancelled': 'grey',
            'mothballed': 'grey',
            'shelved': 'grey'
        }
    },
    /* define the column and values used for the filter UI. There can be multiple filters listed. 
      Additionally a custom `label` can be defined (default is the field), 
      and `values_label` (an array matching elements in `values`)
      */
    filters: [
        {
            field: 'status',
            values: ['operating','construction','permitted','pre-permit', 'announced','retired','cancelled', 'shelved','mothballed'],
        }
    ],
    linkField: 'pid',

    /* define the field for calculating and showing capacity along with label.
       this is defined per tracker since it varies widely */
    capacityField: 'scaling-capacity',
    capacityDisplayField: 'capacity-table',
    capacityLabel: '(MW)',

    /* Labels for describing the assets */
    assetFullLabel: "Coal-fired Units",
    assetLabel: 'units',

    /* the column that contains the asset name. this varies between trackers */
    nameField: 'name',
    countryField: 'areas',

    /* configure the table view, selecting which columns to show, how to label them, 
        and designated which column has the link */
    tableHeaders: {
        values: ['name','unit-name','noneng-name','owner', 'parent', 'capacity-table', 'status', 'start-year', 'retired-year', 'region', 'areas', 'subnat'],
        labels: ['Plant','Unit','Plant name (local)','Owner','Parent','Capacity (MW)','Status','Start year', 'Retired year','Region','Country/Area','Subnational unit (province, state)'],
        clickColumns: ['name'],
        rightAlign: ['unit-name','capacity-table','start-year','retired-year'],
        toLocaleString: ['capacity-table'],
        removeLastComma: ["areas"]

    },
    // interpolate: ["cubic-bezier", 0, 0, 0, 1],

    /* configure the search box; 
        each label has a value with the list of fields to search. Multiple fields might be searched */
    searchFields: { 'Plant': ['name', 'name-search', 'noneng-name', 'other_name'], 
        'Companies': ['owner', 'parent', 'owner-search', 'plant-search'],
        'Start Year': ['start-year']
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
        'noneng-name': {'label': 'Local plant name'},
        'owner': {'label': 'Owner'},
        'parent': {'label': 'Parent'},
        'start-year': {'label': 'Start Year'},
        'retired-year': {'label': 'Retired Year'},
        'areas-subnat-sat-display': {'display': 'location'},
    },



    // /* radius associated with minimum/maximum value on map */
    // minRadius: 2,
    // maxRadius: 10,
    // minLineWidth: 1,
    // maxLineWidth: 10,

    // /* radius to increase min/max to under high zoom */
    // highZoomMinRadius: 4,
    // highZoomMaxRadius: 32,
    // highZoomMinLineWidth: 4,
    // highZoomMaxLineWidth: 32,

    /* radius associated with minimum/maximum value on map */
    // minRadius: .8,
    // maxRadius: 10,
    // // /* radius to increase min/max to under high zoom */
    // highZoomMinRadius: 4,
    // highZoomMaxRadius: 32,

    // showAllPhases: true,
    showMinCapacity: true
}

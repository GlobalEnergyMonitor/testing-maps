var config = {
    // geojson: 'compilation_output/gchi_map_2025-11-10.geojson',
    geojson:  'https://publicgemdata.nyc3.cdn.digitaloceanspaces.com/GChI/2025-11/gchi_map_2025-11-10.geojson',// 'https://publicgemdata.nyc3.cdn.digitaloceanspaces.com/mapfiles/gcct_map_2025-06-18.geojson', // Saying can't be found? TODO march 24th

    
    color: { 
        field: 'status', // prod type
        values: {
            'operating': 'green', 
            // 'Central and South America': 'green',
            // 'Asia Pacific': 'green', 
            // 'Europe': 'green',
            // 'Eurasia': 'green',
            // 'Middle East': 'green',
            // 'North America': 'green',

        }
    },
        filters: [
        {
            field: 'status',
            label: 'Status',
            values: ['operating'],
            values_labels: ['Operating'],

            primary: true
        },
    ],


    linkField: 'pid',
    urlField: 'url',
    statusField: 'status-legend',
    statusDisplayField: 'status',
    countryField: 'areas',
    capacityField: 'capacity', // change to scaling col once added
    // capacityDisplayField: 'capacity',

    capacityLabel: '',  //(millions metric tonnes per annum)



    /* Labels for describing the assets */
    assetFullLabel: "Projects",
    assetLabel: 'projects',

    /* the column that contains the asset name. this varies between trackers */
    nameField: 'name',
    /* configure the table view, selecting which columns to show, how to label them,
        and designated which column has the link */
    tableHeaders: {
        values: ['name','owner', 'primprod', 'feedstock', 'secprod', 'subnat','areas'],
        labels: ['Project','Owner', 'Primary Product', 'Feedstock','Secondary Product','Subnational Unit','Country/Area'],
        clickColumns: ['name'],
        rightAlign: [],
        removeLastComma: ['areas'], 
        toLocaleString: [], 

    },
    /* configure the search box; 
        each label has a value with the list of fields to search. Multiple fields might be searched */
    searchFields: { 'Project': ['name', 'noneng-name'], 
        'Companies': ['owner',  'owners-noneng', 'owner-gem-id'],
        'Primary Products': ['primprod'],
        'Feedstock': ['feedstock']
    },

    /* define fields and how they are displayed. 
        `'display': 'heading'` displays the field in large type
        `'display': 'range'` will show the minimum and maximum values.
        `'display': 'join'` will join together values with a comma separator
        `'display': 'location'` will show the fields over the detail image
        `'label': '...'` prepends a label. If a range, two values for singular and plural.
    */
   
    detailView: {
        // ned to add cement type but unsure what that is in the data
        'name': {'display': 'heading'},
        'owner': {'label': 'Owner'},
        'primprod': {'label': 'Primary Products'},
        'secprod': {'label': 'Secondary Products'},

        'feedstock': {'label': 'Feedstock'},
        'feedacc': {'label': 'Feedstock Accuracy'},

        'subnat': {'display': 'location'},
        'areas': {'display': 'location'}
    },


    minRadius: 4,
    maxRadius: 10,
    highZoomMinRadius: 6,
    highZoomMaxRadius: 32,

    showMaxCapacity: false,
    
}

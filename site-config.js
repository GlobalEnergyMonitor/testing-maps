var site_config = {
    /* Mapbox Access Token */
    accessToken: 'pk.eyJ1IjoiZ2VtdGVhbTEiLCJhIjoiY21la2ozNjdoMDZkbDJzb2xiMms1c3VqeiJ9._Yv1a0HZIELTZjYjFStV0A',
    /* Mapbox Base Map Style */
    mapStyle: 'mapbox://styles/gemteam1/cls98k6sf02li01p2fqtu67lc',
    center: [0, 0],
    projection: 'naturalEarth',
    baseMap: 'Streets',
    icons: [],

    /* Zoom level that asset detail cards open at; this is a good one to override in tracker config,
       depending on scale of facilities */
    img_detail_zoom: 15,

    /* Define labels for sitewide colors, referenced in tracker config */
    site_colors: {
        'red': '#c74a48',
            'light red': '#f28b82',
        'orange': '#fd7e14',
        'yellow': '#f3ff00',
        'green': '#4c9d4f',
            'light green': '#66c26e',
        'blue': '#5c62cf',
            'light blue': '#74add1',
        'purple': '#9370db',
        'grey': '#8f8f8e',
            'light grey': '#e0e0e0',
            'dark grey': '#4b4b4b',
        'black': '#000000',
    },

    /* define the column and associated values for color application */
    color_association: {
        field: 'status',
        values: {
            'operating': 'green',
            'construction': 'yellow',
            'pre-construction': 'orange',
            'announced': 'red',
            'mothballed': 'blue',
            'shelved': 'light blue',
            'retired': 'grey',
            'cancelled': 'light grey',
        },
    },

    /* Mapbox styling applied to all trackers */
    pointPaint: {
        'circle-opacity': 0.85
    },
    linePaint: {
        'line-opacity': 0.85
    },
    lineLayout: {
        'line-cap': 'round', 
        'line-join': 'round'
    },

    /* radius associated with minimum/maximum value on map */
    /* Defined by pixels and be 1- infinity, 0 is invisible */
    minRadius: 1,
    maxRadius: 10,
    minLineWidth: 0.5,
    maxLineWidth: 7,
    
    /* radius to increase min/max to under high zoom */
    /* In  mapbox there are 22 zoom levels, higher zoom usually meaning samller area "closer in"*/
    highZoomMinRadius: 4,
    highZoomMaxRadius: 32,
    highZoomMinLineWidth: 0.5,
    highZoomMaxLineWidth: 7,
    
    /* define column names to pull data from */
    nameField: 'name',
    linkField: 'project-id',
    urlField: 'url',
    countryField: 'country-area1',
    statusField: 'status',
    statusDisplayField: 'status-display',
    capacityField: 'capacity',  // the literal, reported, numerical capacity. If originally blank or non-numeric string, is 0 now. Used to calculate plant/project capacity total.
    capacityScaledField: 'capacity-scaled',  // the capacity value used to scale the circle/dot on the map (often the same as capacity)
    capacityDisplayField: 'capacity-display', // this is what gets used in the details summary unit feature & in the table view where applicable.
    capacityLabel: 'MW',  // future todo: use input file "unit of m" field instead of hard-coded
    locationColumns:{
        lat: 'Latitude',
        long: 'Longitude'
    },

    /* by default, no all phases link; override in tracker config where appropriate */
    showAllPhases: false,
    showMaxCapacity: true,
    showMinCapacity: false,
    minMaxCapacityFilterLabel: 'Capacity (MW)',
    includeCapacityByStatusInDetailView: true,
    // showCapacityTable: true,

    /* zoom level to set map when viewing all phases */
    phasesZoom: 10,

    /* initial load zoom multiplier */
    zoomFactor: 1,

    /* define the column and values used for the filter UI. There can be multiple filters listed.
       Additionally, a custom `label` can be defined (default is the field),
       and `values-label` (an array matching elements in `values`) */
    filters: [
        {
            field: 'status',
            values: ['operating', 'construction', 'pre-construction', 'announced', 'shelved', 'mothballed', 'retired', 'cancelled'],
        },
    ],

    countryFile: '../../src/countries.json', 
    allCountrySelect: true,
    multiCountry: false,

    hitArea: 5, 
    sqrt: true, // need this to trigger the square root interpolation circle asset sizing logic
    geometries: ['Point'],

    useDefaultCapacityInDetailView: true, // for gas finance where we used the unit capacity status functionality but 'Capacity' is hardcoded in for single unit projects and the value is not capacity but finance info here. displayDetails() in stie.js is where this is going to be used.
    showToolTip: false,  // set true in Europe map
};

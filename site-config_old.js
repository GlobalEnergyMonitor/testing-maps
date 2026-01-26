var site_config = {
    /* Mapbox Access Token */
    accessToken: 'pk.eyJ1IjoiZ2VtdGVhbTEiLCJhIjoiY21la2l0bmQ0MDY1eDJqcHB0cGkyZHh6NyJ9.Mas7dPxjgHVMfdnMvYrJig',

    /* Mapbox Base Map Style */
    mapStyle: 'mapbox://styles/gemteam1/cls98k6sf02li01p2fqtu67lc',
    center: [0, 0],
    projection: 'naturalEarth',

    /* Zoom level that asset detail cards open at; this is a good one to override in tracker config,
     depending on scale of facilities */

    img_detail_zoom: 15,

    /* Define labels for sitewide colors, referenced in tracker config */
    colors: {
        'red': '#c74a48',
        'blue': '#5c62cf',
        'green': '#4c9d4f',
        'grey': '#8f8f8e'
    },
    /* style test parameters!

    /* Mapbox styling applied to all trackers */
    pointPaint: {
        'circle-opacity':.85
    },
    linePaint: {
        'line-opacity':.85
    },
    lineLayout: {
        'line-cap': 'round',
        'line-join': 'round'
    },

    minRadius: 1,
    maxRadius: 10,
    highZoomMinRadius: 4,
    highZoomMaxRadius: 32,

    /* radius associated with minimum/maximum value on map */
    // /* Defined by pixels and be 1- infinity, 0 is invisible */
    // minRadius: 2,
    // maxRadius: 30,
    minLineWidth: .5,
    maxLineWidth: 7,

    // /* radius to increase min/max to under high zoom */
    // /* In  mapbox there are 22 zoom levels, higher zoom usually meaning samller area "closer in"*/
    // highZoomMinRadius: 4,
    // highZoomMaxRadius: 32,
    highZoomMinLineWidth: .5,
    highZoomMaxLineWidth: 7,

    /* define column names to pull data from */
    linkField: 'url',

    urlField: 'url',
    countryField: 'country',
    statusField: 'status',
    statusDisplayField: 'status',
    capacityField: 'capacity', //
    capacityDisplayField: 'capacity', // this is what gets used in the details summary unit feature where applicable
    locationColumns:{
        lat: 'lat',
        lng: 'lng'
    },

    /* by default, no all phases link; override in tracker config where appropriate */
    showAllPhases: false,
    showMaxCapacity: true,

    /* zoom level to set map when viewing all phases */
    phasesZoom: 8,

    /* initial load zoom multiplier */
    zoomFactor: 1,

    countryFile: '../../src/countries.json',
    allCountrySelect: true,
    multiCountry: false,

    hitArea: 5,
    sqrt: true, // need this to trigger the square root interpolation circle asset sizing logic
    geometries: ['Point'],

    scale_by_capacity: true, // for gas finance where we used the unit capacity status functionality but 'Capacity' is hardcoded in for single unit projects and the value is not capacity but finance info here. displayDetails() in stie.js is where this is going to be used.
};
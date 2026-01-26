processConfig();

/* Merge site-config.js and config.js - Single-use function */
function processConfig() {
    config = Object.assign(site_config, config);

    // map the color name to the hexcode
    Object.keys(config.color_association.values).forEach((color_key) => {
        config.color_association.values[color_key] = config.site_colors[config.color_association.values[color_key]];
    });
}


/*
    Global variable declaration
*/
let userInteracting = false;
const diacriticMap = {
    a: ['a', 'á', 'à', 'â', 'ã', 'ä', 'å'],
    e: ['e', 'é', 'è', 'ê', 'ë'],
    i: ['i', 'í', 'ì', 'î', 'ï'],
    o: ['o', 'ó', 'ò', 'ô', 'õ', 'ö', 'ø'],
    u: ['u', 'ú', 'ù', 'û', 'ü'],
    c: ['c', 'ç'],
    n: ['n', 'ñ'],
};

// The following values can be changed to control rotation speed:
// At low zooms, complete a revolution every ~two minutes.
const secondsPerRevolution = 150;
// Above zoom level 5, do not rotate.
const maxSpinZoom = 5;
// Rotate at intermediate speeds between zoom levels 3 and 5.
const slowSpinZoom = 3;
let spinEnabled = true;


/*
    Set up mapboxgljs instance, and trigger data load
*/ 
mapboxgl.accessToken = config.accessToken;
const map = new mapboxgl.Map({
    container: 'map',
    style: config.mapStyle,
    zoom: determineZoom(),
    center: config.center,
    projection: config.projection
});
console.log('This is current zoom' + map.zoom)
map.addControl(new mapboxgl.NavigationControl({ showCompass: false }));
const popup = new mapboxgl.Popup({
    closeButton: false,
    closeOnClick: false
});

// add new navigation features
map.scrollZoom.enable();
map.boxZoom.enable();
map.dragRotate.enable();

map.doubleClickZoom.enable();

// declare this so you can customize features depending on if it's first load or filtering
let initialLoad = true;

map.on('load', async () => {
    await loadData();
    setMinMax();
    linkAssets();
    addLayers();
    addEvents();
    console.log('layers and events added');  // TODO DELETE

    // Enable UX as soon as the map is idle, but no later than 3 seconds from now
    setTimeout(enableUX, 3000);
    map.on('idle', enableUX); // enableUX starts to render data
});

map.on('moveend', () => {
    spinGlobe();
});


/*
  Load data in from various formats, and prepare for use in application
*/
/* Initial pull of the map input file using fetch - Single-use function */
async function loadData() {
    console.log('pulling input data');  // TODO DELETE

    let data;

    if ('tiles' in config) {
        addTiles();
        data = await parseCsv(config.csv);
        addGeoJSON(data);

    } else if ('geojson' in config) {
        const response = await fetch(config.geojson);
        if (!response.ok) {
            throw new Error('Failed to load geojson');
        }
        console.log('awaiting data pull');  // TODO DELETE
        data = await response.json();
        console.log('data pulled successfully');  // TODO DELETE
        addGeoJSON(data);

    } else if ('json' in config) {
        const response = await fetch(config.json);
        if (!response.ok) {
            throw new Error('Failed to load json');
        }
        data = await response.json();
        addGeoJSON(data);

    } else {
        data = await parseCsv(config.csv);
        addGeoJSON(data);
    }

    return data;
}

/* Helper function to pull and parse csv input data - Single-use function: called once in loadData(), one of 2 ways */
function parseCsv(url) {
    return new Promise((resolve, reject) => {
        Papa.parse(url, {
            download: true,
            header: true,
            complete: function(results) {
                resolve(results.data);
            },
            error: function(error) {
                reject(error);
            }
        });
    });
}

/* Adds the tiles as a source to the map - Single-use function */
function addTiles() {
    map.addSource('assets-source', {
        'type': 'vector',
        'tiles': config.tiles,
        'minzoom': 1,
        'maxzoom': 10
    });
}

/* TODO Function Summary - Single-use function: called once in loadData(), one of 4 ways */
function addGeoJSON(jsonData) {

    // we want find maxMin max = largest project all units summed together, min = smallest unit
    // find min max outside with preprocessing
    // remove outliers with grouped
    // sort without lodash to find percentile
    // array of values, grouped capacities

    // converts all to geojson 
    if ('type' in jsonData && jsonData['type'] === 'FeatureCollection') {
        config.geojson = jsonData;
    } else {
        config.geojson = {
            'type': 'FeatureCollection',
            'features': []
        };

        jsonData.forEach((asset) => {
            let feature = {
                'type': 'Feature',
                'geometry': {
                    'type': 'Point',
                    'coordinates': [asset[config.locationColumns['long']], asset[config.locationColumns['lat']]]
                },
                'properties': {}
            }
            for (let key in asset) {
                if (key === config.capacityField) {
                    feature.properties[key] = Number(asset[key]);
                } else if (key !== config.locationColumns['long'] && key !== config.locationColumns['lat']) {
                    feature.properties[key] = asset[key];
                }
            }
            if (feature.properties[config['countryField']]) {
                config.geojson.features.push(feature);
            }
        });
    }

    // part to optimize csv/geojson maps
    if (!config.tiles) {
        map.addSource('assets-source', {
            'type': 'geojson',
            'data': config.geojson
        });
    }
}

/* TODO Function Summary - Single-use function */
function setMinMax() {
    console.log('setting min/max line/point capacity');  // TODO DELETE
    config.maxPointCapacity = 0;
    config.minPointCapacity = 1000000;
    config.maxLineCapacity = 0;
    config.minLineCapacity = 1000000;
    let maxCapacityKey;
    let minCapacityKey;
    config.geojson.features.forEach((feature) => {
        if (feature.geometry.type === 'LineString') {
            minCapacityKey = 'minLineCapacity';
            maxCapacityKey = 'maxLineCapacity';
        } else {
            minCapacityKey = 'minPointCapacity';
            maxCapacityKey = 'maxPointCapacity';
        }

        // if the capacity is more than the max capacity so far then it should be used
        // vice versa for min capacity
        // later this is used to size the assets along smoothly by interpolation across the width between min and maxPoint and LineWidth
        // this min and max Line and Point Capacity is crucial to the scaling, along with the unit's capacity
        if (parseFloat(feature.properties[config.capacityScaledField]) > config[maxCapacityKey]) {
            config[maxCapacityKey] =  parseFloat(feature.properties[config.capacityScaledField]);
        }
        if (parseFloat(feature.properties[config.capacityScaledField]) < config[minCapacityKey]) {
            config[minCapacityKey] =  parseFloat(feature.properties[config.capacityScaledField]);
        }
    });
}

/* TODO Function Summary - Frequent-use function; used every time data is filtered */
// Builds lookup of linked assets by the link column
// and when linked assets share location, rebuilds geojson_linked with summed capacity and custom icon
function linkAssets() {
    console.log('linking assets');  // TODO DELETE
    map.off('idle', linkAssets);
    if (!('geojson_filtered' in config)) {  // if the filtered geojson hasn't been initialized
        config.geojson_filtered = config.geojson;
    }

    config.totalCount = 0;

    // First, create a lookup table for linked assets based on linkField
    config.linked_assets = {};
    config.geojson_filtered.features.forEach((feature) => {
        if (! (feature.properties[config.linkField] in config.linked_assets)) {
            config.linked_assets[feature.properties[config.linkField]] = [];
        } 
        config.linked_assets[feature.properties[config.linkField]].push(feature);
    });

    // Next find linked assets that share location. 
    let grouped_assets = {};
    config.geojson_filtered.features.forEach((feature) => {
        if ('geometry' in feature && feature.geometry != null) {
            if ('coordinates' in feature.geometry) {
                let key = feature.properties[config.linkField] + ':' + feature.geometry.coordinates[0] + ',' + feature.geometry.coordinates[1];
                if (! (key in grouped_assets)) {
                    grouped_assets[key] = [];
                }
                // adds feature to dictonary grouped_assets if shares a linkField id and coords, not done for lines
                grouped_assets[key].push(feature);
            }
        }
    });

    // Rebuild GeoJSON with summed capacity, and custom icon for single point display of the grouped assets
    config.geojson_linked = {
        'type': 'FeatureCollection',
        'features': []
    };

    Object.keys(grouped_assets).forEach((key) => {
        let features_in_current_group = grouped_assets[key]; //deep copy
        let group_feature = JSON.parse(JSON.stringify(features_in_current_group[0]))  // make a group (total) feature, deep-copied from the first feature in the group

        // Sum capacity across all linked assets
        group_feature.properties[config.capacityScaledField] = features_in_current_group.reduce((previous, current) => {
            return previous + Number(current.properties[config.capacityScaledField]);
        }, 0);

        // Build summary count of capacity across all linked assets and generate icon based on that label if more than one status
        if (group_feature.geometry.type === 'Point') {
            let icon = Object.assign(...Object.keys(config.color_association.values).map(k => ({ [config.color_association.values[k]]: 0 })));
            features_in_current_group.forEach((feature) => {
                icon[config.color_association.values[feature.properties[config.color_association.field]]] += Number(feature.properties[config.capacityField]);
            });
            if (Object.values(icon).filter(v => v != 0).length > 1) {  // if the icon will contain more than one color
                // normalize values to 10
                let current = 0;
                let total = Object.values(icon).reduce((previous, current) => {
                    return previous + Number(current);
                }, 0);
                icon = Object.assign(...Object.keys(icon).map(k => ({[k]: Math.ceil(11 * (icon[k] / total)) })));  // use 11 and ceil to get 12 pieces on the circle
                let string_icon = JSON.stringify(icon)
                group_feature.properties['icon'] = string_icon;
                if (! config.icons.includes(string_icon)) {
                    generateIcon(icon);
                    config.icons.push(string_icon);
                }
            }
        }

        // Build summary count of filters for legend
        let summary_count = {};
        config.filters.forEach((filter) => {
            summary_count[filter.field] = Object.assign(...filter.values.map(f => ({[f]: 0})));
            features_in_current_group.forEach((feature) => {
                summary_count[filter.field][feature.properties[filter.field]]++;
            });
        });
        group_feature.properties['summary_count'] = JSON.stringify(summary_count);
        config.totalCount += features_in_current_group.length;

        config.geojson_linked.features.push(group_feature);
    });

    // set the map to use the linked assets as input data
    map.getSource('assets-source').setData(config.geojson_linked);
}

/* Generates icon image circles for each unique asset combination - Frequent-use function: called once in linkAssets() in a forEach loop */
function generateIcon(icon) {
    let label = JSON.stringify(icon);
    if (map.hasImage(label)) return;  // if the map has already created an icon (image) with the given label, return
    // ideally, should return more often for the longer time the user spend filtering
    // on initial load, this function will run for every unique icon (image)

    let canvas = document.createElement('canvas');
    canvas.width = 64; // set the size of the canvas
    canvas.height = 64;

    // get the canvas context
    let context = canvas.getContext('2d');

    // calculate the coordinates of the center of the circle
    let centerX = canvas.width / 2;
    let centerY = canvas.height / 2;

    let current = .75;  // start at vertical
    let slices = Object.values(icon).reduce((previous, current) => {
        return previous + Number(current);
    }, 0);

    Object.keys(icon).forEach((k) => {
        if (icon[k] <= 0) return;  // don't attempt to draw a slice that is of a color not on this specific circle
        let next = current + (icon[k] / slices);
        context.fillStyle = k;
        context.beginPath();
        context.moveTo(centerX, centerY);
        context.arc(centerX, centerY, canvas.width / 2, Math.PI * 2 * current, Math.PI * 2 * next);
        context.fill();

        current = next;
    });

    // create a data URL for the canvas image
    let dataURL = canvas.toDataURL();

    // add the image to the map as a custom icon
    map.loadImage(dataURL, (error, image) => {
        if (error) throw error;
        if (! map.hasImage(label)) map.addImage(label, image);
    });
}

/*
  Render Data
*/

/* Adds line layer, point layer - Single-use function */
function addLayers() {
    config.layers = [];
    if (config.geometries.includes('LineString')) addLineLayer();
    if (config.geometries.includes('Point')) addPointLayer();

    map.addLayer({
        id: 'satellite',
        source: { 'type': 'raster', 'url': 'mapbox://mapbox.satellite', 'tileSize': 256 },
        type: 'raster',
        layout: { 'visibility': 'none' }
        },
        config.layers[0]
    );

    map.addSource('countries', {
        'type': 'vector',
        'url': 'mapbox://mapbox.country-boundaries-v1'
    });

    map.addLayer(
        {
            'id': 'country-layer',
            'type': 'fill',
            'source': 'countries',
            'source-layer': 'country_boundaries',
            'layout': {},
            'paint': {
                'fill-color': 'hsla(219, 0%, 100%, 0%)'
            }
        },
        config.layers[0]
    );
}

/* Adds point layer to map obj - Single-use function */
function addPointLayer() {
    // First build circle layer
    //  build style json for circle-color based on config.color_association
    let paint = config.pointPaint;
    if ('color_association' in config) {
        paint['circle-color'] = [
            'match',
            ['get', config.color_association.field],
            ...Object.keys(config.color_association.values).flatMap(key => [key, config.color_association.values[key]]),
            '#000000'
        ];
    }
    let interpolateExpression = ('interpolate' in config ) ? config.interpolate :  ['linear'];

    try {
        // Handle case where all capacity values are the same
        if (config.minPointCapacity === config.maxPointCapacity) {
            paint['circle-radius'] = [
                'interpolate', ['exponential', .5], ['zoom'],
                1, config.minRadius,
                10, config.highZoomMinRadius
            ];
        } else {
            paint['circle-radius'] = [
                'interpolate', ['exponential', .5], ['zoom'],
                1,  ['interpolate', interpolateExpression,
                    ['to-number',['get', config.capacityScaledField]],
                    config.minPointCapacity, config.minRadius,
                    config.maxPointCapacity, config.maxRadius
                ],
                10, ['interpolate', interpolateExpression,
                    ['to-number',['get', config.capacityScaledField]],
                    config.minPointCapacity, config.highZoomMinRadius,
                    config.maxPointCapacity, config.highZoomMaxRadius
                ]
            ];
        }
    } catch (e) {
        console.error('Error setting circle-radius. config.capacityScaledField:', config.capacityScaledField);
        throw e;
    }

    map.addLayer({
        'id': 'assets-points',
        'type': 'circle',
        'source': 'assets-source',
        'filter': ['==', ['geometry-type'], 'Point'],
        ...('tileSourceLayer' in config && {'source-layer': config.tileSourceLayer}),
        'layout': {},
        'paint': paint,
        "icon-opacity": config.pointPaint["circle-opacity"]
    });
    config.layers.push('assets-points');

    // Add layer with proportional icons
    if (config.sqrt) {
        const sqrtMin = Math.sqrt(config.minPointCapacity);
        const sqrtMax = Math.sqrt(config.maxPointCapacity);

        map.addLayer({
            'id': 'assets-symbol', 
            'type': 'symbol',
            'source': 'assets-source',
            'filter': ['==', ['geometry-type'], 'Point'],
            ...('tileSourceLayer' in config && {'source-layer': config.tileSourceLayer}),
            'layout': {
                'icon-image': ['get', 'icon'],
                'icon-allow-overlap': true,
                'icon-size': [
                    'interpolate', ['linear'], ['zoom'],
                    1,  ['interpolate', interpolateExpression,
                        ['sqrt', ['to-number', ['get', config.capacityScaledField]]],
                        sqrtMin, config.minRadius * 2 / 64,
                        sqrtMax, config.maxRadius * 2 / 64],
                    10, ['interpolate', interpolateExpression,
                        ['sqrt',['to-number', ['get', config.capacityScaledField]]],
                        sqrtMin, config.highZoomMinRadius * 2 / 64,
                        sqrtMax, config.highZoomMaxRadius * 2 / 64]
                ]
            }
        });
    }

    else {
        // Add layer with proportional icons
        map.addLayer({
            'id': 'assets-symbol', 
            'type': 'symbol',
            'source': 'assets-source',
            'filter': ['==', ['geometry-type'], 'Point'],
            ...('tileSourceLayer' in config && {'source-layer': config.tileSourceLayer}),
            'layout': {
                'icon-image': ['get', 'icon'],
                'icon-allow-overlap': true,
                'icon-size': [
                    'interpolate', ['exponential', .5], ['zoom'],
                    1,  ['interpolate', interpolateExpression,
                        ['to-number', ['get', config.capacityScaledField]],
                        config.minPointCapacity, config.minRadius * 2 / 64,
                        config.maxPointCapacity, config.maxRadius * 2 / 64],
                    10, ['interpolate', interpolateExpression,
                        ['to-number', ['get', config.capacityScaledField]],
                        config.minPointCapacity, config.highZoomMinRadius * 2 / 64,
                        config.maxPointCapacity, config.highZoomMaxRadius * 2 / 64]
                ]
            }
        });
    }

    // Add highlight layer
    paint = config.pointPaint;
    paint['circle-color'] = '#FFEA00';
    map.addLayer({
        'id': 'assets-points-highlighted',
        'type': 'circle',
        'source': 'assets-source',
        'filter': ['==', ['geometry-type'], 'Point'],
        ...('tileSourceLayer' in config && {'source-layer': config.tileSourceLayer}),
        'layout': {},
        'paint': paint,
        'filter': ['in', (config.linkField), '']  // TODO resolve duplicate key
    });
    map.addLayer({
        'id': 'assets-labels',
        'type': 'symbol',
        'source': 'assets-source',
        'filter': ['==', ['geometry-type'], 'Point'],
        ...('tileSourceLayer' in config && {'source-layer': config.tileSourceLayer}),
        'minzoom': 8,
        'layout': {
            'text-field': '{' + config.nameField + '}',
            'text-font': ['DIN Pro Italic'],
            'text-variable-anchor': ['top'],
            'text-offset': [0, 1],
            'text-size': 14
        },
        'paint': {
            'text-color': '#000000',
            'text-halo-color': 'hsla(220, 8%, 100%, 0.75)',
            'text-halo-width': 1
        }
    });
}

/* Adds line layer to map obj - Single-use function */
function addLineLayer() {
    let paint = config.linePaint;

    if ('color_association' in config) {
        paint['line-color'] = [
            'match',
            ['get', config.color_association.field],
            ...Object.keys(config.color_association.values).flatMap(key => [key, config.color_association.values[key]]),
            '#000000'
        ];
    }

    let interpolateExpression = ('interpolate' in config ) ? config.interpolate :  ['linear'];
    // Handle case where all capacity values are the same
    if (config.minLineCapacity === config.maxLineCapacity) {
        paint['line-width'] = [
            'interpolate', ['linear'], ['zoom'],
            1, config.minLineWidth,
            10, config.highZoomMinLineWidth
        ];
    } else {
        paint['line-width'] = [
            'interpolate', ['linear'], ['zoom'],
            1,  ['interpolate', interpolateExpression,
                ['to-number', ['get', config.capacityScaledField]],
                config.minLineCapacity, config.minLineWidth,
                config.maxLineCapacity, config.maxLineWidth
            ],
            10, ['interpolate', interpolateExpression,
                ['to-number', ['get', config.capacityScaledField]],
                config.minLineCapacity, config.highZoomMinLineWidth,
                config.maxLineCapacity, config.highZoomMaxLineWidth
            ]
        ];
    }

    map.addLayer({
        'id': 'assets-lines', 
        'type': 'line',
        'source': 'assets-source',
        'filter': ['==', ['geometry-type'], 'LineString'],
        ...('tileSourceLayer' in config && {'source-layer': config.tileSourceLayer}),
        'layout': config.lineLayout,
        'paint': paint
    }); 
    config.layers.push('assets-lines');

    paint['line-color'] = '#FFEA00';
    map.addLayer({
        'id': 'assets-lines-highlighted',
        'type': 'line',
        'source': 'assets-source',
        'filter': ['==', ['geometry-type'], 'LineString'],
        ...('tileSourceLayer' in config && {'source-layer': config.tileSourceLayer}),
        'layout': config.lineLayout,
        'paint': paint,
        'filter': ['in', (config.linkField), '']  // TODO resolve duplicate key
    });
}

/* TODO Function Summary - Single-use function */
function enableUX() {
    // handle race condition
    map.off('idle', enableUX);
    if (config.UXEnabled) {
        return
    }
    config.UXEnabled = true;

    // TODO what these functions do, collectively
    console.log('enabling UX');  // TODO DELETE
    buildFilters();
    updateSummary();
    buildTable();
    enableModal();
    enableNavFilters();
    $('#spinner-container').addClass('d-none')
    $('#spinner-container').removeClass('d-flex')
    if (config.projection === 'globe') {
        spinGlobe();
    }
}


/*
  Event Handling
*/

/* Adds events and sets some event handling - Single-use function */
function addEvents() {
    
    // Example trigger of a BoxZoomEvent of type "boxzoomstart"
    map.on('zoomend', (e) => {

        currZoom = map.getZoom();
        console.log('currZoom', currZoom);
        
    });

    map.on('zoomstart', (e)=> {
        userInteracting = true;
        spinGlobe();
    });

    map.on('click', (e) => {
        userInteracting = true;
        spinGlobe();
        const bbox = [ [e.point.x - config.hitArea, e.point.y - config.hitArea], [e.point.x + config.hitArea, e.point.y + config.hitArea] ];
        const selectedFeatures = getUniqueFeatures(map.queryRenderedFeatures(bbox, {layers: config.layers}), config.linkField).sort((a, b) => a.properties[config.nameField].localeCompare(b.properties[config.nameField]));

        if (selectedFeatures.length === 0) return;

        const links = selectedFeatures.map(
            (feature) => feature.properties[config.linkField]
        );

        setHighlightFilter(links);

        if (selectedFeatures.length === 1) {
            config.selectModal = '';
            displayDetails(config.linked_assets[selectedFeatures[0].properties[config.linkField]]);
        } else {
            var modalText = '<h6 class="p-3">There are multiple ' + config.assetFullLabel + ' near this location. Select one for more details</h6>';

            let ul = $('<ul>');
            selectedFeatures.forEach((feature) => {
                var link = $('<li class="asset-select-option">' + feature.properties[config.nameField] + '</li>');
                link.attr('data-feature', JSON.stringify(config.linked_assets[feature.properties[config.linkField]]));
                link.attr('onClick', 'displayDetails(this.dataset.feature)');
                ul.append(link);
            });
            modalText += ul[0].outerHTML;
            config.selectModal = modalText;
            $('.modal-body').html(modalText);
        }

        config.modal.show();
    });

    config.layers.forEach(layer => {
        map.on('mouseenter', layer, (e) => {
            map.getCanvas().style.cursor = 'pointer';
            const coordinates = (map.getLayer(layer).type === 'line' ? e.lngLat : e.features[0].geometry.coordinates.slice());
            const description = e.features[0].properties[config.nameField];
            popup.setLngLat(coordinates).setHTML(description).addTo(map);
        });
    });

    config.layers.forEach(layer => {
        map.on('mouseleave', layer, () => {
            map.getCanvas().style.cursor = '';
            popup.remove();
        }); 
    });

    $('#basemap-toggle').on('click', function() {
        if (config.baseMap === 'Streets') {
           config.baseMap = 'Satellite';
           map.setLayoutProperty('satellite', 'visibility', 'visible');
           map.setFog({
            'range': [0.8, 8],
            'color': '#dc9f9f',
            'horizon-blend': 0.5,
            'high-color': '#245bde',
            'space-color': '#000000',
            'star-intensity': 0.3
            });
        } else {
           config.baseMap = 'Streets';
           map.setLayoutProperty('satellite', 'visibility', 'none');

           map.setFog(null);
        }
    });

    $('#reset-all-button').on('click', function() {
        enableResetAll(); 
    });

    $('#collapse-sidebar').on('click', function() {
        $('#filter-form').hide();
        $('#all-select').hide();
        $('#all-select-section-level').hide();
        $('#collapse-sidebar').hide();
        $('#expand-sidebar').show();
    });

    $('#expand-sidebar').on('click', function() {
        $('#filter-form').show();
        $('#all-select').show();
        $('#all-select-section-level').show();
        $('#collapse-sidebar').show();
        $('#expand-sidebar').hide();
    });

    $('#projection-toggle').on('click', function() {
        if (config.projection === 'globe') {
            config.projection = 'naturalEarth';
            map.setProjection('naturalEarth');
            map.setCenter(config.center);
            map.setZoom(determineZoom());
        } else {
            config.projection = 'globe';
            map.setProjection('globe');
            map.setCenter(config.center);
            spinGlobe();
            map.setZoom(determineZoom());
        }
    })
}

/* Spins the globe */
function spinGlobe() {
    const zoom = map.getZoom();
    if (config.projection === 'globe') {
        if (spinEnabled && !userInteracting && zoom < maxSpinZoom) {
            let distancePerSecond = 360 / secondsPerRevolution;
            if (zoom > slowSpinZoom) {
                // Slow spinning at higher zooms
                const zoomDif =
                    (maxSpinZoom - zoom) / (maxSpinZoom - slowSpinZoom);
                distancePerSecond *= zoomDif;
            }
            const center = map.getCenter();
            center.lng -= distancePerSecond;
            // Smoothly animate the map over one second.
            // When this animation is complete, it calls a 'moveend' event.
            map.easeTo({ center, duration: 1000, easing: (n) => n });
        }
    }
}
// adds option to pause spin with space - important for smaller screens
// TODO bug with needing to press space 3x to get it to spin again?
document.addEventListener('keydown', (e) => {
    spinEnabled = !spinEnabled;
    if (e.code === 'Space') {
        if (spinEnabled) {
            userInteracting = !userInteracting;
            spinGlobe();
        } else {
            map.stop(); // Immediately end ongoing animation
            spinGlobe();
        }
    }
});

function determineZoom() {
    let modifier = 650;
    if (window.innerWidth < 1000) { modifier = 500; }
    else if (window.innerWidth < 1500) { modifier = 575; }
    return config.zoomFactor * (window.innerWidth - modifier) / modifier;
}


/*
  Legend Filters
*/
function makeDomSafe(value) {
    return String(value)
        .trim()
        .replace(/\s+/g, '-')
        .replace(/[^\w\-]/g, '');
}

function buildFilters() {
    countFilteredFeatures();
    config.filters.forEach(filter => {
        // go through each filter in config 
        if (config.showToolTip) {  // used by Europe map and GIST
            // create more space for europe legend
            if (filter.primary && filter.field_hover_text) {
            $('#filter-form').append('<h7 class="card-title">' + (filter.label || filter.field.replaceAll('_',' ')) +
            '<div class="infobox" id="infobox"><span>i</span><div class="tooltip" id="tooltip">' + filter.field_hover_text + 
            '</div></div></h7> <div class="col-12 text-left small" id="all-select-section-level"><a href="" onclick="selectAllFilterSection(\'' +
            filter.field + '\'); return false;">select all section</a> | <a href="" onclick="clearAllFilterSection(\'' + filter.field + '\'); return false;">clear all section</a></div>');
            // add eventlistener for infobox and tooltip to show on hover
            }
            else if (filter.field_hover_text) {
            $('#filter-form').append('<hr /><h7 class="card-title">' + (filter.label || filter.field.replaceAll('_',' ')) + '<div class="infobox" id="infobox"><span>i</span><div class="tooltip" id="tooltip">' + filter.field_hover_text +
            '</div></div></h7> <div class="col-12 text-left small" id="all-select-section-level"><a href="" onclick="selectAllFilterSection(\'' +
            filter.field + '\'); return false;">select all section</a> | <a href="" onclick="clearAllFilterSection(\'' + filter.field + '\'); return false;">clear all section</a></div>');
            }
            else {
            // do same as below but append infobox
            $('#filter-form').append('<hr /><h7 class="card-title">' + (filter.label || filter.field.replaceAll('_',' ')) +
            '</div></div></h7> <div class="col-12 text-left small" id="all-select-section-level"><a href="" onclick="selectAllFilterSection(\'' +
            filter.field + '\'); return false;">select all section</a> | <a href="" onclick="clearAllFilterSection(\'' + filter.field + '\'); return false;">clear all section</a></div>');
            }
        }
        // this creates the section title and adds the select all feature only to the sections after the first one, if there is no tooltip logic so for all non europe maps
        else if (config.color_association.field !== filter.field) {
            $('#filter-form').append('<hr /><h7 class="card-title">' + (filter.label || filter.field.replaceAll('_',' ')) +
            '</div></div></h7> <div class="col-12 text-left small" id="all-select-section-level"><a href="" onclick="selectAllFilterSection(\'' +
            filter.field + '\'); return false;">select all section</a> | <a href="" onclick="clearAllFilterSection(\'' + filter.field + '\'); return false;">clear all section</a></div>');
        }

        for (let i = 0; i < filter.values.length; i++) {
            let check_id =  filter.field + '_' + makeDomSafe(filter.values[i]);
            let check = `<div class="row filter-row" data-checkid="${(check_id).replace('/','\\/')}">`;
            check += '<div class="col-1 checkmark" id="' + check_id + '-checkmark"></div>';
            check += `<div class="col-8"><input type="checkbox" checked class="form-check-input d-none" id="${check_id}">`;
            check += (config.color_association.field === filter.field ? '<span class="legend-dot" style="background-color:' + config.color_association.values[ filter.values[i] ] + '"></span>' : "");
            check += `<span id='${check_id}-label'>` + ('values_labels' in filter ? filter.values_labels[i] : makeDomSafe(filter.values[i]).replaceAll("_", " ")) + '</span></div>';
            check += '<div class="col-3 text-end" style="text-align: right;" id="' + check_id + '-count">' + config.filterCount[filter.field][makeDomSafe(filter.values[i])] + '</div></div>';
            $('#filter-form').append(check);
        }

        // add eventlistener for infobox and tooltip to show on hover
        $('.infobox').each(function() {
            $(this).on('mouseover', function() {
                const infoBox = document.getElementById('infobox');
                const toolTip = document.getElementById('tooltip');
                const infoBoxRect = infoBox.getBoundingClientRect();
                const toolTipRect = toolTip.getBoundingClientRect();
                const windowHeight = window.innerHeight;
                if (infoBoxRect.top < toolTipRect.height + 20) {
                    // Position the tooltip below the infobox
                    toolTip.style.bottom = 'auto';
                    toolTip.style.top = '110%';
                } else {
                    // Position the tooltip above the infobox
                    toolTip.style.top = 'auto';
                    toolTip.style.bottom = '110%';
                }

                $(this).find('.tooltip').css({
                    'opacity': '1',
                    'visibility': 'visible'
                });
            });
            $(this).on('mouseout', function() {
                $(this).find('.tooltip').css({
                    'opacity': '0',
                    'visibility': 'hidden'
                });
            });
        });
    });
    
    $('.filter-row').each(function() {
        this.addEventListener('click', function() {
            $('#' + this.dataset.checkid).click();
            toggleFilter(this.dataset.checkid);

            filterData();
        });
    });
}

function toggleFilter(id) {
    $('#' + id + '-checkmark').toggleClass('checkmark uncheckmark');
}

// for legend level select all and clear all
function selectAllFilter() {
    $('.filter-row').each(function() {
        if (! $('#' + this.dataset.checkid)[0].checked) {
            $('#' + this.dataset.checkid)[0].checked = true;
            toggleFilter(this.dataset.checkid);
        }
    });
    filterData();
}

// for section level select all and clear all
// needs to know field name to distinguish which filter rows to clear and what not to
function selectAllFilterSection(fieldRow) {
    $('.filter-row').each(function() {
        let rowFieldName = this.dataset.checkid.split('_')[0];
        if (rowFieldName === fieldRow && !$('#' + this.dataset.checkid)[0].checked) {
            $('#' + this.dataset.checkid)[0].checked = true;
            toggleFilter(this.dataset.checkid);
        }
    });
    filterData();
}

// for legend level select all and clear all
function clearAllFilter(fieldRow) {
    $('.filter-row').each(function() {
        if ($('#' + this.dataset.checkid)[0].checked) {
            $('#' + this.dataset.checkid)[0].checked = false;
            toggleFilter(this.dataset.checkid);
        }
    });
    filterData();
}

// TODO ISSUE HERE
// only for infra type tab-type
// for section level select all and clear all
function clearAllFilterSection(fieldRow) {
    $('.filter-row').each(function() {
        let rowFieldName = this.dataset.checkid.split('_')[0];
        if (rowFieldName === fieldRow && $('#' + this.dataset.checkid)[0].checked) {
            $('#' + this.dataset.checkid)[0].checked = false;
            toggleFilter(this.dataset.checkid);
        }
    });
    filterData();
}

function countFilteredFeatures() {
    config.filterCount = {};
    config.filters.forEach(filter => {
        config.filterCount[filter.field] = {};
        filter.values.forEach(val => {
            config.filterCount[filter.field][makeDomSafe(val)] = 0;
        });
    });

    config.maxFilteredCapacity = 0;
    config.minFilteredCapacity = 1000000;

    config.geojson_linked.features.forEach(feature => {
        if ('summary_count' in feature.properties) {
            let summary_count = JSON.parse(feature.properties.summary_count);
            Object.keys(summary_count).forEach((filter) => {
                Object.keys(summary_count[filter]).forEach((val) => {
                    config.filterCount[filter][makeDomSafe(val)] += summary_count[filter][val];
                });
            });
        } else {
            config.filters.forEach(filter => {
                filter.values.forEach(val => {
                    if (feature.properties[filter.field] === makeDomSafe(val)) {
                        config.filterCount[filter.field][makeDomSafe(val)]++;
                    }
                });
            });
        }

        if (parseFloat(feature.properties[config.capacityField]) > config.maxFilteredCapacity) {
            config.maxFilteredCapacity =  parseFloat(feature.properties[config.capacityField]);
        }
        if (parseFloat(feature.properties[config.capacityField]) < config.minFilteredCapacity) {
            config.minFilteredCapacity =  parseFloat(feature.properties[config.capacityField]);
        }       
    });
}

function filterData() {
    $('#spinner-container').removeClass('d-none')
    $('#spinner-container').addClass('d-flex')

    if (config.tiles) {
        filterTiles();
    } else {
        filterGeoJSON();
    }
}

function filterTiles() {
    let filterStatus = {};
    config.filters.forEach(filter => {
        filterStatus[filter.field] = [];
    });
    $('.form-check-input').each(function() {
        if (this.checked) {
            let [field, ...value] = this.id.split('_');
            filterStatus[field].push(value.join('_'));
        }
    });

    config.filterExpression = [];
    if (config.searchText.length >= 3) {
        
        let searchExpression = ['any'];
        config.selectedSearchFields.split(',').forEach((field) => {
            searchExpression.push(['in', ['literal', config.searchText], ['downcase', ['get', field]]]);

        });
        config.filterExpression.push(searchExpression);
    }
    if (config.selectedCountries.length > 0) {
        // updated to handle so doesn't catch when countries are substrings of each other (Niger/Nigeria)
        // added ';' at end of each country
        let countryExpression = ['any'];
        config.selectedCountries.forEach(country => {
            if (config.multiCountry) {
                country = country + ';'; //this is needed to filter integrated file by country select but doesn't affect filtering by region // TODO verify if actually needed, at any stage in processing
                countryExpression.push(['in', ['string', country], ['string', ['get', config.countryField]]]);
            } else {
                countryExpression.push(['==', ['string', country], ['string', ['get', config.countryField]]]);
            }
        })
        config.filterExpression.push(countryExpression);
    }

    for (let field in filterStatus) {
        config.filterExpression.push(['in', ['get', field], ['literal', filterStatus[field]]]);
    }
    if (config.filterExpression.length === 0) {
        config.filterExpression = null;
    } else {
        config.filterExpression.unshift('all');
    }
    config.layers.forEach(layer => {
        config.filterExpression.push(['==', ['geometry-type'],
            map.getLayer(layer).type === 'line' ? 'LineString' : 'Point'
        ]);
        map.setFilter(layer, config.filterExpression);
        config.filterExpression.pop();
    });
    if (config.geometries.includes('Point')) {
        map.setFilter('assets-labels', config.filterExpression);
    }

    if ($('#table-container').is(':visible')) {
        filterGeoJSON();
    } else {
        map.on('idle', filterGeoJSON);
    }
}

function filterGeoJSON() {
    map.off('idle', filterGeoJSON);

    let filterStatus = {};
    config.filters.forEach(filter => {
        filterStatus[filter.field] = [];
    });
    $('.form-check-input').each(function () {
        if (this.checked) {
            let [field, ...value] = this.id.split('_');
            filterStatus[field].push(value.join('_'));
        }
    });
    let filteredGeoJSON = {
        'type': 'FeatureCollection',
        'features': []
    };
    config.geojson.features.forEach(feature => {  // for each unit in the original geojson
        let include = true;
        for (let field in filterStatus) {  // for pre-defined filters (left side)
            if (!filterStatus[field].includes(makeDomSafe(feature.properties[field]))) include = false;
        }
        // filter by text search bar
        if (config.searchText.length >= 3) {
            userInteracting = true;
            if (config.selectedSearchFields.split(',').filter((field) => {
                // remove diacritics from mapValue
                if (feature.properties[field] != null) {
                    let mapValue = removeDiacritics(feature.properties[field]);
                    return mapValue.toLowerCase().includes(config.searchText);
                }
            }).length === 0) include = false;
        }
        // filter by country select, gets hit when just filtering by legend too
        if (config.selectedCountries.length > 0) {
            // This checks if any of the selected countries are associated with the project
            try {
            const projectCountries = feature.properties[config.countryField].split(';').map(country => country.trim());
                if (!config.selectedCountries.some(country => projectCountries.includes(country))) {
                    include = false;
                }
            } catch (err) {
                console.error('Country field error for feature:', feature.properties[config.nameField], err);
                include = false;
            }
        }

        // for those projects that aren't associated with selected countries it makes the include flag false so it is not displayed
        if (include) {
            filteredGeoJSON.features.push(feature);
        }
    });
    config.geojson_filtered = filteredGeoJSON;
    linkAssets();
    config.tableDirty = true;
    updateTable();
    updateSummary();
}

function updateSummary() {
    $('#spinner-container').addClass('d-none')
    $('#spinner-container').removeClass('d-flex')
    $('#total_in_view').text(config.totalCount.toLocaleString())
    $('#summary').html('Total ' + config.assetFullLabel + ' selected');
    countFilteredFeatures();
    config.filters.forEach((filter) => {
        for (let i = 0; i < filter.values.length; i++) {
            const count_id = filter.field + "_" + makeDomSafe(filter.values[i]) + "-count";
            $('#' + count_id).text(config.filterCount[filter.field][makeDomSafe(filter.values[i])]);
        }
    });

    if (config.showMaxCapacity) {
        $('#max_capacity').text(Math.round(config.maxFilteredCapacity).toLocaleString());
        $('#capacity_summary_max').html('Maximum ' + config.minMaxCapacityFilterLabel);
    }
    if (config.showMinCapacity) {
        $('#min_capacity').text(Math.round(config.minFilteredCapacity).toLocaleString());
        $('#capacity_summary_min').html('Minimum ' + config.minMaxCapacityFilterLabel);
    }
}


/*
  Table View
*/
function buildTable() {
    $('#table-toggle').on('click', function() {
        if (! $('#table-container').is(':visible')) {
            $('#table-toggle-label').html('Map view <img src="../../src/img/arrow-right.svg" width="15" height="50" style="text-align: center;">');
            $('#map').hide();
            $('#btn-spin').hide();
            $('#sidebar').hide();
            $('#table-container').show();
            $('#basemap-toggle').hide();
            $('#projection-toggle').hide();
            updateTable(true);
        } else {
            $('#table-toggle-label').html('Table view <img src="../../src/img/arrow-right.svg" width="15" height="50" style="text-align: center;">');
            $('#map').show();
            $('#btn-spin').show();
            $('#sidebar').show();
            $('#table-container').hide();
            $('#basemap-toggle').show();
            $('#projection-toggle').show();

        }
    });
}

function createTable() {
    if ('rightAlign' in config.tableHeaders) {
        config.tableHeaders.rightAlign.forEach((col) => {
            $('#site-style').get(0).sheet.insertRule('td:nth-child(' + (config.tableHeaders.values.indexOf(col)+1) + ') { text-align:right }', 0);
        });
    }
    if ('noWrap' in config.tableHeaders) {
        config.tableHeaders.noWrap.forEach((col) => {
            $('#site-style').get(0).sheet.insertRule('td:nth-child(' + (config.tableHeaders.values.indexOf(col)+1) + ') { white-space: nowrap }', 0);
        });        
    }
    config.table = $('#table').DataTable({
        data: geoJSON2Table(),
        searching: false,
        pageLength: 100,
        fixedHeader: true,
        columns: config.tableHeaders.labels.map((header) => { return {'title': header} })
    });
}

function updateTable(force) {
    // table create/update with large number of rows is slow, only do it if visible
    if ($('#table-container').is(':visible') || force) {
        if (config.table == null) {
            createTable();
        } else if (config.tableDirty) {
            config.table.clear();
            config.table.rows.add(geoJSON2Table()).draw();
        }
        config.tableDirty = false;
    } else {
        config.tableDirty = true;
    }
}

function geoJSON2Table() {  // TODO rework?
    return config.geojson_filtered.features.map(feature => {
        return config.tableHeaders.values.map((header) => {
            let value = feature.properties[header];
            if ('displayValue' in config.tableHeaders && Object.keys(config.tableHeaders.displayValue).includes(header)) {
                value = config[config.tableHeaders.displayValue[header]].values[value];
            }
            if ('appendValue' in config.tableHeaders && Object.keys(config.tableHeaders.appendValue).includes(header)) {
                value += ' ' + config[config.tableHeaders.appendValue[header]].values[feature.properties[config[config.tableHeaders.appendValue[header]].field]];
            }
            if ('clickColumns' in config.tableHeaders && config.tableHeaders.clickColumns.includes(header)) {
                value = "<a href='" + feature.properties[config.urlField] + "' target='_blank'>" + value + '</a>';
            }
            return value;
        });
    });
}


/*
  Modals
*/
function setHighlightFilter(links) {
    if (! Array.isArray(links)) links = [links];
    let filter;
    let highlightExpression = [
        'in',
        ['get', config.linkField],
        ['literal', links]
    ];
    if (config.filterExpression != null) {
        filter = JSON.parse(JSON.stringify(config.filterExpression));
        filter.push(highlightExpression);
    } else {
        filter = ['all', highlightExpression];
    }
    config.layers.forEach(layer => {
        filter.push(['==', ['geometry-type'],
            map.getLayer(layer).type === 'line' ? 'LineString' : 'Point'
        ]);
        map.setFilter(layer + '-highlighted', filter);
    });
}

/* Creates the modal that pops up after clicking an asset */
function displayDetails(features) {
    if (typeof features == 'string') {
        features = JSON.parse(features);
    }
    var detail_text = '';
    var location_text = '';

    Object.keys(config.detailView).forEach((detail) => {
        const value = features[0].properties[detail];
        const invalidValues = ['', 'unknown', 'undefined', 'nan', null, 0, []];
        if (invalidValues.includes(value) || Number.isNaN(value)) {
            detail_text += ''
        } else if (Object.keys(config.detailView[detail]).includes('display')) {
            // TODO remove unused options from this if-statement
            if (config.detailView[detail]['display'] === 'heading') {
                detail_text += '<h4>' + features[0].properties[detail] + '</h4>';
            } else if (config.detailView[detail]['display'] === 'simple_markup') {
                let value = features[0].properties[detail];
                if (value && value !== '') {
                    // Extract URL if present
                    const urlMatch = value.match(/(https?:\/\/[^\s]+)/);
                    if (urlMatch) {
                        const url = urlMatch[1];
                        const textWithoutUrl = value.replace(url, '').trim();
                        detail_text += '<br/><div>' + textWithoutUrl + ' <a href="' + url + '" target="_blank"> here </a></div>';
                    } else {
                        detail_text += '<br/><div>' + value + '</div><br/>';
                    }
                }
            } else if (config.detailView[detail]['display'] === 'join') {  // TODO To delete, likely
                let join_array = features.map((feature) => feature.properties[detail]);
                join_array = join_array.filter((value, index, array) => array.indexOf(value) === index);
                if (join_array.length > 1) {
                    if (Object.keys(config.detailView[detail]).includes('label')) {
                        detail_text += '<span class="fw-bold">' + config.detailView[detail]['label'][1] + '</span>: ';
                    }
                    detail_text += '<span class="text-capitalize">' + join_array.join(',').replaceAll('_', ' ') + '</span><br/>';
                } else {
                    if (Object.keys(config.detailView[detail]).includes('label')) {
                        detail_text += '<span class="fw-bold">' + config.detailView[detail]['label'][0] + '</span>: ';
                    }
                    detail_text += '<span class="text-capitalize">' + join_array[0].replaceAll('_', ' ') + '</span><br/>';
                }
            } else if (config.detailView[detail]['display'] === 'range') {  // TODO To delete, likely
                let greatest = features.reduce((accumulator, feature) => {
                    return (feature.properties[detail] !== '' && feature.properties[detail] > accumulator ? feature.properties[detail] : accumulator);
                }, 0);
                let least = features.reduce((accumulator, feature) => {
                    return (feature.properties[detail] !== '' && feature.properties[detail] < accumulator ? feature.properties[detail] : accumulator);
                }, 5000);

                if (least !== 5000) {
                    if (least === greatest) {
                        detail_text += '<span class="fw-bold">' + config.detailView[detail]['label'][0] + '</span>: ' + least.toString() + '<br/>';
                    } else {
                        detail_text += '<span class="fw-bold">' + config.detailView[detail]['label'][1] + '</span>: ' + least.toString() + ' - ' + greatest.toString() + '<br/>';
                    }
                }
            } else if (config.detailView[detail]['display'] === 'hyperlink') {  // TODO To delete, likely
                detail_text += '<br/><a href="' + features[0].properties[detail] + '" target="_blank">More Info on the related infrastructure project here</a><br/>';
            } else if (config.detailView[detail]['display'] === 'location') {
                if (Object.keys(features[0].properties).includes(detail)) {
                    if (location_text.length > 0) {
                        location_text += ', ';
                    }
                    location_text += features[0].properties[detail];
                }
            } else if (config.detailView[detail]['display'] === 'colorcoded') {  // TODO To delete, likely
                // to create the circle dot we have for most status
                // if it has this colorcoded label then it goes to the color dictionary
                // matches up the field name, uses fieldLabel to display label and then also uses color
                let colorLabel = features.map((feature) => feature.properties[detail]);
                detail_text += '<span class="fw-bold">' + config.color_association.fieldLabel + '</span>: ' +
                    '<span class="legend-dot" style="background-color:' + config.color_association.values[features[0].properties[config.color_association.field]] + '"></span>' +
                    '<span class="text-capitalize">' + features[0].properties[config.color_association.field] + '</span><br/>';
            }
        } else if (Object.keys(config.detailView[detail]).includes('table')) {  // make small table in detail view popup
            const tableConfig = config.detailView[detail];
            const tableTitle = tableConfig.table;
            const headerMap = tableConfig.tableHeaders;
            const table_data_as_array = features[0].properties[detail];
            if (!Array.isArray(table_data_as_array) || table_data_as_array.length === 0) { return; }

            let tableHtml = '<br/>';
            if (tableTitle) {
                tableHtml += `<div style='font-size: 0.75rem; font-weight: 600; margin-bottom: 5px;'>${tableTitle}</div>`;
            }

            tableHtml += `
                <table class='table table-sm table-bordered' style='font-size: 0.75rem;'>
                    <thead>
                        <tr>`;

            // populate header row of the table
            const keys = Object.keys(headerMap);
            keys.forEach(key => {
                tableHtml += `
                    <th style='text-transform: none; font-size: 0.7rem;'>
                        ${headerMap[key]}
                    </th>`;
            });

            tableHtml += `</tr>
                    </thead>
                    <tbody>`;

            // populate each row of the table
            table_data_as_array.forEach(row => {
                tableHtml += '<tr>';
                keys.forEach(key => {
                    let value = row[key];
                    if (value === undefined || value === null) {
                        value = '';
                    }

                    // Numeric formatting if applicable
                    const num = Number(value);
                    const displayValue = Number.isFinite(num)
                        ? num.toLocaleString()
                        : value;

                    tableHtml += `<td>${displayValue}</td>`;
                });
                tableHtml += '</tr>';
            });

            tableHtml += `</tbody>
                </table>`;

            detail_text += tableHtml;
        } else {
            const value = features[0].properties[detail];
            const invalidValues = ["", undefined, 0, "nan", null, "Unknown [unknown %]", "unknown"];
            if (!invalidValues.includes(value)) {
                if (Object.keys(config.detailView[detail]).includes('label')) {
                    detail_text += '<span class="fw-bold">' + config.detailView[detail]['label'] + '</span>: ' + features[0].properties[detail];
                    if (Object.keys(config.detailView[detail]).includes('trailing-label')) {  // if the value has a trailing label (eg unit of measurement)
                        detail_text += ' ' + config.detailView[detail]['trailing-label'];
                    }
                    detail_text += '<br/>';
                }
            }
        }
    });

    // get the asset and capacity label
    // if a dict and not a string (eg in multi-tracker maps), get the specific labels for each tracker within
    let assetLabel = typeof config.assetLabel === 'string'
        ? config.assetLabel
        : config.assetLabel.values[features[0].properties[config.assetLabel.field]];
    let capacityLabel = typeof config.capacityLabel === 'string'
        ? config.capacityLabel
        : config.capacityLabel.values[features[0].properties[config.capacityLabel.field]];

    if (config.includeCapacityByStatusInDetailView) {
        // TODO lots of room for optimization in this if-statement body
        if (features.length > 1) {  // if there are multiple units in this project
            let filterIndex = 0;
            for (const[index, filter] of config.filters.entries()) {
                if (filter.field === config.statusField) {
                    filterIndex = index;
                }
            }

            // Initialize capacity and count objects using reduce to avoid summary build bug
            // first builds an array of filter values then with reduce makes it an object
            // then initializes the start point with 0
            let capacity = Object.fromEntries(
                config.filters[filterIndex].values.map(f => [f, 0])
            );

            let count = Object.fromEntries(
                config.filters[filterIndex].values.map(f => [f, 0])
            );

            features.forEach((feature) => {
                let capacityFloat = feature.properties[config.capacityDisplayField]

                if (typeof feature.properties[config.capacityDisplayField] === 'string') {
                    capacityFloat = Number(capacityFloat);

                } else {
                    capacityFloat = parseFloat(capacityFloat);
                }

                if (typeof capacity[feature.properties[config.statusField]] === 'undefined') {
                    capacity[feature.properties[config.statusField]] = 0;
                }
                capacity[feature.properties[config.statusField]] += capacityFloat;

                if (typeof count[feature.properties[config.statusField]] === 'undefined') {
                    count[feature.properties[config.statusField]] = 0;
                }

                count[feature.properties[config.statusField]]++;
            });

            let detail_capacity = '';
            Object.keys(count).forEach((k) => {
                // status legend mapping
                if (k === 'proposed-plus') {
                    display_k = 'proposed/announced/<br>discovered';
                } else if (k === 'mothballed-plus') {
                    display_k = 'mothballed/idle/shut in';
                } else if (k === 'construction-plus') {
                    display_k = 'construction/in development'
                } else if (k === 'retired-plus') {
                    display_k = 'retired/closed/<br>decommissioned';
                } else {
                    display_k = k;
                }

                if (capacity[k] === 0) {
                    if (config.color_association.field === config.statusField) {
                        if (count[k] !== 0) {
                            // TODO I need to have a dictionary to reverse from status-legend to status Display so we can still filter by status legend but show the status display via k
                            detail_capacity +=
                                '<div class="row">' +
                                '<div class="col-5">' +
                                '<span class="legend-dot" style="background-color:' + config.color_association.values[k] + '"></span>' +
                                display_k +
                                '</div>' +
                                '<div class="col-4">' + 'Not found or N/A' + '</div>' +
                                '<div class="col-3">' + count[k] + ' of ' + features.length + '</div>' +
                                '</div>';
                        }
                    } else {
                        if (count[k] !== 0) {
                            detail_capacity +=
                                '<div class="row">' +
                                '<div class="col-5">' + display_k + '</div>' +
                                '<div class="col-4">' + 'Not found or N/A' + '</div>' +
                                '<div class="col-3">' + count[k] + ' of ' + features.length + '</div>' +
                                '</div>';
                        }
                    }
                } else {
                    if (config.color_association.field === config.statusField) {
                        if (count[k] !== 0) {
                            // TODO I need to have a dictionary to reverse from status-legend to status Display so we can still filter by status legend but show the status display via k
                            detail_capacity +=
                                '<div class="row">' +
                                '<div class="col-5">' +
                                '<span class="legend-dot" style="background-color:' + config.color_association.values[k] + '"></span>' +
                                display_k +
                                '</div>' +
                                '<div class="col-4">' + Number(capacity[k]).toLocaleString() + '</div>' +
                                '<div class="col-3">' + count[k] + ' of ' + features.length + '</div>' +
                                '</div>';
                        }
                    } else {
                        if (count[k] !== 0) {
                            detail_capacity +=
                                '<div class="row">' +
                                '<div class="col-5">' + display_k + '</div>' +
                                '<div class="col-4">' + Number(capacity[k]).toLocaleString() + '</div>' +
                                '<div class="col-3">' + count[k] + ' of ' + features.length + '</div>' +
                                '</div>';
                        }
                    }
                }
            });
            detail_text +=
                '<div>' +
                '<div class="row pt-2 justify-content-md-center">Total ' + assetLabel + ': ' + features.length + '</div>' +
                '<div class="row" style="height: 2px"><hr/></div>' +
                '<div class="row ">' +
                '<div class="col-5 text-capitalize">Status</div>' +
                '<div class="col-4">Capacity (' + capacityLabel + ')</div>' +
                '<div class="col-3">#&nbsp;of&nbsp;' + assetLabel + '</div>' +
                '</div>' +
                detail_capacity +
                '</div>';
        }
        // else when there is only one feature or one unit per project in the popup modal
        else {
            // add default capacity to detail view popup
            if (config.useDefaultCapacityInDetailView) {
                let capacityFloatandLabel;
                let capacity = features[0].properties[config.capacityDisplayField];

                if (capacity === '') {  // if capacity is an empty string
                    capacityFloatandLabel = 'Not found or N/A';
                } else if (!isNaN(Number(capacity))) {  // if capacity is a number
                    let capacityFloat = Number(capacity);
                    capacityFloatandLabel = parseFloat(capacityFloat).toFixed(2).replace(/\.?0+$/, '') + ' ' + capacityLabel;
                } else {  // if capacity is any other string
                    capacityFloatandLabel = capacity;
                }
                detail_text += '<span class="fw-bold text-capitalize">Capacity</span>: ' + capacityFloatandLabel + '<br/>';
            }

            // add status to detail view popup
            detail_text += '<span class="fw-bold text-capitalize">Status</span>: '
            if (config.color_association.field == config.statusField) {  // add color dot if it is an expected status
                detail_text += '<span class="legend-dot" style="background-color:' + config.color_association.values[features[0].properties[config.statusDisplayField]] + '"></span>'
            }
            detail_text += '<span class="text-capitalize">' + features[0].properties[config.statusDisplayField] + '</span><br/>';
        }
    } else {  // only put project-wide status in detail view
        if (config.color_association.field === 'status') {
            detail_text += '<span class="fw-bold text-capitalize">Status</span>: ' +
                '<span class="legend-dot" style="background-color:' + config.color_association.values[features[0].properties[config.statusDisplayField]] + '"></span>' +
                '<span class="text-lowercase">' + features[0].properties[config.statusDisplayField] + '</span><br/>';
        }
    }

    //Location by azizah from <a href="https://thenounproject.com/browse/icons/term/location/" target="_blank" title="Location Icons">Noun Project</a> (CC BY 3.0)
    //Arrow Back by Nursila from <a href="https://thenounproject.com/browse/icons/term/arrow-back/" target="_blank" title="Arrow Back Icons">Noun Project</a> (CC BY 3.0)
    $('.modal-body').html(
        '<div class="row m-0">' +
        '<div class="col-sm-5 rounded-top-left-1" id="detail-satellite" style="background-image:url(' + buildSatImage(features) + ')">' +
        (config.selectModal !== '' ? '<span onClick="showSelectModal()"><img id="modal-back" src="../../src/img/back-arrow.svg" /></span>' : '') +
        '<img id="detail-location-pin" src="../../src/img/location.svg" width="30">' +

        '<span class="detail-location">' + location_text + '</span><br/>' +
        '<span class="align-bottom p-1" id="detail-more-info"><a href="' + features[0].properties[config.urlField] + '" target="_blank">MORE INFO</a></span>' +
        (config.showAllPhases && features.length > 1 ? '<span class="align-bottom p-1" id="detail-all-phases"><a onClick="showAllPhases(\'' + features[0].properties[config.linkField] + '\')">ALL PHASES</a></span>' : '') +
        '</div>' +
        '<div class="col-sm-7 py-2" id="total_in_view">' + detail_text + '</div>' +
        '</div>');

    setHighlightFilter(features[0].properties[config.linkField]);
}

function enableModal() {
    config.modal = new bootstrap.Modal($('#modal'));
    $('#modal').on('hidden.bs.modal', function (event) {
        setHighlightFilter('');
    })
}

function buildSatImage(features) {
    let location_arg = '';
    let bbox = geoJSONBBox({'type': 'FeatureCollection', features: features });

    if (bbox[0] === bbox[2] && bbox[1] === bbox[3]) {
        location_arg = bbox[0].toString() + ',' + bbox[1].toString() + ',' + config.img_detail_zoom.toString();
    } else {
        location_arg = '[' + bbox.join(',') + ']';
    }

    return 'https://api.mapbox.com/styles/v1/mapbox/satellite-v9/static/' + location_arg + '/350x350?attribution=false&logo=false&access_token=' + config.accessToken;
}

function showAllPhases(link) {
    config.modal.hide();
    setHighlightFilter(link);
    var bbox = geoJSONBBox({'type': 'FeatureCollection', features: config.linked_assets[link] });
    map.flyTo({center: [(bbox[0]+bbox[2])/2,(bbox[1]+bbox[3])/2], zoom: config.phasesZoom});
}

function showSelectModal() {
    $('.modal-body').html(config.selectModal);
}


/* 
  Toolbar Filters
*/
function enableNavFilters() {
    enableSearch();
    enableSearchSelect();
    enableCountrySelect();

    document.addEventListener('DOMContentLoaded', function() {
        // make it as accordion for smaller screens
        if (window.innerWidth < 992) {  // TODO Magic number
            // close all inner dropdowns when parent is closed
            $('.navbar .dropup').forEach((everydropdown) => {
                everydropdown.addEventListener('hidden.bs.dropdown', function () {
                    // after dropdown is hidden, then find all submenus
                    $('.submenu').forEach((everysubmenu) => {
                        // hide every submenu as well
                        everysubmenu.style.display = 'none';
                    });
                })
            });

            $('.dropdown-menu a').forEach((element) => {
                element.addEventListener('click', function (e) {
                    let nextEl = this.nextElementSibling;
                    if (nextEl && nextEl.classList.contains('submenu')) {
                        // prevent opening link if link needs to open dropdown
                        e.preventDefault();
                        if (nextEl.style.display === 'block') {
                            nextEl.style.display = 'none';
                        } else {
                            nextEl.style.display = 'block';
                        }
                    }
                });
            })
        }
        // end if innerWidth  // TODO?
    }); 
}

function enableCountrySelect() {
    $.ajax({
        type: 'GET',
        url: config.countryFile,
        dataType: 'json',
        success: function(jsonData) { config.countries = jsonData; buildCountrySelect(); }
    });
}

function buildCountrySelect() {
    if (config.allCountrySelect) {
        $('#country_select').append('<li><a class="country-dropdown-item dropdown-item h4" data-countries="" data-countryText="" href="#">all</a></li>');
    }
    Object.keys(config.countries).forEach((continent, continent_idx) => {
        let dropdown_html = '';
        // Add continent as a selectable item (clicking selects all countries in continent)
        dropdown_html += `<li class="continent-li"><a class="country-dropdown-item dropdown-item h4 continent-select" data-countries="${config.countries[continent].join(';')}" data-countryText="${continent}" href="#">${continent}</a>`;
        dropdown_html += '<ul class="submenu dropdown-menu">';
        config.countries[continent].forEach((country, country_idx) => {
            dropdown_html += `<li><a class="h5 country-dropdown-item dropdown-item" data-countries="${country}" data-countryText="${country}" href="#">${country}</a></li>`;
            if (country_idx !== config.countries[continent].length - 1) {
                dropdown_html += '<li><hr class="dropdown-divider"></li>';
            }
        });
        dropdown_html += '</ul></li>';

        if (continent_idx !== Object.keys(config.countries).length - 1) {
            dropdown_html += '<li><hr class="dropdown-divider"></li>';
        }

        $('#country_select').append(dropdown_html);
    });

    // Click handler: select continent or country
    $('.country-dropdown-item').each(function() {
        this.addEventListener('click', function(e) {
            // Only filter if not just expanding submenu
            config.selectedCountryText = this.dataset.countrytext;
            config.selectedCountries = (this.dataset.countries.length > 0 ? this.dataset.countries.split(';') : []);
            $('#selectedCountryLabel').text(config.selectedCountryText || 'all');

            filterData();
        });
    });

    // Hover logic for continent: show submenu, keep open when moving to submenu
    $('.continent-li').each(function() {
        let $li = $(this);
        let $submenu = $li.children('.submenu');
        let submenuTimeout;

        // Show submenu on hover
        $li.children('.continent-select').on('mouseenter', function() {
            clearTimeout(submenuTimeout);
            $submenu.css({ display: 'block' });
        });

        // Hide submenu when mouse leaves both continent and submenu
        $li.children('.continent-select').on('mouseleave', function() {
            submenuTimeout = setTimeout(() => {
                $submenu.css({ display: 'none' });
            }, 200);
        });

        $submenu.on('mouseenter', function() {
            clearTimeout(submenuTimeout);
            $submenu.css({ display: 'block' });
        });

        $submenu.on('mouseleave', function() {
            submenuTimeout = setTimeout(() => {
                $submenu.css({ display: 'none' });
            }, 200);
        });
    });

    config.selectedCountries = [];
    config.selectedCountryText = '';
}

// this removes diacritics in the data so that when you search you get all the possible options ignored special diacritics
// this is applied so that only the non tile maps are impacted
// for tile maps it'll be too slow so we do it in data prep (having a special search column and adding that to the column options to search within)
// TODO possibly make redundant by prepping geojson files properly
function removeDiacritics(value) {
    let noDiacriticsValue = value;
    for (const char of value) {
        for (const [key, values] of Object.entries(diacriticMap)) {
            if (values.includes(char)) {
                noDiacriticsValue = noDiacriticsValue.replace(char, key);
            }
        }
    }
    return noDiacriticsValue;
}

function enableSearch() {
    $('#search-text').on('keyup paste', debounce(function() {
        config.searchText = $('#search-text').val().toLowerCase();

        filterData();
    }, 500));
    config.searchText = '';
}

function enableSearchSelect() {
    let dropdown_html = '';
    let allSearchFields = [];
    Object.keys(config.searchFields).forEach((field_label) => {
        dropdown_html += `<li><a class="h5 search-dropdown-item dropdown-item" data-searchFieldText="${field_label}" data-searchFields="${config.searchFields[field_label].join(',')}" href="#">${field_label}</a></li>`;
        allSearchFields = allSearchFields.concat(config.searchFields[field_label]);
    });
    dropdown_html = `<li><a class="h5 search-dropdown-item dropdown-item" data-searchFieldText="all" data-searchFields="${allSearchFields.join(',')}" href="#">all</a></li>` 
        + dropdown_html;
    $('#search_type_select').append(dropdown_html);

    $('.search-dropdown-item').each(function() {
        this.addEventListener('click', function() {
            config.selectedSearchFields = this.dataset.searchfields;
            $('#selectedSearchLabel').text(this.dataset.searchfieldtext);

            filterData();
        });
    });

    config.selectedSearchFields = allSearchFields.join(',');
}
function enableClearSearch() {

function enableResetAll() {
    $('#selectedCountryLabel').text('all');
    config.selectedCountryText = '';
    config.selectedCountries = [];
    
    // // clear search text by making search text ''
    config.searchText = ''; 
    $('#search-text').val('');

    // put search field category back to all
    let allSearchFields = [];
    Object.keys(config.searchFields).forEach((field_label) => {
        allSearchFields = allSearchFields.concat(config.searchFields[field_label]);
    });
    config.selectedSearchFields = allSearchFields.join(',');
    $('#selectedSearchLabel').text('all');

    filterData();
}  


/* 
  Util Functions
*/
function getUniqueFeatures(features, comparatorProperty) {
    const uniqueIds = new Set();
    const uniqueFeatures = [];
    for (const feature of features) {
        const id = feature.properties[comparatorProperty];
        if (!uniqueIds.has(id)) {
            uniqueIds.add(id);
            uniqueFeatures.push(feature);
        }
    }
    return uniqueFeatures;
}

function debounce(func, wait, immediate) {
    var timeout;
    return function() {
        var context = this, args = arguments;
        var later = function() {
            timeout = null;
            if (!immediate) func.apply(context, args);
        };
        var callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) func.apply(context, args);
    };
}

/* from https://github.com/geosquare/geojson-bbox */
function geoJSONBBox(gj) {
    var coords, bbox;
    if (!gj.hasOwnProperty('type')) return;
    coords = getCoordinatesDump(gj);
    bbox = [
        Number.POSITIVE_INFINITY, Number.POSITIVE_INFINITY,
        Number.NEGATIVE_INFINITY, Number.NEGATIVE_INFINITY,
    ];
    return coords.reduce(function(prev,coord) {
        return [
            Math.min(coord[0], prev[0]),
            Math.min(coord[1], prev[1]),
            Math.max(coord[0], prev[2]),
            Math.max(coord[1], prev[3])
        ];
    }, bbox);
}
  
function getCoordinatesDump(gj) {
    let coords;
    if (gj.type === 'Point') {
        coords = [gj.coordinates];
    } else if (gj.type === 'LineString' || gj.type === 'MultiPoint') {
        coords = gj.coordinates;
    } else if (gj.type === 'Polygon' || gj.type === 'MultiLineString') {
        coords = gj.coordinates.reduce(function(dump,part) {
            return dump.concat(part);
        }, []);
    } else if (gj.type === 'MultiPolygon') {
        coords = gj.coordinates.reduce(function(dump,poly) {
            return dump.concat(poly.reduce(function(points,part) {
                return points.concat(part);
            },[]));
        },[]);
    } else if (gj.type === 'Feature') {
        coords = getCoordinatesDump(gj.geometry);
    } else if (gj.type === 'GeometryCollection') {
        coords = gj.geometries.reduce(function(dump,g) {
            return dump.concat(getCoordinatesDump(g));
        },[]);
    } else if (gj.type === 'FeatureCollection') {
        coords = gj.features.reduce(function(dump,f) {
            return dump.concat(getCoordinatesDump(f));
        },[]);
    }
    return coords;
}

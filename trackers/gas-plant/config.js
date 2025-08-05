
var config = {

    geojson: 'https://publicgemdata.nyc3.cdn.digitaloceanspaces.com/GOGPT/2025-08-05/gogpt_map_2025-08-05.geojson',
    linkField: 'pid',
    countryField: 'areas',
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
    filters: [
        {
            field: 'status',
            values: ['operating','construction','pre-construction','announced','retired','cancelled','shelved','mothballed'],
        }
    ],
    capacityField: 'scaling-capacity',
    capacityDisplayField: 'capacity-table',
    capacityLabel: '(MW)',
    assetFullLabel: "Gas Units",
    assetLabel: 'units',
    nameField: 'name',
    tableHeaders: {
        values: ['name','unit-name', 'owner', 'parent', 'capacity-table', 'status', 'region', 'areas', 'subnat', 'start-year'],
        labels: ['Plant','Unit','Owner','Parent','Capacity (MW)','Status','Region','Country/Area(s)','Subnational unit (province/state)','Start year'],
        clickColumns: ['name'],
        rightAlign: ['unit-name','capacity-table','start-year'],
        toLocaleString: ['capacity-(mw)'],
        removeLastComma: ['areas']
    },
    searchFields: { 
        'Plant': ['name'], 
        'Companies': ['owner(s)', 'parent(s)', 'operator(s)'],
        'Start Year': ['start-year']
    },
    detailView: {
        'name': {'display': 'heading'},
        // 'project': {},
        'owner(s)': {'label': 'Owner(s)'},
        'parent(s)': {'label': 'Parent(s)'},
        'turbine/engine-technology': {'label': 'Turbine/Engine Technology'},
        'fuel': {'label': 'Fuel'},
        'start-year': {'label': 'Start year'},
        'areas-subnat-sat-display': {'display': 'location'},
        'areas': {'display': 'location'}
    }
};

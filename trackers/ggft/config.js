var config = {
    // geojson:'https://publicgemdata.nyc3.cdn.digitaloceanspaces.com/ggft/2025-12/ggft_map_2025-12-05.geojson',
    geojson: 'https://publicgemdata.nyc3.cdn.digitaloceanspaces.com/ggft/2025-12/ggft_map_2025-12-19.geojson',
    geometries: ['Point'],
    // copied starting coords from Asia map for now
    // center: [60, 20], # was for Asia, commenting out now.
    // zoomFactor: 1.9,
    // img_detail_zoom: 10,
    center: [0, 0],

    statusField: 'finstatus', // financing status
    statusDisplayField: 'finstatus', // need shorter names? where does ficing come from ... should not be there
    
    
    color: {

        field: 'finstatus',
        values: {  
            // 'known': 'red',
            'Known': 'red',
            'Unknown': 'blue'
        }
    },

    filters: [

        {
            field: 'finstatus',
            label: 'Financing Status',
            values: ['Known', 'Unknown'],
            values_labels: ['Known project finance','No known project finance'],
            primary: true

        },
        {
            field: 'infra-filter',
            label: 'Infrastructure Type',
            values: ['Gas_Power_Plants', 'LNG_Terminals'], // frontend does not like spaces put _ there
            values_labels: ['Gas Plants', 'LNG Terminals'],
            // values_hover_text: ['hover text for fuels', '', '']
            // field_hover_text: 'Hydrogen projects are classified as either planning to blend hydrogen into methane gas or use 100% hydrogen. For the projects that plan to use hydrogen but do not specify a percentage, it is assumed they are blending. Blended projects only appear as hydrogen projects and do not also appear as methane projects, though they will use both fuel types.',
        },
        {
            field: 'finbucket',//'financing', 
            label: ' Total known project finance', // info button explaining what it means
            values: ['na','low', 'mid-low', 'mid', 'mid-high', 'high'],//'high'], # mid-low', 'low', 'mid-high', 'na', 'high'
            values_labels: ['Not available', '$1-500 million', '$501-1000 million', '$1001-1500 million', '$1501-2000 million', '$2001+ million'], //'$2001-2500 million'
            // values_hover_text: ['hover tesct for fuels', '', '']
            // field_hover_text: 'GEM assesses whether hydrogen projects have met criteria (specific to each infrastructure type) demonstrating progress toward completion, since many hydrogen projects lack core details or commitments from stakeholders. For more information on these criteria, see the <a href="https://globalenergymonitor.org/projects/europe-gas-tracker/methodology/">EGT methodology page</a>'

        },

    ],

    
    /* Labels for describing the assets */
    assetFullLabel: "Units",
    assetLabel: 'units',

    capacityField: 'project-fin-scaling', // used for sizing assets NOT display // all na 'project_cap_fin_scaling', // this will be financing, and smallest value when its unknown
    linkField: 'pid',
    capacityLabel: 'million dollars', // bug with solo ones showing weird status and capacity
    showMaxCapacity: false,

    nameField: 'name', // name of projects
    countryFile: 'countries.json',
    allCountrySelect: false,
    countryField: 'areas', // country
    // multiCountry: true,
    capacityDisplayField: 'fin-by-transac', // need this since it'll sum .. need to make float, this is what gets used in site.js for all details. 

    useDefaultCapacityInDetailView: false, //originally created this to allow for both finance data and capacity data by unit in the popup, but should be useful to fix the issue when there is one unit and we do not want capacity (in this case financing info) to show up because project level financing is already shown when available

    // if they want to include capacity values by unit in the popup would need this, but they don't say it's a priority so comment out
    // capacityLabel2:  {       
    //     field: 'infra-filter',
    //     values: {
    //         'LNG_Terminals': 'MTPA',
    //         'Gas_Power_Plants': 'MW'
    // },

    // FOR DEBUGGING  
    // 'project-fin-scaling','fin-by-transac', 
    // 'debug capacityField project-fin-scaling','debug capacityDisplayField fin-by-transac',
    tableHeaders: {
        values: ['fin', 'name', 'unitname', 'debtequityelse','owner', 'parent', 'importexport','opstatus', 'areas', 'startyear', 'capacitymw', 'capacitymtpa'],
        labels: ['Financier', 'Project Name', 'Unit Name','Financing Type','Owner', 'Parent','Terminal Facility Type', 'Operational Status','Country/Area(s)','Start year', 'Capacity (MW)', 'Capacity (MTPA)'],
        clickColumns: ['name'],
        rightAlign: ['startyear',], 
        removeLastComma: ['areas'], 
        toLocaleString: [''],


    },
    searchFields: { 'Project': ['name', 'othername', 'localname', 'name-search', 'unit-name', 'unitid', 'pid'], 
        'Project Financier': ['owner', 'parent', 'fin',  'owner-search', 'parent-search'],
   

        
    },
    detailView: {
        'name': {'display': 'heading'},
        // 'unitname': {'label': 'Unit Name'},
        'debt-project-financing': {'label': 'Debt Project Financing ($ million)'},
        'equity-project-financing': {'label': 'Equity Project Financing ($ million)'},
        // 'debtequityelse': {'label': 'Financing Type'},
        'startyear': {'label': 'Start Year'},
        'fin': {'label': 'Financier'},
        'opstatus': {'label': 'Operating Status'},
        // 'capacitymtpa': {'label': 'Capacity (mtpa)'},
        // 'capacitymw': {'label': 'Capacity (mw)'},
        'owner': {'label': 'Owner'},
        'parent': {'label': 'Parent'},
        'areas': {'display': 'location'}, 
    },

        /* radius associated with minimum/maximum value on map */
    minRadius: 4,
    maxRadius: 10,
    // minLineWidth: 1,
    // maxLineWidth: 3,

    // /* radius to increase min/max to under high zoom */
    highZoomMinRadius: 4,
    highZoomMaxRadius: 32,
    // highZoomMinLineWidth: 4,
    // highZoomMaxLineWidth: 32,
    
    showAllPhases: true




};
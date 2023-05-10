var config = {
    accessToken: 'pk.eyJ1IjoiZWFydGhyaXNlIiwiYSI6ImNqeDExNmtrZzAwM2E0OW16eHZ1dzg1eWEifQ.8LTFXyY-n7OsZOoWN9ONPQ',
    csv: 'data.csv',
    color: { /* will be processed both into style json for paint circle-color property, and for legend. 
            what's right property name?? is color also listing values used in the summary? 
            should this just be made part of the filter? that might allow to address multiple properties */
        field: 'status',
        values: {
            //update this list
            'operating': '#ff0000',
            'pre-construction': '#0000ff',
            'construction': '#00ff00',
            'retired': '#000000',
            'cancelled': '#000000',
            'pre-permit': '#0000ff',
            'shelved': '#000000',
            'mothballed': '#000000',
            'announced': '#0000ff',
            'permitted': '#00ff00'
            // contining
        }
    },
    paint: {
        /* this could be made dynamic based on the range of values in the data */
        'circle-radius': ["max", 3, ["/", ["to-number", ["get", "capacity"]], 500]]
    },
    filters: [
        {
            field: 'status',
            /* values need to be specified for ordering */
            values: ['operating','construction','pre-construction','retired','cancelled','pre-permit','shelved','mothballed','announced','permitted']
        }
    ],
    capacity_field: 'capacity',
    search_fields: ['name', 'country', 'company'] /* company could be owner, operator or parent, need to specify */

}
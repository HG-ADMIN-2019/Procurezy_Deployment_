let url = window.location.href
is_edit = false
split_url = url.split('/')
last_index = split_url.slice(-1)[0]
let document_number = 'create';
if(last_index.includes('doc_number')){
    is_edit = true
    document_number = last_index.split('-')[1]
}
 
 
 // Function to create dropdown options based on the dropdown value passed
 const get_options_from_string = string => {
    var options = '<option value="" selected>Select</option>';

    if(string.includes(',')){
        values = string.split(',')
        for(i = 0; i < values.length; i++) {
        options += '<option value="'+ values[i] +'">' + values[i] + '</option>'
        }
    } else {
        if(string == 'Country'){
            for(i = 0; i < country.length; i++) {
                options += '<option value="'+ country[i]['country_code'] +'">' + country[i]['country_code'] + ' - ' + country[i]['country_name'] + '</option>'
            }
        }
        if(string == 'Currency'){
            for(i = 0; i < currency.length; i++) {
             options += '<option value="'+ currency[i]['currency_id'] +'">' + currency[i]['currency_id'] + ' - ' + currency[i]['description'] + '</option>'
            }
        }
    }
    return options;
}

// Function to restrict user from entering special characters in input boxes
const restrict_special_char = e => {
    var k;
    document.all ? k = e.keyCode : k = e.which;
    return ((k > 64 && k < 91) || (k > 96 && k < 123) || k == 8 || k == 32 || (k >= 48 && k <= 57));
}


const go_back_to_sc = () => {
    get_document_url = localStorage.getItem('opened_document-' + document_number)
    location.href = get_document_url + '/edit'
}
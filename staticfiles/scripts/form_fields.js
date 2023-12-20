eform_configured = 'eform_configured' in sessionStorage ? JSON.parse(sessionStorage.getItem("eform_configured")) : new Array();
used_timeframe_array = 'used_timeframe_array' in sessionStorage ? JSON.parse(sessionStorage.getItem("used_timeframe_array")) : new Array();

$(window).on('beforeunload', function () {
    if (eform_configured.length > 0) {
        sessionStorage.setItem("eform_configured", JSON.stringify(eform_configured));
        sessionStorage.setItem("used_timeframe_array", JSON.stringify(used_timeframe_array));
    }
});

window.onload = function () {
    $('#eform_details').hide();
    if (eform_configured.length > 0) {
        display_fields_from_array(true);
        $('#eform_details').show()
    }
}

//Display submenu  for purchaser and purchaser assist role
nav_bar_content_management() ;

// // Function to display options based on dropdown selections
// const get_dropdown_options = (element, index) => {
//     if (element == 'Country') {
//         return country_list
//     }
//     if (element == 'Currency') {
//         return currency_list
//     }
//     if (element == 'custom_options') {
//         if(index == ''){
//             comma_seperated_values = $('#added_dropdown_values').val()
//         } else {
//             comma_seperated_values = index
//         }
//         split_comma = comma_seperated_values.split(',')
//         var custom_options = new Array();
//         for (i = 0; i < split_comma.length; i++) {
//             value = split_comma[i].replace(/\s+/g, '')
//             if (value != '') {
//                 custom_options.push(value)
//             }
//         }
//         return custom_options
//     }
// }

// // Function to create form fields and appends it to array
// const create_fields = () => {
//     var label_name = document.getElementById('field_name').value
//     var input_type = document.getElementById('field_type').value
//     var is_required = document.getElementById('is_required').checked
//     var is_special_char = document.getElementById('allow_special_characters').checked

//     validations = create_popup_validations(input_type)
//     if (validations != '') {
//         $('#create_error_div').html(validations)
//         $('#create_error_div').show()
//         return
//     } else $('#create_error_div').hide()

//     var eform_object = {}

//     eform_object['input_type'] = input_type
//     eform_object['input_label'] = to_title_case(label_name)
//     eform_object['required'] = is_required
//     eform_object['allow_special_char'] = is_special_char

//     if (input_type == 'dropdown') {
//         dropdown_type = document.getElementById('select_dropdown').value
//         eform_object['dropdown_options'] = get_dropdown_options(dropdown_type, '')
//         eform_object['dropdown_type'] = dropdown_type
//     }

//     if (input_type == 'date') {
//         timeframe_value = document.getElementById('select_timeframe').value
//         used_timeframe_array.push(timeframe_value)
//     }

//     eform_configured.push(eform_object)
//     display_fields_from_array()

//     $('.dynamic_field').val('')
//     document.getElementById('is_required').checked = false
//     document.getElementById('allow_special_characters').checked = false
//     $('#create_new_fields_popup').modal('hide')
//     $('#eform_details').show()
//     $('#dropdown-values').hide()
//     $('#custom_options_div').hide()
//     $('#timeframe').hide()
// }

// Function to display create pop based on conditions
const create_field_popup = () => {
    if (eform_configured.length == 10) {
                   
                    var msg = "JMSG023";
                    var msg_type ;
                  msg_type = message_config_details(msg);
                  $("#error_msg_id").prop("hidden", false)

                  if(msg_type.message_type == "ERROR"){
                        display_message("error_msg_id", msg_type.messages_id_desc)
                  }
                  else if(msg_type.message_type == "WARNING"){
                     display_message("id_warning_msg_id", msg_type.messages_id_desc)
                  }
                  else if(msg_type.message_type == "INFORMATION"){
                     display_message("id_info_msg_id", msg_type.messages_id_desc)
                  }
                  var display = msg_type.messages_id_desc;
                  $('#save_error_div').html(display)

        $('#save_error_div').show()
        scroll_top()
        return
    } else {
        $('#save_error_div').hide()
        $('#special_character_div').hide()
        $('#create_error_div').hide()
        $('#create_new_fields_popup').modal('show')
        if (used_timeframe_array.includes('From Date')) {
            $('#value_to').prop('hidden', false)
            $('#value_on').prop('hidden', true)
            $('#value_from').prop('hidden', true)
        } else if (used_timeframe_array.includes('On Date')) {
            $('#value_to').prop('hidden', true)
            $('#value_on').prop('hidden', true)
            $('#value_from').prop('hidden', true)
        } else {
            $('#value_to').prop('hidden', true)
            $('#value_on').prop('hidden', false)
            $('#value_from').prop('hidden', false)
        }
    }
}

// Function to remove form elements from UI
const remove_element = (element) => {
    $('#remove_error_div').hide();
    var input_label = element.split('-')[0];
    var array_index = element.split('-')[1];
    var eform_array_input_type = eform_configured[array_index].field_data_type;

    if(eform_array_input_type == 'date'){
        used_timeframe_array.length = 0
    }
    if (array_index > -1) {
        eform_configured.splice(array_index, 1);
    }
    display_fields_from_array(false)
    if (eform_configured.length == 0) {
        $('#eform_details').hide()
        sessionStorage.removeItem('eform_configured')
        sessionStorage.removeItem('used_timeframe_array')
    }
    else {
        sessionStorage.setItem("eform_configured", JSON.stringify(eform_configured));
        sessionStorage.setItem("eform_configured", JSON.stringify(used_timeframe_array));
    }
}


const display_fields_from_array = (delete_disable_flag) => {
    $('#eform_body').empty()
    var div_content = '';

    $.each(eform_configured, function (index, value) {
        field_data_type = value['field_data_type'];
        field_name = value['field_name'];
        is_required = value['required'];
        var delete_html = ''
        if(delete_disable_flag){
            delete_html = '<button id="' + field_name + '-' + index + '" type="button" onclick="remove_element(this.id)"  class="btn btn-outline-danger btn-sm btn-delete toggle_mode" disabled><i class="far fa-trash-alt"></i></button>';
        }
        else{
            delete_html = '<button id="' + field_name + '-' + index + '" type="button" onclick="remove_element(this.id)"  class="btn btn-outline-danger btn-sm btn-delete toggle_mode"><i class="far fa-trash-alt"></i></button>';
        }

        var options = '<option value="" selected>Select</option>';

        if (field_data_type == 'dropdown') {
            get_dropdown = value['dropdown_options']
            get_dropdown_type = value['dropdown_type']
            if (get_dropdown_type == 'Currency'){
                for (i = 0; i < currency_list.length; i++) {
                    options += '<option value="' + currency_list[i]['currency_id'] + '">' + currency_list[i]['currency_id']+ ' - ' + currency_list[i]['description'] + '</option>'
                }
            }

            if (get_dropdown_type == 'Country'){
                for (i = 0; i < country_list.length; i++) {
                    options += '<option value="' + country_list[i]['country_code'] + '">' + country_list[i]['country_code']+ ' - ' + country_list[i]['country_name'] + '</option>'
                }
            }

            if (get_dropdown_type == 'dropdown_custom_options'){
                for (i = 0; i < get_dropdown.length; i++) {
                    options += '<option value="' + get_dropdown[i] + '">' + get_dropdown[i] + '</option>'
                }
            }
            
            div_content = '<div class="form-row eform-field-wrapper" id="array_index-' + index + '"><div class="form-group col-md-11"> <label  for="' + field_name + '">' + field_name + '</label><span id="span_' + field_name + '"></span> <select class="form-control toggle_mode">' + options + '</select></div> <div class="col-auto eform-field-btn-wrapper"> '+delete_html+'</div> </div>'
        }
        else if (field_data_type == 'checkbox') {
            div_content = '<div class="form-row eform-field-wrapper" id="array_index-' + index + '"> <div class="form-group col-md-11"> <input class="toggle_mode" type="' + field_data_type + '"> <label  for="' + field_name + '">' + field_name + '</label><span id="span_' + field_name + '"></span> </div> <div class="col-auto eform-field-btn-wrapper"> '+delete_html+'</div> </div>'
        }
        else if (field_data_type == 'textarea') {
            div_content = '<div class="form-row eform-field-wrapper" id="array_index-' + index + '"> <div class="form-group col-md-11"> <label  for="' + field_name + '">' + field_name + '</label><span id="span_' + field_name + '"></span> <textarea class="form-control toggle_mode"></textarea> </div> <div class="col-auto eform-field-btn-wrapper"> '+delete_html+'</div> </div>'
        }

        else if (field_data_type == 'date') {
            var date_type = $('input:radio[name="check_input_datetime_type"]:checked').attr('id');

            if(date_type == 'datetime_value_on'){
                div_content = '<div class="form-row eform-field-wrapper" id="array_index-' + index + '"> <div class="form-group col-md-11"> <label  for="' + field_name + '">' + field_name + '</label><span id="span_' + field_name + '"></span> <input class="form-control toggle_mode" type="' + field_data_type + '"> </div> <div class="col-auto eform-field-btn-wrapper"> '+delete_html+'</div> </div>'
            } else if(date_type == 'datetime_value_timeframe') {
                div_content = '<div class="form-row eform-field-wrapper" id="array_index-' + index + '"> <div class="form-group col-md-11"> <label for="">Form Date</label><span id="span_' + field_name + '"></span> <input class="form-control toggle_mode" type="date"> <label for="">To Date</label><span id="span_' + field_name + '"></span> <input class="form-control toggle_mode" type="date"> </div> <div class="col-auto eform-field-btn-wrapper"> '+delete_html+'</div> </div>'
            }
        }
        else {
            div_content = '<div class="form-row eform-field-wrapper" id="array_index-' + index + '"> <div class="form-group col-md-11"> <label  for="' + field_name + '">' + field_name + '</label><span id="span_' + field_name + '"></span> <input class="form-control toggle_mode" type="' + field_data_type + '"></div> <div class="col-auto eform-field-btn-wrapper"> '+delete_html+'</div> </div>'
        }

        $('#eform_body').append(div_content)
        if (is_required) {
            var required_label = document.getElementById('span_' + field_name);
            required_label.classList.add('hg_required');
        }
    });
}

const create_popup_validations = (field_data_type) => {
    var error_message = ''
    if (document.getElementById('field_name').value == '') {
           
                    var msg = "JMSG007";
                    var msg_type ;
                  msg_type = message_config_details(msg);
                  $("#error_msg_id").prop("hidden", false)

                  if(msg_type.message_type == "ERROR"){
                        display_message("error_msg_id", msg_type.messages_id_desc)
                  }
                  else if(msg_type.message_type == "WARNING"){
                     display_message("id_warning_msg_id", msg_type.messages_id_desc)
                  }
                  else if(msg_type.message_type == "INFORMATION"){
                     display_message("id_info_msg_id", msg_type.messages_id_desc)
                  }
                   var display5 = msg_type.messages_id_desc;
        error_message = display5+ "field name";
        return error_message
    }

    // if (document.getElementById('field_type').value == '') {
    //     error_message = messageConstants["JMSG007"] + "input type"
    //     return error_message
    // }

        // if (input_type == 'dropdown') {
        //     selected_dropdown = document.getElementById('select_dropdown').value
        //     if (selected_dropdown == '') {
        //         error_message = messageConstants["JMSG005"] + "dropdown values"
        //         return error_message
        //     }
        //     if (selected_dropdown == 'custom_options') {
        //         custom_options = document.getElementById('added_dropdown_values').value
        //         if (custom_options == '') {
        //             error_message = messageConstants["JMSG007"] + "custom options"
        //             return error_message
        //         }
        //         if (!custom_options.includes(',')) {
        //             error_message = messageConstants["JMSG029"];
        //             return error_message
        //         }
        //     }

        // }

    return error_message
}


const handle_all_dropdown_changes = (element) => {
    $('#special_character_div').hide()
    $('#timeframe').hide()
    $('#dropdown-values').hide()
    $('#custom_options_div').hide()
    if (element == '') return
    if (element == 'dropdown') {
        $('#dropdown-values').show()
    }

    if (element == 'text') {
        $('#special_character_div').show()
    }

    if (element == 'select_dropdown') {
        var selected_dropdown_value = document.getElementById('select_dropdown').value
        $('#dropdown-values').show()
        if (selected_dropdown_value == 'custom_options') {
            $('#field_name').val('')
            $('#custom_options_div').show()
        } else {
            $('#field_name').val(selected_dropdown_value)
        }
    }

    if (element == 'date') {
        if (used_timeframe_array.length == 2) {
                  
                    var msg = "JMSG023";
                    var msg_type ;
                  msg_type = message_config_details(msg);
                  $("#error_msg_id").prop("hidden", false)

                  if(msg_type.message_type == "ERROR"){
                        display_message("error_msg_id", msg_type.messages_id_desc)
                  }
                  else if(msg_type.message_type == "WARNING"){
                     display_message("id_warning_msg_id", msg_type.messages_id_desc)
                  }
                  else if(msg_type.message_type == "INFORMATION"){
                     display_message("id_info_msg_id", msg_type.messages_id_desc)
                  }
                  var dispaly =  msg_type.messages_id_desc;
                   $('#create_error_div').html(display)

            $('#create_error_div').show()
            $('#field_type').val('')
            return
        }
        if (used_timeframe_array.includes('On Date')) {
                
                    var msg = "JMSG023";
                    var msg_type ;
                  msg_type = message_config_details(msg);
                  $("#error_msg_id").prop("hidden", false)

                  if(msg_type.message_type == "ERROR"){
                        display_message("error_msg_id", msg_type.messages_id_desc)
                  }
                  else if(msg_type.message_type == "WARNING"){
                     display_message("id_warning_msg_id", msg_type.messages_id_desc)
                  }
                  else if(msg_type.message_type == "INFORMATION"){
                     display_message("id_info_msg_id", msg_type.messages_id_desc)
                  }
                    var display = msg_type.messages_id_desc;
                   $('#create_error_div').html(display)

            $('#create_error_div').show()
            $('#field_type').val('')
            return
        }
        $('#create_error_div').hide()
        $('#timeframe').show()
        $('#dropdown-values').hide()
    }

    if (element == 'select_timeframe') {
        timeframe_value = document.getElementById('select_timeframe').value
        if (timeframe_value == 'From Date') {
            document.getElementById('field_name').value = 'From Date'
        } else if (timeframe_value == 'On Date') {
            document.getElementById('field_name').value = 'On Date'
        } else {
            document.getElementById('field_name').value = 'To Date'
        }
    }

}


const save_form_validation = (supplier_id, supplier_description, product_category, supplier_article_number, lead_time) => {
    var is_valid = true
    var save_form_errors = ''
    if (supplier_id == '') {
        is_valid = false
          
                            var msg = "JMSG004";
                            var msg_type ;
                          msg_type = message_config_details(msg);
                          $("#error_msg_id").prop("hidden", false)

                          if(msg_type.message_type == "ERROR"){
                                display_message("error_msg_id", msg_type.messages_id_desc)
                          }
                          else if(msg_type.message_type == "WARNING"){
                             display_message("id_warning_msg_id", msg_type.messages_id_desc)
                          }
                          else if(msg_type.message_type == "INFORMATION"){
                             display_message("id_info_msg_id", msg_type.messages_id_desc)
                          }

                           var display8 = msg_type.messages_id_desc;
        save_form_errors += display8+ "supplier ID";
    }
    if (supplier_description == '') {
        is_valid = false
               
                    var msg = "JMSG007";
                    var msg_type ;
                  msg_type = message_config_details(msg);
                  $("#error_msg_id").prop("hidden", false)

                  if(msg_type.message_type == "ERROR"){
                        display_message("error_msg_id", msg_type.messages_id_desc)
                  }
                  else if(msg_type.message_type == "WARNING"){
                     display_message("id_warning_msg_id", msg_type.messages_id_desc)
                  }
                  else if(msg_type.message_type == "INFORMATION"){
                     display_message("id_info_msg_id", msg_type.messages_id_desc)
                  }
                   var display5 = msg_type.messages_id_desc;
        save_form_errors += display5+ "supplier description";
    }
    if (product_category == '') {
        is_valid = false
          
                            var msg = "JMSG004";
                            var msg_type ;
                          msg_type = message_config_details(msg);
                          $("#error_msg_id").prop("hidden", false)

                          if(msg_type.message_type == "ERROR"){
                                display_message("error_msg_id", msg_type.messages_id_desc)
                          }
                          else if(msg_type.message_type == "WARNING"){
                             display_message("id_warning_msg_id", msg_type.messages_id_desc)
                          }
                          else if(msg_type.message_type == "INFORMATION"){
                             display_message("id_info_msg_id", msg_type.messages_id_desc)
                          }

                           var display8 = msg_type.messages_id_desc;
        save_form_errors += display8+ "product category" ;
    }
    if (supplier_article_number == '') {
        is_valid = false
           
                    var msg = "JMSG007";
                    var msg_type ;
                  msg_type = message_config_details(msg);
                  $("#error_msg_id").prop("hidden", false)

                  if(msg_type.message_type == "ERROR"){
                        display_message("error_msg_id", msg_type.messages_id_desc)
                  }
                  else if(msg_type.message_type == "WARNING"){
                     display_message("id_warning_msg_id", msg_type.messages_id_desc)
                  }
                  else if(msg_type.message_type == "INFORMATION"){
                     display_message("id_info_msg_id", msg_type.messages_id_desc)
                  }
                   var display5 = msg_type.messages_id_desc;
        save_form_errors += display5+ "supplier article number"
    }
    if (lead_time == '') {
        is_valid = false
           
                    var msg = "JMSG007";
                    var msg_type ;
                  msg_type = message_config_details(msg);
                  $("#error_msg_id").prop("hidden", false)

                  if(msg_type.message_type == "ERROR"){
                        display_message("error_msg_id", msg_type.messages_id_desc)
                  }
                  else if(msg_type.message_type == "WARNING"){
                     display_message("id_warning_msg_id", msg_type.messages_id_desc)
                  }
                  else if(msg_type.message_type == "INFORMATION"){
                     display_message("id_info_msg_id", msg_type.messages_id_desc)
                  }
                   var display5 = msg_type.messages_id_desc;
        save_form_errors += display5+ "lead time";
    }
    return is_valid, save_form_errors
}

const to_title_case = string => {
    return string.replace(/\w\S*/g, function (text) {
        return text.charAt(0).toUpperCase() + text.substr(1).toLowerCase();
    });
}

// Function to open and initiate data-table for supplier table
$('#supplier_id_free_text').click(function(){
    setTimeout(function() {
        $('.select_supplier_datatable').DataTable( {
            "scrollY": "300px",
            "scrollCollapse": true,
        } );
    }, 500);
    $('#select_supplier_modal').modal('show');
});



$('#select_supplier').click(function(){
    $('#supplier_table TBODY TR').each(function(){
        var row = $(this);
        var check = row.find("TD").eq(0).find('input[type="radio"]').is(':checked');

        if (check){
            supplier_desc = row.find("TD").eq(1).text();
            supplier_id = row.find("TD").eq(2).text();
            document.getElementById('supplier_id_free_text').value = supplier_desc;
            $('#select_supplier_modal').modal('hide');
        }
    });
});

// Function to open and initiate data-table for Product category table
$('#product_category_free_text').click(function(){
    $('#select_prod_cat_modal').modal('show');
    setTimeout(function() {
        $('.prod_cat_datatable').DataTable( {
            "scrollY": "300px",
            "scrollCollapse": true,
        } );
    }, 500);
});

// Function to update Product category value
$('#select_product_category').click(function(){
    var prod_cat_value = ''
    $('#product_category_table TBODY TR').each(function(){
        var row = $(this);
        var check = row.find("TD").eq(0).find('input[type="radio"]').is(':checked');
        if (check){
            prod_cat_id = row.find("TD").eq(1).text();
            prod_cat_desc = row.find("TD").eq(2).text();
            prod_cat_value = prod_cat_id.concat(' - ', prod_cat_desc)

            document.getElementById('product_category_free_text').value = prod_cat_value;
            $('#select_prod_cat_modal').modal('hide');
        }
    });
})


// var eform_configured_new = new Array();

const create_fields = () => {
    var field_name = $('#field_name').val();
    var field_data_type = $('input:radio[name="eform_input_type"]:checked').val();
    var is_required = document.getElementById('is_required').checked;
    var is_special_char = document.getElementById('no_special_characters').checked;

    validations = create_popup_validations(field_data_type)
    if (validations != '') {
        $('#create_error_div').html(validations)
        $('#create_error_div').show()
        return
    } else $('#create_error_div').hide()

    var eform_object = {};

    eform_object['field_data_type'] = field_data_type;
    eform_object['field_name'] = to_title_case(field_name);
    eform_object['required'] = is_required;
    eform_object['allow_special_char'] = is_special_char;

    if (field_data_type == 'dropdown') {
        dropdown_type = $('input:radio[name="check_dropdown_type"]:checked').val();
        var prd_option_type = $('input:radio[name="dp_prd_option"]:checked').val();
        if ((prd_option_type !='Country') && (prd_option_type !='Currency')){
        eform_object['dropdown_options'] = get_dropdown_options(dropdown_type)
        }

        if(dropdown_type == 'dropdown_predefined_options'){

            if (prd_option_type == 'Country') {
                eform_object['dropdown_type'] = prd_option_type;
            }
            else if (prd_option_type == 'Currency') {
                eform_object['dropdown_type'] = prd_option_type;
            }
        } else{
            eform_object['dropdown_type'] = dropdown_type;
            
        };
        
    }

    if (field_data_type == 'date') {
        // timeframe_value = document.getElementById('select_timeframe').value
        var date_type = $('input:radio[name="check_input_datetime_type"]:checked').attr('id');

        if(date_type == 'datetime_value_on'){
            used_timeframe_array.push('On Date');
        } else if(date_type == 'datetime_value_timeframe') {
            used_timeframe_array.push('From Date', 'To Date');
        }
        
    }

    eform_configured.push(eform_object)
    display_fields_from_array()

    $('.dynamic_field').val('')
    document.getElementById('is_required').checked = false
    document.getElementById('no_special_characters').checked = false
    $('#create_new_fields_popup').modal('hide')
    $('#dropdown-values').hide()
    $('#custom_options_div').hide()
    $('#timeframe').hide()
    $('#create_eform_fields_popup').modal('hide');
    $("html, body").animate({ scrollTop: document.body.scrollHeight }, "slow");
}

function get_dropdown_options(dropdown_type) {
    if(dropdown_type == 'dropdown_predefined_options'){
        
        var prd_option_type = $('input:radio[name="dp_prd_option"]:checked').val();
        if (prd_option_type == 'Country') {
            return country_list;
        }
        else if (prd_option_type == 'Currency') {
            return currency_list;
        }
    }
    else if(dropdown_type == 'dropdown_custom_options') {
        var custom_options = new Array();
        $("#table_id_eform_dropdown TBODY TR").each(function() {
            var row = $(this); 

            // vo_table_data.default_option = row.find("TD").eq(0).find('input[type="radio"]').is(':checked');
            option_value = row.find("TD").eq(1).find('input[type="text"]').val();
            
            custom_options.push(option_value);
        });
        return custom_options
    }
}

function create_eform_field_popup(){
    clear_eform_selection();
    
    if(eform_configured.some(eform_option_data => eform_option_data.field_data_type == "date")) {
        console.log('Exists');
        $('.eform-card-type-date').addClass("eform-date-disable");

    } else {
        $('.eform-card-type-date').removeClass("eform-date-disable");
    }

    if(eform_configured.some(eform_option_data => eform_option_data.dropdown_type == "Country")) {
        $('.dp-prd-badge-country').addClass("dp-prd-badge-disable");
    } else {
        $('.dp-prd-badge-country').removeClass("dp-prd-badge-disable");
    }

    if(eform_configured.some(eform_option_data => eform_option_data.dropdown_type == "Currency")) {
        $('.dp-prd-badge-currency').addClass("dp-prd-badge-disable");
    } else {
        $('.dp-prd-badge-currency').removeClass("dp-prd-badge-disable");
    }


    $('#create_eform_fields_popup').modal('show');
}

function clear_eform_selection() {
    $('input[name="eform_input_type"]').prop('checked', false);
    $(".select-input-container").find(".selected").removeClass("selected");
    $('#eform_input_field_properties').hide();
    $(".dp-prd-opt-wrapper").find(".selected").removeClass("selected");
    $('#tbody_eform_dropdown').empty();
}
function enable_disable(action){
    $(".dummy_ft_button_class").hide();
    if(action == 'EDIT'){
        $("#ft_save").show();
        $("#ft_cancel").show();
        $('.toggle_mode').prop('disabled', false)
    }
    else{
        $("#ft_edit").show();
        $('.toggle_mode').prop('disabled', true)
    }
}
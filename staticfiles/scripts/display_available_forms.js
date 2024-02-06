$(document).ready(function () {
    $('#form_buttons').hide()
    $('#edit_button').show()
    $('#cancel_button').prop('hidden', false)
    $('#reset_button').prop('hidden', true)
});
    
//Display submenu  for purchaser and purchaser assist role
nav_bar_content_management() ;

// Function to get form id of the item and displays confirmation pop-up before deleting
var delete_form_id = '';
function get_form_id_to_delete(element) {
    var delete_id = element.split('-')
    const transaction_flag = ["False", "false"];
    if(transaction_flag.includes(delete_id[1]) ){
        delete_form_id = delete_id[0]
        document.getElementById("form_id_del").innerHTML = delete_form_id;
        $('#confirm_delete_pop_up').modal('show')
    }
}


const edit_mode = () => {
    form_id = document.getElementById('form_id').value
    if(used_forms.includes(form_id)){
             
                    var msg = "JMSG022";
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
                  $('#save_error_div').html(display + form_id)

        $('#save_error_div').show()
        scroll_top()
        return
    }
    $('#form_buttons').show()
    $('#edit_button').hide()
    $('.toggle_mode').prop('disabled', false)
    $('.btn-delete').show()
    $('#page_header').html('Edit Freetext Form')
}

const display_mode = () => {
    $('#form_buttons').hide()
    $('#edit_button').show()
    $('.toggle_mode').prop('disabled', true)
    $('.btn-delete').hide()
    $('#page_header').html('Display Freetext Form')
}

const fields_to_update = (response) => {
    $('#supplier_id_free_text').val(response.update_form_instance.supplier_id)
    $('#supplier_description').val(response.update_form_instance.description)
    $('#product_category_free_text').val(response.update_form_instance.product_category_id)
    $('#supplier_article_number').val(response.update_form_instance.supplier_article_number)
    $('#lead_time').val(response.update_form_instance.lead_time)
    $('#catalog_id').val(response.update_form_instance.catalog_id)
    $('#form_id').val(response.update_form_instance.form_id)
    $('#display_form_div').hide()
    $('#form_field_div').show()
    eform_configured = []
    used_timeframe_array = []
    data = response.update_form_instance.eform_configured
    for (index = 0; index < data.length; index++) {
        data_object = {}
        get_fields = data[index]
        input_type = get_fields['input_type']
        input_label = get_fields['form_field']
        if (input_type == 'date') {
            used_timeframe_array.push(input_label)
        }
        if (input_type.includes('dropdown')) {
            det_dropdown_options = input_type.split('-')[1]
            if (det_dropdown_options.includes(',')) {
                data_object['dropdown_type'] = 'custom_options'
                param = 'custom_options'
            } else {
                data_object['dropdown_type'] = det_dropdown_options
                param = det_dropdown_options
            }
            data_object['dropdown_options'] = get_dropdown_options(param, det_dropdown_options)
        }
        data_object['input_type'] = input_type.split('-')[0]
        data_object['input_label'] = input_label
        data_object['required'] = get_fields['required']
        data_object['allow_special_char'] = get_fields['allow_special_char']
        eform_configured.push(data_object)
    }
    display_fields_from_array()
    if (eform_configured.length > 0) {
        $('#eform_details').show()
    } else {
        $('#eform_details').hide()
    }
    $('.toggle_mode').prop('disabled', true)
    $('.btn-delete').hide()
    $('#page_header').html('Display Freetext Form')
}

const go_back = () => {
    $('#display_form_div').show()
    $('#form_field_div').hide()
}

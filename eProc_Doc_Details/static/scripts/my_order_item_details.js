// Function to hide and display limit order details in 1st step of shopping cart wizard
$(document).ready(function(){
    $("#display_limit_item").click(function(){
      $("#limit_order_detail_section").toggle();
    });
});

// display shop role sub menu in nav bar
nav_bar_shop();
item_table_css();
var eform_configured = []
var item_call_off = ''
var item_guid_number = ''
var item_eform = ''
var item_number = ''
var is_edit = false;
var GLOBAL_CHECK_BOX_GUID = ''
var GLOBAL_ITEM_NUM = ''
// Checbox on change
// const checkbox_onchange = (element) => {
//     if($(element).prop("checked") == true){
//         item_call_off = ''
//         item_guid_number = ''
//         item_eform = ''
//         item_number = ''
//         check_box_id = element.id.split('-')
//         item_call_off = check_box_id[1]
//         item_guid_number = check_box_id[2]
//         GLOBAL_CHECK_BOX_GUID = item_guid_number
//         item_eform = check_box_id[3]
//         item_number = check_box_id[4]
//         GLOBAL_ITEM_NUM = item_number
//         if(item_call_off == 'Limit'){
//             document.getElementById('display_limit_item').style.display = 'inline-block';
//         } else {
//             document.getElementById('display_limit_item').style.display = 'none';
//         }
//         if(is_edit){
//             document.getElementById('update_item').style.display = 'inline-block';
//             document.getElementById('delete_item_button').style.display = 'inline-block'
//         }
//         if(item_eform != 'None'){
//             document.getElementById('display_eform').style.display = 'inline-block';
//         } else {
//             document.getElementById('display_eform').style.display = 'none'
//         }
//     } else {
//         document.getElementById('display_limit_item').style.display = 'none';
//         document.getElementById('update_item').style.display = 'none';
//         document.getElementById('delete_item_button').style.display = 'none'
//         document.getElementById('display_eform').style.display = 'none'
//         item_call_off = ''
//         item_guid_number = ''
//         item_eform = ''
//         item_number = ''
//     }
// }


$("input:checkbox").on('click', function() {
// in the handler, 'this' refers to the box clicked on
    var $box = $(this);
    
    if ($box.is(":checked")) {
        // the name of the box is retrieved using the .attr() method
        // as it is assumed and expected to be immutable
        var group = "input:checkbox[name='" + $box.attr("name") + "']";
        // the checked state of the group/box on the other hand will change
        // and the current value is retrieved using .prop() method
        $(group).prop("checked", false);
        $box.prop("checked", true);
    } else {
        $box.prop("checked", false);
    }
});


dropdowndata = document.getElementsByClassName('dropdowndata')
for (i = 0; i < dropdowndata.length; i++) {
    dropdowndata[i].style.left = '-100px'
}

// item level edit update
var edit_account_assignment_cat = '';
var accounting_guid_at_item = ''
function edit_account_assign(edit_account_assignment_cat_button) {
    edit_account_assignment_cat = edit_account_assignment_cat_button.split('-')[1]
    accounting_guid_at_item = edit_account_assignment_cat_button.split('-')[2]
    changeAccCat()
}

var change_address_item_num = '';
var edit_address_item_num = '';
function change_item_address(change_item_address_button, loop_counter) {
    edit_row_index = loop_counter;
    change_address_item_num = change_item_address_button.split('-')[1]    
    $('#ChngShipAddr').modal('show')
}

function edit_item_address(edit_item_address_button, loop_counter) {
    edit_row_index = loop_counter;
    document.getElementById('EditShipAddr').style.display = 'block'
    edit_address_item_num = edit_item_address_button.split('_')[2]
    shippingAddress()
}


// Function to get guid of the item and displays confirmation pop-up before deleting
var delete_item_guid = '';
function get_item1(item_guid) {
    if(item_guid != ''){
        $('#delete_item_popup').modal('show')
        delete_item_guid = item_guid;
    }

}

// Function to hide and show hidden table row contents
function showSection(obj, data) {
    item_number = data.split('-')[1]
    GLOBAL_SELECT_ITEM_NUM = item_number
    document.getElementById('item_info_tr-'+item_number).hidden = false;
    if (data.includes('attachments')) {
        get_attachment_IDB(item_number)
    }
    var dropdownContentClass = data;
    var rowId = document.getElementById(dropdownContentClass);
    var rowClass = rowId.className;
    var hideableRowSection = document.getElementsByClassName(rowClass);

    for (var i = 0; i < hideableRowSection.length; i++) {
        var current_element = hideableRowSection[i].id
        if (current_element == dropdownContentClass) {
            hideableRowSection[i].style.display = 'block';
        } else {
            hideableRowSection[i].style.display = 'none';
        }
    }
}


// Function to toggle note type textarea
function selectNoteType(data) {
    var getNotebtnClass1 = data.className.split(" ")[0]
    var getNotebtnClass2 = data.className.split(" ")[1]
    var activeNoteBtn = document.getElementsByClassName(getNotebtnClass1);
    var noteBtnId = data.id
    var textareaId = document.getElementById(getNotebtnClass2);
    var textareaClass = textareaId.className;
    var hideableNoteText = document.getElementsByClassName(textareaClass);


    for (var i = 0; i < hideableNoteText.length; i++) {
        var current_element = hideableNoteText[i].id
        if (current_element == getNotebtnClass2) {
            hideableNoteText[i].style.display = 'block';
        } else {
            hideableNoteText[i].style.display = 'none';
        }
    }

    for (var i = 0; i < activeNoteBtn.length; i++) {
        var current_button = activeNoteBtn[i].id
        if (current_button==noteBtnId){
            activeNoteBtn[i].style.backgroundColor = '#007bff';
            activeNoteBtn[i].style.color = '#ffffff';
        } else{
            activeNoteBtn[i].style.backgroundColor = '#dbdad9';
            activeNoteBtn[i].style.color = '#000000';
        }
    }

}


// Close action sections i item details table
function closeAttachSection(obj, data) {
    item_number = data.substr(-1)
    var x = data;
    document.getElementById(x).style.display = "none"
    document.getElementById('item_info_tr-'+item_number).hidden = true;
}

// Restrict user to enter special characters in add internal and supplier note
//$('textarea').on('keypress', function (event) {
//    var regex = new RegExp("^[a-zA-Z0-9 ]+$");
//    var key = String.fromCharCode(!event.charCode ? event.which : event.charCode);
//    if (!regex.test(key)) {
//        event.preventDefault();
//        return false;
//    }
//});

const display_eform_first_step = (response) => {
    // If the form has eform than based on fields displays the form_fields and values
    if (response.is_eform) {
        eform = true;
        document.getElementById("eform").style.display = "block";
        $('#eform').empty();
        content = '';
        form_field_value = ''
        // For loop to get form field value and inserts a input box if form fields are configured
        for (i = 8; i < 18; i++) {
            span_id = i - 7;
            var form_field = Object.keys(response)[i];
            form_field_value = response[form_field]
            if (form_field_value) {
                content += '<div class="hg_do_clmSpc">' + '<label>' + form_field_value + ':' + '</label>' + '<span id="field' + span_id + '"></span>' + '</br>' + '<input class="hg_updateInputField" type="text" id="' + form_field + '"><br>' + '</div>'
                $('#eform').append(content);
                content = '';
            }
        }
        field_id = 1
        for (i = 18; i < 28; i++) {
            var key = Object.keys(response)[i];
            field_value = response[key]
            final_id = $('#form_field' + field_id);
            if (final_id.length > 0) {
                $('#form_field' + field_id).val(field_value);
            }
            field_id += 1
        }

        for (i = 28; i < 38; i++) {
            var required_key = Object.keys(response)[i];
            required_check = response[required_key]
            if (required_check) {
                // To get check box number and add required attribute and class
                var form_field_id = String(required_key.match(/\d+/));
                document.getElementById("form_field" + form_field_id).required = true;
                document.getElementById("field" + form_field_id).classList.add("required");
            }
        }

    } else {
        document.getElementById("eform").style.display = "none";
    }
}


const display_eform_document_detail = () => {
    // If the form has eform than based on fields displays the form_fields and values
    if (response.is_eform) {
        eform = true;
        document.getElementById("eform").style.display = "block";
        $('#eform').empty();
        content = '';
        form_field_value = ''
        // For loop to get form field value and inserts a input box if form fields are configured
        for (i = 8; i < 18; i++) {
            span_id = i - 7;
            var form_field = Object.keys(response)[i];
            form_field_value = response[form_field]
            if (form_field_value) {
                content += '<div class="hg_do_clmSpc">' + '<label>' + form_field_value + ':' + '</label>' + '<span id="field' + span_id + '"></span>' + '</br>' + '<input class="hg_updateInputField" type="text" id="' + form_field + '"><br>' + '</div>'
                $('#eform').append(content);
                content = '';
            }
        }
        field_id = 1
        for (i = 18; i < 28; i++) {
            var key = Object.keys(response)[i];
            field_value = response[key]
            final_id = $('#form_field' + field_id);
            if (final_id.length > 0) {
                $('#form_field' + field_id).val(field_value);
            }
            field_id += 1
        }

        for (i = 28; i < 38; i++) {
            var required_key = Object.keys(response)[i];
            required_check = response[required_key]
            if (required_check) {
                // To get check box number and add required attribute and class
                var form_field_id = String(required_key.match(/\d+/));
                document.getElementById("form_field" + form_field_id).required = true;
                document.getElementById("field" + form_field_id).classList.add("required");
            }
        }

    } else {
        // document.getElementById("eform").style.display = "none";
    }
}

// Function to get form data to update in update form
eform = false;
var GLOBAL_UPDATE_ITEM_ROW = '';
function update(item_number, item_call_off, item_guid_number) {
    GLOBAL_UPDATE_ITEM_ROW = item_number
    call_off = item_call_off
    guid = item_guid_number
    var price_unit
    var currency
    update_item_guid = guid;
    document.getElementById("update_limit_form").style.display = "none";
    document.getElementById("update_freetext_form").style.display = "none";
    document.getElementById("update_pr_form").style.display = "none"; 
    document.getElementById("update_catalog_form").style.display = "none"; 
    $('#update_modal_popup').modal('show');
    if (call_off == '04') {
        document.getElementById("update_limit_form").style.display = "block";
    }
    if (call_off == '02') {
        document.getElementById("update_freetext_form").style.display = "block";
    }
    if (call_off == '03') {
        document.getElementById("update_pr_form").style.display = "block";
        if(update_item_guid in update_item_details) {
            item_update_details = update_item_details[update_item_guid]
            document.getElementById("update-pr-item_name").value = item_update_details.description
            document.getElementById("update-pr-product_id").value = item_update_details.int_product_id
            document.getElementById("update-pr-price").value = item_update_details.price
            document.getElementById('update-pr-currency').value = item_update_details.currency
            document.getElementById('update-pr-prod_cat').value = item_update_details.prod_cat_id
            document.getElementById('update-pr-uom').value = item_update_details.unit
            document.getElementById("update-pr-lead_time").value = item_update_details.lead_time
            document.getElementById("update-pr-quantity").value = item_update_details.quantity
            return
        };
    }

    if (item_guid_number != ''){
        update_item_data = {};
        update_item_data.guid = guid;

        var update_item_result = ajax_update_item_data(update_item_data);

        if(update_item_result) {

            item_guid_number = ''
            item_number = ''
            // To get limit item details
            if (call_off == '04') {
                document.getElementById("id_description").value = response.item_name
                document.getElementById('upl_prod_cat').value = response.prod_cat;
                document.getElementById('currency').value = response.currency;
                document.getElementById("id_overall_limit").value = response.overall_limit
                document.getElementById("id_expected_value").value = response.expected_value
                document.getElementById('req').selected = response.required;
                document.getElementById('upl_supp_id').selected = response.supp_id;
                document.getElementById('follow_up_actions').selected = response.follow_up_action;

                if (response.required == 'On') {
                    document.getElementById("OnDate").value = response.item_del_date
                    document.getElementById("frm_dat").style.display = "none";
                    document.getElementById("to_dat").style.display = "none";
                    document.getElementById("on_dat").style.display = "block";
                } else if (response.required == 'Between') {
                    document.getElementById("StartDate").value = response.start_date
                    document.getElementById("EndDate").value = response.end_date
                    document.getElementById("frm_dat").style.display = "block";
                    document.getElementById("to_dat").style.display = "block";
                    document.getElementById("on_dat").style.display = "none";
                } else {
                    document.getElementById("StartDate").value = response.start_date
                    document.getElementById("frm_dat").style.display = "block";
                    document.getElementById("to_dat").style.display = "none";
                    document.getElementById("on_dat").style.display = "none";
                }
            }
            // To get Purchase requisition update form with values
            if (call_off == '03') {
                document.getElementById("update-pr-item_name").value = response.item_name
                document.getElementById("update-pr-prod_desc").value = response.item_long_desc
                document.getElementById("update-pr-product_id").value = response.prod_id
                document.getElementById("update-pr-price").value = response.price
                document.getElementById('update-pr-currency').value = response.currency
                $('#update-pr-currency').selectpicker('val', response.currency)
                document.getElementById('update-pr-prod_cat').value = response.prod_cat_id
                $('#update-pr-prod_cat').selectpicker('val', response.prod_cat_id)
                document.getElementById('update-pr-uom').value = response.unit
                $('#update-pr-uom').selectpicker('val', response.unit)
                document.getElementById("update-pr-lead_time").value = response.lead_time
                document.getElementById("update-pr-quantity").value = response.quantity
            }
            if (call_off == '01'){
                $('#update_pop_up').modal('show');
                var cat_qnt = "item_quantity-"+guid
                var value = $("#"+cat_qnt).text()
                document.getElementById("catalog_quantity").value             = value
                document.getElementById("cat_price_per_unit").value           = response.price
                document.getElementById("update_catalog_form").style.display = "block";
            }
            // To get freetext form with values
            if (call_off == '02') {
                $('#eform_card_details').empty();
                //display_configured_fields(response.configured_eform_fields, response.free_text_context)
                if (document_detail_mode == 'True'){
                    item_name = response.free_text_context.item_name
                    prod_desc = response.free_text_context.item_long_desc
                    price = response.free_text_context.price
                    price_unit = response.free_text_context.price_unit
                    unit = response.free_text_context.unit
                    del_date = response.free_text_context.del_date
                    quantity = response.free_text_context.quantity
                    supp_id = response.free_text_context.supp_id
                    currency = response.free_text_context.currency_id

                } else {
                    display_eform_first_step(response)
                    item_name = response.item_name
                    prod_desc = response.prod_desc
                    price = response.price
                    unit = response.unit
                    del_date = response.del_date
                    quantity = response.quantity
                    supp_id = response.supp_id
                }
                document.getElementById("product_name").value = item_name
                document.getElementById("free_text_desc").value = prod_desc
                document.getElementById("price_per_unit").value = price_unit
                document.getElementById("id_price").value = price
                document.getElementById("estimated_price_currency").innerHTML = currency
                document.getElementById(unit).selected = true;
                document.getElementById("delivery_date").value = del_date
                document.getElementById("quantity").value = quantity
                document.getElementById("supplier_id").value = supp_id 
            }
            eform_configured = response.eform_configured
            display_fields_from_array(response.eform_configured)

        }
    }
}

const display_fields_from_array = (eform_configured) => {
    $('#eform_card_details').empty()
    var div_content = '';
    var user_data = '';
    //$('#eform_card_details').append('Additional Information')
    $.each(eform_configured, function (index, value) {
        field_data_type = value['field_data_type'];
        field_name = value['field_name'];
        is_required = value['required'];

        var options = '<option value="" selected>Select</option>';

        if (field_data_type == 'dropdown') {
            get_dropdown = value['dropdown_options']
            get_dropdown_type = value['dropdown_type']
            if (get_dropdown_type == 'Currency'){
                for (i = 0; i < currency_list.length; i++) {
                    if(value.user_field_data == country_list[i]['country_code']){
                        user_data = '<option value="' + currency_list[i]['currency_id'] + '">' + currency_list[i]['currency_id']+ ' - ' + currency_list[i]['description'] + '</option>'
                     }
                    else{
                        options += '<option value="' + currency_list[i]['currency_id'] + '">' + currency_list[i]['currency_id']+ ' - ' + currency_list[i]['description'] + '</option>'

                    }
                }
                options = user_data+options;
            }

            if (get_dropdown_type == 'Country'){
                for (i = 0; i < country_list.length; i++) {
                    if(value.user_field_data == country_list[i]['country_code']){
                        user_data = '<option value="' + country_list[i]['country_code'] + '">' + country_list[i]['country_code']+ ' - ' + country_list[i]['country_name'] + '</option>'
                    }
                    else{
                        options += '<option value="' + country_list[i]['country_code'] + '">' + country_list[i]['country_code']+ ' - ' + country_list[i]['country_name'] + '</option>'

                    }
                }
                options = user_data+options;
            }
            if (get_dropdown_type == 'dropdown_custom_options'){
                for (i = 0; i < get_dropdown.length; i++) {
                    if(value.user_field_data == get_dropdown[i]){
                        user_data = '<option value="' + get_dropdown[i] + '">' + get_dropdown[i] + '</option>'
                    }
                    else{
                    options += '<option value="' + get_dropdown[i] + '">' + get_dropdown[i] + '</option>';
                    }
                }
                options = user_data+options;
            }

            div_content = '<div class="form-row eform-field-wrapper" id="array_index-' + index + '"><div class="form-group col-md-11"> <label  for="' + field_name + '">' + field_name + '</label><span id="span_' + field_name + '"></span> <select class="form-control toggle_mode" id="'+value.eform_transaction_guid+'">' + options + '</select></div> <div class="col-auto eform-field-btn-wrapper"> </div> </div>'
        }
        else if (field_data_type == 'checkbox') {
            div_content = '<div class="form-row eform-field-wrapper" id="array_index-' + index + '"> <div class="form-group col-md-11"> <input class="toggle_mode" type="' + field_data_type + '" id="'+value.eform_transaction_guid+'" > <label  for="' + field_name + '">' + field_name + '</label><span id="span_' + field_name + '"></span> </div> <div class="col-auto eform-field-btn-wrapper"> </div> </div>'
        }
        else if (field_data_type == 'textarea') {
            div_content = '<div class="form-row eform-field-wrapper" id="array_index-' + index + '"> <div class="form-group col-md-11"> <label  for="' + field_name + '">' + field_name + '</label><span id="span_' + field_name + '"></span> <textarea class="form-control toggle_mode" id="'+value.eform_transaction_guid+'">'+value.user_field_data+'</textarea> </div> <div class="col-auto eform-field-btn-wrapper"> </div> </div>'
        }

        else if (field_data_type == 'date') {
            var date_type = $('input:radio[name="check_input_datetime_type"]:checked').attr('id');

            if(date_type == 'datetime_value_on'){
                div_content = '<div class="form-row eform-field-wrapper" id="array_index-' + index + '"> <div class="form-group col-md-11"> <label  for="' + field_name + '">' + field_name + '</label><span id="span_' + field_name + '"></span> <input class="form-control toggle_mode" type="' + field_data_type + '" value="'+value.user_field_data+'" id="'+value.eform_transaction_guid+'"> </div> <div class="col-auto eform-field-btn-wrapper"> </div> </div>'
            } else if(date_type == 'datetime_value_timeframe') {
                div_content = '<div class="form-row eform-field-wrapper" id="array_index-' + index + '"> <div class="form-group col-md-11"> <label for="">Form Date</label><span id="span_' + field_name + '"></span> <input class="form-control toggle_mode" type="date" id="'+value.eform_transaction_guid+'"> <label for="">To Date</label><span id="span_' + field_name + '"></span> <input class="form-control toggle_mode" type="date" value="'+value.user_field_data+'"> </div> <div class="col-auto eform-field-btn-wrapper"> </div> </div>'
            }
        }
        else {
            div_content = '<div class="form-row eform-field-wrapper" id="array_index-' + index + '"> <div class="form-group col-md-11"> <label  for="' + field_name + '">' + field_name + '</label><span id="span_' + field_name + '"></span> <input class="form-control toggle_mode" type="' + field_data_type + '" value="'+value.user_field_data+'" id="'+value.eform_transaction_guid+'"></div> <div class="col-auto eform-field-btn-wrapper"> </div> </div>'
        }

        $('#eform_card_details').append(div_content)
        if (is_required) {
            var required_label = document.getElementById('span_' + field_name);
            required_label.classList.add('hg_required');
        }
    });
    $('#eform_card_details').show()
}



// Function to delete an item from the cart and update in the UI using ajax call
function delete_cart_item() {
    let total_value = document.getElementById('ScHeader-total_value-' + GLOBAL_HEADER_GUID).innerHTML;

    let header_guid = document.getElementById('header_guid').value;
    $('#delete_item_popup').modal('hide');
    delete_sc_data = {};
    delete_sc_data.del_item_guid = delete_item_guid;
    delete_sc_data.total_value = total_value;
    delete_sc_data.header_guid = header_guid;
    
    OpenLoaderPopup();

    if(delete_item_guid != ''){
        $.ajax({
            type: 'POST',
            url: delete_my_order_sc_item_url,
            data: delete_sc_data,
            success: function(response){
                item_guid_number = ''
                if (response.count === 0) {
                    window.opener.location.reload();
                    window.close()
                } else {
                    $('#total_items').html(response.count)
                    document.getElementById("ScHeader-total_value-" + GLOBAL_HEADER_GUID).innerHTML = response.total_value
                    var get_item_number = $("[id^=item_number_]")
                    var row = document.getElementById(delete_item_guid);
                    row.parentNode.removeChild(row);
                    get_update_count = document.getElementsByClassName('update_item_count')
                    for(i = 0; i < get_update_count.length; i++){
                        get_update_count[i].innerHTML = i + 1
                    }
                    CloseLoaderPopup();
                }
            },
            error: function(error) {
                console.log(error);
                CloseLoaderPopup();

            },
        });
    }
    
}

// Function to delete cart and update in the UI using ajax call
function delete_sc() {

    delete_sc_data = {};
    delete_sc_data.delete_sc = 'delete_sc';
    delete_sc_data.header_guid = document.getElementById('header_guid').value;

    var delete_sc_result = ajax_my_order_delete_sc(delete_sc_data);

    if(delete_sc_result){
        location.href = '/doc_search_and_display/search_shopping_carts'
    }
}
function show_image_div(){
    $(".catalog_img").hide();
    $(".catalog_img:eq(" + image_visible_div + ")").show();

}
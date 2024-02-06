$(document).ready(function () {
    nav_bar_shop();

    $('body').css('padding-top', '7rem');

});
var CONST_MULTIPLE = ''
var manager_detail_initial = shopping_cart_errors.manager_detail.length
var sc_errors_initial = shopping_cart_errors.sc_error
var sc_info_messsages = shopping_cart_errors.sc_info
var error_messages_initial = '' 

if (sc_info_messsages.length > 0){
    var info_messages = '';
    for(info = 0; info <= sc_info_messsages.length; info++){
        info_dict_obj = sc_info_messsages[info]
        for (var info_key in info_dict_obj) {
            if (info_key == '0'){
                info_messages += 'Info : ' + info_dict_obj[info_key] + '<br>'
            } else {
                info_messages += 'Info at item ' + info_key + ': ' + info_dict_obj[info_key] + '<br>'
            }
        }
    }
    $('#sc_info_messages').html(info_messages)
    $('#sc_info_messages').show()
}

if (sc_errors_initial.length == 0 && manager_detail_initial != 0) {

                    var msg = "JMSG042";
                    var msg_type ;
                  msg_type = get_message_desc(msg);
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
                  var display3 = msg_type.messages_id_desc;
                  $('#sc_success_messages').html(display3)

    $('#sc_success_messages').show()
    document.getElementById('sc_error_msg').style.display = 'none';
    $('#sc_error_msg').html('');
} else {
    for (i = 0; i < sc_errors_initial.length; i++) {
        dict_obj = sc_errors_initial[i]
        for (var key in dict_obj) {
            if (key == '0') {
                error_messages_initial += 'Error: ' + dict_obj[key] + '<br>'
            } else {
                error_messages_initial += 'Error at item ' + key + ': ' + dict_obj[key] + '<br>'
            }
        }
    }
    if (shopping_cart_errors['msg_info']) {
        error_messages_initial += shopping_cart_errors['msg_info']
    }

    $('#sc_error_msg').html(error_messages_initial);
    document.getElementById('sc_success_messages').style.display = 'none';
    document.getElementById('sc_error_msg').style.display = 'block';
}

// function to scroll to Approval process overview section
$("#display_approver_div").click(function () {
    $('html,body').animate({scrollTop: $("#approval_process_overview").offset().top}, 'slow');
});

// On button hover display title text
$('button').hover(function () {
    let titlename= $(this).text();
    this.title = titlename;
});

// Onclick of save approver note button 
$('#save_approver_note').click(function(){
    var txt = $('#approver_text').val()
    if (txt==''){
        console.log("it is null")
    } else{
        $('#add_approver_note_btn').removeClass('btn-primary').addClass('btn-success');
        $('#add_approver_note_btn').children().removeClass('fa-plus').addClass('fa-check');
    }
});


//prefixes of implementation that we want to test
window.indexedDB = window.indexedDB || window.mozIndexedDB ||
window.webkitIndexedDB || window.msIndexedDB;

//prefixes of window.IDB objects
window.IDBTransaction = window.IDBTransaction ||
    window.webkitIDBTransaction || window.msIDBTransaction;
window.IDBKeyRange = window.IDBKeyRange || window.webkitIDBKeyRange ||
    window.msIDBKeyRange


if (!window.indexedDB) {

        var msg = "JMSG044";
        var msg_type ;
      msg_type = get_message_desc(msg);
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
        window.alert(display8)
}

var db;
var request = window.indexedDB.open("store_attachments", 1);

request.onerror = function (event) {
    console.log("error: ");
};

request.onsuccess = function (event) {
    db = request.result;
    get_attachment_data().then((value) => null)
};

request.onupgradeneeded = function (event) {
    var db = event.target.result;
    var objectStore = db.createObjectStore("attachments", { keyPath: "attachment_data" });
}

var highest_value_item_number = document.getElementById('highest_item').value
var highest_item_acc_asgn_cat = (document.getElementById('change_acc_type_'+highest_value_item_number).innerHTML).split(' - ')[0]
var highest_item_change_acc_value = (document.getElementById('change_acc_value_'+highest_value_item_number).innerHTML).split(' - ')[0]
var cart_length = parseInt(document.getElementById('cart_counter').innerHTML)

// Function to edit cart name in sc second step
function edit_sc_name(){
    $('#edit_sc_name_window').modal('show');

    var sc_name = document.getElementById('sc_name_id').innerHTML;

    document.getElementById('sc_name_input').value   = sc_name
}

// Function to submit edit SC name
function submitSCname(){
    var sc_name = document.getElementById('sc_name_input').value

    document.getElementById('sc_name_id').innerHTML   = sc_name

    $('#edit_sc_name_window').modal('hide');
}




// Function to get sc data to check
function get_data_for_check(){
    var sc_item_guid = JSON.parse(document.getElementById('cart_items_guid_list').textContent);
    var data_for_check = new Array()
    var supplier_id = ''
    supplier = $("[id^=supp_]")
    adr_num  = $("[id^=address_number_]")
    for(i=0;i<supplier.length;i++){
        data = {}
        incremented_i = i+1
        var supp_id = supplier[i].id;
        var address_info = 'address_number_'+incremented_i;
        var acc_info = 'change_acc_type_'+incremented_i;
        var acc_val_info = 'change_acc_value_'+incremented_i;
        var gl_num_info = 'gl_acc_val_'+incremented_i;
        var prod_cat_info = 'prod_cat_'+incremented_i;
        var internal_note = document.getElementById("int_note_text-"+incremented_i).value
        var supplier_note = document.getElementById("sup_note_text-"+incremented_i).value
        remove_special_characters(internal_note, supplier_note, incremented_i)
        supplier_info = document.getElementById(supp_id).innerHTML;
        data.item_num = incremented_i
        data.delivery_date = document.getElementById('del_date-' + rendered_item_guid[i]).innerHTML
        data.supplier_name = document.getElementById(supp_id).innerHTML;
        data.address_number = document.getElementById(address_info) ? document.getElementById(address_info).innerHTML : 'None'
        data.acc_acc_cat = (document.getElementById(acc_info).innerHTML).split(' - ')[0]
        data.acc_acc_val = (document.getElementById(acc_val_info).innerHTML).split(' - ')[0]

        data.gl_acc_num = (document.getElementById(gl_num_info).innerHTML).split(' - ')[0].trim()
        data.prod_cat = (document.getElementById(prod_cat_info).innerHTML)
        create_id = 'product_id-' + incremented_i + '-'
        get_product_ids = $('[id^="' + create_id + '"]')
        if(get_product_ids.length > 0){
            data.product_id = get_product_ids[0].id.split('-')[2]
            data.lead_time  = document.getElementById('lead_time-'+incremented_i).innerHTML
            data.item_price = document.getElementsByClassName('item_price-' + incremented_i)[0].innerHTML
            data.item_guid = sc_item_guid[incremented_i-1]
            data.quantity = document.getElementById('quant_'+rendered_item_guid[i]).innerHTML
        }
        data_for_check.push(data)
    }
    return data_for_check
}


function get_sc_data(){
    total_value = document.getElementById("total_cart_value").innerHTML
    cart_name = document.getElementById("sc_name_id").innerHTML
    address_number_element = document.getElementById("address_number")
    street_element = document.getElementById("street_output")
    area_element = document.getElementById("area_output")
    landmark_element = document.getElementById("landmark_output")
    city_element = document.getElementById("city_output")
    pcode_element = document.getElementById("pcode_output")
    region_element = document.getElementById("region_output")
    test = $('#address_number').html()
    adr_num   = address_number_element ? address_number_element.innerHTML : 'None'
    street    = street_element ? street_element.innerHTML : 'None'
    area      = area_element ? area_element.innerHTML : 'None'
    landmark  = landmark_element ? landmark_element.innerHTML : 'None'
    city      = city_element ? city_element.innerHTML : 'None'
    pcode     = pcode_element ? pcode_element.innerHTML : 'None'
    region    = region_element ? region_element.innerHTML : 'None'
    var receiver_id = document.getElementById('receiver');
    receiver = receiver_id.className;
    cart_counter = document.getElementById("cart_counter").innerHTML
    get_silent_po = document.getElementById("silent_PO").checked
    acc_assign_cat = document.getElementById("change_acc_type").innerHTML
    acc_assign_cat = acc_assign_cat.split(' - ')[0]
    acc_assign_val = document.getElementById("change_acc_value").innerHTML
    acc_assign_val = acc_assign_val.split(' - ')[0]
    approver_text = document.getElementById("approver_text").value
    var silent_po = 0;
    if(get_silent_po){
        silent_po = 1;
    } else {
        silent_po = 0;
    }
    data = new FormData();
    array_index = 0;
    for(i=1;i<parseInt(cart_counter)+1;i++){
        last_index_attachments = parseInt(sessionStorage.getItem('last_added_file_number-'+i))
        // for(j=0;j<final_attachment_array.length; j++){
            var j = 1;
            while(j<=last_index_attachments){
                if(j>last_index_attachments){
                    break;
                }
                check_for_file = "attachment_data"+i+'_'+j;
                if(indexed_db_keys.includes(check_for_file)){
                    attachment_object = final_attachment_array[array_index]
                    if(typeof attachment_object != 'undefined'){
                        file_base64 = attachment_object.dataUrl
                        if(typeof file_base64 != 'undefined'){
                            file_number = j
                            file_n = attachment_object.file_name
                            file_ext = attachment_object.file_extension_id
                            file_ty = attachment_object.type
                            file_nam = attachment_object.file_name
                            no_att = attachment_object.no_attachments
                            atta_name = attachment_object.attachment_name
                            data.append('attachment' + i + '_' + file_number, dataURLtoFile(file_base64, attachment_object.file_name))
                            data.append("file_extension" + i+'_'+j, attachment_object.file_extension_id)
                            data.append("attachment_type" + i, attachment_object.type)
                            data.append("attachment_name" + i, attachment_object.attachment_name)
                            data.append('no_attachments' + i, attachment_object.no_attachments)
                        }
                    }
                }
                else{
                    array_index--
                }
            array_index++
            j++
            }
        // }
        data.append('last_index_attachments'+i, last_index_attachments)
        data.append("internal_note" + i, document.getElementById("int_note_text-"+i).value)
        data.append("supplier_note" + i, document.getElementById("sup_note_text-"+i).value)
        data.append("address_number" + i, $("#address_number_"+i).html())
        data.append("street_output" + i, $("#street_output"+i).html())
        data.append("area_output" + i, $("#area_output"+i).html())
        data.append("landmark_output" + i, $("#landmark_output"+i).html())
        data.append("city_output" + i, $("#city_output"+i).html())
        data.append("pcode_output" + i, $("#pcode_output"+i).html())
        data.append("region_output" + i, $("#region_output"+i).html())
        data.append("change_acc_type" + i, $("#change_acc_type_"+i).html())
        data.append("change_acc_value" + i, $("#change_acc_value_"+i).html())
        var item_level_gl = ($("#gl_acc_val_"+i).html()).trim()
        data.append("gl_acc_val" + i, item_level_gl.split(' - ')[0])
    }
    data.append('total_value' , total_value)
    data.append('receiver' , receiver)
    data.append('cart_name' , cart_name)
    data.append('adr_num' , adr_num)
    data.append('street' , street)
    data.append('area' , area)
    data.append('landmark' , landmark)
    data.append('city' , city)
    data.append('pcode' , pcode)
    data.append('region' , region)
    data.append('get_silent_po' , get_silent_po)
    data.append('approver_text' , approver_text)
    data.append('acc_assign_cat' , acc_assign_cat)
    data.append('acc_assign_val' , acc_assign_val)
	data.append('manger_detail' , JSON.stringify(GLOBAL_MANAGER_DETAIL))
    data.append('sc_completion_flag', sc_completion_flag)
    data.append('requester', $('#shopping_cart_requester').val())
    return data;
}

// Function called on trigger of order-shopping-cart-button 
function order_shopping_cart(){
    sc_data = get_sc_data()
    check_shopping_cart('order', sc_data, highest_item_acc_asgn_cat, highest_item_change_acc_value)
}


// Function to convert File type to base64 type
const toBase64 = file => new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result);
    reader.onerror = error => reject(error);
});



// Function to upload attachments to session
async function upload_attachments(id) {
    item_number = id.slice(-1)
    item_number_attached = item_number
    file_number = 0;
    last_added_file_number = sessionStorage.getItem('last_added_file_number-' + item_number)
    if (last_added_file_number != null) {
        file_number = parseInt(last_added_file_number)
    }
    input_id = id.split('-')[1]
    $('#attachment_tbody_id-' + item_number).empty()
    const file = document.querySelector('#' + input_id)
    internal_radio_check = document.getElementById("internal" + item_number).checked
    external_radio_check = document.getElementById("external" + item_number).checked
    type = '';
    if (!(internal_radio_check || external_radio_check)) {

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
        $('#attachment_error' + item_number).html(display8 + "attachment type")
        $('#attachment_error' + item_number).show()
        return false;
    } else {
        $('#attachment_error' + item_number).html('')
        $('#attachment_error' + item_number).hide()
        if (internal_radio_check) {
            type = 'Internal Use';
        } else {
            type = 'External Use'
        }
    }
    attachment_value = document.getElementById('attachment_data' + item_number).value
    attachment_name = document.getElementById('attachment_name' + item_number).value
    is_special_character = check_for_special_char(attachment_name)
    if (!is_special_character) {

         var msg = "JMSG003";
         var msg_type ;
         msg_type = message_config_details(msg);
         $("#error_msg_id").prop("hidden", false)
         var display5 = msg_type.messages_id_desc;
        $('#attachment_error' + item_number).html(display5 + "Attachment Name")
        $('#attachment_error' + item_number).show()
        return false;
    }
    if (!attachment_value) {

         var msg = "JMSG005";
         var msg_type ;
         msg_type = get_message_desc(msg);
         $("#error_msg_id").prop("hidden", false)
         var display3 = msg_type.messages_id_desc;
        $('#attachment_error' + item_number).html(display3 + "Files to upload")
        $('#attachment_error' + item_number).show()
        return false;
    } else {
        $('#attachment_error' + item_number).html('')
        $('#attachment_error' + item_number).hide()
    }
    if (!attachment_name) {

         var msg = "JMSG005";
         var msg_type ;
         msg_type = get_message_desc(msg);
         $("#error_msg_id").prop("hidden", false)
         var display5 = msg_type.messages_id_desc;
        $('#attachment_error' + item_number).html(display5 + "Attachment Name")
        $('#attachment_error' + item_number).show()
        return false;
    } else {
        $('#attachment_error' + item_number).html('')
        $('#attachment_error' + item_number).hide()
    }

    for (i = 0; i < file.files.length; i++) {
        attached_file = file.files[i];
        if (attached_file) {
            incremented_i = file_number + (i + 1);
            var attachment_id = 'attachment_data' + item_number + '_' + incremented_i;
            no_attachments = file.files.length
            file_extension_id = 'file_extension' + item_number + '_' + incremented_i;
            file_extension = (attached_file.name).split(".")[1]
            base64_converted = await toBase64(attached_file);
            var request = db.transaction(["attachments"], "readwrite")
                .objectStore("attachments")
                .add({ attachment_data: attachment_id, dataUrl: base64_converted, attachment_name: attachment_name, no_attachments: no_attachments, file_name: attached_file.name, file_extension_id: file_extension, type: type });

            request.onsuccess = function (event) {
                $('#attachment_name' + item_number).val('')
                $('#attachment_data' + item_number).val('')
                $('#internal' + item_number).prop('checked', false)
                $('#external' + item_number).prop('checked', false)

            };

            request.onerror = function (event) {

                    var msg = "JMSG046";
                    var msg_type ;
                  msg_type = get_message_desc(msg);
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
                  alert(display5);

            }
        }
    }
    await get_attachment_IDB(item_number);
    display_attachment_icon(item_number, "UPLOAD");
    get_attachment_data().then((value) => null)
}

// Function convert base64 converted url to File type
function dataURLtoFile(dataUrl, filename) {
    var array = dataUrl.split(','),
        mime = array[0].match(/:(.*?);/)[1],
        converted_to_atob = atob(array[1]),
        atob_length = converted_to_atob.length,
        u8arr = new Uint8Array(atob_length);

    while (atob_length--) {
        u8arr[atob_length] = converted_to_atob.charCodeAt(atob_length);
    }
    file_data = new File([u8arr], filename, { type: mime })
    return file_data;
}

// Function to delete attachments from session
function delete_attachments(element) {
    element_id = element.id
    item_file_number = element_id.split('-')[1]
    item_number = item_file_number.split('_')[0]
    file_number = parseInt(item_file_number.split('_')[1])
    attachment_id = 'attachment_data' + item_file_number
    var request = db.transaction(["attachments"], "readwrite")
        .objectStore("attachments")
        .delete(attachment_id);

    request.onsuccess = function (event) {
        $(element).parent().parent().remove();
        var rowCount = $('#attachment_tbody_id-' + item_number).children('tr').length;
        if (rowCount == 0) {
            document.getElementById('added_attachments_display-' + item_number).style.display = 'none';
            sessionStorage.removeItem('last_added_file_number-' + item_number)
        }
    };
    display_attachment_icon(item_number, "DELETE");
    get_attachment_data().then((value) => null)
}

// function to show or hide attachment existence icon based on action
const display_attachment_icon = (item_number, action) => {
    if (action == 'UPLOAD') {
        $('#attachment_added-' + item_number).prop("hidden", false);
    } else if (action == 'DELETE') {
        $('#attachment_added-' + item_number).prop("hidden", true);
    }
}

// Function to open header level change account assignment pop-up
function changeAccCat(acc_id) {
    $('#change_acc_cat').modal('show');
    var gl_acc_value = '';
    acc_level = acc_id.split('-')[1]
    $('#select_gl_acc_num').empty();
    if (acc_level == "header") {
        $('#gl_acc_change_id').css('display', 'none');
        var account_assignment_category = $('#change_acc_type').html().trim()
        var account_assignment_value = $('#change_acc_value').html().trim()
        update_accounting_popup_data(account_assignment_category, account_assignment_value, gl_acc_value)
    }
    else {
        //var gl_acc_id = 'gl_acc_val_'+edit_account_assignment_cat
        var acc_cat = $('#change_acc_type_' + edit_account_assignment_cat).text().trim();
        var acc_cat_val = $('#change_acc_value_' + edit_account_assignment_cat).text().trim();
        var gl_acc_value = $('#gl_acc_val_' + edit_account_assignment_cat).text().trim();
        var html_option = ''
        var html_option_default = '';

        // based on item acc type,put option in first place
        $('#select_acc_type option[value="' + acc_cat + '"]').remove()
        html_option_default = '<option value="' + acc_cat + '" selected>' + acc_cat + '</option>'
        $("#select_acc_type").prepend(html_option_default);
        $("#select_acc_type")[0].options[0].selected = true;

        var acc_assign_value_field_class = document.getElementsByClassName('account_assignment_secondary');
        for (i = 0; i < acc_assign_value_field_class.length; i++) {
            acc_assign_value_field_id = acc_assign_value_field_class[i].id;
            if (acc_cat != acc_assign_value_field_id) {
                document.getElementById(acc_assign_value_field_id).value = ''
            } else {
                document.getElementById(acc_assign_value_field_id).value = acc_cat_val
            }
        }
        $('#select_gl_acc_num').val(gl_acc_value)
        $('#gl_acc_change_id').css('display', 'block');
    }
    //$('#change_acc_cat').modal('show');
}

const check_ui_errors_warnings = (error_messages) => {
    var warning_messages = '';
    var error_messages = '';
    var msg_type;
    check_address_number = document.getElementsByClassName('check_address_number');
    address_number_array = new Array();
    for (i = 0; i < check_address_number.length; i++) {
        address_number_array.push(check_address_number[i].innerHTML);
    }
    //    var msg_address = "JMSG049";
    //    msg_type = message_config_details(msg_address, url_new);

    is_multiple_delivery_addresses = address_number_array.every((val, i, arr) => val === arr[0])
    if (!is_multiple_delivery_addresses) {

                    var msg = "JMSG026";
                    var msg_type ;
                  msg_type = get_message_desc(msg);
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
                  var display9 =  msg_type.messages_id_desc;
                  warning_messages += display9;

        $('#sc_warning_messages').html(warning_messages)
        $('#sc_warning_messages').show()
    } else $('sc_warning_messages').hide()

    // Check for Multiple Acct Assignment Values
    check_account_assignment_type = document.getElementsByClassName('change_account_type')
    change_acc_type_array = new Array();
    for (i = 0; i < check_account_assignment_type.length; i++) {
        change_acc_type_array.push(check_account_assignment_type[i].innerHTML)
    }

    is_multiple_account_assignment = change_acc_type_array.every((val, i, arr) => val === arr[0])
    if (!is_multiple_account_assignment && (acct_assignment_cat == '0')) {

                    var msg = "JMSG047";
                    var msg_type ;
                  msg_type = get_message_desc(msg);
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
                  var display2 = msg_type.messages_id_desc;
                  error_messages += display2;

        $('#sc_error_msg').html(error_messages);
        $('#sc_error_msg').show();
    } else if (!is_multiple_account_assignment && (acct_assignment_cat == '1')) {

                    var msg = "JMSG047";
                    var msg_type ;
                  msg_type = get_message_desc(msg);
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
                  var display1 = msg_type.messages_id_desc ;
                  warning_messages += display1;

        $('#sc_warning_messages').html(warning_messages);
        $('#sc_warning_messages').show();
        check_account_assignment_value = document.getElementsByClassName('check_account_assignment_values');
        change_acc_value_array = new Array();
        for (i = 0; i < check_account_assignment_value.length; i++) {
            change_acc_value_array.push(check_account_assignment_value[i].innerHTML);
        }
        is_multiple_account_assignment_value = change_acc_value_array.every((val, i, arr) => val === arr[0]);

        if (!is_multiple_account_assignment_value && (acct_assignment_cat == '0')) {

                    var msg = "JMSG047";
                    var msg_type ;
                  msg_type = get_message_desc(msg);
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
                  var display4 = messages_id_desc;
                   error_messages += display4;

            $('#sc_error_msg').html(error_messages);
            $('#sc_error_msg').show();
        } else if (!is_multiple_account_assignment_value && (acct_assignment_cat == '1')) {

                    var msg = "JMSG048";
                    var msg_type ;
                  msg_type = get_message_desc(msg);
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
                  var display9 = msg_type.messages_id_desc;
                  warning_messages += display9;

            $('#sc_warning_messages').html(warning_messages);
            $('#sc_warning_messages').show();
        } else $('sc_warning_messages').hide();
    }

    // Checking for multiple purchasing group
    var msg = "JMSG049";

    msg_type = message_config_details(msg);
    if (multiple_purch_group.length != 0) {
        if (multiple_purch_group[0] == CONST_MULTIPLE && (purchase_group == 0)) {
            error_messages += msg_type.messages_id_desc;
            //        $('#sc_error_msg').html(error_messages);
            //        $('#sc_error_msg').show();
            message_type_check("sc_error_msg", msg_type.messages_id_desc)
        } else $('sc_error_msg').hide()
        if (multiple_purch_group[0] == CONST_MULTIPLE && (purchase_group == 1)) {
            warning_messages += msg_type.messages_id_desc;
            message_type_check("sc_warning_messages", msg_type.messages_id_desc)
            //        $('#sc_warning_messages').html(warning_messages)
            //        $('#sc_warning_messages').show()
        }
    }

    for (j = 0; j < internal_supplier_error_itemNumber.length; j++) {
        var url_new = "{% url 'eProc_Basic:get_message_description' %}";

                var msg = "JMSG003";
                var msg_type ;
              msg_type = get_message_desc(msg);
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

              var display4 = msg_type.messages_id_desc;
                 error_messages += 'Error at item ' + internal_supplier_error_itemNumber[j] + ': ' + display4 + "Internal or Supplier Note" + '<br>'

    }
	 return error_messages


}

const check_manager_detail = (response) => {
    GLOBAL_MANAGER_DETAIL = response.approver_id;
    $('#div_manager_detail').empty();
    var manager_icon = '';
    error_message = '';
    $('#id_dynamic').empty();
    if (response.manager_detail) {
        $.each(response.manager_detail, function (i, item) {
            if (item == 'Auto') {
                double_angular = '<div class="approval-overview__next-icon-container"><i class="fas fa-angle-double-right fa-3x"></i></div>';
                manager_icon += '' + double_angular + '<div class="approval-overview__user-icon-container ao-workflow-user"><div class="workflow-user-bg"><i class="fas fa-user-check fa-2x icon-workflow-auto" aria-hidden="true"></i></div><button type="button" class="button-workflow-user">' + item.first_name + '</button></div>';
            }
            else {
                double_angular = '<div class="approval-overview__next-icon-container"><i class="fas fa-angle-double-right fa-3x"></i></div>';
                manager_icon += '' + double_angular + '<div class="approval-overview__user-icon-container ao-workflow-user"><div class="workflow-user-bg"><i class="fa fa-user-tie fa-3x" aria-hidden="true"> </i></div><button type="button" class="button-workflow-user">' + item.first_name + '</button></div>';
            }
        });
    }
    if (response.msg_info) {
        error_message = response.msg_info + '<br>'
    }
    $('#div_manager_detail').append(manager_icon);
    return error_message
}



// Funtion to clear session storage
function clear_session_data() {
    sessionStorage.clear();
    localStorage.clear();
    var req = window.indexedDB.deleteDatabase('store_attachments');
    req.onsuccess = function () {

                    var msg = "JMSG050";
                    var msg_type ;
                  msg_type = get_message_desc(msg);
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
                  var display5 = msg_type.messages_id_desc ;
                    alert(display5);

    };
}



// Function to get attachment data from session and display based on item
function get_attachment_IDB(item_number) {
    var item_number_check;
    var total_keys_available = []
    attachment_data_array = new Array();
    var objectStore = db.transaction("attachments").objectStore("attachments");
    objectStore.openCursor().onsuccess = function (event) {
        var cursor = event.target.result;
        if (cursor) {
            attachment_data_object = {}
            attachment_pk = cursor.value.attachment_data
            if (attachment_pk.includes('attachment_data' + item_number)) {
                attachment_data_object.id = attachment_pk
                item_number_check = cursor.value.attachment_data.substr(-3).split('_')[0]
                if (item_number_check.includes(item_number_attached)) {
                    total_keys_available.push(parseInt(cursor.value.attachment_data.substr(-1)))
                }
                attachment_data_object.dataUrl = cursor.value.dataUrl
                attachment_data_object.file_extension = cursor.value.file_extension_id
                attachment_data_object.file_name = cursor.value.file_name
                attachment_data_object.no_attachments = cursor.value.no_attachments
                attachment_data_object.attachment_name = cursor.value.attachment_name
                attachment_data_object.type = cursor.value.type
                attachment_data_array.push(attachment_data_object)
            }
            cursor.continue();
        } else {
            max_number_of_file_attached = Math.max.apply(Math, total_keys_available)
            if (typeof item_number_check != 'undefined') { sessionStorage.setItem('last_added_file_number-' + item_number_check, max_number_of_file_attached) }
            var attachment_tbody_content = '';
            $('#attachment_tbody_id-' + item_number).empty()
            for (i = 0; i < attachment_data_array.length; i++) {
                array_data = attachment_data_array[i]
                item_file_number = array_data.id.substr(-3)
                file_name = array_data.file_name
                attachment_name = array_data.attachment_name
                attachment_data = array_data.dataUrl
                type = array_data.type
                attachment_tbody_content += '<tr><td>' + '<a href="' + attachment_data + '" download="' + file_name + '">' + attachment_name + '</a>' + '</td><td>' + type + '</td><td>' + file_name + '<td class="hg_display"><i style="color: #F0B64D;" id="delete_attachment-' + item_file_number + '" onclick="delete_attachments(this)" class="fas fa-trash-alt"></td></tr>'
                document.getElementById('added_attachments_display-' + item_number).style.display = 'block';
            }
            $('#attachment_tbody_id-' + item_number).append(attachment_tbody_content)
            attachment_tbody_content = ''
        }
    };
}



// Function to get all the attachments from session and update to an array
var final_attachment_array = new Array()
var indexed_db_keys = new Array()
let get_attachment_data = async () => {
    final_attachment_array = []
    indexed_db_keys = []
    var attachment_array;
    let tx = db.transaction('attachments', 'readonly')
    let store = tx.objectStore('attachments')

    let allSavedItems = await store.getAll()
    allSavedItems.onsuccess = function (event) {
        attachment_array = event.target.result
        for (i = 0; i < attachment_array.length; i++) {
            data = attachment_array[i]
            indexed_db_keys.push(data.attachment_data)
            final_attachment_array.push(attachment_array[i])
        }
    }
}


/* Function to change goods reciever */
function select_goods_reciever() {
    var reciever_value = document.getElementById('search_receiver').value
    var split_name = reciever_value.split(' ');
    var first_name = split_name[0];
    var last_name = split_name[1];
    var email_id = split_name.pop();

    var goods_reciever_email = {};
    goods_reciever_email.email_id = email_id;
    var goods_reciever_data = ajax_update_goods_reciever(goods_reciever_email);

    if (goods_reciever_data) {
        var empty_space = " "
        var reciever_name = first_name.concat(empty_space, last_name);
        document.getElementById('receiver').innerHTML = reciever_name
        $('#receiver').addClass(response.user_name)
    }

}

// Order shopping cart function ajax call
var shopping_cart_number = '';
function order_shopping_cart_ajax(sc_data) {

    var order_sc_response = ajax_order_shopping_cart(sc_data);

    if (order_sc_response) {
        shopping_cart_number = response.sc_details[0]
        clear_session_data()
        display_third_step("ORDER_SC")
        success_message = 'Shopping cart ' + response.sc_details[1] + ' with number <a>' + response.sc_details[0] + '</a> ordered successfully'
        $('#sc_success_messages').html(success_message);
        document.getElementById('sc_success_messages').style.display = 'block';
        $('#sc_success_messages').show();
        $("#id_del_ind_checkbox").prop("hidden", false);
    }
}



// Save shopping cart function ajax call
function save_shopping_cart_ajax(sc_data) {

    var save_sc_response = ajax_save_shopping_cart(sc_data);

    if (save_sc_response.sc_details) {
        success_message = 'Shopping cart ' + response.sc_details[1] + ' with number ' + response.sc_details[0] + ' saved successfully';
        $('#sc_success_messages').html(success_message);
        document.getElementById('sc_success_messages').style.display = 'block';
        $('#sc_success_messages').show();
        clear_session_data();
        window.indexedDB.deleteDatabase('store_attachments');
        display_third_step("SAVE_SC");
        $('#hg_loder').modal('hide');
    } else if (save_sc_response.error_ms) {
        sc_detail = document.getElementById("sc_details");
        if (data.responseJSON.error_ms) {
            $('#sc_error_msg').html(data.responseJSON.error_ms)
        } else {

                    var msg = "JMSG018";
                    var msg_type ;
                  msg_type = get_message_desc(msg);
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
                  var display2 = msg_type.messages_id_desc;
                  $('#sc_error_msg').html(display2);

        }
        document.getElementById('sc_error_msg').style.display = 'block';
    }
}


    

// Funtion to print PDF of sc in 3rd step
function sc_print_pdf(){
    print_pdf_url = "/search/sc_pdf/"+shopping_cart_number
    window.open(print_pdf_url)
}

function clear_session_storage() {
    sessionStorage.removeItem('approver_text');
    sessionStorage.removeItem('sc_name');
}

// Function to display notes icon on adding suppplier or internal note 
$(document).on("change",'.sc_notes', function(){       
    var item_number = (this.id).split('-')[1];

    var sup_note_text = $('#sup_note_text-'+item_number).val();
    var int_note_text = $('#int_note_text-'+item_number).val();
    if(sup_note_text != '' || int_note_text != ''){
        $('#notes_added-'+item_number).prop("hidden", false);
    } else {
        $('#notes_added-'+item_number).prop("hidden", true);
    };
});
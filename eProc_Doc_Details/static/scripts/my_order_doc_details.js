var GLOBAL_ID_IGNORE_LIST = ['select_acc_type','catalog_quantity','CC - Cost Center','AS - Asset','WBS - Project','select_gl_acc_num','attachment','internal','external', 'select_item-', 'id_description', 'upl_prod_cat', 'currency', 'id_overall_limit', 'id_expected_value', 'req', 'StartDate', 'EndDate', 'OnDate', 'upl_supp_id', 'follow_up_actions']


//on change in input, select, textarea add sc_field_change class
$(document).ready(function () {
    $('#nav_menu_items').remove();
    $("body").css("padding-top", "3.7rem");
    $(".majjaka-main-navbar").css("box-shadow", "0px 0px 10px 0px rgba(0, 0, 0, 0.45)");
    $('.text-dark').hide();
    $('.editable_mode').hide();

    let document_url = location.href.split('/')
    if(document_url.includes('edit')){
        document_edit_mode();
        check_shopping_cart('check', 'sc_data', highest_item_acc_asgn_cat, highest_item_change_acc_value);
    }
    
    $('input, select, textarea').on('change', function () {
        element_id = this.id
        var id_value = element_id.split('-');
        if (id_value[0] !== 'select_item'){
            if (!(GLOBAL_ID_IGNORE_LIST.includes(element_id)) ){
                //if (!(element_id.includes('attachment') || element_id.includes('internal') || element_id.includes('external'))) {
                    var sc_id = $(this).attr("id");
                    $(this).addClass('sc_field_change');
                //}
            }
        }
    });
    for (i = 1; i <= total_items; i++) {
        window['previous_attachment-' + i] = document.getElementById('attachment_tbody_id-' + i).innerHTML
        var rowCount = $('#attachment_tbody_id-' + i).children('tr').length;
        if (rowCount == 0) {
            document.getElementById('added_attachments_display-' + i).style.display = 'none';
        }
    }

});

const close_manager_detail_popup = () => {
    $('body').css({
        'overflow': 'auto',
        'pointer-events':'auto'
    })
    document.getElementById('manger_pop_up').style.display='none'
}

$("#display_approver_div").click(function () {
    $('html,body').animate({
        scrollTop: $("#approval_process_overview").offset().top
    },
        'slow');
});


var indexedDB_count;

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
    window.alert(display)
}

var db;
var request = window.indexedDB.open("store_attachments_document_details", 1);

request.onerror = function (event) {
    console.log("error: ");
};

request.onsuccess = function (event) {
    db = request.result;
    var transaction = db.transaction(['attachments'], 'readonly');
    var objectStore = transaction.objectStore('attachments');

    var countRequest = objectStore.count();
    countRequest.onsuccess = function () {
        indexedDB_count = countRequest.result;
    }
};

request.onupgradeneeded = function (event) {
    var db = event.target.result;
    var objectStore = db.createObjectStore("attachments", { keyPath: "attachment_data" });

}

var GLOBAL_ACCOUNTING_DATA_CHANGE_TYPE = '';
var GLOBAL_ACCOUNTING_DATA_CHANGE_GUID = '';
var edit_row_index = '';
// Function to open change account assignment pop-up
function changeAccCat(element,loop_counter) {
    edit_row_index = loop_counter;
    var gl_acc_value = ''
    console.log("edit item - " + edit_row_index)
    var button_type = element.split('-')[1]
    GLOBAL_ACCOUNTING_DATA_CHANGE_TYPE = button_type
    if (button_type == "header")
    {
        GLOBAL_ACCOUNTING_DATA_CHANGE_TYPE = button_type
        $('#gl_acc_change_id').css('display','none');
        var account_assignment_category = $('#ScAccounting-acc_cat-' + rendered_header_level_acc_guid[0]).html().trim()
        var account_assignment_value = $('#ScAccounting-acc_val-' + rendered_header_level_acc_guid[0]).html().trim()
        var header_account_assignment_category = account_assignment_category.split(' - ')[0]
        var data = {}
        data.acc = header_account_assignment_category
        data.acc_desc = account_assignment_category
        update_accounting_popup_data(data, account_assignment_value, gl_acc_value)
    }
    else
    {
        $('#gl_acc_change_id').css('display','block');
        split_id_accounting = element.split('-')
        place_to_be_updated = split_id_accounting[1]
        accounting_change_guid = split_id_accounting[2]
        GLOBAL_ACCOUNTING_DATA_CHANGE_GUID = accounting_change_guid
        var account_assignment_category = $('#ScAccounting-acc_cat-' + accounting_change_guid).html().trim()
        var account_assignment_value = $('#ScAccounting-acc_val-' + accounting_change_guid).html().trim()
        gl_acc_value = $('#ScAccounting-gl_acc_num-' + accounting_change_guid).html().trim()
        var header_account_assignment_category = account_assignment_category.split(' - ')[0]
        var data = {}
        data.acc = header_account_assignment_category
        data.acc_desc = account_assignment_category
        update_accounting_popup_data(data, account_assignment_value, gl_acc_value)

    }
    $('#change_acc_cat').modal('show');
}


const get_title = {
    'AS - Asset': 'Asset',
    'CC - Cost Center': 'Cost Center',
    'WBS - Project': 'WBS'
}

function display_block(acc_ass_val) {
    $(".hg_acc_val_class_div").hide();
    switch (acc_ass_val) {
        case "CC":
            document.getElementById('id_cc_drop_down').style.display = 'block'
            break;
        case "WBS":
            document.getElementById('id_wbs_drop_down').style.display = 'block'
            break;
        case "OR":
            document.getElementById('id_or_drop_down').style.display = 'block'
            break;
        case "AS":
            document.getElementById('id_asset_drop_down').style.display = 'block'
            break;
        default:
    }

}

// on click of edit icone
function edit_sc_name() {
    $('#edit_sc_name_window').modal('show');

    var sc_name = document.getElementById('ScHeader-description-' + GLOBAL_HEADER_GUID).innerHTML;

    document.getElementById('sc_name_input').value = sc_name
}

// on click of save edit popup
function submitSCname() {
    var sc_name = document.getElementById('sc_name_input').value;
    $("#sc_name_input").removeClass("sc_field_change")
    document.getElementById('ScHeader-description-' + GLOBAL_HEADER_GUID).innerHTML = sc_name
    $('#ScHeader-description-' + GLOBAL_HEADER_GUID).addClass("sc_field_change")

    $('#edit_sc_name_window').modal('hide');
}


// Function to trigger check SC on click of button
$("#id_order_sc").on("click", function () {
    check_shopping_cart('order', 'sc_data', highest_item_acc_asgn_cat, highest_item_change_acc_value);

});

// Function to trigger save SC on click of button
$("#id_save_sc").on("click", function () {
    save_my_order_doc_detail('save')
});


$('#save_approver_note').click(function(){
    var txt = $('#approver_text').val()
    if (txt==''){
        console.log("it is null")
    } else{
        $('#add_approver_note_btn').removeClass('btn-primary').addClass('btn-success');
        $('#add_approver_note_btn').children().removeClass('fa-plus').addClass('fa-check');
    }
});

function check_manager_detail(response){
    var double_angular = ''
    var manager_icon = ''
    manager_detail = response.manager_detail.length
    GLOBAL_MANAGER_DETAIL = response.approver_id;
    $('#div_manager_detail').empty();
    var manager_icon = '';
    $('#id_dynamic').empty();
    if (response.manager_detail) {
        $.each(response.manager_detail, function (i, item) {
            double_angular = '<div class="workflow-overview__next-icon-container"><i class="fas fa-angle-double-right fa-3x"></i></div>';
            manager_icon += '' + double_angular + '<div class="workflow-overview__user-icon-container"><div class="workflow-user-bg workflow-inactive"><i class="fas fa-user-tie fa-3x" aria-hidden="true"> </i></div><button type="button" class="button-workflow-user">' + item.first_name + '</button></div>';
        });
    }
    if (response.error_message) {
        $('#sc_error_msg').append(response.error_message)
        $('#sc_error_msg').show()
    }
    $('#div_manager_detail').append(manager_icon);
}

const document_edit_mode = () => {
    is_edit = true;
    $('#shopping_cart_mode').html('Edit Shopping Cart')
    document.getElementById('id_edit_sc').style.display = 'none';
    $('.editable_mode').show()
    $(".hg_is_hidden").prop("hidden", false);
    $(".hg_is_disabled").prop("disabled", false);
    item_call_off = ''
    item_guid_number = ''
    item_eform = ''
    item_number = ''
    $('input:checkbox').removeAttr('checked');
    $('#add_id').prop('hidden', false)
}

// // Function to change doc deatils to editable mode 
// $("#id_edit_sc").on("click", function () {
//     get_attachment_data().then((value) => null)
//     on_click_sc_completion = true;

//     var delivery_dates = new Array()
//     td_id = $('td[id^="del_date-"]')
//     for (i = 0; i < td_id.length; i++) {
//         delivery_dates.push(td_id[i].id)
//     }
//     update_date_requirements = {}
//     update_date_requirements['header_guid'] = GLOBAL_HEADER_GUID
//     update_date_requirements['delivery_dates'] = delivery_dates

//     var update_date_req_result = ajax_update_date_requirements(update_date_requirements);

//     if(update_date_req_result) {
//         $.each(response.updated_date, function (key, value) {
//             $('#' + key).text(value);
//         });
//         document_edit_mode();

//     }

// });


//############ Functions to add and delete attachments for items #############

// Function to convert File type to base64 type
const toBase64 = file => new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result);
    reader.onerror = error => reject(error);
});

async function upload_attachments(id) {
    split_id = id.split('-')
    item_number = split_id[2]
    item_guid = split_id[3]
    item_number_attached = item_number
    file_number = 0;
    last_added_file_number = sessionStorage.getItem('last_added_file_number_doc_detail-' + item_number)
    previous_attachment = document.getElementById('attachment_tbody_id-' + item_number).innerHTML
    if (last_added_file_number != null) {
        file_number = parseInt(last_added_file_number)
    }
    input_id = id.split('-')[1]
    const file = document.querySelector('#' + input_id + '-' + item_number)
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
        $('#attachment_error' + item_number).html(display8+ "attachment type")
        return false;
    } else {
        $('#attachment_error' + item_number).html('')
        if (internal_radio_check) {
            type = 'Internal Use';
        } else {
            type = 'External Use'
        }
    }
    attachment_value = document.getElementById('attachment_data-' + item_number).value
    attachment_name = document.getElementById('attachment_name' + item_number).value
    is_special_character = check_for_special_char(attachment_name)
    if(!is_special_character){
                          
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
        $('#attachment_error'+item_number).html(display8+ "Attachment name")
        return false;
    }
    if (!attachment_value) {
          
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
        $('#attachment_error' + item_number).html(display8+ "files to upload")
        return false;
    } else $('#attachment_error' + item_number).html('')
    if (!attachment_name) {
           
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
        $('#attachment_error' + item_number).html(display5+ " attachment name")
        return false;
    } else $('#attachment_error' + item_number).html('')

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
                .add({ attachment_data: attachment_id, dataUrl: base64_converted, attachment_name: attachment_name, no_attachments: no_attachments, file_name: attached_file.name, file_extension_id: file_extension, type: type, item_guid: item_guid });

            request.onsuccess = function (event) {
                $('#attachment_name' + item_number).val('')
                $('#attachment_data-' + item_number).val('') 
                $('#internal' + item_number).prop('checked', false)
                $('#external' + item_number).prop('checked', false)
                get_attachment_data().then((value) => null)
            };

            request.onerror = function (event) {
                  
                    var msg = "JMSG046";
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
                  alert(display);

            }
        }
    }
    get_attachment_IDB(item_number)
    display_attachment_icon(item_guid, "UPLOAD");
}


var item_number_attached = '';
// Function to get attachment data from session and display based on item
function get_attachment_IDB(item_number) {
    var item_number_check;
    var total_keys_available = []
    attachment_data_array = new Array();
    total_items = total_items;
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
            if (typeof item_number_check != 'undefined') { sessionStorage.setItem('last_added_file_number_doc_detail-' + item_number_check, max_number_of_file_attached) }
            var attachment_tbody_content = '';
            for (i = 0; i < attachment_data_array.length; i++) {
                $('#attachment_tbody_id-' + item_number).empty()
                array_data = attachment_data_array[i]
                item_file_number = array_data.id.substr(-3)
                file_name = array_data.file_name
                attachment_name = array_data.attachment_name
                attachment_data = array_data.dataUrl
                type = array_data.type
                attachment_tbody_content += window['previous_attachment-' + item_number] + '<tr><td>' + '<a href="' + attachment_data + '" download="' + file_name + '">' + attachment_name + '</a>' + '</td><td>' + type + '</td><td>' + file_name + '<td class="hg_is_hidden"><i style="color: #F0B64D;" id="delete_attachment-' + item_file_number + '" onclick="delete_attachments(this)" class="fas fa-trash-alt"></td></tr>'
                $('#attachment_tbody_id-' + item_number).append(attachment_tbody_content)
                document.getElementById('added_attachments_display-' + item_number).style.display = 'block';
            }
        }
    };
}


var final_attachment_array = new Array()
var indexed_db_keys = new Array()
let get_attachment_data = async () => {
    final_attachment_array = []
    indexed_db_keys = []
    var attachment_array;
    let tx = db.transaction('attachments', 'readonly')
    let store = tx.objectStore('attachments')

    // add, clear, count, delete, get, getAll, getAllKeys, getKey, put
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

// Function to delete attachment from item cart
function delete_attachments(element) {
    element_id = element.id
    if (element_id.includes('_')) {
        item_file_number = element.id.substr(-3)
        item_number = item_file_number.split('_')[0]
        attachment_id = 'attachment_data' + item_file_number
        var request = db.transaction(["attachments"], "readwrite")
            .objectStore("attachments")
            .delete(attachment_id);
    } else {
        element_id = element.id.split('-')
        guid = element_id[1]
        item_number = element_id[0]
        item_guid = element_id[2]
        if (element_id != '') {

            delete_attachment_data = {};
            delete_attachment_data.attachment_guid = guid;
            delete_attachment_data.document_number = $('#document_number').html();
            delete_attachment_data.item_guid = item_guid;
            delete_attachment_data.header_guid = $('#header_guid').val();

            delete_attachment_result = ajax_delete_attachments(delete_attachment_data);

            if(delete_attachment_result) {
                array_object = response.available_attachments;
                previous_attachment = '';
                path_url = attachment_path_url;
                for (i = 0; i < array_object.length; i++) {
                    previous_attachment += '<tr id="' + 'available_attachments-' + array_object[i].attachment_guid + '">' + '<td>' + '<a href="' + path_url + array_object[i].file_path + '">' + array_object[i].attachment_name + '</a>' + '</td>' + '<td>' + array_object[i].type + '</td>' + '<td>' + array_object[i].file_name + '</td>' + '<td><i style="color: #F0B64D;" id="' + array_object[i].item_num + '-' + array_object[i].attachment_guid + '-' + array_object[i].item_guid + '" onclick="delete_attachments(this)" class="fas fa-trash-alt"></i></td>' + '</tr>'
                }
                window['previous_attachment-' + item_number] = previous_attachment

            }
        }
    }

    $(element).parent().parent().remove();
    var rowCount = $('#attachment_tbody_id-' + item_number).children('tr').length;
    if (rowCount == 0) {
        document.getElementById('added_attachments_display-' + item_number).style.display = 'none';
        display_attachment_icon(item_guid, "DELETE");
    }

    var transaction = db.transaction(['attachments'], 'readonly');
    var objectStore = transaction.objectStore('attachments');

    var countRequest = objectStore.count();
    countRequest.onsuccess = function () {
        if (countRequest.result == 0) {
            sessionStorage.removeItem('last_added_file_number_doc_detail-' + item_number)
        }
    }
}

// function to show or hide attachment existence icon based on action
const display_attachment_icon = (item_guid, action) => {
    if(action=='UPLOAD') {
        $('#attachment_added-'+item_guid).css("display", "block");
    } else if (action=='DELETE') {
        $('#attachment_added-'+item_guid).css("display", "none");
    }
}

// Start of  SC UI checks
const check_ui_errors_warnings = (error_messages) => {
    var warning_messages = ''
    var error_messages = ''
    check_address_number = document.getElementsByClassName('check_address_number')
    address_number_array = new Array();
    for(i = 0; i < check_address_number.length; i++) {
        address_number_array.push(check_address_number[i].innerHTML)
    }
    is_multiple_delivery_addresses = address_number_array.every( (val, i, arr) => val === arr[0] )
    if(!is_multiple_delivery_addresses){
                 
                    var msg = "JMSG026";
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
                  warning_messages += display ;

        $('#sc_warning_messages').html(warning_messages)
        $('#sc_warning_messages').show()
    } else $('sc_warning_messages').hide()
    
    check_account_assignment_type = document.getElementsByClassName('change_account_type')
    change_acc_type_array = new Array();
    for(i = 0; i < check_account_assignment_type.length; i++) {
        change_acc_type_array.push(check_account_assignment_type[i].innerHTML)
    }
    is_multiple_account_assignment = change_acc_type_array.every( (val, i, arr) => val === arr[0] )
    if(!is_multiple_account_assignment){
                  
                    var msg = "JMSG047";
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
                  warning_messages += display;

        $('#sc_warning_messages').html(warning_messages)
        $('#sc_warning_messages').show()
    } else $('sc_warning_messages').hide() 
    if(is_multiple_account_assignment){
        check_account_assignment_value = document.getElementsByClassName('check_account_assignment_values')
        change_acc_value_array = new Array();
        for(i = 0; i < check_account_assignment_value.length; i++) {
            change_acc_value_array.push(check_account_assignment_value[i].innerHTML)
        }
        is_multiple_account_assignment_value = change_acc_value_array.every( (val, i, arr) => val === arr[0] )
        if(!is_multiple_account_assignment_value){
                
                    var msg = "JMSG048";
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
                 warning_messages += display;

            $('#sc_warning_messages').html(warning_messages)
            $('#sc_warning_messages').show()
        } else $('sc_warning_messages').hide() 
    }

    for(j = 0; j < internal_supplier_error_itemNumber.length; j++ ) {
           var url_new = "{% url 'eProc_Basic:get_message_description' %}";
            var msg = "JMSG003";
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
          var display4 = msg_type.messages_id_desc;
          error_messages += 'Error at item ' + internal_supplier_error_itemNumber[j] + ': ' +  display4 + "Internal or supplier note" + '<br>'

    }

    return error_messages
}
// End of sc UI checks

// Function to get my order data for check
function get_data_for_check() {
    var data_for_check = new Array()
    var supplier_id = '';
    supplier = $("[id^=supp-]")
    adr_num = $("[id^=address_number_]")
    for (i = 0; i < supplier.length; i++) {
        data = {}
        incremented_i = i + 1
        var supp_id = supplier[i].id;
        var address_info = 'ScAddresses-address_number-' + rendered_addr_guid[i];
        var acc_info = 'ScAccounting-acc_cat-' + rendered_acc_guid[i];
        var acc_acc_cat = (document.getElementById(acc_info).innerHTML).split(' - ')[0].trim();
        data.acc_acc_cat = acc_acc_cat.replace(/\s/g, '')
        var gl_num_info = 'ScAccounting-gl_acc_num-' + rendered_acc_guid[i];
        var prod_cat_info = 'prod_cat_id-' + rendered_item_guid[incremented_i - 1];
        supplier_info = document.getElementById(supp_id).textContent;
        var internal_note = document.getElementById("Notes-note_text-"+rendered_int_note[i] + '-I').value
        var supplier_note = document.getElementById("Notes-note_text-" + rendered_supp_note[i] + "-S").value
        remove_special_characters(internal_note, supplier_note, incremented_i)
        data.item_num = incremented_i
        data.supplier_name = document.getElementById(supp_id).textContent;
        data.address_number = document.getElementById(address_info).innerHTML
        data.acc_acc_cat = (document.getElementById(acc_info).innerHTML).split(' - ')[0].trim()
        data.acc_acc_val = (document.getElementById('ScAccounting-acc_val-' + rendered_acc_guid[i]).innerHTML).split(' - ')[0].trim()
        data.gl_acc_num = (document.getElementById(gl_num_info).innerHTML).split(' - ')[0]
        delivery_date = document.getElementById('del_date-' + rendered_item_guid[i]).innerHTML
        if(delivery_date.includes('limit-')){
            delivery_date = (document.getElementById('del_date-limit-' + rendered_item_guid[i]).innerHTML).split('limit-')[1]
        }
        data.delivery_date = delivery_date
        data.item_guid = rendered_item_guid[i]

        data.prod_cat = (document.getElementById(prod_cat_info).innerHTML)
        create_id = 'product_id-' + incremented_i + '-'
        get_product_ids = $('[id^="' + create_id + '"]')
        if(get_product_ids.length > 0){
            split_array = get_product_ids[0].id.split('-')
            data.product_id = split_array[2]
            data.lead_time  = split_array[3]
            data.item_price = document.getElementById("ScIem-price-"+rendered_item_guid[i]).innerHTML
            data.quantity = document.getElementById("item_quantity-"+rendered_item_guid[i]).innerHTML
        }
        data_for_check.push(data)
    }
    return data_for_check
}    

// Funtion to add a new item to saved cart
function add_item_to_saved_cart(item_type) {
    doc_number_encrypted = doc_number_encrypted
    header_val = document.getElementById("header_guid").value;
    url_remove_display = location.href.split('/')
    url_remove_display.pop()
    url_remove_display = url_remove_display.join('/')
    localStorage.setItem('opened_document-' + doc_number_encrypted, url_remove_display)

    if (item_type === '01') {
        url = '/shop/products_services/All/' + 'doc_number-' + doc_number_encrypted
        location.href = url
    }
    if (item_type === '02') {
        url = '/shop/products_services/All/' + 'doc_number-' + doc_number_encrypted
        location.href = url
    }
    if (item_type === '03') {
        url = '/add_item/purchase_requisition/' + 'doc_number-' + doc_number_encrypted
        location.href = url
    }
}

// Funtion to update goods reciever
function select_goods_reciever(){
    var reciever_value = document.getElementById('search_receiver').value
    var split_name = reciever_value.split(' ');
    var first_name = split_name[0];
    var last_name = split_name[1];
    var email_id = split_name.pop();

    var goods_reciever_email = {};
    goods_reciever_email.email_id = email_id;
    var goods_reciever_data = ajax_update_goods_reciever(goods_reciever_email);

    if(goods_reciever_data) {
        var empty_space = " "
        var reciever_name = first_name.concat(empty_space, last_name);
        document.getElementById('ScHeader-requester-'+ GLOBAL_HEADER_GUID).innerHTML = reciever_name;
        $('#ScHeader-requester-'+ GLOBAL_HEADER_GUID).addClass(response.user_name);
    }
}

// Function to display notes icon on adding suppplier or internal note 
$(document).on("change",'.sc_notes', function(){       
    var get_selected_note_guid = (this.id).split('-')[2];
    var note_type = (this.id).split('-')[3];
    var item_guid = '';

    // if 'S' get internal note guid
    if(note_type == 'S') {
        var [item_guid, s_or_i_note_guid] = get_notes_data(get_selected_note_guid, note_type);
        var sup_note_text = $('#Notes-note_text-'+get_selected_note_guid+'-S').val();
        var int_note_text = $('#Notes-note_text-'+s_or_i_note_guid+'-I').val();
    } 
    // if 'I' get supplier note guid
    else if (note_type == 'I') {
        var [item_guid, s_or_i_note_guid] = get_notes_data(get_selected_note_guid, note_type);
        var sup_note_text = $('#Notes-note_text-'+s_or_i_note_guid+'-S').val();
        var int_note_text = $('#Notes-note_text-'+get_selected_note_guid+'-I').val();
    }
    
    if(sup_note_text != '' || int_note_text != ''){
        $('#notes_added-'+item_guid).css("display", "block");
    } else {
        $('#notes_added-'+item_guid).css("display", "none");
    };
});

// 
function get_items_guids(get_selected_note_guid, note_type) {
    if(note_type == 'I') {
        for (i=0; i<rendered_int_details.length; i++) {
            var get_notes_guid = rendered_int_details[i].note_guid;
            if(get_selected_note_guid == get_notes_guid) {
                return rendered_int_details[i].item_guid;
            }
        };
    } else if (note_type == 'S') {
        for (i=0; i<rendered_supplier_note_details.length; i++) {
            var get_notes_guid = rendered_supplier_note_details[i].note_guid;
            if(get_selected_note_guid == get_notes_guid) {
                return rendered_supplier_note_details[i].item_guid;
            }
        };
    };
};

// 
function get_notes_data (get_selected_note_guid, note_type) {
    if(note_type == 'S') {
        var item_guid = get_items_guids(get_selected_note_guid, note_type);

        for (i=0; i<rendered_int_details.length; i++) {
            var get_item_guid = rendered_int_details[i].item_guid;
            if(item_guid == get_item_guid) {
                return [item_guid, rendered_int_details[i].note_guid];
            };
        };
    } else if(note_type == 'I') {
        var item_guid = get_items_guids(get_selected_note_guid, note_type);

        for (i=0; i<rendered_supplier_note_details.length; i++) {
            var get_item_guid = rendered_supplier_note_details[i].item_guid;
            if(item_guid == get_item_guid) {
                return [item_guid, rendered_supplier_note_details[i].note_guid];
            }
        };
    };
};


function get_item_guid_edit (item_number) {
    index = item_number-1;
    item_guid_data = rendered_item_guid[index];
    return item_guid_data;
}
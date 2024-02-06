var message_id_desc_data = new Array();
var validate_add_attributes = [];
var main_table_low_value = [];
var message_id_desc={};

// $(document).ready(function () {
//     $('#nav_menu_items').remove();
//     $("body").css("padding-top", "3.7rem");
//     $("#display_basic_table").DataTable({
//            "columnDefs": [{
//            'searchable':false,
//             'orderable':false,
//             "bSort":false,
//             "selectAllPages": false,
//        }],
//      })
//     table_sort_filter('display_basic_table');
// });

//******************
// on click copy icon display the selected checkbox data
function onclick_copy_button() {
    GLOBAL_ACTION = "COPY"
    onclick_copy_update_button()
    document.getElementById("id_del_add_button").style.display = "block";
}

//***********************************
// on click update icon display the selected checkbox data to update
function onclick_update_button() {
    GLOBAL_ACTION = "UPDATE"
    onclick_copy_update_button()
    document.getElementById("id_del_add_button").style.display = "none";
}

//onclick of cancel empty the popup table body and error messages
$(".remove_upload_data").click(() => {
    $("#id_error_msg_id").html("");
    $("#id_popup_tbody").empty();
    $("#id_error_msg_id").empty();
    $('#msg_desc_Modal').modal('hide');
    $("#id_error_msg_id").prop("hidden", true);
    $("#id_error_msg_length").prop("hidden", true);
    $("#id_check_error_messages").prop("hidden", true);
    $("#id_check_success_messages").prop("hidden", true);
    $("#id_check_special_character_messages").prop("hidden", true)
    $("#id_check_data").prop("hidden", true);
    $('#id_popup_table').DataTable().destroy();
});

//*************************
// on click edit icon display the data in edit mode
function onclick_edit_button() {
    //display the add,cancel and upload buttons and select all checkbox,select heading and checkboxes for each row
    $('#display_basic_table').DataTable().destroy();
    $("#hg_select_checkbox").prop("hidden", false);
    $(".class_message_checkbox").prop("hidden", false);
    $("#hg_select_checkbox").show();
    //hide the edit,delete,copy and update buttons
    $("#id_edit_data").hide();
    $("#id_check_all").show();
    $("#id_cancel_data").show();
    table_sort_filter('display_basic_table');
}

// **********************************
//onclick of checkbox display delete,update and copy Buttons
function valueChanged() {
    if ($('.checkbox_check').is(":checked")) {
        $("#id_delete_data").show();
        $("#id_copy_data").show();
        $("#id_update_data").show();
    }
    else {
        $("#id_delete_data").hide();
        $("#id_copy_data").hide();
        $("#id_update_data").hide();
    }
}

//onclick of cancel display the table in display mode............
function display_basic_db_data() {
    $('#display_basic_table').DataTable().destroy();
    $('#id_message_tbody').empty();
    var edit_basic_data = '';
    var desc = ''; var lang_code;
    $.each(rendered_message_id_desc_data, function (i, item) {
        lang_code = item.language_id;
        for (i = 0; i < render_language_data.length; i++) {
            if (lang_code == render_language_data[i].language_id)
                desc = render_language_data[i].description
        }
        edit_basic_data += '<tr><td class="class_message_checkbox"><input class="checkbox_check" onclick="valueChanged()" type="checkbox" required></td>'+
        '<td>' + item.messages_id + '</td><td>' + item.messages_id_desc + '</td>'+
        '<td>' + desc + '</td>'+
        '<td hidden>' + item.msg_id_desc_guid + '</td>'+
       '</tr>';
    });
    $('#id_message_tbody').append(edit_basic_data);
    $("#hg_select_checkbox").prop("hidden", true);
    $(".class_message_checkbox").prop("hidden", true);
    $('input:checkbox').removeAttr('checked');
    $("#id_edit_data").show();
    $("#id_cancel_data").hide();
    $("#id_delete_data").hide();
    $("#id_copy_data").hide();
    $("#id_update_data").hide();
    $('#id_save_confirm_popup').modal('hide');
    $("#id_delete_confirm_popup").hide();
    $("#id_check_all").hide();
    table_sort_filter('display_basic_table');
}

function display_error_message(error_message){
    $("#error_msg_id").css("display", "block");
     $("#error_msg_id").prop("hidden", false)
    $('#error_message').text(error_message);
    document.getElementById("error_msg_id").style.color = "Red";
    document.getElementById("error_msg_id").innerHTML = error_message;
    $('#id_save_confirm_popup').modal('hide');
    $('#msg_desc_Modal').modal('show');
}

// Functtion to hide and display save related popups
$('#save_id').click(function () {
    $('#msg_desc_Modal').modal('hide');
    message_id_desc_data = read_popup_data();
    $('#id_save_confirm_popup').modal('show');
});

//Read popup table data
function read_popup_data() {
    $('#id_popup_table').DataTable().destroy();
    message_id_desc_data = new Array();
    validate_add_attributes = [];
    $("#id_popup_table TBODY TR").each(function () {
        var row = $(this);
        message_id_desc={};
        message_id_desc.del_ind = row.find("TD").eq(5).find('input[type="checkbox"]').is(':checked');
        message_id_desc.messages_id = row.find("TD").eq(1).find('select[type="text"]').val();
        message_id_desc.messages_id_desc = row.find("TD").eq(2).find('input[type="text"]').val();
        message_id_desc.language_id = row.find("TD").eq(3).find('select[type="text"]').val();
        message_id_desc.msg_id_desc_guid = row.find("TD").eq(4).find('input[type="text"]').val();
        if (message_id_desc == undefined){
            message_id_desc.messages_id = row.find("TD").eq(1).find('select[type="text"]').val();
        }
        if(message_id_desc.msg_id_desc_guid == undefined) {
            message_id_desc.msg_id_desc_guid = ''
        }
        var desc='';
        for (i = 0; i < render_language_data.length; i++) {
            if (message_id_desc.language_id == render_language_data[i].language_id)
                desc = render_language_data[i].description;
        }
         var compare = message_id_desc.messages_id+'-'+desc;
        validate_add_attributes.push(compare);
        message_id_desc_data.push(message_id_desc);
    });
    table_sort_filter('id_popup_table');
    return message_id_desc_data;
}

// Function for add a new row data
function new_row_data() {
    basic_add_new_html = '<tr><td><input type="checkbox" required></td>'+
    '<td><select id="messages_id" name="messages_id" title="Select.." class="form-control"  type="text" onchange="get_language_dropdown(this)">'+ message_id_dropdown +'</select></td>' +
    '<td><input class="input form-control check_special_char" type="text" id="messages_desc" name="messages_desc"  required></td>'+
    '<td><select id="language" name="language_id" title="Select..." class="form-control"  type="text">' + language_dropdown +'</select></td>' +
    '<td hidden><input  type="text" class="form-control"  name="guid"></td>'+
    '<td class="class_del_checkbox" hidden><input type="checkbox" required></td>'+
    '</tr>';
    $('#id_popup_tbody').append(basic_add_new_html);
    table_sort_filter('id_popup_table');
}

function get_language_dropdown(selectElement) {
    var selectedMessage = selectElement.value;
    var language_dropdown = $(selectElement).closest('tr').find('.form-control').eq(2);
    var languages = main_table_data[selectedMessage];
    var usedLanguage = {}; // Object to store the used node values for the selected node type

    // Loop through the node values in the main_table_data and store the used ones for the selected node type
    $.each(languages, function(index, value) {
        usedLanguage[value] = true;
    });
    language_dropdown.empty();

    // Now, populate the dropdown with only the unused node values
    $.each(render_language_data, function(i, item) {
        var language = item.language_id;
        var description = item.description;

        if (!usedLanguage.hasOwnProperty(description)) {
            language_dropdown.append('<option value="' + language + '">' + description + '</option>');
        }
    });
}

// Function to get main table data
function get_main_table_data() {
    main_table_low_value = [];
    $('#display_basic_table').DataTable().destroy();
    $("#display_basic_table TBODY TR").each(function () {
        var row = $(this);
        var main_attribute = {};
        main_attribute.messages_id = row.find("TD").eq(1).html();
        main_attribute.messages_desc = row.find("TD").eq(2).html();
        main_attribute.language_id = row.find("TD").eq(3).html();
        var compare_maintable = main_attribute.messages_id+'-'+main_attribute.language_id;
        main_table_low_value.push(compare_maintable);
    });
    table_sort_filter('display_basic_table');
}

function get_msg_id_data() {
    main_table_data = {}; // Object to store node values for each node type
    $('#display_basic_table').DataTable().destroy();
    $("#display_basic_table TBODY TR").each(function() {
        var row = $(this);
        var main_attribute = {};
        main_attribute.messages_id = row.find("TD").eq(1).html();
        main_attribute.messages_desc = row.find("TD").eq(2).html();
        main_attribute.language_id = row.find("TD").eq(3).html();
        var compare_maintable = main_attribute.messages_id + '-' + main_attribute.messages_desc+ '-' + main_attribute.language_id;
        if (!main_table_data.hasOwnProperty(main_attribute.messages_id)) {
            main_table_data[main_attribute.messages_id] = [];
        }
        main_table_data[main_attribute.messages_id].push(main_attribute.language_id);
    });
    table_sort_filter('display_basic_table');
}

// Function to get the selected row data
function get_selected_row_data() {
    $("#display_basic_table TBODY TR").each(function () {
        var row = $(this);
        var message_id_desc_arr_obj = {};
        var lang_desc;
        var lang_code;
        lang_desc = row.find("TD").eq(3).html();
        for (i = 0; i < render_language_data.length; i++) {
            if (lang_desc == render_language_data[i].description)
                lang_code = render_language_data[i].language_id
        }
        message_id_desc_arr_obj.del_ind = row.find("TD").eq(0).find('input[type="checkbox"]').is(':checked');
        if(message_id_desc_arr_obj.del_ind){
            message_id_desc_arr_obj.messages_id = row.find("TD").eq(1).html();
            message_id_desc_arr_obj.messages_id_desc = row.find("TD").eq(2).html();
            message_id_desc_arr_obj.language_id = lang_code;
            message_id_desc_arr_obj.msg_id_desc_guid = row.find("TD").eq(4).html();
            main_table_message_id_desc_checked.push(message_id_desc_arr_obj);
        }
    });
}
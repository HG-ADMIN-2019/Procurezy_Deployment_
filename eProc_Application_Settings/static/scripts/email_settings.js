var email_setting_data = new Array();
var validate_add_attributes = [];
var main_table_low_value = [];

//onclick of add button display emailsModal popup and set GLOBAL_ACTION button value
function onclick_add_button(button) {
    email_type_dropdown();
    $("#error_msg_id").css("display", "none")
    $("#header_select").prop( "hidden", false );
    GLOBAL_ACTION = button.value
    $('#id_popup_table').DataTable().destroy();
    $("#id_popup_tbody").empty();
    $('#emailsModal').modal('show');
    new_row_data();  // Add a new row in popup
    $("#id_del_ind_checkbox").prop("hidden", true);
    document.getElementById("id_del_add_button").style.display = "block";
    $("#save_id").prop("hidden", false);
}

// on click update icon display the selected checkbox data to update
function onclick_update_button() {
    GLOBAL_ACTION = "UPDATE"
    onclick_copy_update_button("update")
    document.getElementById("id_del_add_button").style.display = "none";
}

//**********************************************************
function onclick_copy_update_button(data) {
    email_type_dropdown();
    $("#error_msg_id").css("display", "none")
    $('#display_basic_table').DataTable().destroy();
    $('#id_popup_table').DataTable().destroy();
    $("#id_popup_tbody").empty();
    //Reference the Table.
    var grid = document.getElementById("display_basic_table");
    //Reference the CheckBoxes in Table.
    var checkBoxes = grid.getElementsByTagName("INPUT");
    var edit_basic_data = "";
    var unique_input = '';
    //Loop through the CheckBoxes.
    for (var i = 1; i < checkBoxes.length; i++) {
        if (checkBoxes[i].checked) {
            var row = checkBoxes[i].parentNode.parentNode;
            if(GLOBAL_ACTION == "UPDATE"){
                unique_input = '<select class="form-control" type="text" name="email_type" disabled><option>' + row.cells[1].innerHTML + '</option></select>'
                edit_basic_data += '<tr><td hidden><input type="checkbox" required></td>'+
                    '<td>'+unique_input+'</td>'+
                    '<td><select class="form-control" type="text"  name="language_id" disabled><option>'+ row.cells[2].innerHTML +'</option></select></td>'+
                    '<td><textarea class="form-control check_special_char"  type="text"   name="email_subject" required>' + row.cells[3].innerHTML + '</textarea></td>'+
                    '<td><textarea class="form-control check_special_char" type="text"   name="email_header" required>' + row.cells[4].innerHTML + '</textarea></td>'+
                    '<td><textarea class="form-control check_special_char" type="text"  name="email_body" required>' + row.cells[5].innerHTML + '</textarea></td>'+
                    '<td><textarea class="form-control check_special_char" type="text"    name="email_footer" required>' + row.cells[6].innerHTML + '</textarea></td><td hidden><input class="form-control"  name="email_guid" required></td>'+
                    '<td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
                $("#header_select").prop("hidden", true);
            }
        }
    }
    $('#id_popup_tbody').append(edit_basic_data);
    $("#id_del_ind_checkbox").prop("hidden", true);
    $('#emailsModal').modal('show');
    table_sort_filter('id_popup_table');
    table_sort_filter('display_basic_table');
}

 //************************currency code
//onclick of cancel empty the popup table body and error messages
$(".remove_upload_data").click(() => {
    $("#id_error_msg").html("");
    $("#id_popup_tbody").empty();
    $("#id_error_msg").empty();
    $('#emailsModal').modal('hide');
    $("#id_error_msg").prop("hidden", true);
    $("#id_error_msg_email_type").prop("hidden", true);
    $("#id_error_msg_email_sub").prop("hidden", true);
    $("#id_error_msg_email_length").prop("hidden", true);
    $("#id_check_error_messages").prop("hidden", true);
    $("#id_check_success_messages").prop("hidden", true);
    $("#id_check_special_character_messages").prop("hidden", true)
    $("#id_check_data").prop("hidden", true);
    $('#id_popup_table').DataTable().destroy();
});

function display_error_message(error_message){  
    $('#error_message').text(error_message);
    document.getElementById("error_message").style.color = "Red";
    $("#error_msg_id").css("display", "block")
    $('#id_save_confirm_popup').modal('hide');
    $('#emailsModal').modal('show');
}

//*******************************************************
// on click add icon display the row in to add the new entries
function add_popup_row() {
    email_type_dropdown();
    $("#error_msg_id").css("display", "none")
    basic_add_new_html = '';
    var display_db_data = '';
    $('#id_popup_table').DataTable().destroy();
    $(".modal").on("hidden.bs.modal", function () {
        $("#id_error_msg").html(" ");
    });
    new_row_data();   // Add a new row in popup
    $('#delete_data').hide()
}

//onclick of cancel display the table in display mode............
function display_basic_db_data() {
    $('#display_basic_table').DataTable().destroy();
    $('#id_email_tbody').empty();
    var edit_basic_data = '';
    var lang_desc;
    var lang_code;

    $.each(rendered_email_data, function (i, item) {
        lang_code = item.language_id;
        for (i = 0; i < render_language_data.length; i++) {
            if (lang_code == render_language_data[i].language_id)
            lang_desc = render_language_data[i].description
        }
        edit_basic_data += '<tr ><td class="class_select_checkbox"><input class="checkbox_check" onclick="valueChanged()" type="checkbox" required></td>'+
        '<td>' + item.object_type + '</td>'+
        '<td>' + lang_desc + '</td>'+
        '<td>' + item.subject + '</td>'+
        '<td>' + item.header + '</td>'+
        '<td>' + item.body + '</td>'+
        '<td>' + item.footer + '</td>'+
        '<td hidden>' + item.email_contents_guid + '</td>'+
        '</tr>';
    });
    $('#id_email_tbody').append(edit_basic_data);
    $("#hg_select_checkbox").prop("hidden", true);
    $(".class_select_checkbox").prop("hidden", true);
    $('input:checkbox').removeAttr('checked');
    $('#id_edit_data').show();
    $('#id_cancel_data').hide();
    $('#id_delete_data').hide();
    $('#id_copy_data').hide();
    $('#id_update_data').hide();
    $('#id_save_confirm_popup').modal('hide');
    $('#id_delete_confirm_popup').modal('hide');
    $('#id_check_all').hide(); 
    table_sort_filter('display_basic_table');
}

// Function to hide and display save related popups
$('#save_id').click(function () {
    $('#emailsModal').modal('hide');
    email_setting_data = read_popup_data();
    $('#id_save_confirm_popup').modal('show');
});

//Read popup table data
function read_popup_data(){
    email_setting_data = new Array();
    validate_add_attributes = [];
    $("#id_popup_table TBODY TR").each(function () {
        var row = $(this);
        var language = row.find("TD").eq(2).find('select[type="text"]').val();
        for (i = 0; i < render_language_data.length; i++) {
            if (language == render_language_data[i].description){
                lang_id = render_language_data[i].language_id
            }
        }
        email={};
        email.del_ind = row.find("TD").eq(8).find('input[type="checkbox"]').is(':checked');
        email.email_type = row.find("TD").eq(1).find('select[type="text"]').val();
        email.email_subject = row.find("TD").eq(3).find('textarea[type="text"]').val();
        email.email_header = row.find("TD").eq(4).find('textarea[type="text"]').val();
        email.email_body = row.find("TD").eq(5).find('textarea[type="text"]').val();
        email.email_footer = row.find("TD").eq(6).find('textarea[type="text"]').val();
        email.email_guid = row.find("TD").eq(7).find('input[type="text"]').val();
        if(GLOBAL_ACTION == "UPDATE"){
            email.language_id = lang_id;
        }
        else
        {
            email.language_id = row.find("TD").eq(2).find('select[type="text"]').val();
        }
        if (email == undefined){
            email.email_type = row.find("TD").eq(1).find('select[type="text"]').val();
        }
        var compare = email.email_type+'-'+email.language_id
        validate_add_attributes.push(compare);
        email_setting_data.push(email);
    });
    return email_setting_data;
}

// Function for add a new row data
function new_row_data(){
    basic_add_new_html = '<tr><td><input  type="checkbox" required></td>'+
    '<td><select class="form-control"  type="text"  name="email_type" required>'+email_type_dropdwn+'</select></td>'+
    '<td><select class="form-control"  type="text"  name="language_id" required>'+language_dropdown+'</select></td>'+
    '<td><textarea class="form-control " type="text"  name="email_subject" required></textarea></td>'+
    '<td><textarea class="form-control check_special_char" type="text"  name="email_header" required></textarea></td>'+
    '<td><textarea class="form-control check_special_char" type="text"  name="email_body"  required></textarea></td>'+
    '<td><textarea class="form-control check_special_char" type="text"  name="email_footer" required></textarea></td>'+
    '<td hidden><input class="form-control" type="text" maxlength="100"  name="email_guid" required></td><td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
    $('#id_popup_tbody').append(basic_add_new_html);
    table_sort_filter('id_popup_table');
}

// Function to get main table data
function get_main_table_data(){
    main_table_low_value = [];
    $('#display_basic_table').DataTable().destroy();
    $("#display_basic_table TBODY TR").each(function() {
        var row = $(this);
        var main_attribute = {};
        var lang_desc;
        var lang_code;
        lang_desc = row.find("TD").eq(2).html();
        for (i = 0; i < render_language_data.length; i++) {
            if (lang_desc == render_language_data[i].description)
                lang_code = render_language_data[i].language_id
        }
        main_attribute.email_type = row.find("TD").eq(1).html();
        main_attribute.language_id = lang_code;
        var compare_maintable = main_attribute.email_type+'-'+main_attribute.language_id
        main_table_low_value.push(compare_maintable);
    });
    table_sort_filter('display_basic_table');
}

// Function to get the selected row data
function get_selected_row_data(){
    $("#display_basic_table TBODY TR").each(function () {
        var row = $(this);
        var email_arr_obj ={};
        var lang_desc;
        var lang_code;
        lang_desc = row.find("TD").eq(2).html();
        for (i = 0; i < render_language_data.length; i++) {
            if (lang_desc == render_language_data[i].description)
                lang_code = render_language_data[i].language_id
        }
        email_arr_obj.del_ind = row.find("TD").eq(0).find('input[type="checkbox"]').is(':checked');
        if(email_arr_obj.del_ind){
            email_arr_obj.email_type = row.find("TD").eq(1).html();
            email_arr_obj.language_id = lang_code;
            email_arr_obj.email_subject = row.find("TD").eq(3).html();
            email_arr_obj.email_header = row.find("TD").eq(4).html();
            email_arr_obj.email_body = row.find("TD").eq(5).html();
            email_arr_obj.email_footer = row.find("TD").eq(6).html();
            main_table_email_checked.push(email_arr_obj);
        }
    });
}

//Get message for check data function
function get_msg_desc_check_data(msg){
    var msg_type ;
    msg_type = message_config_details(msg);
    $("#error_msg_id").prop("hidden", false);
    return msg_type.messages_id_desc;
}

var language_data = new Array();
var validate_add_attributes = [];
var main_table_low_value = [];
var language={};

// Hide delete popup
function hideModal() {
    $('#languageModal').modal('hide');
}


//onclick of add button display languageModal popup and set GLOBAL_ACTION button value
function onclick_add_button(button) {
    $("#error_msg_id").css("display", "none")
    $( "#header_select").prop( "hidden", false );
    GLOBAL_ACTION = button.value
    display_button();
    $('#id_popup_table').DataTable().destroy();
    $("#id_popup_tbody").empty();
    $('#languageModal').modal('show');
    new_row_data();   // Add a new row in popup
    table_sort_filter('id_popup_table');
    $("#id_del_ind_checkbox").prop("hidden", true);
    document.getElementById("id_del_add_button").style.display = "block";
    $("#save_id").prop("hidden", false);
}

//onclick of upload button display id_data_upload popup and set GLOBAL_ACTION button value
function onclick_upload_button() {
    GLOBAL_ACTION = "language_upload"
    display_button();
    $("#id_error_msg_upload").prop("hidden",true)
    $("#id_popup_tbody").empty();
    $('#id_data_upload').modal('show');
    document.getElementById('id_file_data_upload').value = "";
    $("#save_id").prop("hidden", false);
}

// on click copy icon display the selected checkbox data
function onclick_copy_button() {
    GLOBAL_ACTION = "COPY"
    display_button();
    onclick_copy_update_button("copy")
    document.getElementById("id_del_add_button").style.display = "block";
    $("#save_id").prop("hidden", false);
}

 // onclick of valid popup
function valid_popup(){
  $('#id_data_upload').modal('hide');
  $("#valid_upload").modal('show');
}

// on click update icon display the selected checkbox data to update
function onclick_update_button() {
    GLOBAL_ACTION = "UPDATE"
    display_button();
    onclick_copy_update_button("update")
    document.getElementById("id_del_add_button").style.display = "none";
}

function onclick_copy_update_button(data) {
    $("#error_msg_id").css("display", "none")
    $('#id_popup_table').DataTable().destroy();
    $("#id_popup_tbody").empty();
    //Reference the Table.
    var res = get_all_checkboxes(); // Function to get all the checkboxes
    var $chkbox_all = $('td input[type="checkbox"]', res);
    //Reference the CheckBoxes in Table.
    var edit_basic_data = "";
    var unique_input = '';
    //Loop through the CheckBoxes.
    for (var i = 0; i < $chkbox_all.length; i++) {
        if ($chkbox_all[i].checked) {
            var row = $chkbox_all[i].parentNode.parentNode;
            if(GLOBAL_ACTION == "UPDATE"){
                unique_input = '<input class="form-control check_character_no_space" type="text" value="' + row.cells[1].innerHTML + '" name="country code"  maxlength="2" style="text-transform:uppercase" disabled>'
                edit_basic_data += '<tr><td hidden><input type="checkbox" required></td>'+
                    '<td>'+unique_input+'</td>'+
                    '<td><input class="form-control check_only_character" value="' + row.cells[2].innerHTML + '" type="text"  name="language description"  maxlength="100"  required></td>'+
                    '<td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
                $("#header_select").prop("hidden", true);
            }
            else{
                unique_input = '<input class="form-control check_character_no_space" type="text" value="' + row.cells[1].innerHTML + '" name="country code"  maxlength="2" style="text-transform:uppercase" required>'
                edit_basic_data += '<tr><td><input type="checkbox" required></td><td>'+unique_input+'</td><td><input class="form-control check_only_character" value="' + row.cells[2].innerHTML + '" type="text"  name="language description"  maxlength="100"  required></td><td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
                $("#header_select").prop("hidden", false);
            }
        }
    }
    $('#id_popup_table').append(edit_basic_data);
    $("#id_del_ind_checkbox").prop("hidden", true);
    $('#languageModal').modal('show');
    table_sort_filter('id_popup_table');
}

//onclick of cancel empty the popup table body and error messages
$(".remove_upload_data").click(() => {
    $("#id_error_msg").html("");
    $("#id_popup_tbody").empty();
    $("#id_error_msg").empty();
    $('#languageModal').modal('hide');
    $("#id_error_msg").prop("hidden", true);
    $("#id_error_msg_language_id").prop("hidden", true);
    $("#id_error_msg_description").prop("hidden", true);
    $("#id_error_msg_language_length").prop("hidden", true);
    $("#id_check_error_messages").prop("hidden", true);
    $("#id_check_success_messages").prop("hidden", true);
    $("#id_check_special_character_messages").prop("hidden", true)
    $("#id_check_data").prop("hidden", true);
    $('#id_popup_table').DataTable().destroy();
});

function display_error_message(error_message){
    $("#error_msg_id").css("display", "none")
    $('#error_message').text(error_message); 
    document.getElementById("error_message").style.color = "Red";    
    $("#error_msg_id").css("display", "block")
    $('#id_save_confirm_popup').modal('hide');
    $('#languageModal').modal('show');
}

// on click add icon display the row in to add the new entries
function add_popup_row() {
    $("#error_msg_id").css("display", "none")
    basic_add_new_html = '';
    var display_db_data = '';
    $('#id_popup_table').DataTable().destroy();
    $(".modal").on("hidden.bs.modal", function() {
        $("#id_error_msg").html(" ");
    });
     if (GLOBAL_ACTION == "language_upload") {
        basic_add_new_html = '<tr ><td><input type="checkbox" required></td><td><input class="form-control check_character_no_space" type="text"  title="Minimum length is 2" minlength="2" maxlength="2"  name="languageid" style="text-transform:uppercase;" required></td><td><input class="form-control check_only_character" type="text" maxlength="100"  name="description"  required></td><td class="class_del_checkbox"><input type="checkbox" required></td></tr>';
        $('#id_popup_tbody').append(basic_add_new_html);
        table_sort_filter('id_popup_table');
        $(".class_del_checkbox").prop("hidden", false);
        $("#id_del_ind_checkbox").prop("hidden", false);
    }
    else{
    new_row_data();   // Add a new row in popup
    table_sort_filter('id_popup_table');
    }
}

//onclick of cancel display the table in display mode............
function display_basic_db_data() {
    $('#display_basic_table').DataTable().destroy();
    $('#id_language_tbody').empty();
    var edit_basic_data = '';
    $.each(rendered_language_data, function(i, item) {
        edit_basic_data += '<tr ><td class="class_select_checkbox"><input class="checkbox_check" onclick="valueChanged()" type="checkbox" required></td><td>' + item.language_id + '</td><td>' + item.description + '</td></tr>';
    });
    $('#id_language_tbody').append(edit_basic_data);
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


//deletes the duplicate data
function delete_duplicate() {
    $('#id_popup_table').DataTable().destroy();
    var language_id_check = new Array();
    var main_table_low_value = new Array();
    $("#id_popup_table TBODY TR").each(function () {
        var row = $(this);

        // Read data from the pop-up
        language_id = row.find("TD").eq(1).find('input[type="text"]').val().toUpperCase();
        description = row.find("TD").eq(2).find('input[type="text"]').val().toUpperCase();
        checked_box = row.find("TD").eq(3).find('input[type="checkbox"]').is(':checked');

        if (checked_box) {
            del_ind = '1';
        } else {
            del_ind = '0';

            // Check if both language_id and description are not empty
            if (language_id.trim() !== '' && description.trim() !== '') {
                if (language_id_check.includes(language_id)) {
                    $(row).remove();
                }
                language_id_check.push(language_id);

                main_table_low_value = get_main_table_data_upload(); // Read data from the main table
                if (main_table_low_value.includes(language_id)) {
                    $(row).remove();
                }
                main_table_low_value.push(language_id);
            }
        }
    });
    table_sort_filter_popup_pagination('id_popup_table');
    check_data();
}


// Function to hide and display save related popups
$('#save_id').click(function () {
    $('#languageModal').modal('hide');
    language_data = read_popup_data();
    $('#id_save_confirm_popup').modal('show');
});

//Read popup table data
function read_popup_data(){
    $('#id_popup_table').DataTable().destroy();
    language_data = new Array();
    validate_add_attributes = [];
    $("#id_popup_table TBODY TR").each(function () {
        var row = $(this);
        language={};
        language.del_ind = row.find("TD").eq(3).find('input[type="checkbox"]').is(':checked');
        language.description = row.find("TD").eq(2).find('input[type="text"]').val().toUpperCase();
        language.language_id  = row.find("TD").eq(1).find('input[type="text"]').val().toUpperCase();
        if (language == undefined){
            language.language_id = row.find("TD").eq(1).find('input[type="text"]').val();
        }
        validate_add_attributes.push(language.language_id);
        language_data.push(language);
    });
    table_sort_filter('id_popup_table');
    return language_data;
}

// Function for add a new row data
function new_row_data(){
    basic_add_new_html = '<tr><td><input type="checkbox" required></td><td><input class="form-control check_character_no_space" type="text"  title="Minimum length is 2" minlength="2" maxlength="2"  name="languageid" style="text-transform:uppercase;" required></td><td><input class="form-control check_only_character" type="text" maxlength="100"  name="description"  required></td><td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
    $('#id_popup_tbody').append(basic_add_new_html);
}

// Function to get main table data
function get_main_table_data(){
    main_table_low_value = [];
    $('#display_basic_table').DataTable().destroy();
    $("#display_basic_table TBODY TR").each(function() {
        var row = $(this);
        var main_attribute = {};
        main_attribute.language_id = row.find("TD").eq(1).html();
        main_table_low_value.push(main_attribute.language_id);
    });
    table_sort_filter('display_basic_table');
}

// Function to get main table data
function get_main_table_data_upload() {
    main_table_low_value = [];
    $('#display_basic_table').DataTable().destroy();
    $("#display_basic_table TBODY TR").each(function() {
        var row = $(this);
        var main_attribute = {};
        main_attribute.language_id = row.find("TD").eq(1).html();
        main_attribute.del_ind = row.find("TD").eq(3).find('input[type="checkbox"]').is(':checked');
        var compare = main_attribute.language_id
        main_table_low_value.push(compare);
    });
    table_sort_filter('display_basic_table');
    return main_table_low_value
}

// Function to get the selected row
function get_row_data(tableSelector) {
    main_table_checked = [];
    $(tableSelector).DataTable().$('input[type="checkbox"]').each(function () {
        var checkbox = $(this);
        var row = checkbox.closest("tr");
        var language_arr_obj = {};
        language_arr_obj.del_ind = checkbox.is(':checked');
        if(language_arr_obj.del_ind) {
            language_arr_obj.language_id = row.find("TD").eq(1).find('input[type="text"]').val() || row.find("TD").eq(1).html();
            language_arr_obj.description = row.find("TD").eq(2).find('input[type="text"]').val() || row.find("TD").eq(2).html();
            main_table_checked.push(language_arr_obj);
        }
    });
}

// Function to get the selected row data
function get_selected_row_data(){
    $("#display_basic_table TBODY TR").each(function() {
        var row = $(this);
        var language_arr_obj = {};
        language_arr_obj.del_ind = row.find("TD").eq(0).find('input[type="checkbox"]').is(':checked');
        if(language_arr_obj.del_ind){
            language_arr_obj.language_id = row.find("TD").eq(1).html();
            language_arr_obj.description = row.find("TD").eq(2).html();
            main_table_language_checked.push(language_arr_obj);
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

//**************************************
function update_check_message(messages) {
     $.each(messages, function (i, message) {
        $("#id_check_success_messages").append('<p>' + message + '</p>')
     });
    $("#id_check_success_messages").prop("hidden",false)
}
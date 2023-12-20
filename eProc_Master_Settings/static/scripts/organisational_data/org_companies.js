var company_data = new Array();
var validate_add_attributes = [];
var main_table_low_value = [];
var orgcompany={};

//hide the myModal popup: Implemented Dependency delete purpose
function hideModal() {
    $('#companyModal').modal('hide');
}

//onclick of upload button display id_data_upload popup and set GLOBAL_ACTION button value
function onclick_upload_button() {
    GLOBAL_ACTION = "orgcompany_upload"
    display_button();
    $("#id_error_msg_upload").prop("hidden",true)
    $("#id_popup_tbody").empty();
    $('#id_data_upload').modal('show');
    document.getElementById('id_file_data_upload').value = "";
}


    // onclick of valid popup
function valid_popup(){
  $('#id_data_upload').modal('hide');
  $("#valid_upload").modal('show');
}


// on click copy icon display the selected checkbox data
function onclick_copy_button() {
    GLOBAL_ACTION = "COPY"
    display_button();
    onclick_copy_update_button("copy")
    document.getElementById("id_del_add_button").style.display = "block";
     $("#save_id").prop("hidden", false);
}

// on click update icon display the selected checkbox data to update
function onclick_update_button() {
    GLOBAL_ACTION = "UPDATE"
    display_button();
    onclick_copy_update_button("update")
    document.getElementById("id_del_add_button").style.display = "none";
     $("#save_id").prop("hidden", false);
}

//onclick of add button display companyModal popup and set GLOBAL_ACTION button value
function onclick_add_button(button) {
    $("#error_msg_id").css("display", "none")
    $("#header_select").prop( "hidden", false );
    GLOBAL_ACTION = button.value
    display_button();
    $('#id_popup_table').DataTable().destroy();
    $("#id_popup_tbody").empty();
    $('#companyModal').modal('show');
    new_row_data(); // Add a new row in popup
    table_sort_filter('id_popup_table');
    $("#id_del_ind_checkbox").prop("hidden", true);
    document.getElementById("id_del_add_button").style.display = "block";
    $("#save_id").prop("hidden", false);
}

// on click add icon display the row in to add the new entries
function add_popup_row() {
    $("#error_msg_id").css("display", "none")
    basic_add_new_html = '';
    var display_db_data = '';
    $('#id_popup_table').DataTable().destroy();
    $(".modal").on("hidden.bs.modal", function() {
        $("#id_error_msg").html("");
    });
    if (GLOBAL_ACTION == "orgcompany_upload") {
        basic_add_new_html = '<tr> <td><input class="input" type="checkbox" required></td><td><input class="form-control check_alphastar_no_space color_change" type="text"  name= "company_id"  minlength="4" maxlength="8"></td><td><input class="form-control check_only_character" type="text" name="name1"  maxlength="100"></td><td><input class="form-control check_only_character" type="text" name="name2" maxlength="100"></td><td hidden></td><td hidden><input value="GUID" hidden></td><td class="class_del_checkbox"><input type="checkbox" required></td></tr>';
        $('#id_popup_tbody').append(basic_add_new_html);
        table_sort_filter('id_popup_table');
        $(".class_del_checkbox").prop("hidden", false);
        $("#id_del_ind_checkbox").prop("hidden", false);
    }
    else{
         new_row_data(); // Add a new row in popup
         table_sort_filter('id_popup_table');
    }
}

//**********************************************************
function onclick_copy_update_button() {
    var dropdown_select_array = []
    $("#error_msg_id").css("display", "none")
    $('#id_popup_table').DataTable().destroy();
    $("#id_popup_tbody").empty();
    //Reference the Table.
    var res = get_all_checkboxes(); // Function to get all the checkboxes
    var $chkbox_all = $('td input[type="checkbox"]', res);
    //Reference the CheckBoxes in Table.
    var edit_basic_data = "";
    var guid= '';
    //Loop through the CheckBoxes.
    for (var i = 0; i <  $chkbox_all.length; i++) {
        if ($chkbox_all[i].checked) {
        var row = $chkbox_all[i].parentNode.parentNode;
            if(GLOBAL_ACTION == "COPY"){
                guid = 'GUID';
                edit_basic_data += '<tr><td><input type="checkbox"></td><td><input class="form-control check_alphastar_no_space" type="text" value="' + row.cells[1].innerHTML + '" minlength="4" maxlength="08" name="company_id" required></td><td><input class="form-control check_only_character" type="text" value="' + row.cells[2].innerHTML + '" maxlength="100" name="name1" required></td><td><input class="form-control check_only_character" type="text" value="' + row.cells[3].innerHTML + '" maxlength="100" name="name2" required></td><td hidden></td><td hidden><input value="' + guid + '"></td><td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';;
                $("#header_select").prop("hidden",false);
            }
            else{
                guid = row.cells[5].innerHTML;

                edit_basic_data += '<tr><td hidden><input type="checkbox"></td><td><input class="form-control check_alphastar_no_space" type="text" value="' + row.cells[1].innerHTML + '" minlength="4" maxlength="08" name="company_id" disabled></td><td><input class="form-control check_only_character" type="text" value="' + row.cells[2].innerHTML + '" maxlength="100" name="name1" required></td><td><input class="form-control check_only_character" type="text" value="' + row.cells[3].innerHTML + '" maxlength="100" name="name2" required><td hidden></td><td hidden><input value="' + guid + '"></td><td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';

                $("#header_select").prop("hidden",true);
            }
            var row = $chkbox_all[i].parentNode.parentNode;
            var company_id = row.cells[1].innerHTML
            dropdown_select_array.push([company_id])
        }
    }
    $('#id_popup_table').append(edit_basic_data);
    var i =0;
    $("#id_del_ind_checkbox").prop("hidden", true);
    $('#companyModal').modal('show');
    table_sort_filter('display_basic_table');
    table_sort_filter('id_popup_table');
}

//onclick of cancel empty the popup table body and error messages
$(".remove_upload_data").click(() => {
    $("#id_error_msg").html("");
    $("#id_popup_tbody").empty();
    $("#id_error_msg").empty();
    $('#companyModal').modal('hide');
    $("#id_error_msg").prop("hidden", true);
    $("#id_error_msg_aad_code").prop("hidden", true);
    $("#id_error_msg_aad_name").prop("hidden", true);
    $("#id_error_msg_aad_length").prop("hidden", true);
    $("#id_check_error_messages").prop("hidden", true);
    $("#id_check_success_messages").prop("hidden", true);
    $("#id_check_special_character_messages").prop("hidden", true)
    $("#id_check_data").prop("hidden", true);
    $('#id_popup_table').DataTable().destroy();
});

// Functtion to hide and display save related popups
$('#save_id').click(function () {
    $('#companyModal').modal('hide');
    company_data = read_popup_data();
    $('#id_save_confirm_popup').modal('show');
});

//Read popup table data
function read_popup_data(){
    $('#id_popup_table').DataTable().destroy();
    validate_add_attributes = [];
    company_data = new Array();
    $("#id_popup_table TBODY TR").each(function() {
        var row = $(this);
        orgcompany = {};
        orgcompany.del_ind = row.find("TD").eq(6).find('input[type="checkbox"]').is(':checked');
        orgcompany.object_id = row.find("TD").eq(4).find('input').val();
        orgcompany.name1 = row.find("TD").eq(2).find('input[type="text"]').val().toUpperCase();
        orgcompany.name2= row.find("TD").eq(3).find('input[type="text"]').val();
        orgcompany.company_id = row.find("TD").eq(1).find('input[type="text"]').val();
        orgcompany.company_guid = row.find("TD").eq(5).find('input[type="text"]').val();
        if (orgcompany == undefined) {
            orgcompany.company_id=row.find("TD").eq(3).find('input[type="text"]').val();
        }
        if(orgcompany.company_guid == undefined) {
            orgcompany.company_guid = ''
        }
        if(orgcompany.object_id == undefined) {
            orgcompany.object_id = '';
        }
        if(orgcompany.object_id == null) {
         orgcompany.object_id = '';
        }
        validate_add_attributes.push(orgcompany.company_id);
        company_data.push(orgcompany);
    });
    table_sort_filter('id_popup_table');
    return company_data;
}

//onclick of cancel display the table in display mode............
function display_basic_db_data() {
    $('#display_basic_table').DataTable().destroy();
    $('#id_company_tbody').empty();
     $('#display_data').empty();
    var edit_basic_data = '';
    $.each(rendered_orgcompany_data, function(i, item) {
        var data = '';
        if (item.object_id == null){
            data = ''
        }
        else{
            data = item.object_id
        }
        edit_basic_data += '<tr><td class="class_select_checkbox"><input class="checkbox_check" onclick="valueChanged()" type="checkbox" required></td><td>' + item.company_id + '</td><td>' + item.name1 + '</td><td>' + item.name2 + '</td><td>' + data + '</td><td hidden>'+item.company_guid+'</td><td hidden>'+item.del_ind+'</td></tr>';
    });
    $('#id_company_tbody').append(edit_basic_data);
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

//*******************************************************
function display_error_message(error_message) {
    $('#error_message').text(error_message);
    document.getElementById("error_message").style.color = "Red";
    $("#error_msg_id").css("display", "block")
    $('#id_save_confirm_popup').modal('hide');
    $('#companyModal').modal('show');
}

//**********************************************
function update_check_message(messages) {
    $.each(messages, function (i, message) {
        $("#id_check_success_messages").append('<p>' + message + '</p>')
    });
    $("#id_check_success_messages").prop("hidden",false)
}

// Function for add a new row data
function new_row_data(){
    basic_add_new_html = '<tr> <td><input class="input" type="checkbox" required></td><td><input class="form-control check_alphastar_no_space color_change" type="text"  name= "company_id"  minlength="4" maxlength="8"></td><td><input class="form-control check_only_character" type="text" name="name1"  maxlength="100"></td><td><input class="form-control check_only_character" type="text" name="name2" maxlength="100"></td><td hidden></td><td hidden><input value="GUID" hidden></td><td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
    $('#id_popup_tbody').append(basic_add_new_html);
}

// Function to get main table data
function get_main_table_data(){
    main_table_low_value = [];
    $('#display_basic_table').DataTable().destroy();
    $("#display_basic_table TBODY TR").each(function() {
        var row = $(this);
        var main_attribute = {};
        main_attribute.company_id = row.find("TD").eq(1).html();
        main_table_low_value.push(main_attribute.company_id);
    });
    table_sort_filter('display_basic_table');
}

// Function to get the selected row data
function get_selected_row_data() {
    $("#display_basic_table TBODY TR").each(function() {
        var row = $(this);
        var orgcompany_arr_obj = {};
        orgcompany_arr_obj.del_ind = row.find("TD").eq(0).find('input[type="checkbox"]').is(':checked');
        if(orgcompany_arr_obj.del_ind){
        orgcompany_arr_obj.object_id = row.find("TD").eq(4).html();
        orgcompany_arr_obj.name1 = row.find("TD").eq(2).html();
        orgcompany_arr_obj.name2 = row.find("TD").eq(3).html();
        orgcompany_arr_obj.company_id = row.find("TD").eq(1).html();
        orgcompany_arr_obj.company_guid = row.find("TD").eq(5).html();
        main_table_orgcompany_checked.push(orgcompany_arr_obj);
        }
    });
}

// Function to get the selected row data
function get_row_data(tableSelector) {
    main_table_checked = [];
    $(tableSelector).DataTable().$('input[type="checkbox"]').each(function () {
        var checkbox = $(this);
        var row = checkbox.closest("tr");
        var orgcompany_arr_obj = {};
        orgcompany_arr_obj.del_ind = checkbox.is(':checked');
        if(orgcompany_arr_obj.del_ind) {
            orgcompany_arr_obj.company_id = row.find("TD").eq(1).find('input[type="text"]').val() || row.find("TD").eq(1).html();
            orgcompany_arr_obj.name1 = row.find("TD").eq(2).find('input[type="text"]').val() || row.find("TD").eq(2).html();
            orgcompany_arr_obj.name2 = row.find("TD").eq(3).find('input[type="text"]').val() || row.find("TD").eq(3).html();
            orgcompany_arr_obj.object_id = row.find("TD").eq(4).find('input').val() || row.find("TD").eq(4).html();
            main_table_checked.push(orgcompany_arr_obj);
        }
    });
}

// Function to get main table data
function get_main_table_data_upload() {
    main_table_low_value = [];
    $('#display_basic_table').DataTable().destroy();
    $("#display_basic_table TBODY TR").each(function() {
        var row = $(this);
        var main_attribute = {};
        main_attribute.company_id = row.find("TD").eq(1).html();
        main_attribute.del_ind = row.find("TD").eq(6).find('input[type="checkbox"]').is(':checked');
        var compare = main_attribute.company_id
        main_table_low_value.push(compare);
    });
    table_sort_filter('display_basic_table');
    return main_table_low_value
}


//Get message for check data function
function get_msg_desc_check_data(msg){
    var msg_type ;
    msg_type = message_config_details(msg);
    $("#error_msg_id").prop("hidden", false);
    return msg_type.messages_id_desc;
}

function delete_duplicate() {
    $('#id_popup_table').DataTable().destroy();
    var company_check = new Array
    var main_table_low_value = new Array
    $("#id_popup_table TBODY TR").each(function () {
        var row = $(this);
        //*************** reading data from the pop-up ***************
        name2 = row.find("TD").eq(3).find('input[type="text"]').val();
        name1 = row.find("TD").eq(2).find('input[type="text"]').val();
        company_id = row.find("TD").eq(1).find('input[type="text"]').val().toUpperCase();
        checked_box = row.find("TD").eq(6).find('input[type="checkbox"]').is(':checked')
         if (checked_box){
                del_ind = '1'
         }
         else{
             del_ind = '0'
             if (company_id && name1 && name2) {
                 if (company_check.includes(company_id)) {
                    $(row).remove();
                 }
                 company_check.push(company_id);
                 main_table_low_value = get_main_table_data_upload(); //Read data from main table
                 if (main_table_low_value.includes(company_id)) {
                    $(row).remove();
                 }
                 main_table_low_value.push(company_id);
             }
         }
    });
    table_sort_filter_popup_pagination('id_popup_table')
    check_data()
}

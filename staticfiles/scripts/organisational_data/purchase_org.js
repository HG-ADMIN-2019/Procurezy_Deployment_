var porg_data = new Array();
var validate_add_attributes = [];
var main_table_low_value = [];
var porg={};

//onclick of upload button display id_data_upload popup and set GLOBAL_ACTION button value
function onclick_upload_button() {
    GLOBAL_ACTION = "purchase_org_upload"
    $("#id_error_msg_upload").prop("hidden",true)
    $("#id_popup_tbody").empty();
    $('#id_data_upload').modal('show');
    document.getElementById('id_file_data_upload').value = "";
}

// on click copy icon display the selected checkbox data
function onclick_copy_button() {
    GLOBAL_ACTION = "COPY"
    onclick_copy_update_button("copy")
    document.getElementById("id_del_add_button").style.display = "block";
    $("#save_id").prop("hidden", false);
}

// on click update icon display the selected checkbox data to update
function onclick_update_button() {
    GLOBAL_ACTION = "UPDATE"
    onclick_copy_update_button("update")
    document.getElementById("id_del_add_button").style.display = "none";
     $("#save_id").prop("hidden", false);
}

//**********************************************************
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
    var porg_guid= '';
    var dropdown_values = [];
    //Loop through the CheckBoxes.
    for (var i = 0; i < $chkbox_all.length; i++) {
        if ($chkbox_all[i].checked) {
            var row = $chkbox_all[i].parentNode.parentNode;
            if(GLOBAL_ACTION == "UPDATE"){
                porg_guid = row.cells[5].innerHTML
                unique_input = '<input class="input form-control check_alpha_no_space"  value="' + row.cells[1].innerHTML + '" type="text" maxlength="8"  name="porg_id" disabled>'
                edit_basic_data += '<tr><td hidden><input type="checkbox"></td><td>'+unique_input+' </td><td><input class="form-control check_only_character" value="' + row.cells[2].innerHTML + '" type="text" name="description"  maxlength="100"  required></td><td hidden><input value="' + porg_guid + '"></td><td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
                $("#header_select").prop("hidden", true); 
            }
            else{
                porg_guid = 'GUID';
                unique_input = '<input class="input form-control check_alpha_no_space" value="' + row.cells[1].innerHTML + '"  type="text" maxlength="8"  name="porg_id"required>'
                edit_basic_data += '<tr><td><input type="checkbox" required></td><td>'+unique_input+'</td><td><input class="form-control check_only_character" value="' + row.cells[2].innerHTML + '" type="text"  name="description"  maxlength="100"  required></td><td hidden><input value="' + porg_guid + '"></td><td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
                $("#header_select").prop("hidden", false);
            }
            var row = $chkbox_all[i].parentNode.parentNode;
            var company_id_value = row.cells[3].innerHTML
            var object_id_value = row.cells[4].innerHTML
            dropdown_values.push([company_id_value,object_id_value])
        }
    }
    $('#id_popup_tbody').append(edit_basic_data);
    $("#id_del_ind_checkbox").prop("hidden", true);
    $('#Porg_Modal').modal('show');
    table_sort_filter('id_popup_table');
}

//onclick of cancel display the table in display mode............
$(".remove_upload_data").click(() => {
    $("#id_error_msg").html("");
    $("#id_popup_tbody").empty();
    $("#id_error_msg").empty();
    $('#Porg_Modal').modal('hide');
    $("#id_error_msg").prop("hidden", true);
    $("#id_error_msg_porg_id").prop("hidden", true);
    $("#id_error_msg_description").prop("hidden", true);
    $("#id_error_msg_pgrouporg_length").prop("hidden", true);
    $("#id_check_error_messages").prop("hidden", true);
    $("#id_check_success_messages").prop("hidden", true);
    $("#id_check_special_character_messages").prop("hidden", true)
    $("#id_check_data").prop("hidden", true);
    $('#id_popup_table').DataTable().destroy();
});


//onclick of add button display Porg_Modal popup and set GLOBAL_ACTION button value

function onclick_add_button(button) {
    $("#error_msg_id").css("display", "none")
    $("#header_select").prop( "hidden", false );
    GLOBAL_ACTION = button.value;
    $('#id_popup_table').DataTable().destroy();
    $("#id_popup_tbody").empty();
    $('#Porg_Modal').modal('show');
    basic_add_new_html = '<tr><td><input type="checkbox" required></td>'+
        '<td><input class="form-control check_alpha_no_space"  type="text"  minlength="5" maxlength="8"  name="porg_id" style="text-transform:uppercase;" required></td>'+
        '<td><input class="input form-control check_only_character"  type="text" maxlength="100"  name="description"  required></td>'+
        '<td hidden><input value=""></td>'+
        '<td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
    $('#id_popup_tbody').append(basic_add_new_html);
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
    $(".modal").on("hidden.bs.modal", function () {
        $("#id_error_msg").html(" ");
    });
     if (GLOBAL_ACTION == "purchase_org_upload") {
         basic_add_new_html = '<tr><td><input type="checkbox" required></td>'+
        '<td><input class="form-control check_alpha_no_space"  type="text"  minlength="5" maxlength="8"  name="porg_id" style="text-transform:uppercase;" required></td>'+
        '<td><input class="input form-control check_only_character"  type="text" maxlength="100"  name="description"  required></td>'+
        '<td hidden><input value=""></td>'+
        '<td class="class_del_checkbox"><input type="checkbox" required></td></tr>';
        $('#id_popup_tbody').append(basic_add_new_html);
        $(".class_del_checkbox").prop("hidden", false);
        $("#id_del_ind_checkbox").prop("hidden", false);
        table_sort_filter('id_popup_table');
    }
    else{
       basic_add_new_html = '<tr><td><input type="checkbox" required></td>'+
        '<td><input class="form-control check_alpha_no_space"  type="text"  minlength="5" maxlength="8"  name="porg_id" style="text-transform:uppercase;" required></td>'+
        '<td><input class="input form-control check_only_character"  type="text" maxlength="100"  name="description"  required></td>'+
        '<td hidden><input value=""></td>'+
        '<td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
        $('#id_popup_tbody').append(basic_add_new_html);
        table_sort_filter('id_popup_table');
    }

}

//onclick of cancel display the table in display mode............
function display_basic_db_data(){
    $('#display_basic_table').DataTable().destroy();
    $('#id_purchase_org_tbody').empty();
    $('#display_data').empty();
    var edit_basic_data = '';
    $.each(rendered_orgporg_data, function (i, item) {
        var data = '';
        if (item.object_id == null){
            data = ''
        }
        else{
        data = item.object_id
        }
        edit_basic_data += '<tr ><td class="class_select_checkbox"><input class="checkbox_check" onclick="valueChanged()" type="checkbox" required></td><td>' + item.porg_id + '</td><td>' + item.description + '</td><td>' + data + '</td><td hidden>' + item.porg_guid + '</td><td hidden>' + item.del_ind + '</td></tr>';
    });
    $('#id_purchase_org_tbody').append(edit_basic_data);
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

//**********************************************************
function display_error_message(error_message){
    $('#error_message').text(error_message);
    document.getElementById("error_message").style.color = "Red";
    $("#error_msg_id").css("display", "block")
    $('#id_save_confirm_popup').modal('hide');
    $('#Porg_Modal').modal('show');
}

//**********************************************************
function delete_duplicate() {
    $('#id_popup_table').DataTable().destroy();
    var porg_code_check = new Array
    var main_table_low_value = new Array
    $("#id_popup_table TBODY TR").each(function () {
        var row = $(this);
        //*************** reading data from the pop-up ***************
        porg_id = row.find("TD").eq(1).find('input[type="text"]').val().toUpperCase();
        description = row.find("TD").eq(2).find('input[type="text"]').val();
        company_id = row.find("TD").eq(4).find('input[type="text"]').val();
        object_id = row.find("TD").eq(3).find('input[type="text"]').val();
        checked_box = row.find("TD").eq(4).find('input[type="checkbox"]').is(':checked')
          if (checked_box){
                del_ind = '1'
          }
          else{
                del_ind = '0'
                if (porg_id && description) {
                    if (porg_code_check.includes(porg_id)) {
                        $(row).remove();
                    }
                    porg_code_check.push(porg_id);
                     main_table_low_value = get_main_table_data_upload(); //Read data from main table
                    if (main_table_low_value.includes(porg_id)) {
                        $(row).remove();
                    }
                    main_table_low_value.push(porg_id);
                }
          }
    });
    table_sort_filter_popup_pagination('id_popup_table')
    check_data()
}

// onclick of valid popup
function valid_popup(){
  $('#id_data_upload').modal('hide');
  $("#valid_upload").modal('show');
}


// Function to hide and display save related popups
$('#save_id').click(function () {
    $('#Porg_Modal').modal('hide');
    porg_data = read_popup_data();
    $('#id_save_confirm_popup').modal('show');
});

//Read popup table data
function read_popup_data() {
    $('#id_popup_table').DataTable().destroy();
    porg_data = new Array();
    validate_add_attributes = [];
    $("#id_popup_table TBODY TR").each(function () {
        var row = $(this);
        porg={};
        porg.del_ind = row.find("TD").eq(4).find('input[type="checkbox"]').is(':checked');
        porg.porg_guid = row.find("TD").eq(5).find('input').val();
        porg.porg_id = row.find("TD").eq(1).find('input').val().toUpperCase();
        porg.description = row.find("TD").eq(2).find('input').val();
        porg.object_id = row.find("TD").eq(3).find('select').val();
        if (porg == undefined){
                porg.porg_id = row.find("TD").eq(1).find('input[type="text"]').val();
        }
        if(porg.porg_guid == undefined) {
            porg.porg_guid = '';
        }
        if(porg.object_id == undefined) {
            porg.object_id = '';
        }
        validate_add_attributes.push(porg.porg_id);
        porg_data.push(porg);
    });
    table_sort_filter('id_popup_table');
    return porg_data;
}

//**********************************************************
function update_check_message(messages){
    $.each(messages, function (i, message) {
        $("#id_check_success_messages").append('<p>' + message + '</p>')
    });
    $("#id_check_success_messages").prop("hidden",false)
}

// Function for add a new row data
function new_row_data(){
    basic_add_new_html = '<tr><td><input type="checkbox" required></td>'+
        '<td><input class="form-control check_alpha_no_space"  type="text"  minlength="5" maxlength="8"  name="porg_id" style="text-transform:uppercase;" required></td>'+
        '<td><input class="input form-control check_only_character"  type="text" maxlength="100"  name="description"  required></td>'+
        '<td hidden><input value=""></td>'+
        '<td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
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
        main_attribute.porg_id = row.find("TD").eq(1).html();
        main_table_low_value.push(main_attribute.porg_id);
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
        main_attribute.porg_id = row.find("TD").eq(1).html();
        main_attribute.del_ind = row.find("TD").eq(5).find('input[type="checkbox"]').is(':checked');
        var compare = main_attribute.porg_id
        main_table_low_value.push(compare);
    });
    table_sort_filter('display_basic_table');
    return main_table_low_value
}

// Function to get the selected row data
function get_selected_row_data(){
    $("#display_basic_table TBODY TR").each(function () {
        var row = $(this);
        var pgorg_arr_obj ={};
        pgorg_arr_obj.del_ind = row.find("TD").eq(0).find('input[type="checkbox"]').is(':checked');
        if(pgorg_arr_obj.del_ind) {
            pgorg_arr_obj.porg_id = row.find("TD").eq(1).html();
            pgorg_arr_obj.description = row.find("TD").eq(2).html();
            pgorg_arr_obj.company_id = row.find("TD").eq(3).html();
            pgorg_arr_obj.object_id = row.find("TD").eq(4).html();
            pgorg_arr_obj.porg_guid = row.find("TD").eq(5).html();
            main_table_pgorg_checked.push( pgorg_arr_obj);
        }
    });
}

//Get message for check data functionupdate_check_message
function get_msg_desc_check_data(msg){
    var msg_type ;
    msg_type = message_config_details(msg);
    $("#error_msg_id").prop("hidden", false);
    return msg_type.messages_id_desc;
}


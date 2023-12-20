var accasscat_data = new Array();
var validate_add_attributes = [];
var main_table_low_value = [];
var aac={};

//hide the myModal popup: Implemented Dependency delete purpose
function hideModal() {
    $('#accasscat_Modal').modal('hide');
}

//onclick of cancel empty the popup table body and error messages
$(".remove_upload_data").click(() => {
    $("#id_error_msg").html("");
    $("#id_popup_tbody").empty();
    $("#id_error_msg").empty();
    $('#accasscat_Modal').modal('hide');
    $("#id_error_msg").prop("hidden", true);
    $("#id_error_msg_aac_code").prop("hidden", true);
    $("#id_error_msg_aac_name").prop("hidden", true);
    $("#id_error_msg_aac_length").prop("hidden", true);
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
    $('#accasscat_Modal').modal('show');
}

//onclick of cancel display the table in display mode............
function display_basic_db_data() {
    $('#display_basic_table').DataTable().destroy();
    $('#id_aac_tbody').empty();
    var edit_basic_data = '';
    $.each(rendered_aac_data, function (i, item) {
        edit_basic_data += '<tr ><td class="class_select_checkbox"><input class="checkbox_check" onclick="valueChanged()" type="checkbox" required></td><td>' + item.account_assign_cat + '</td><td>' + item.description + '</td></tr>';
    });
    $('#id_aac_tbody').append(edit_basic_data);
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

// Function to delete duplicates
function delete_duplicate() {
    $('#id_popup_table').DataTable().destroy();
    var aac_code_check = new Array
    $("#id_popup_table TBODY TR").each(function() {
        var row = $(this);
        //*************** reading data from the pop-up ***************
        description = row.find("TD").eq(2).find('input[type="text"]').val().toUpperCase();
        account_assign_cat = row.find("TD").eq(1).find('input[type="text"]').val().toUpperCase();
        checked_box = row.find("TD").eq(3).find('input[type="checkbox"]').is(':checked')
        if (aac_code_check.includes(account_assign_cat)) {
            $(row).remove();
        }
        aac_code_check.push(account_assign_cat);
    })
    table_sort_filter('id_popup_table')
    check_data()
}

//Functtion to hide and display save related popups
$('#save_id').click(function () {
    $('#accasscat_Modal').modal('hide');
    accasscat_data = read_popup_data();
    $('#id_save_confirm_popup').modal('show');
});

//Read popup table data
function read_popup_data(){
    $('#id_popup_table').DataTable().destroy();
    accasscat_data = new Array();
    validate_add_attributes = [];
    $("#id_popup_table TBODY TR").each(function() {
        var row = $(this);
        aac = {};
        aac.del_ind = row.find("TD").eq(3).find('input[type="checkbox"]').is(':checked');
        aac.description = row.find("TD").eq(2).find('input[type="text"]').val();
        aac.account_assign_cat = row.find("TD").eq(1).find('select[type="text"]').val();
        if (aac == undefined) {
            aac.account_assign_cat= row.find("TD").eq(1).find('select[type="text"]').val();
        }
        validate_add_attributes.push(aac.account_assign_cat);
        accasscat_data.push(aac);
    });
    table_sort_filter('id_popup_table');
    return accasscat_data;
}

// Function for add a new row data
function new_row_data() {
    basic_add_new_html = '<tr><td><input type="checkbox" required></td>'+
    '<td><select type="text" class="input form-control acct_assignment_category"  name="acct_assignment_category" onchange="GetSelectedTextValue(this)">'+ aac_dropdown +'</select></td>'+
    '<td><input class="form-control description check_special_char" type="text"  name="description" value="'+aact_desc+'" disabled></td><td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
    $('#id_popup_tbody').append(basic_add_new_html);
    table_sort_filter('id_popup_table');
}

//********************************************
function GetSelectedTextValue(rowid){
        var row = $(rowid);
             var selectedText = "";
          var selectedValue = row[0].value;
             $.each (rendered_aac_values, function(i, item){
            if(selectedValue == item.field_type_id){
              row[0].parentNode.nextElementSibling.children.description.value = item.field_type_desc;
            }
          });
    }

// Function to get the selected row data
function get_row_data(tableSelector) {
    main_table_aac_checked = []; // Clear the previous data before collecting new data
    $(tableSelector).DataTable().$('input[type="checkbox"]').each(function () {
        var checkbox = $(this);
        var row = checkbox.closest("tr");
        var aac_arr_obj = {};
        aac_arr_obj.del_ind = row.find("TD").eq(0).find('input[type="checkbox"]').is(':checked');
        if(aac_arr_obj.del_ind){
            aac_arr_obj.account_assign_cat = row.find("TD").eq(1).find('input[type="text"]').val() || row.find("TD").eq(1).html();
            aac_arr_obj.description = row.find("TD").eq(2).find('input[type="text"]').val() || row.find("TD").eq(2).html();
            main_table_aac_checked.push(aac_arr_obj);
        }
    });
}

// Function to get main table data
function get_main_table_data() {
    main_table_low_value = [];
    $('#display_basic_table').DataTable().destroy();
    $("#display_basic_table TBODY TR").each(function() {
        var row = $(this);
        var main_attribute = {};
        main_attribute.account_assign_cat = row.find("TD").eq(1).html();
        main_table_low_value.push(main_attribute.account_assign_cat);
    });
    table_sort_filter('display_basic_table');
}
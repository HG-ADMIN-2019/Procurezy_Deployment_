var main_table_data = new Array();
var numberranges_data = new Array();
var main_table_low_value = [];
var validate_add_attributes = [];
var number_range={};
var seq_array= [];

//onclick of add button display myModal popup and set GLOBAL_ACTION button value
function onclick_add_button(button) {
    $("#error_msg_id").css("display", "none")
    $("#header_select").prop( "hidden", false );
    GLOBAL_ACTION = button.value
    $('#id_popup_table').DataTable().destroy();
    $("#id_popup_tbody").empty();
    $('#myModal').modal('show');
    basic_add_new_html = '<tr ><td class="number_range_checkbox"><input type="checkbox" required></td><td><input class="form-control" value="' + max_sequence + '" type="number"  name="sequence"  disabled></td><td><input class="form-control" type="number" maxlength="10"  name="starting"  required></td><td><input class="form-control" type="number" maxlength="10"  name="ending"  required></td><td><input class="form-control" type="number" maxlength="10"  name="current"  required></td>><td hidden><input type="text" value=""></td><td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
    $('#id_popup_tbody').append(basic_add_new_html);
    table_sort_filter('id_popup_table');
    $("#id_del_ind_checkbox").prop("hidden", true);
    document.getElementById("id_del_add_button").style.display = "block";
    $("#save_id").prop("hidden", false);
    nextval = max_sequence;
    display_button(); // Call the display_button function to show/hide the buttons
}

// on click update icon display the selected checkbox data to update
function onclick_update_button() {
    GLOBAL_ACTION = "UPDATE"
    onclick_copy_update_button("update")
    document.getElementById("id_del_add_button").style.display = "none";
    display_button(); // Call the display_button function to show/hide the buttons
}

//*************************************
function onclick_copy_update_button() {
    $("#error_msg_id").css("display", "none")
    $('#display_basic_table').DataTable().destroy();
    $('#id_popup_table').DataTable().destroy();
    $("#id_popup_tbody").empty();
    //Reference the Table.
    var grid = document.getElementById("display_basic_table");
    //Reference the CheckBoxes in Table.
    var checkBoxes = grid.getElementsByTagName("INPUT");
    var edit_basic_data = "";
    var guid = '';
    //Loop through the CheckBoxes.
    for (var i = 1; i < checkBoxes.length; i++) {
        if (checkBoxes[i].checked) {
            var row = checkBoxes[i].parentNode.parentNode;
            if (GLOBAL_ACTION == "UPDATE") {
                guid = row.cells[5].innerHTML;
                edit_basic_data += '<tr ><td><input type="checkbox" required></td><td><input type="number" class="form-control" value="' + row.cells[1].innerHTML + '" name="sequence"  maxlength="5"  disabled></td><td><input class="form-control" value="' + row.cells[2].innerHTML + '" type="number"  name="starting"  maxlength="100000000"  disabled></td><td><input value="' + row.cells[3].innerHTML + '" type="number" class="form-control"  name="ending"  maxlength="10"  required></td><td><input value="' + row.cells[4].innerHTML + '" type="number" class="form-control"  name="current"  maxlength="10"  disabled></td><td hidden><input  type="text" class="form-control" value="' + guid + '"></td><td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
            }
            else if (GLOBAL_ACTION == "DELETE") {
                if ((row.cells[1].innerHTML=="False")){
                    check = '<input type="checkbox" disabled>'
                    $('#delete_data').prop('disabled', true);
                }
                else
                {
                    check = '<input type="checkbox">'
                    $('#delete_data').prop('disabled', false);
                }
                edit_basic_data +=
                '<tr >'+
                    '<td><input type="checkbox" required></td>'+
                    '<td><input type="number" class="form-control" value="' + row.cells[1].innerHTML + '" name="sequence"  maxlength="5"  disabled></td>'+
                    '<td><input class="form-control" value="' + row.cells[2].innerHTML + '" type="number"  name="starting"  maxlength="100000000"  disabled></td>'+
                    '<td><input value="' + row.cells[3].innerHTML + '" type="number" class="form-control"  name="ending"  maxlength="10"  disabled></td>'+
                    '<td><input value="' + row.cells[4].innerHTML + '" type="number" class="form-control"  name="current"  maxlength="10"  disabled></td>'+
                    '<td hidden><input  type="text" class="form-control" value="' + guid + '"></td>'+
                    '<td class="class_del_checkbox" hidden><input type="checkbox" required></td>'+
                '</tr>';
            }
        }
    }
    $('#id_popup_table').append(edit_basic_data);
    $("#id_del_ind_checkbox").prop("hidden", true);
    table_sort_filter('display_basic_table');
    table_sort_filter('id_popup_table');
    $('#myModal').modal('show');
}

//onclick of cancel empty the popup table body and error messages
$(".remove_upload_data").click(() => {
    $("#id_error_msg").html("");
    $("#id_popup_tbody").empty();
    $("#id_error_msg").empty();
    $('#myModal').modal('hide');
    $("#id_error_msg").prop("hidden", true);
    $("#id_error_msg_sequence").prop("hidden", true);
    $("#id_error_msg_starting").prop("hidden", true);
    $("#id_error_msg_ending").prop("hidden", true);
    $("#id_error_msg_current").prop("hidden", true);
    $("#id_check_error_messages").prop("hidden", true);
    $("#id_check_success_messages").prop("hidden", true);
    $("#id_check_special_character_messages").prop("hidden", true)
    $("#id_check_data").prop("hidden", true);
    $('#id_popup_table').DataTable().destroy();
});

//*********************************
function list_out_of_range(number_range){
    var range_flag = true
    $.each(number_range, function (i, number) {
        if(range_flag){
            range_flag = inRange(number.current,number.starting,number.ending)
        }
    });
    return range_flag
}

//********************************************************
function range_check_function(number_range,check_number_range){
    var validation_error = true
    $.each(number_range, function (i, number) {
        if (validation_error){
            $.each(check_number_range, function (j, check_number) {
                if(i!=j){
                    validation_error = inRange(number.starting,check_number.starting,check_number.ending)
                    if(validation_error == false){
                        return validation_error
                    }
                    else{
                        validation_error = inRange(number.ending,check_number.starting,check_number.ending)
                    }
                }
            });
        }
    });
    return validation_error
}

//***********************************************************
function main_range_check_function(number_range,check_number_range){
    var validation_error = true
    $.each(number_range, function (i, number) {
        if (validation_error){
            $.each(check_number_range, function (j, check_number) {
                validation_error = inRange(number.starting,check_number.starting,check_number.ending)
                if(validation_error == false){
                    return validation_error
                }
                else{
                    validation_error = inRange(number.ending,check_number.starting,check_number.ending)
                }
                if(validation_error == false){
                    return validation_error
                }
            });
        }
    });
    return validation_error
}

//**************************
function inRange(x, min, max) {
    return !((x-min)*(x-max) <= 0);
}

var nextval = max_sequence ;
// on click add icon display the row in to add the new entries
function add_popup_row() {
    $("#error_msg_id").css("display", "none")
    basic_add_new_html = '';
    var display_db_data = '';
    $('#id_popup_table').DataTable().destroy();
    $(".modal").on("hidden.bs.modal", function () {
        $("#id_error_msg").html("");
    });
    nextval += 1;
    basic_add_new_html = '<tr ><td class="number_range_checkbox"><input type="checkbox" required></td><td><input class="form-control"  type="number" maxlength="2" value = '+ nextval +'  name="sequence"  required disabled></td><td><input class="form-control" type="number" maxlength="100000000"  name="starting"  required></td><td><input class="form-control" type="number" maxlength="100000000"  name="ending" required></td><td><input class="form-control" type="number" maxlength="100000000"  name="current"  required></td>><td hidden><input class="form-control" type="text" value=""></td><td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
    $('#id_popup_tbody').append(basic_add_new_html);
    if (GLOBAL_ACTION == "number_range") {
        $(".class_del_checkbox").prop("hidden", false);
    }
    table_sort_filter('id_popup_table');
}

//function to delete selected row in popup
function delete_popup_row(myTable) {
    $('#id_popup_table').DataTable().destroy();
    try {
        var table = document.getElementById(myTable);
        var rowCount = table.rows.length;
        for (var i = 0; i < rowCount; i++) {
            var row = table.rows[i];
            var chkbox = row.cells[0].childNodes[0];
            if (null != chkbox && true == chkbox.checked) {
                table.deleteRow(i);
                nextval -= 1;
                rowCount--;
                i--;
            }
        }
        $("#id_delete_data").hide();
        $("#id_copy_data").hide();
        $("#id_update_data").hide();
        table_sort_filter('id_popup_table');
        return rowCount;
    } catch (e) {
        alert(e);
    }
}

//onclick of cancel display the table in display mode............
function display_basic_db_data() {
    $('#display_basic_table').DataTable().destroy();
    $('#id_number_range_tbody').empty();
    var edit_basic_data = '';
    $.each(rendered_number_range_data, function (i, item) {
        edit_basic_data += '<tr ><td class="class_select_checkbox"><input class="checkbox_check" onclick="valueChanged()" type="checkbox" required></td><td>' + item.sequence + '</td><td>' + item.starting + '</td><td>' + item.ending + '</td><td>' + item.current + '</td><td hidden>' + item.guid + '</td></tr>';
    });
    $('#id_number_range_tbody').append(edit_basic_data);
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
    $('#myModal').modal('hide');
    numberranges_data = read_popup_data();
    $('#id_save_confirm_popup').modal('show');
});

//Read popup table data
function read_popup_data() {
    $('#id_popup_table').DataTable().destroy();
    numberranges_data = new Array();
    validate_add_attributes = [];
    $('#id_popup_table').DataTable().destroy();
    $("#id_popup_table TBODY TR").each(function () {
        var row = $(this);
        number_range={};
        number_range.del_ind = row.find("TD").eq(6).find('input[type="checkbox"]').is(':checked');
        number_range.sequence = row.find("TD").eq(1).find('input[type="number"]').val();
        number_range.starting = parseInt(row.find("TD").eq(2).find('input[type="number"]').val());
        number_range.ending = parseInt(row.find("TD").eq(3).find('input[type="number"]').val());
        number_range.current= parseInt(row.find("TD").eq(4).find('input[type="number"]').val());
        number_range.document_type = "DOC01"
        number_range.guid = row.find("TD").eq(5).find('input[type="text"]').val();
        if (number_range == undefined){
            number_range.sequence = row.find("TD").eq(1).find('input[type="number"]').val();
        }
        if(number_range.guid == undefined) {
            number_range.guid = ''
        }
        validate_add_attributes.push(number_range.sequence);
        numberranges_data.push(number_range);
    });
    table_sort_filter('id_popup_table');
    return numberranges_data;
}

//*******************************************
function display_error_message(error_message){
    $('#error_message').text(error_message);
    document.getElementById("error_message").style.color = "Red";
    $("#error_msg_id").css("display", "block")
    $('#id_save_confirm_popup').modal('hide');
    $('#myModal').modal('show');
}

// Function to get main table data
function get_main_table_data() {
    main_table_low_value = [];
    $('#display_basic_table').DataTable().destroy();
    $("#display_basic_table TBODY TR").each(function () {
        var row = $(this);
        var main_attribute = {};
        main_attribute.sequence = row.find("TD").eq(1).html();
        main_attribute.starting = row.find("TD").eq(2).html();
        main_attribute.ending = row.find("TD").eq(3).html();
        main_attribute.current = row.find("TD").eq(4).html();
        main_attribute.guid = row.find("TD").eq(5).html();
        main_table_low_value.push(main_attribute.sequence);
        main_table_data.push(main_attribute)
    });
    table_sort_filter('display_basic_table');
}

// Function to get the selected row data
function get_row_data(tableSelector) {
    main_table_number_range_checked = [];
    $(tableSelector).DataTable().$('input[type="checkbox"]').each(function () {
        var checkbox = $(this);
        var row = checkbox.closest("tr");
        var number_range_arr_obj = {};
        number_range_arr_obj.del_ind = checkbox.is(':checked');
    if (number_range_arr_obj.del_ind) {
      number_range_arr_obj.sequence = row.find("TD").eq(1).find('input').val() || row.find("TD").eq(1).html();
      number_range_arr_obj.starting = row.find("TD").eq(2).find('input').val() || row.find("TD").eq(2).html();
      number_range_arr_obj.ending = row.find("TD").eq(3).find('input').val() || row.find("TD").eq(3).html();
      number_range_arr_obj.current = row.find("TD").eq(4).find('input').val() || row.find("TD").eq(4).html();
      number_range_arr_obj.guid = row.find("TD").eq(5).find('input').val() || row.find("TD").eq(5).html();
      number_range_arr_obj.document_type = "DOC01";
      main_table_number_range_checked.push(number_range_arr_obj);
    }
  });
}
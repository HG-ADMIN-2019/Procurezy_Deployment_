var prodcat_data = new Array();
var validate_add_attributes = [];
var prodcat={};
var main_table_low_value = [];

//hide the myModal popup: Implemented Dependency delete purpose
function hideModal() {
    $('#unspscModal').modal('hide');
}


//onclick of add button display unspscModal popup and set GLOBAL_ACTION button value
function onclick_add_button(button) {
    $("#error_msg_id").css("display", "none")
    $("#header_select").prop( "hidden", false );
    GLOBAL_ACTION = button.value
    display_button();
    $('#id_popup_table').DataTable().destroy();
    $("#id_popup_tbody").empty();
    new_row_data();
    $('#unspscModal').modal('show');
    $("#id_del_ind_checkbox").prop("hidden", true);
    document.getElementById("id_del_add_button").style.display = "block";
}

// on click copy icon display the selected checkbox data
function onclick_copy_button() {
    GLOBAL_ACTION = "COPY"
    display_button();
    onclick_copy_update_button("copy")
    document.getElementById("id_del_add_button").style.display = "block";
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
                unique_input = '<input class="form-control" type="text" value="' + row.cells[1].innerHTML + '" name="prod_cat_id"  maxlength="20"  disabled>'
                edit_basic_data += '<tr><td><input type="checkbox" required></td><td>'+unique_input+'</td><td><input type="text" class="form-control check_special_char" value="' + row.cells[2].innerHTML + '" name="prod_cat_desc"  maxlength="100" required></td><td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
                $("#header_select").prop("hidden", false);
            }
            else if (GLOBAL_ACTION == "COPY"){
                unique_input = '<input class="form-control check_number" type="text" value="' + row.cells[1].innerHTML + '" name="prod_cat_id"  maxlength="20"  required>'
                edit_basic_data += '<tr><td><input type="checkbox" required></td><td>'+unique_input+'</td><td><input type="text" class="form-control check_special_char" value="' + row.cells[2].innerHTML + '" name="prod_cat_desc"  maxlength="100" required></td><td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
                $("#header_select").prop("hidden", false);
            }
            else {
                $('#save_id').show();
                document.getElementById('save_id').style.visibility = 'visible';
                $('#delete_data').hide();
            }
        }
    }
    $('#id_popup_tbody').append(edit_basic_data);
    $("#id_del_ind_checkbox").prop("hidden", true);
    $('#unspscModal').modal('show');
    table_sort_filter('id_popup_table');
}

//onclick of cancel empty the popup table body and error messages
$(".remove_upload_data").click(() => {
    $("#id_error_msg").html("");
    $("#id_popup_tbody").empty();
    $("#id_error_msg").empty();
    $('#unspscModal').modal('hide');
    $("#id_error_msg").prop("hidden", true);
    $("#id_error_msg_prodcat").prop("hidden", true);
    $("#id_check_error_messages").prop("hidden", true);
    $("#id_check_success_messages").prop("hidden", true);
    $("#id_check_special_character_messages").prop("hidden", true)
    $("#id_check_data").prop("hidden", true);
    $('#id_popup_table').DataTable().destroy();
});

function display_error_message(error_message){
    var errorElement = document.getElementById("error_message");
    if (errorElement) {
        errorElement.textContent = error_message;
        errorElement.style.color = "Red";
    }
    $("#error_msg_id").css("display", "block");
    $('#id_save_confirm_popup').modal('hide');
    $('#unspscModal').modal('show');
}

// on click add icon display the row in to add the new entries
function add_popup_row() {
    $("#error_msg_id").css("display", "none")
    basic_add_new_html = '';
    var display_db_data = '';
    $('#id_popup_table').DataTable().destroy();
    $(".modal").on("hidden.bs.modal", function() {
        $("#id_error_msg").html("No records to be saved");
    });
    new_row_data();
    table_sort_filter('id_popup_table');
    if (GLOBAL_ACTION == "prodcat_upload") {
        $(".class_del_checkbox").prop("hidden", false);
        $("#id_del_ind_checkbox").prop("hidden", false);
    }
    $('#delete_data').hide()
}

//onclick of cancel display the table in display mode............
function display_basic_db_data() {
    $('#display_basic_table').DataTable().destroy();
    $('#id_prodcat_tbody').empty();
    var edit_basic_data = '';
    // get rendered data
    $.each(rendered_prodcat_data, function(i, item) {
        edit_basic_data += '<tr><td class="class_select_checkbox"><input class="checkbox_check" onclick="valueChanged()" type="checkbox" required></td><td>' + item.prod_cat_id + '</td><td>' + item.prod_cat_desc + '</td><td hidden>' + item.del_ind_flag  + '</td></tr>';
    });
    $('#id_prodcat_tbody').append(edit_basic_data);
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

// Functtion to hide and display save related popups
$('#save_id').click(function () {
    $('#unspscModal').modal('hide');
    prodcat_data = read_popup_data();
    $('#id_save_confirm_popup').modal('show');
});

//Read popup table data
function read_popup_data(){
    $('#id_popup_table').DataTable().destroy();
    prodcat_data = new Array();
    validate_add_attributes = [];
    $("#id_popup_table TBODY TR").each(function () {
        var row = $(this);
        prodcat={};
        prodcat.del_ind = row.find("TD").eq(3).find('input[type="checkbox"]').is(':checked');
        prodcat.prod_cat_id = row.find("TD").eq(1).find('input[type="text"]').val().toUpperCase();
        prodcat.prod_cat_desc = row.find("TD").eq(2).find('input[type="text"]').val().toUpperCase();
        if (prodcat == undefined){
        prodcat.prod_cat_id = row.find("TD").eq(1).find('input[type="text"]').val();
        }
        validate_add_attributes.push(prodcat.prod_cat_id);
        prodcat_data.push(prodcat);
    });
    table_sort_filter('id_popup_table');
    return prodcat_data;
}

// Function to get main table data
function get_main_table_data(){
    main_table_low_value = [];
    $('#display_basic_table').DataTable().destroy();
    $("#display_basic_table TBODY TR").each(function() {
        var row = $(this);
        var main_attribute = {};
        main_attribute.prod_cat_id = row.find("TD").eq(1).html();
        main_table_low_value.push(main_attribute.prod_cat_id);
    });
    table_sort_filter('display_basic_table');
}

// Function to get the selected row data
function get_row_data(tableSelector) {
    main_table_prodcat_checked = [];
    $(tableSelector).DataTable().$('input[type="checkbox"]').each(function () {
        var checkbox = $(this);
        var row = checkbox.closest("tr");
        var prodcat_arr_obj = {};
        prodcat_arr_obj.del_ind = checkbox.is(':checked');
        if(prodcat_arr_obj.del_ind) {
            prodcat_arr_obj.prod_cat_id = row.find("TD").eq(1).find('input[type="text"]').val() || row.find("TD").eq(1).html();
            prodcat_arr_obj.prod_cat_desc = row.find("TD").eq(2).find('input[type="text"]').val() || row.find("TD").eq(2).html();
            main_table_prodcat_checked.push(prodcat_arr_obj);
        }
    });
}

// Function for add a new row data
function new_row_data() {
    basic_add_new_html =
    `<tr>
        <td><input type="checkbox" required></td>
        <td><input class="input form-control check_number" type="text" title="Minimum length is 2" minlength="10" maxlength="10"  name="prod_cat_id" required></td>
        <td><input class="input form-control check_only_character" type="text" maxlength="20" name="prod_cat_desc" required></td>
        <td class="class_del_checkbox" hidden><input type="checkbox" required></td>
    </tr>`;
    $('#id_popup_tbody').append(basic_add_new_html);
    table_sort_filter('id_popup_table');
}



var cust_prod_cat_data = new Array();
var validate_add_attributes = [];
var cusprodcat={};

// on click edit icon display the data in edit mode
function onclick_edit_button() {
    //display the add,cancel and upload buttons and select all checkbox,select heading and checkboxes for each row
    $('#display_basic_table').DataTable().destroy();
    $("#hg_select_checkbox").prop("hidden", false);
    $(".class_select_checkbox").prop("hidden", false);
     $( ".hg_unspsc_th_column").prop( "hidden", false );
     $( ".hg_unspsc_td_column").prop( "hidden", false );
     $(".hg_unspsc_td_column").show()
    //hide the edit,delete,copy and update buttons
    $('#id_cancel_data').show();
    $('#id_edit_data').hide();
    $('#id_check_all').show();
    table_sort_filter('display_basic_table');
}

//**********************************************************
// on click edit icon display the data in edit mode
function edit_basic(){
    $('#display_basic_table').DataTable().destroy();
     $( "#hg_select_checkbox").prop( "hidden", false );
     $( ".hg_unspsc_th_column").prop( "hidden", false );
     $( ".hg_unspsc_td_column").prop( "hidden", false );
     $(".hg_unspsc_td_column").show()

    document.getElementById("add_line_up_div").style.display = "block";
    document.getElementById("basic_edit_save").style.display = "block";
    document.getElementById("edit_up_data_div").style.display = "none";
    document.getElementById("delete_line_up_div").style.display = "none";
    document.getElementById("copy_line_up_div").style.display = "none";
    table_sort_filter('display_basic_table');
}

//onclick of add button display myModal popup and set GLOBAL_ACTION button value
function onclick_add_button(button) {
    GLOBAL_ACTION = button.value
    $("#id_popup_tbody").empty();
    $('#myModal').modal('show');
    basic_add_new_html = '<tr><td><input type="checkbox" required></td><td><select class="form-control" type="text">'+prod_cat_id_dropdown+'</select></td><td><select class="form-control"disabled>'+description_dropdown+'</select></td><td hidden>prod_cat_guid</td><td hidden>del_ind</td></tr>';
    $('#id_popup_tbody').append(basic_add_new_html);
    $("#id_del_ind_checkbox").prop("hidden", true);
    document.getElementById("id_del_add_button").style.display = "block";
    $("#save_id").prop("hidden", false);
}


//onclick of upload button display id_data_upload popup and set GLOBAL_ACTION button value
function onclick_upload_button() {
    GLOBAL_ACTION = "cusprodcat_upload"
    $("#id_popup_tbody").empty();
    $('#id_data_upload').modal('show');
    document.getElementById('id_file_data_upload').value = "";
}
//***************************

// on click copy icon display the selected checkbox data
function onclick_copy_button() {
    GLOBAL_ACTION = "cusprodcat_copy"
    onclick_copy_update_button("copy")
    document.getElementById("id_del_add_button").style.display = "block";
}

// on click update icon display the selected checkbox data to update
function onclick_update_button() {
    GLOBAL_ACTION = "cusprodcat_update"
    onclick_copy_update_button("update")
    document.getElementById("id_del_add_button").style.display = "none";
}

//**********************************************************
function onclick_copy_update_button(data) {
        $("#id_popup_tbody").empty();
        $('#display_basic_table').DataTable().destroy();
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
                if(GLOBAL_ACTION == "cusprodcat_update"){
                    unique_input = '<input class="form-control" type="number" value="' + row.cells[1].innerHTML + '" name="product category"  maxlength="8"  disabled>'
                    edit_basic_data += '<tr ><td hidden><input type="checkbox" required></td><td>'+unique_input+'</td><td><input class="form-control" value="' + row.cells[2].innerHTML + '" type="text" onkeypress="return /[a-z ]/i.test(event.key)" name="description"  maxlength="100" style="text-transform:uppercase" required></td><td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
                    $("#header_select").prop("hidden", true);
                }
                else{
                    unique_input = '<input class="form-control" type="number" value="' + row.cells[1].innerHTML + '" name="product category" maxlength="8" required>'
                    edit_basic_data += '<tr ><td><input type="checkbox" required></td><td>'+unique_input+'</td><td><input class="form-control" value="' + row.cells[2].innerHTML + '" type="text" onkeypress="return /[a-z ]/i.test(event.key)" name="description"  maxlength="100" style="text-transform:uppercase" required></td><td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
                    $("#header_select").prop("hidden", false);
                }
            }
        }

        $('#id_popup_tbody').append(edit_basic_data);
        $("#id_del_ind_checkbox").prop("hidden", true);
        $('#myModal').modal('show');
        table_sort_filter('id_popup_table');
        table_sort_filter('display_basic_table');

    }
 //************************currency code
//onclick of cancel empty the popup table body and error messages
$(".remove_upload_data").click(() => {
    $("#id_error_msg").html("");
    $("#id_popup_tbody").empty();
    $("#id_error_msg").empty();
    $('#myModal').modal('hide');
    $("#id_error_msg").prop("hidden", true);
    $("#id_error_msg_country_code").prop("hidden", true);
    $("#id_error_msg_country_name").prop("hidden", true);
    $("#id_error_msg_country_length").prop("hidden", true);
    $("#id_check_error_messages").prop("hidden", true);
    $("#id_check_success_messages").prop("hidden", true);
    $("#id_check_special_character_messages").prop("hidden", true)
    $("#id_check_data").prop("hidden", true);
    $('#id_popup_table').DataTable().destroy();


});

//validate by comparing  main table values and popup table values
function maintable_validation(validate_add_attributes, main_table_low_value) {
    var no_duplicate_entries = 'Y'
    var common = [];
    jQuery.grep(validate_add_attributes, function (el) {
        if (jQuery.inArray(el, main_table_low_value) != -1) { common.push(el); }
    });
    if (common.length != 0) {
        $("#id_error_msg").prop("hidden", false)
        $('#id_error_msg').text(messageConstants["JMSG001"])
        document.getElementById("id_error_msg").style.color = "Red";
        $('#id_save_confirm_popup').modal('hide');
        $('#myModal').modal('show');
        no_duplicate_entries = 'N'
    }
    return no_duplicate_entries
}

// validating the  popup table for duplicate entries
function compare_table_for_duplicate_entries(validate_add_attributes, country) {
    add_attr_duplicates = false;
    var add_attr_duplicates_list = [];
    var add_attr_unique_list = [];
    var no_duplicate_value = 'Y'
    $.each(validate_add_attributes, function (index, value) {
        if ($.inArray(value, add_attr_unique_list) == -1) {
            add_attr_unique_list.push(value);
        }
        else {
            if ($.inArray(value, add_attr_duplicates_list) == -1) {
                add_attr_duplicates_list.push(value);
            }
        }
    });
    if (add_attr_duplicates_list.length != 0) {
        $("#id_error_msg").prop("hidden", false)
       //document.getElementById("id_error_msg").innerHTML = messageConstants["JMSG001"];
       document.getElementById("id_error_msg").style.color = "Red";
        $('#id_save_confirm_popup').modal('hide');
        $('#myModal').modal('show');
        no_duplicate_value = 'N'
    }
    else if (country.country_code.length == 0) {
        $("#id_error_msg").prop("hidden", false)
        Error_msg = "";
        Error_msg = messageConstants["JMSG002"]+ "Country Code";
        document.getElementById("id_error_msg").innerHTML = Error_msg;
        document.getElementById("id_error_msg").style.color = "Red";
        $('#id_save_confirm_popup').modal('hide');
        $('#myModal').modal('show');
        no_duplicate_value = 'N'
    }
    else if (country.country_name.length == 0) {
        $("#id_error_msg").prop("hidden", false)
        Error_msg = "";
        Error_msg = messageConstants["JMSG002"]+ "Country Name";
        document.getElementById("id_error_msg").innerHTML = Error_msg;
        document.getElementById("id_error_msg").style.color = "Red";
        $('#id_save_confirm_popup').modal('hide');
        $('#myModal').modal('show');
        no_duplicate_value = 'N'
    }
    country_name = country.country_name.replace(/\s\s+/g, ' ')
    if (country_name == " ") {
        $("#id_error_msg").prop("hidden", false)
        Error_msg = "";
        Error_msg = "Enter Valid data in Country name";
        document.getElementById("id_error_msg").innerHTML = Error_msg;
        document.getElementById("id_error_msg").style.color = "Red";
        $('#id_save_confirm_popup').modal('hide');
        $('#myModal').modal('show');
        no_duplicate_value = 'N'
    }
    return no_duplicate_value
}

//*******************************************************
// on click add icon display the row in to add the new entries
function add_popup_row() {
    basic_add_new_html = '';
    var display_db_data = '';
    $('#id_popup_table').DataTable().destroy();
    $(".modal").on("hidden.bs.modal", function () {
    $("#id_error_msg").html(" ");
     });
    basic_add_new_html = '<tr ><td><input type="checkbox" required></td><td><input class="input" class="form-control"  type="number" name="productcategory" required></td><td><input class="input" class="form-control" type="text" maxlength="100" onkeypress="return /[a-z ]/i.test(event.key)" name="Description" required"></td><td hidden></td></tr>';
    $('#id_popup_tbody').append(basic_add_new_html);
    if (GLOBAL_ACTION == "cusprodcat_upload") {
        $(".class_del_checkbox").prop("hidden", false);
    }
    table_sort_filter_popup('id_popup_table');
}


function delete_duplicate() {
    $('#id_popup_table').DataTable().destroy();
    var cusprodcat_code_check = new Array
    $("#id_popup_table TBODY TR").each(function () {
        var row = $(this);

        //*************** reading data from the pop-up ***************
        country_name = row.find("TD").eq(2).find('input[type="text"]').val().toUpperCase();
        country_code = row.find("TD").eq(1).find('input[type="text"]').val().toUpperCase();
        checked_box = row.find("TD").eq(3).find('input[type="checkbox"]').is(':checked')


        if (country_code_check.includes(country_code)) {
            $(row).remove();
        }
        country_code_check.push(country_code);
    })
    table_sort_filter_popup_pagination('id_popup_table')
    check_data()
}

// Function to hide and display save related popups
$('#save_id').click(function () {
    $('#myModal').modal('hide');
    $('#id_save_confirm_popup').modal('show');
});

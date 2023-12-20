var payment_term_data = new Array();
var validate_add_attributes = [];
var main_table_low_value = [];
var payment_term={};

//hide the myModal popup: Implemented Dependency delete purpose
function hideModal() {
    $('#payment_term_Modal').modal('hide');
}

//onclick of add button display payment_term_Modal popup and set GLOBAL_ACTION button value
function onclick_add_button(button) {
    $("#error_msg_id").css("display", "none")
    $( "#header_select").prop( "hidden", false );
    GLOBAL_ACTION = button.value
    display_button();
    $('#id_popup_table').DataTable().destroy();
    $("#id_popup_tbody").empty();
    $('#payment_term_Modal').modal('show');
    new_row_data();   // Add a new row in popup
    table_sort_filter('id_popup_table');
    $("#id_del_ind_checkbox").prop("hidden", true);
    document.getElementById("id_del_add_button").style.display = "block";
    $("#save_id").prop("hidden", false);
}

//onclick of cancel empty the popup table body and error messages
$(".remove_upload_data").click(() => {
    $("#id_error_msg").html("");
    $("#id_popup_tbody").empty();
    $("#id_error_msg").empty();
    $('#payment_term_Modal').modal('hide');
    $("#id_error_msg").prop("hidden", true);
    $("#id_error_msg_payment_term_key").prop("hidden", true);
    $("#id_error_msg_description").prop("hidden", true);
    $("#id_error_msg_description_length").prop("hidden", true);
    $("#id_check_error_messages").prop("hidden", true);
    $("#id_check_success_messages").prop("hidden", true);
    $("#id_check_special_character_messages").prop("hidden", true)
    $("#id_check_data").prop("hidden", true);
    $('#id_popup_table').DataTable().destroy();
});

// on click add icon display the row in to add the new entries
function add_popup_row() {
    $("#error_msg_id").css("display", "none")
    basic_add_new_html = '';
    var display_db_data = '';
    $('#id_popup_table').DataTable().destroy();
    $(".modal").on("hidden.bs.modal", function () {
        $("#id_error_msg").html("");
    });
    new_row_data();   // Add a new row in popup
    if (GLOBAL_ACTION == "payment_term_upload") {
        $(".class_del_checkbox").prop("hidden", false);
    }
}

//***********************************************
function display_error_message(error_message){
    $('#error_message').text(error_message);
    document.getElementById("error_message").style.color = "Red";
    $("#error_msg_id").css("display", "block")
    $('#id_save_confirm_popup').modal('hide');
    $('#payment_term_Modal').modal('show');
}

$('#save_id').click(function () {
    $('#payment_term_Modal').modal('hide');
    payment_term_data =  read_popup_data();
    $('#id_save_confirm_popup').modal('show');
});

//Read popup table data
function read_popup_data() {
    $('#id_popup_table').DataTable().destroy();
    payment_term_data = new Array();
    validate_add_attributes = [];
    $("#id_popup_table TBODY TR").each(function () {
        var row = $(this);
        payment_term = {};
        payment_term.payment_term_guid = row.find("TD").eq(3).find('input[type="text"]').val();
        payment_term.del_ind = row.find("TD").eq(2).find('input[type="checkbox"]').is(':checked');
        payment_term.payment_term_key = row.find("TD").eq(1).find('input[type="number"]').val();
        if (payment_term == undefined) {
            payment_term.payment_term_key = row.find("TD").eq(1).find('input[type="number"]').val();
        }
            if(payment_term.payment_term_guid == undefined) {
                payment_term.payment_term_guid = ''
            }
        validate_add_attributes.push(payment_term.payment_term_key);
        payment_term_data.push(payment_term);
    });
    table_sort_filter('id_popup_table');
    return payment_term_data;
}

// Function for add a new row data
function new_row_data() {
    basic_add_new_html = '<tr><td><input type="checkbox" required></td><td><input class="form-control check_number" type="number" minlength="3" maxlenght="4"  name="payment_term_key" style="text-transform:uppercase;" required></td><td class="class_del_checkbox" hidden><input type="checkbox" required></td><td hidden><input  type="text"  name="guid"></td></tr>';
    $('#id_popup_tbody').append(basic_add_new_html);
    table_sort_filter('id_popup_table');
}

// Function to get main table data
function get_main_table_data() {
    main_table_low_value = [];
    $('#display_basic_table').DataTable().destroy();
    $("#display_basic_table TBODY TR").each(function () {
        var row = $(this);
        var main_attribute = {};
        main_attribute.payment_term_key = row.find("TD").eq(1).html();
        main_table_low_value.push(main_attribute.payment_term_key);
    });
    table_sort_filter('display_basic_table');
}

// Function to get the selected row data
function get_selected_row_data() {
    $("#display_basic_table TBODY TR").each(function () {
        var row = $(this);
        var payment_term_arr_obj = {};
        payment_term_arr_obj.del_ind = row.find("TD").eq(0).find('input[type="checkbox"]').is(':checked');
        if(payment_term_arr_obj.del_ind){
        payment_term_arr_obj.payment_term_guid = row.find("TD").eq(3).html();
        payment_term_arr_obj.payment_term_key = row.find("TD").eq(1).html();
        main_table_payment_term_checked.push(payment_term_arr_obj);
        }
    });
}

// Function to get the selected row data
function get_row_data(tableSelector) {
    main_table_checked = [];
    $(tableSelector).DataTable().$('input[type="checkbox"]').each(function () {
        var checkbox = $(this);
        var row = checkbox.closest("tr");
        var payment_term_arr_obj = {};
        payment_term_arr_obj.del_ind = checkbox.is(':checked');
        if(payment_term_arr_obj.del_ind) {
            payment_term_arr_obj.payment_term_key = row.find("TD").eq(1).find('input[type="number"]').val() || row.find("TD").eq(1).html();
            main_table_checked.push(payment_term_arr_obj);
        }
    });
}
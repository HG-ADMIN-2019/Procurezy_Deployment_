var orgnodetyp_data = new Array();
var validate_add_attributes = [];
var org_node_type = {};

//hide the myModal popup: Implemented Dependency delete purpose
function hideModal() {
    $('#org_node_Modal').modal('hide');
}

//onclick of cancel empty the popup table body and error messages
$(".remove_upload_data").click(() => {
    $("#id_error_msg").html("");
    $("#id_popup_tbody").empty();
    $("#id_error_msg").empty();
    $('#org_node_Modal').modal('hide');
    $("#id_error_msg").prop("hidden", true);
    $("#id_error_msg_org_node_type_code").prop("hidden", true);
    $("#id_error_msg_org_node_type_name").prop("hidden", true);
    $("#id_error_msg_org_node_type_length").prop("hidden", true);
    $("#id_check_error_messages").prop("hidden", true);
    $("#id_check_success_messages").prop("hidden", true);
    $("#id_check_special_character_messages").prop("hidden", true)
    $("#id_check_data").prop("hidden", true);
    $('#id_popup_table').DataTable().destroy();
});

//*******************************************
function display_error_message(error_message){
    $("#error_msg_id").css("display", "block");
//    $('#error_message').text(error_message);
    document.getElementById("error_msg_id").innerHTML = error_message;
    document.getElementById("error_msg_id").style.color = "Red";
    $('#id_save_confirm_popup').modal('hide');
    $('#org_node_Modal').modal('show');
}

// Function to hide and display save related popups
$('#save_id').click(function () {
    $('#org_node_Modal').modal('hide');
    orgnodetyp_data = read_popup_data();
    $('#id_save_confirm_popup').modal('show');
});

//Read popup table data
function read_popup_data(){
    $('#id_popup_table').DataTable().destroy();
    orgnodetyp_data = new Array();
    validate_add_attributes = [];
    $("#id_popup_table TBODY TR").each(function() {
        var row = $(this);
        org_node_type = {};
        org_node_type.del_ind_flag = row.find("TD").eq(5).find('input[type="checkbox"]').is(':checked');
        org_node_type.node_type = row.find("TD").eq(1).find("select").val();
        org_node_type.description = row.find("TD").eq(2).find("input").val();
        org_node_type.node_type_guid = row.find("TD").eq(3).find('input').val();
        org_node_type.del_ind = row.find("TD").eq(4).find('input[type="checkbox"]').is(':checked');
        if (org_node_type == undefined) {
            org_node_type.node_type = row.find("TD").eq(1).find("select").val();
        }
        if(org_node_type.node_type_guid == undefined) {
            org_node_type.node_type_guid = '';
        }
        validate_add_attributes.push(org_node_type.node_type);
        orgnodetyp_data.push(org_node_type);
    });
     table_sort_filter('id_popup_table');
    return orgnodetyp_data;
}

// Function to get main table data
function get_main_table_data(){
    main_table_low_value = [];
    $('#display_basic_table').DataTable().destroy();
    $("#display_basic_table TBODY TR").each(function() {
        var row = $(this);
        var main_attribute = {};
        main_attribute.country_code = row.find("TD").eq(1).html();
        main_table_low_value.push(main_attribute.country_code);
    });
    table_sort_filter('display_basic_table');
}

// Function for add a new row data
function new_row_data() {
    basic_add_new_html = '<tr><td><input type="checkbox" required></td><td><select type="text" class="input form-control nodetype" name="nodetype" onchange="GetSelectedTextValue(this)">' + node_type_dropdown + '</select></td><td><input class="form-control description" type="text"  name="description" value="'+desc_nodetype+'" disabled></td><td hidden>guid</td><td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
    $('#id_popup_tbody').append(basic_add_new_html);
    table_sort_filter('id_popup_table');
}

// Function to get the selected row data
function get_row_data(tableSelector) {
    main_table_org_node_type_checked = []; // Clear the previous data before collecting new data
    $(tableSelector).DataTable().$('input[type="checkbox"]').each(function () {
        var checkbox = $(this);
        var row = checkbox.closest("tr");
        var org_node_type_arr_obj = {};
        org_node_type_arr_obj.del_ind = checkbox.is(':checked');
        if(org_node_type_arr_obj.del_ind)
        {
            org_node_type_arr_obj.node_type = row.find("TD").eq(1).find('input[type="text"]').val() || row.find("TD").eq(1).html();
            org_node_type_arr_obj.description = row.find("TD").eq(2).find('input[type="text"]').val() || row.find("TD").eq(2).html();
            org_node_type_arr_obj.node_type_guid = row.find("TD").eq(3).find('input[type="text"]').val() || row.find("TD").eq(3).html();
            main_table_org_node_type_checked.push(org_node_type_arr_obj);
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
var calendarconfig_data = new Array();
var country_list = new Array();
var validate_add_attributes = [];
var main_table_low_value = [];
var calendar={};

//hide the myModal popup: Implemented Dependency delete purpose
function hideModal() {
    $('#Calendar_Modal').modal('hide');
}

// on click update icon display the selected checkbox data to update
function onclick_update_button() {
    GLOBAL_ACTION = "UPDATE"
    display_button();
    onclick_copy_update_button("UPDATE")
    document.getElementById("id_del_add_button").style.display = "none";
}

//onclick of cancel empty the popup table body and error messages
$(".remove_upload_data").click(() => {
    $("#id_error_msg").html("");
    $("#id_popup_tbody").empty();
    $("#id_error_msg").empty();
    $('#Calendar_Modal').modal('hide');
    $("#id_error_msg").prop("hidden", true);
    $("#id_error_msg_calendar_code").prop("hidden", true);
    $("#id_error_msg_calendar_name").prop("hidden", true);
    $("#id_error_msg_calendar_length").prop("hidden", true);
    $("#id_check_error_messages").prop("hidden", true);
    $("#id_check_success_messages").prop("hidden", true);
    $("#id_check_special_character_messages").prop("hidden", true)
    $("#id_check_data").prop("hidden", true);
    $('#id_popup_table').DataTable().destroy();
});

function display_error_message(error_message){
    $('#error_message').text(error_message);
    document.getElementById("error_message").style.color = "Red";
    $("#error_msg_id").css("display", "block");
    $('#id_save_confirm_popup').modal('hide');
    $('#Calendar_Modal').modal('show');
}

//onclick of cancel display the table in display mode............
function display_basic_db_data() {
    $('#display_basic_table').DataTable().destroy();
    $('#id_calendar_tbody').empty();
    calendar_drpdown();
    var edit_basic_data = '';
    var desc = ''; var country_code, country_name;
    var wdays = [];
    var wday_array = [];
    var wd_value = '';
    $.each(rendered_calendar_data, function (i, item) {
        wdays = []
        country_code = item.country_code;
        for (i = 0; i < render_country_data.length; i++) {
            if (country_code == render_country_data[i].country_code)
                country_name = render_country_data[i].country_name;
        }
        wday_array = item.working_days.split(",");
        for(j=0; j<wday_array.length; j++) {
            wdays[j] = get_days(wday_array[j]);
        }
        wday_array = [];
        wd_value = '';
        for(i=0; i<wdays.length;i++){
            wd_value += ' <span id="id_wdays"  class="badge badge-primary wdays_copy"> '+ wdays[i] +'</span>' + '';
        }
        edit_basic_data += 
        '<tr> <td class="class_select_checkbox"><input class="checkbox_check" onclick="valueChanged()" type="checkbox" required> </td> <td>' + item.calender_id + '</td>'+
        '<td>' + country_name + '</td> '+
        '<td>' + item.description + '</td>'+
        '<td>' + item.year + '</td>'+
        '<td>'+ wd_value +'</td>'+
        '<td hidden>' + item.calendar_config_guid + '</td></tr>';
    });
    $('#id_calendar_tbody').append(edit_basic_data);
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
    $('#Calendar_Modal').modal('hide');
    calendarconfig_data = read_popup_data();
    $('#id_save_confirm_popup').modal('show');
});

//Read popup table data
function read_popup_data() {
    $('#id_popup_table').DataTable().destroy();
    calendarconfig_data = new Array();
    validate_add_attributes = [];
    $("#id_popup_table TBODY TR").each(function () {
        var row = $(this);
        calendar = {};
        var workingDay;
        calendar.calender_id = (row.find("TD").eq(1).find('input[type="text"]').val())
        calendar.country = (row.find("TD").eq(2).find('select[type="text"]').val())
        calendar.description = (row.find("TD").eq(3).find('input[type="text"]').val())
        calendar.year = (row.find("TD").eq(4).find('input[type="text"]').val())
        workingDay = (row.find("TD").eq(5).find('select[type="text"]').val())
        calendar.working_days = workingDay.join()
        calendar.del_ind = row.find("TD").eq(6).find('input[type="checkbox"]').is(':checked')
        calendar.calendar_config_guid = row.find("TD").eq(7).find('input[type="text"]').val()
        if(calendar.calendar_config_guid == undefined) {
            calendar.calendar_config_guid = ''
        }
        if(calendar.calender_id == undefined) {
            calendar.calender_id = ''
        }
        validate_add_attributes.push(calendar.calender_id);
        calendarconfig_data.push(calendar);
    });
    table_sort_filter('id_popup_table');
    return calendarconfig_data;
}

// Function to get main table data
function get_main_table_data() {
    main_table_low_value = [];
    $('#display_basic_table').DataTable().destroy();
    $("#display_basic_table TBODY TR").each(function () {
        var row = $(this);
        var main_attribute = {};
        main_attribute.calender_id = row.find("TD").eq(1).html();
        main_table_low_value.push(main_attribute.calender_id);
    });
    table_sort_filter('display_basic_table');
}

// Function to get the selected row data
function get_row_data(tableSelector) {
    $('#id_popup_table').DataTable().destroy();
    main_table_calendar_checked = [];
    $(tableSelector + " TBODY TR").each(function () {
        var row = $(this);
        var calendar_arr_obj = {};
        calendar_arr_obj.del_ind = row.find("TD").eq(0).find('input[type="checkbox"]').is(':checked');
        if(calendar_arr_obj.del_ind){
            var cntry_name;
            var cntry_code;
            cntry_name = (row.find("TD").eq(2).find('input[type="text"]').val()) || row.find("td:eq(2)").html();
            for (i = 0; i < render_country_data.length; i++) {
                if (cntry_name == render_country_data[i].country_name)
                    cntry_code = render_country_data[i].country_code;
            }
            calendar_arr_obj.calender_id = (row.find("TD").eq(1).find('input[type="text"]').val()) || row.find("TD").eq(1).html();
            calendar_arr_obj.country = cntry_code || row.find("TD").eq(2).html();
            calendar_arr_obj.description = (row.find("TD").eq(3).find('input[type="text"]').val()) || row.find("TD").eq(3).html();
            calendar_arr_obj.year = (row.find("TD").eq(4).find('input[type="text"]').val()) || row.find("TD").eq(4).html();
            calendar_arr_obj.working_days = row.find("td").eq(5).find('select[id="working_days"]').val() || row.find("td").eq(5).html();
            calendar_arr_obj.del_ind = row.find("TD").eq(0).find('input[type="checkbox"]').is(':checked');
            calendar_arr_obj.calendar_config_guid = row.find("TD").eq(7).find('input[type="text"]').val() || row.find("TD").eq(6).html();
            main_table_calendar_checked.push(calendar_arr_obj);
        }
    });
}

function add_popup_row() {
        $('#id_popup_table').DataTable().destroy();
        $("#error_msg_id").css("display", "none")
        var edit_basic_data = "";
        calendar_drpdown();
        edit_basic_data +=
        '<tr>'+
            '<td><input type="checkbox" required></td>'+
            '<td><input class="form-control" type="text" value="" name="calender_id"  maxlength="10" style="text-transform:uppercase" ></td>'+
            '<td><select id="country" class="input form-control" type="text" name="country">' + country_dropdwn + '</select></td>'+
            '<td><input value=""  class="form-control check_special_char" type="text" name="description"></td>'+
            '<td><input value="" class="form-control yearPicker" type="text" maxlength="4"  name="year"></td>'+
            '<td style="width: 230px;"> <select id="working_days"  class="form-control multiple_select working_days" type="text" name="working_days"  multiple  title="Select.." data-selected-text-format="count" data-actions-box="true" >'+workingdays_dropdown+'</select> </td>'+
            '<td class="class_del_checkbox" hidden> <input type="checkbox" ></td>'+
            '<td hidden><input type="text" id="calendar_config_guid" value=""></td>'+
        '</tr> ';
        $("#header_select").prop("hidden", false);
        $('#id_popup_tbody').append(edit_basic_data);
        DatePicker();
        MultipleSelect();
        $("#id_del_ind_checkbox").prop("hidden", true);
        $('#Calendar_Modal').modal('show');
        table_sort_filter('id_popup_table');
    }
$(document).ready(function () {
    $('.generic-help-text-badge').text('Valid characters are A-Z a-z 0-9 [!@#$/| ] ')
    $('.star-search-help-text-badge').text('Use * as a wild card search criteria (eg. Apple - App*, *ple, *ppl*)')

    $('.help-text-alpha-numeric-special').text('Valid characters are A-Z a-z 0-9 [!@#$/| ] ')
    // <span class="badge help-text-badge help-text-alpha-numeric-special"></span>

    $('.help-text-alpha-numeric').text('Valid characters are A-Z a-z 0-9 ')
    // <span class="badge help-text-badge help-text-alpha-numeric"></span>
    
    $('.help-text-star-search').text('Use * as a wild card search criteria (eg. Apple - App*, *ple, *ppl*)')
    // <span class="badge help-text-badge help-text-star-search"></span>

    $('.help-text-phone-numbers').text('Valid characters for Phone, Mobile and Fax are 0-9 [-+ ]')
    // <small class="form-text text-muted help-text-phone-numbers"></small>

    $('.help-text-porg_dropdown').text('Porg is the precedence and override other search crieteria')

});

var GLOBAL_MANAGER_DETAIL = []
// To hide date fields based on users selection

function Hide() {

    var field = document.getElementById("id_required");

    required = field.value
    if (required == 'From') {
        $('#id_from_date').show()
        $('#id_to_date').hide()
        $('#id_on_date').hide()
        document.getElementById("dateControl").innerHTML = "From:"
    }

    else if (required == 'Between') {
        $('#id_from_date').show()
        $('#id_to_date').show()
        $('#id_on_date').hide()
        document.getElementById("dateControl").innerHTML = "From:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; To: "
    }

    else if (required == 'On') {
        $('#id_from_date').hide()
        $('#id_to_date').hide()
        $('#id_on_date').show()
        document.getElementById("dateControl").innerHTML = "On:"
    }
}

// Function to switch between tabs in Email Notification
function openTab(evt, tabNames) {
    var i, x, tablinks;
    x = document.getElementsByClassName("tab");
    for (i = 0; i < x.length; i++) {
        x[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablink");
    for (i = 0; i < x.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" w3-amber", "");
    }
    document.getElementById(tabNames).style.display = "block";
    evt.currentTarget.className += " w3-amber";
}

// Function to Hide contact information in free text page
function hide_contact_info() {

    var prod_info = document.getElementById("prod_info");
    prod_info.style.display = "block";

    var contact_info = document.getElementById("contact_info");
    contact_info.style.display = "none";
}

// Function to Hide product information in free text page
function hide_prod_info() {
    var contact_info = document.getElementById("contact_info");
    contact_info.style.display = "block";

    var prod_info = document.getElementById("prod_info");
    prod_info.style.display = "none";
}



// Function to reset form values
function resetForm() {
    document.getElementByClassName("myForm").reset();
}



// Function to hide and display date in update limit order form
function hide_date() {
    var req = document.getElementById("req")
    var required = req.options[req.selectedIndex].value
    var from_date = document.getElementById("frm_dat");
    var to_date = document.getElementById("to_dat");
    var on_date = document.getElementById("on_dat");

    if (required == 'From') {
        from_date.style.display = "block";
        to_date.style.display = "none";
        on_date.style.display = "none";
        $("#StartDate").prop('required', true);
    }

    if (required == 'On') {
        on_date.style.display = "block";
        from_date.style.display = "none";
        to_date.style.display = "none";
        $("#OnDate").prop('required', true);
    }

    if (required == 'Between') {
        on_date.style.display = "none";
        from_date.style.display = "block";
        to_date.style.display = "block";
        $("#StartDate").prop('required', true);
        $("#EndDate").prop('required', true);
    }

    if (required == 'None') {
        on_date.style.display = "none";
        from_date.style.display = "none";
        to_date.style.display = "none";
    }

}




// Function to expand number ranges in tree in application settings
var action = 1;
function number_ranges() {
    var num_range = document.getElementById("num_disp")
    if (action == 1) {
        num_range.style.display = "block";
        action = 2;
    }
    else {
        num_range.style.display = "none";
        action = 1;
    }
}

// Function to toggle sc_num_ranges div
function sc_num_ranges() {
    document.getElementById('create_num_ran').style.display = 'block';
}


function item_name_validation(item_name) {
    if (/^[a-zA-Z0-9- ]*$/.test(item_name) == false) {
        var message = 'Item name cannot contain any special characters'
        return false, message;
    } else if (item_name.length < 3) {
        message = 'Item name must contain at least 3 characters'
        return false, message;
    } else if (item_name.length > 40) {
        message = 'Item name should be less than 40 characters  '
        return false, message;
    } else {
        return true;
    }
}

function limit_item_validation(item_name, prod_cat, currency, supp_id, follow_up_action, required, from_date, to_date, on_date, overall_limit, expected_value) {
    message = item_name_validation(item_name)
    if (message != true) {
        return false, message;
    }
    if (prod_cat == '') {
        return false, 'Please select product category'
    }
    if (currency == '') {
        return false, 'Please select currency'
    }
    if (supp_id == '') {
        return false, 'Please select supplier'
    }
    if (follow_up_action == '') {
        return false, 'Please select follow up actions'
    }
    if (required == '') {
        return false, 'Please select date'
    }
    if (required == 'Between') {
        if (from_date.length == '' || to_date.length == '') {
            return false, 'Please select From and To date'
        }

        dates = validate_from_to_date(from_date, to_date)
        if (dates != true) {
            return false, dates;
        }
    }

    if (required == 'On') {
        if (on_date == '') {
            return false, 'Please select On date'
        }
    }

    if (required == 'From') {
        if (from_date == '') {
            return false, 'Please select From date'
        }
    }

    if (parseFloat(expected_value) > parseFloat(overall_limit)) {
        return false, 'Expected value cannot be greater than overall limit'
    }
    if (expected_value.length == '') {
        return false, 'Enter overall limit and expected value'
    } else {
        return true;
    }
}

function check_for_special_char(string) {
    if (/^[a-zA-Z0-9- ]*$/.test(string) == false) {
        return false
    } else {
        return true;
    }
}


function validate_from_to_date(start_date, end_date) {
    if ((Date.parse(end_date) < Date.parse(start_date))) {
        return false, 'From date cannot be less than to date'
    } else {
        return true
    }
}

function pr_form_validation(item_name, price, lead_time, quantity) {
    if (item_name.length < 3) {
        return false, 'Item name cannot contain any special characters'
    }
    is_valid = check_for_special_char(item_name)
    if (!is_valid) {
        return false, 'Item name cannot contain any special characters';
    }
    if (price.length > 15) {
        return false, 'Price cannot contain more than 15 digits'
    }
    if (lead_time.length > 3) {
        return false, 'Lead time cannot contain more than 3 digits'
    }
    if (quantity.length > 7) {
        return false, 'Quantity cannot contain more than 7 digits'
    } else {
        return true;
    }
}

//################################ Nav bar sub menu display #############################################################

function nav_bar_user_settings() {
    document.getElementById("shop_shop_plus_submenu").style.display = 'none';
    document.getElementById("user_settings_sub_menu").style.display = 'block';
    document.getElementById("admin_sub_menu").style.display = 'none';
    document.getElementById("purchaser_sub_menu").style.display = 'none';
    document.getElementById("goods_receipts_sub_menu").style.display = 'none';
    document.getElementById("approvals_sub_menu").style.display = 'none';
    document.getElementById("content_management_sub_menu").style.display = 'none';
    document.getElementById("configuration_sub_menu").style.display = 'none';
    document.getElementById("time_sheet_sub_menu").style.display = 'none';
    document.getElementById("som_sub_menu").style.display = 'none';
    document.getElementById("shop_assist_sub_menu").style.display = 'none';
    document.getElementById("whatsapp_marketing_sub_menu").style.display = 'none';
}

function nav_bar_shop() {
    document.getElementById("shop_shop_plus_submenu").style.display = 'block';
    document.getElementById("user_settings_sub_menu").style.display = 'none';
    document.getElementById("admin_sub_menu").style.display = 'none';
    document.getElementById("purchaser_sub_menu").style.display = 'none';
    document.getElementById("goods_receipts_sub_menu").style.display = 'none';
    document.getElementById("approvals_sub_menu").style.display = 'none';
    document.getElementById("content_management_sub_menu").style.display = 'none';
    document.getElementById("configuration_sub_menu").style.display = 'none';
    document.getElementById("time_sheet_sub_menu").style.display = 'none';
    document.getElementById("som_sub_menu").style.display = 'none';
    document.getElementById("shop_assist_sub_menu").style.display = 'none';
    document.getElementById("whatsapp_marketing_sub_menu").style.display = 'none';
}
function nav_bar_goods_receipts() {
    document.getElementById("shop_shop_plus_submenu").style.display = 'none';
    document.getElementById("user_settings_sub_menu").style.display = 'none';
    document.getElementById("admin_sub_menu").style.display = 'none';
    document.getElementById("purchaser_sub_menu").style.display = 'none';
    document.getElementById("goods_receipts_sub_menu").style.display = 'block';
    document.getElementById("approvals_sub_menu").style.display = 'none';
    document.getElementById("content_management_sub_menu").style.display = 'none';
    document.getElementById("configuration_sub_menu").style.display = 'none';
    document.getElementById("time_sheet_sub_menu").style.display = 'none';
    document.getElementById("som_sub_menu").style.display = 'none';
    document.getElementById("shop_assist_sub_menu").style.display = 'none';
    document.getElementById("whatsapp_marketing_sub_menu").style.display = 'none';
}
function nav_bar_admin() {
    document.getElementById("shop_shop_plus_submenu").style.display = 'none';
    document.getElementById("user_settings_sub_menu").style.display = 'none';
    document.getElementById("admin_sub_menu").style.display = 'block';
    document.getElementById("purchaser_sub_menu").style.display = 'none';
    document.getElementById("goods_receipts_sub_menu").style.display = 'none';
    document.getElementById("approvals_sub_menu").style.display = 'none';
    document.getElementById("content_management_sub_menu").style.display = 'none';
    document.getElementById("configuration_sub_menu").style.display = 'none';
    document.getElementById("time_sheet_sub_menu").style.display = 'none';
    document.getElementById("som_sub_menu").style.display = 'none';
    document.getElementById("shop_assist_sub_menu").style.display = 'none';
    document.getElementById("whatsapp_marketing_sub_menu").style.display = 'none';
}

function nav_bar_purchaser() {
    document.getElementById("shop_shop_plus_submenu").style.display = 'none';
    document.getElementById("user_settings_sub_menu").style.display = 'none';
    document.getElementById("admin_sub_menu").style.display = 'none';
    document.getElementById("purchaser_sub_menu").style.display = 'block';
    document.getElementById("goods_receipts_sub_menu").style.display = 'none';
    document.getElementById("approvals_sub_menu").style.display = 'none';
    document.getElementById("content_management_sub_menu").style.display = 'none';
    document.getElementById("configuration_sub_menu").style.display = 'none';
    document.getElementById("time_sheet_sub_menu").style.display = 'none';
    document.getElementById("som_sub_menu").style.display = 'none';
    document.getElementById("shop_assist_sub_menu").style.display = 'none';
    document.getElementById("whatsapp_marketing_sub_menu").style.display = 'none';
}
function nav_bar_approvals() {
    document.getElementById("shop_shop_plus_submenu").style.display = 'none';
    document.getElementById("user_settings_sub_menu").style.display = 'none';
    document.getElementById("admin_sub_menu").style.display = 'none';
    document.getElementById("purchaser_sub_menu").style.display = 'none';
    document.getElementById("goods_receipts_sub_menu").style.display = 'none';
    document.getElementById("approvals_sub_menu").style.display = 'block';
    document.getElementById("content_management_sub_menu").style.display = 'none';
    document.getElementById("configuration_sub_menu").style.display = 'none';
    document.getElementById("time_sheet_sub_menu").style.display = 'none';
    document.getElementById("som_sub_menu").style.display = 'none';
    document.getElementById("shop_assist_sub_menu").style.display = 'none';
    document.getElementById("whatsapp_marketing_sub_menu").style.display = 'none';
}

function nav_bar_content_management() {
    document.getElementById("shop_shop_plus_submenu").style.display = 'none';
    document.getElementById("user_settings_sub_menu").style.display = 'none';
    document.getElementById("admin_sub_menu").style.display = 'none';
    document.getElementById("purchaser_sub_menu").style.display = 'none';
    document.getElementById("goods_receipts_sub_menu").style.display = 'none';
    document.getElementById("approvals_sub_menu").style.display = 'none';
    document.getElementById("content_management_sub_menu").style.display = 'block';
    document.getElementById("configuration_sub_menu").style.display = 'none';
    document.getElementById("time_sheet_sub_menu").style.display = 'none';
    document.getElementById("som_sub_menu").style.display = 'none';
    document.getElementById("shop_assist_sub_menu").style.display = 'none';
    document.getElementById("whatsapp_marketing_sub_menu").style.display = 'none';
}

function nav_bar_configuration() {
    document.getElementById("shop_shop_plus_submenu").style.display = 'none';
    document.getElementById("user_settings_sub_menu").style.display = 'none';
    document.getElementById("admin_sub_menu").style.display = 'none';
    document.getElementById("purchaser_sub_menu").style.display = 'none';
    document.getElementById("goods_receipts_sub_menu").style.display = 'none';
    document.getElementById("approvals_sub_menu").style.display = 'none';
    document.getElementById("content_management_sub_menu").style.display = 'none';
    document.getElementById("time_sheet_sub_menu").style.display = 'none';
    document.getElementById("configuration_sub_menu").style.display = 'block';
    document.getElementById("som_sub_menu").style.display = 'none';
    document.getElementById("shop_assist_sub_menu").style.display = 'none';
    document.getElementById("whatsapp_marketing_sub_menu").style.display = 'none';
}
function nav_bar_timesheet() {
    document.getElementById("shop_shop_plus_submenu").style.display = 'none';
    document.getElementById("user_settings_sub_menu").style.display = 'none';
    document.getElementById("admin_sub_menu").style.display = 'none';
    document.getElementById("purchaser_sub_menu").style.display = 'none';
    document.getElementById("goods_receipts_sub_menu").style.display = 'none';
    document.getElementById("approvals_sub_menu").style.display = 'none';
    document.getElementById("content_management_sub_menu").style.display = 'none';
    document.getElementById("configuration_sub_menu").style.display = 'none';
    document.getElementById("user_settings_sub_menu").style.display = 'none';
    document.getElementById("time_sheet_sub_menu").style.display = 'block';
    document.getElementById("som_sub_menu").style.display = 'none';
    document.getElementById("shop_assist_sub_menu").style.display = 'none';
    document.getElementById("whatsapp_marketing_sub_menu").style.display = 'none';

}
function nav_bar_som() {
    document.getElementById("shop_shop_plus_submenu").style.display = 'none';
    document.getElementById("user_settings_sub_menu").style.display = 'none';
    document.getElementById("admin_sub_menu").style.display = 'none';
    document.getElementById("purchaser_sub_menu").style.display = 'none';
    document.getElementById("goods_receipts_sub_menu").style.display = 'none';
    document.getElementById("approvals_sub_menu").style.display = 'none';
    document.getElementById("content_management_sub_menu").style.display = 'none';
    document.getElementById("configuration_sub_menu").style.display = 'none';
    document.getElementById("user_settings_sub_menu").style.display = 'none';
    document.getElementById("time_sheet_sub_menu").style.display = 'none';
    document.getElementById("shop_assist_sub_menu").style.display = 'none';
    document.getElementById("som_sub_menu").style.display = 'block';
    document.getElementById("whatsapp_marketing_sub_menu").style.display = 'none';
}
function nav_bar_shop_assist() {
    document.getElementById("shop_shop_plus_submenu").style.display = 'none';
    document.getElementById("user_settings_sub_menu").style.display = 'none';
    document.getElementById("admin_sub_menu").style.display = 'none';
    document.getElementById("purchaser_sub_menu").style.display = 'none';
    document.getElementById("goods_receipts_sub_menu").style.display = 'none';
    document.getElementById("approvals_sub_menu").style.display = 'none';
    document.getElementById("content_management_sub_menu").style.display = 'none';
    document.getElementById("configuration_sub_menu").style.display = 'none';
    document.getElementById("user_settings_sub_menu").style.display = 'none';
    document.getElementById("time_sheet_sub_menu").style.display = 'none';
    document.getElementById("som_sub_menu").style.display = 'none';
    document.getElementById("shop_assist_sub_menu").style.display = 'block';
    document.getElementById("whatsapp_marketing_sub_menu").style.display = 'none';
}

function hide_nav_and_leftpanel(parent_url) {
    let url = parent_url.split('/')
    let is_edit = url.includes(window.sessionStorage.getItem('sc_header_guid'))
    if (is_edit) {
        document.getElementById('slide_menu').style.display = "none";
        $('#nav_menu_items').css('pointer-events', 'none');
        document.getElementById('sc_cart_counter').style.display = "none";
        let get_nav = document.getElementsByClassName("navbar_cnt")
    } else {
        $('#nav_menu_items').css('pointer-events', '');
    }
    return is_edit
}

// Function to clear session and local storage
function clear_session_data() {
    sessionStorage.clear();
    localStorage.clear();
}

function table_sort_filter_basic(class_name) {
    $('.' + class_name).DataTable();
}

// Datatables script to generate sort and filter feature for tables
function table_sort_filter(id_name) {
    $('#' + id_name).DataTable();
}

function table_sort_filter_popup(id_name) {
    $('#' + id_name).DataTable(
    {
        "scrollY": "280px",
        "scrollCollapse": true,
        "scrollX":false,
    });
}

// Temporary
function table_sort_filter_page(id_name) {
    $('#' + id_name).DataTable({
        "dom": '<"top"f>rt<"bottom"lip><"clear">'
    });
}

function table_sort_filter_popup_pagination(id_name){
    $('#' + id_name).DataTable({
        "dom": '<"top">rt<"bottom"lip><"clear">'
    });
}

// Datatables script to generate sort filter & export to excel feature for tables
function table_sort_filter_export_excel() {
    $('.table_sort_filter_export_excel').DataTable({
        dom: '<"row"<"col"l><"datatableBtn col"fB>> rt <"row"<"col"i><"col"p>>',
        buttons: [
            {
                extend: 'excel',
                title: 'Data export',
                text: 'Export to Excel',
            },
        ],
    });
}

function table_sort_filter_catalog(id_name) {
    setTimeout(function() {
        $('#' + id_name).DataTable({
            "scrollY": "23rem"
        });
    }, 500);
    
}



function application_settings_delete_Row(myTable) {
    try {
        var table = document.getElementById(myTable);
        var rowCount = table.rows.length;

        for (var i = 0; i < rowCount; i++) {
            var row = table.rows[i];
            var chkbox = row.cells[0].childNodes[0];
            if (null != chkbox && true == chkbox.checked) {

                table.deleteRow(i);
                rowCount--;
                i--;
            }
        }
        return rowCount;
    } catch (e) {
        alert(e);
    }
}


function scroll_top() {
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
}

const remove_special_characters = (internal_note, supplier_note, item_number) => {
    internal_note = check_for_special_char(internal_note)
    supplier_note = check_for_special_char(supplier_note)
    if (!internal_note){
        if(!internal_supplier_error_itemNumber.includes(item_number)){
            internal_supplier_error_itemNumber.push(item_number)
        }
    }
    if (!supplier_note){
        if(!internal_supplier_error_itemNumber.includes(item_number)){
            internal_supplier_error_itemNumber.push(item_number) 
        }
    }
}

const no_slide_menu_style = () => {
    navOuter = document.getElementById('navOuter')
    navOuter.style.removeProperty('margin-left')
    navOuter.style.removeProperty('transition')
    main_div = document.getElementById('main_div')
    main_div.style.removeProperty('margin-left')
    main_div.style.removeProperty('transition')
    document.getElementById('slide_menu').style.display = "none";
    //$('#nav_menu_items').css('pointer-events', 'none');
    document.getElementById('my_order_btn').style.display = "none";

}

const open_close_document_detail = (type) => {

    if(type == 'YES'){
        $('#confirm_add_item').modal('hide')
    } else {
        get_document_url = localStorage.getItem('opened_document-' + document_number)
        location.href = get_document_url + '/edit'
    }
}

// $('input').on('keypress', function (event) {
//     var regex = new RegExp("^[a-zA-Z0-9]+$");
//     var key = String.fromCharCode(!event.charCode ? event.which : event.charCode);
//     if (!regex.test(key)) {
//         event.preventDefault();
//         return false;
//     }
// });

// Function to apply table-striped
const item_table_css = () => {
    let table_rows = document.getElementsByClassName("item-table-striped")
    for (let i = 0; i < table_rows.length; i++) {
        if (i%2==0) {
                let currentRows=table_rows[i]
                $( table_rows[i]).children().css( "background-color", "#FFFFFF" );
        }else{
            $( table_rows[i]).children().css( "background-color", "#F2F2F2" );
        }
    }
}

//// Ajax call function for submitting formdata
//function FormAjaxCallAPI(urlLink,data)
//{
//     console.log(urlLink)
//   {
//        jQuery.ajax({
//            async : false,
//            type: 'POST',
//            url: urlLink,
//            contentType: "application/json; charset=utf-8",
//            data: data,
//            success: function(result){
//                response = result;
//            },
//            error: function(xhr, resp, text) {
//            },
//			cache: false,
//			processData: false,
//			contentType: false,
//
//        });
//    }
//    return response;
//};
//
//
//function AjaxCallAPI(urlLink, data){
//    jQuery.ajax({
//        async : false,
//        type: 'POST',
//        url: urlLink,
//        dataType :'json',
//        data: JSON.stringify(data),
//        success: function(result){
//            response = result;
//        },
//        error: function(xhr, resp, text) {
//        },
//        cache: false,
//        processData: false,
//        contentType: false,
//
//    });
//    return response;
//};

function hide_notif_add_to_cart(){
    $("#notification_icon_div_id").css("display", "none");
    $("#add_to_cart_div_id").css("display", "none");
}
function show_notif_add_to_cart(){
    $("#notification_icon_div_id").css("display", "block");
    $("#add_to_cart_div_id").css("display", "block");
}


// Function to display or hide sub menu cards in configuration settings app 
function display_sub_menu(id) {
    var x = document.getElementById("upload-configuration-data");
    var y = document.getElementById(id)
    if (x.style.display === "none") {
      x.style.display = "block";
      y.style.display = "none";
    } else {
      x.style.display = "none";
      y.style.display = "block";
    }
}


// Function to display Description based on element Id
function message_type_check(id, description){
                $('#'+id).html(description);
                $('#'+id).css("display", "block");
                $('#myModal').modal('show');

}
// Function to display Description based on element Id for UI messages
function display_message_UI(id, description, str){
                $('#'+id).html(description + str);
                $('#'+id).show();

}

// Function to toggle between sub menu tabs
function NavigateTabs() {
    const tabs = document.querySelectorAll('[data-tab-target]')
    const tabContents = document.querySelectorAll('[data-tab-content]')
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const target = document.querySelector(tab.dataset.tabTarget)
            tabContents.forEach(tabcontent => {
                tabcontent.classList.remove('active')
            });
            tabs.forEach(tab => {
                tab.classList.remove('active')
            });
            tab.classList.add('active');
            target.classList.add('active');
        })
    })
}


function regex_char_restriction(event){
    var regex = new RegExp("^[A-Za-z0-9? ,_-()]+$");
    var key = String.fromCharCode(!event.charCode ? event.which : event.charCode);
    if (!regex.test(key)) {
        event.preventDefault();
        return false;
    }
}

// Function to display Description based on element Id
function display_message(id, description){
                $('#'+id).html(description);
                $('#'+id).css("display", "block");
                $('#id_save_confirm_popup').modal('hide');
                $('#myModal').modal('show');

}


function validateAddressField(string) {
    if (/^[a-zA-Z0-9_@./#&+-, ]*$/.test(string) == false) {
        return false
    } else {
        return true;
    }
}
function test(){
    alert("function called");
}

function message_display_time(){
    if ($('.alert-success').is(":hidden")) {
      $('.alert-success').prop("hidden", false);
      setTimeout(function() {
                    $('.alert-success').prop("hidden", true);
     }, msg_display_interval*1000);
    } else {
    $('.alert-success').prop("hidden", true);
    }
    $('.check_success_message').prop("hidden", true);
}
function message_display_time_specific(){
      setTimeout(function() {
                    $('.msg-display-class').prop("hidden", true);
     }, msg_display_interval*1000);
}

//validate by comparing  main table values and popup table values
function maintable_validation(validate_add_attributes, main_table_low_value) {
    var no_duplicate_entries = 'Y'
    var error_message =''
    var common = [];
    jQuery.grep(validate_add_attributes, function(el) {
        if (jQuery.inArray(el, main_table_low_value) != -1) {
            common.push(el);
        }
    });
    if (common.length != 0) {
         display_duplicate_entry(common);  //Function to highlight the rows in popup
         error_message = ui_messeges("JMSG001")
         no_duplicate_value = 'N'
         return [no_duplicate_value,error_message]
    }
    return [no_duplicate_entries,error_message]
}
// Function to fetch ui messages from backend
function ui_messeges(messages_id){
     $.each(messages_list, function (i, item){
        if (item.messages_id == messages_id){
            error_message = item.messages_id_desc
            return error_message
        }
     });
       return error_message
}

function row_color_highlight(row){                  //for duplicate entries
     $(row).css('background-color', '#ff6633');
}
function row_color_highlight_special(row){              //for special entries
     $(row).css('background-color', '#FFCCCB');
}
function row_color_highlight_empty(row){                //for empty entries
     $(row).css('background-color', '#FFB6C1');
}
function row_color_highlight_minlength(row){
    $(row).css('background-color', '#FFCCCB');        //for minimum
}
function row_color_no_highlight(row){                 //not highlighting
     $(row).css('background-color', '');
}

// Function to get all the checkboxes from main table
function get_all_checkboxes(){
    var table = $('#display_basic_table').DataTable();
    var $table = table.table().node();
    var res = table.rows().nodes();
    return res;
}

function format(date) {
  date = new Date(date);
  var day = ('0' + date.getDate()).slice(-2);
  var month = ('0' + (date.getMonth() + 1)).slice(-2);
  var year = date.getFullYear();
  return day + '-' + month + '-' + year;
}
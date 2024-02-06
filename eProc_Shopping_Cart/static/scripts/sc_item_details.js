// display shop role sub menu in nav bar
nav_bar_shop()

// Function to hide and display limit order details in 1st step of shopping cart wizard
$(document).ready(function(){
    $("#display_limit_item").click(function(){
      $("#limit_order_detail_section").toggle();
    });
});

var item_call_off = ''
var item_guid_number = ''
var item_eform = ''
var item_number = ''
var is_edit = false;
var internal_supplier_error_itemNumber = []

// Function to display and hide More button on "check" of checkbox for freetext and limitorder item
// On "un-check" hide More button & item details section
// const checkbox_onchange = (element) => {
//     item_call_off = ''
//     item_guid_number = ''
//     item_eform = ''
//     item_number = ''
//     if($(element).prop("checked") == true){
//         check_box_id = element.id.split('-')
//         item_call_off = check_box_id[1]
//         item_guid_number = check_box_id[2]
//         item_eform = check_box_id[3]
//         item_number = check_box_id[4]
//         eform_id = check_box_id[5]

//         // if limit order item
//         if(item_call_off === 'Limit'){
//             item_guid_number = item_guid_number;
//             document.getElementById('display_limit_item').style.display = 'inline-block';
//         } else {
//             document.getElementById('display_limit_item').style.display = 'none';
//         }

//         // if freetext item
//         if(item_eform != '' || eform_id != ''){
//             document.getElementById('display_eform').style.display = 'inline-block';
//         } else {
//             document.getElementById('display_eform').style.display = 'none'
//         }

//     } else if($(element).prop("checked") == false){
//         check_box_id = element.id.split('-')
//         item_call_off = check_box_id[1]
//         item_guid_number = check_box_id[2]
//         item_eform = check_box_id[3]
//         item_number = check_box_id[4]

//         // if limit order item
//         if(item_call_off === 'Limit'){
//             document.getElementById('display_limit_item').style.display = 'none';
//             document.getElementById('limit_order_detail_section').style.display = 'none'
//         }

//         // if freetext item
//         if(item_eform != '' || eform_id != ''){
//             document.getElementById('display_eform').style.display = 'none'
//             document.getElementById("display_eform_"+item_guid_number).style.display="none"
//             $('#item_info_tr-'+item_number).prop('hidden', true);
//         }
        
//     }
// }




$("input:checkbox").on('click', function() {
    var $box = $(this);

    if ($box.is(":checked")) {
        var group = "input:checkbox[name='" + $box.attr("name") + "']";
        $(group).prop("checked", false);
        $box.prop("checked", true);
        } else {
        $box.prop("checked", false);
    }
});


var my_order_doc_detail = '';

document.getElementById("total_items").innerHTML = document.getElementById("cart_counter").innerHTML

var edit_account_assignment_cat = '';
function edit_account_assign(edit_account_assignment_cat_button){
    edit_account_assignment_cat = edit_account_assignment_cat_button.split('-')[2]
    changeAccCat(edit_account_assignment_cat_button)
}

var change_address_item_num = '';
var edit_address_item_num = '';
function change_item_address(change_item_address_button) {
    $('#ChngShipAddr').modal('show');
    change_address_item_num = change_item_address_button.split('_')[2]
}

function edit_item_address(edit_item_address_button) {
    $('#EditShipAddr').modal('show');
    edit_address_item_num = edit_item_address_button.split('_')[2]
    shippingAddress()
}


//################################## START SHOW IMAGE  #################################################################
function show_image_div(){
    $(".catalog_img").hide();
    $(".catalog_img:eq(" + image_visible_div + ")").show();

}
//################################## END SHOW IMAGE  #################################################################



// Function to hide and show hidden table row contents
function showSection(obj, data) {
    item_number = data.split('-')[1]
    GLOBAL_SELECT_ITEM_NUM = item_number
    document.getElementById('item_info_tr-'+item_number).hidden = false;
    if(data.includes('attachments')){
        $('#attachment_tbody_id-'+item_number).empty()
        get_attachment_IDB(item_number)
    }
    var showsectionid=obj.id;
    var dropdownContentClass = data;
    var rowId = document.getElementById(dropdownContentClass);
    var rowClass = rowId.className;
    var hideableRowSection = document.getElementsByClassName(rowClass);

    for (var i=0; i < hideableRowSection.length; i++){
        var current_element = hideableRowSection[i].id
        if(current_element == dropdownContentClass){
            hideableRowSection[i].style.display = 'block';
        } else{
            hideableRowSection[i].style.display = 'none';
        }
    }
}


// Function to toggle note type textarea
function selectNoteType(data) {
    var getNotebtnClass1 = data.className.split(" ")[0]
    var getNotebtnClass2 = data.className.split(" ")[1]
    var activeNoteBtn = document.getElementsByClassName(getNotebtnClass1);
    var noteBtnId = data.id
    var textareaId = document.getElementById(getNotebtnClass2);
    var textareaClass = textareaId.className;
    var hideableNoteText = document.getElementsByClassName(textareaClass);


    for (var i = 0; i < hideableNoteText.length; i++) {
        var current_element = hideableNoteText[i].id
        if (current_element == getNotebtnClass2) {
            hideableNoteText[i].style.display = 'block';
        } else {
            hideableNoteText[i].style.display = 'none';
        }
    }

    for(var i=0; i < activeNoteBtn.length; i++){
        var current_button = activeNoteBtn[i].id
        if (current_button==noteBtnId){
            activeNoteBtn[i].style.backgroundColor = '#007bff';
            activeNoteBtn[i].style.color = '#ffffff';
        } else{
            activeNoteBtn[i].style.backgroundColor = '#dbdad9';
            activeNoteBtn[i].style.color = '#000000';
        }
    }

}

// Functo to close 
function closeSelectSection(obj, data) {
    item_number = data.substr(-1)
    var x = data;
    document.getElementById(x).style.display="none"
    document.getElementById('item_info_tr-'+item_number).hidden = true;
}

// Restrict user to enter special characters in add internal and supplier note
$('textarea').on('keypress', function (event) {
    var regex = new RegExp("^[A-Za-z0-9? ,_-()]+$");
    var key = String.fromCharCode(!event.charCode ? event.which : event.charCode);
    if (!regex.test(key)) {
        event.preventDefault();
        return false;
    }
});


// Function to delete an item from the cart and update in the UI using ajax call
// function delete_cart_item(){
//     guid = delete_item_guid
//     data = {};
//     data.guid = guid;
//     $('#sc-delete-single-item').modal('hide');

//     var delete_cart_item_result = ajax_delete_cart_item(data);

//     if(delete_cart_item_result) {
//         // Updating total value after deleting an item
//         if_item_value = $("#item_value_"+guid);
//         if(if_item_value.length > 0){
//             total_value    = document.getElementById("total_cart_value").innerHTML
//             item_value     = document.getElementById("item_value_"+guid).innerHTML
//             up_total_value = parseFloat(total_value) - parseFloat(item_value)
//             document.getElementById("total_cart_value").innerHTML = up_total_value
//         }

//         // Updates cart counter after deleting
//         document.getElementById("total_items").innerHTML  = response.message
//         document.getElementById("cart_counter").innerHTML = response.message
//         // If there are no items in cart redirect to home page
//         if (response.message == 0){
//             window.location.href = "{% url 'eProc_Shop_Home:shopping_cart_home' %}"
//         } else {
//             var row = document.getElementById('row_id_'+ guid);
//             row.parentNode.removeChild(row);
//         }
//         // Updating of items left after deleting an item
//         item_number_class = document.getElementsByClassName('update_item_number')
//         for(let item_number = 0; item_number < item_number_class.length; item_number++) {
//             item_number_class[item_number].innerHTML = item_number + 1
//         }
//     }
// }


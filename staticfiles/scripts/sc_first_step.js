// display shop role sub menu in nav bar
nav_bar_shop()

$(document).ready(function(){
    $('#sc-proceed-checkout').click(function () {
        OpenLoaderPopup();
    });

    $('body').css('padding-top', '7rem');
});

// Function to add favourite cart items
$('#add_favourite_cart').submit(function (e){
    e.preventDefault();
    $('#fav_name_error_message').html('');
    $('#fav_name_error_message').hide();
    $('#fav_name_success_message').html('');
    $('#fav_name_success_message').hide();
    favourite_sc_data = {}; 
    favourite_sc_data.total_cart_value = $('#total_cart_value').html();
    favourite_sc_data.total_cart_currency = $('#total_cart_currency').html();
    favourite_sc_data.favourite_cart_name = $('#favourite_sc_name_input').val();
    favourite_sc_data.csrfmiddlewaretoken = $('input[name=csrfmiddlewaretoken]').val()
    var fsc_result = ajax_add_favourite_cart(favourite_sc_data); 

    if(fsc_result) {
        if(response.success_message){
            $('#fav_name_success_message').html(response.success_message);
            $('#fav_name_success_message').show();
            $("#favourite_sc_button").find('.material-icons').html("favorite").css("color", "red");
        } else if (response.error_message) {
            $('#fav_name_error_message').html(response.error_message);
            $('#fav_name_error_message').show();
        }
    }

});

function onclick_fav_sc(){
    $('#fav_name_success_message').empty();
    $('#fav_name_error_message').empty();
     $('#fav_name_success_message').hide();
     $('#fav_name_error_message').hide();
     $('#favourite_sc_name_input').val('');

}


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

function closeSelectSection(obj, data) {
    item_number = data.substr(-1)
    var x = data;
    document.getElementById(x).style.display="none"
    document.getElementById('item_info_tr-'+item_number).hidden = true;
}
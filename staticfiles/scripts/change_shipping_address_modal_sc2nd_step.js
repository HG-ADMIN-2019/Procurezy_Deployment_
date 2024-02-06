// datatable plugin for change shipping address pop-up
$(document).ready( function () {
    $('.mydatatable').DataTable({
        "ordering": false,
        "scrollY": "320px",
        "scrollCollapse": true,
    });
} );

// Function to display edited shipping address in Shipping details section
function submitAddress() {
    $('#edit_address_error_div').html('')
    $('#edit_address_error_div').hide()
    street_output_id = 'street_output'
    area_output_id = 'area_output'
    landmark_output_id = 'landmark_output'
    city_output_id = 'city_output'
    pcode_output_id = 'pcode_output'
    region_output_id = 'region_output'
    is_special_character = false;
    

    special_character_class = document.getElementsByClassName('hg_special_character')
    for (i = 0; i < special_character_class.length; i++) {
        value = special_character_class[i].value
        check_value = validateAddressField(value)
        if (!check_value) {
            is_special_character = true
        }
    }

    if (is_special_character) {
       var url_new = "{% url 'eProc_Basic:get_message_description' %}";
                var msg = "JMSG003";
                var msg_type ;
              msg_type = message_config_details(msg);
              $("#error_msg_id").prop("hidden", false)

              if(msg_type.message_type == "ERROR"){
                    display_message("error_msg_id", msg_type.messages_id_desc)
              }
              else if(msg_type.message_type == "WARNING"){
                 display_message("id_warning_msg_id", msg_type.messages_id_desc)
              }
              else if(msg_type.message_type == "INFORMATION"){
                 display_message("id_info_msg_id", msg_type.messages_id_desc)
              }
              var display4 = msg_type.messages_id_desc;
              $('#edit_address_error_div').html(display4 + "Address fields" )

        $('#edit_address_error_div').show()
        return
    }

    if (edit_address_item_num != '') {
        street_output_id += edit_address_item_num
        area_output_id += edit_address_item_num
        landmark_output_id += edit_address_item_num
        city_output_id += edit_address_item_num
        pcode_output_id += edit_address_item_num
        region_output_id += edit_address_item_num
        $('#shippingAddress_added-'+edit_address_item_num).prop("hidden", false);
        $('#shipping_address_info').css("display", "block");
    }

    if (edit_address_item_num == '') {
        for (i = 0; i < cart_length; i++) {
            incremented_id = i + 1
            document.getElementById(street_output_id + incremented_id).innerHTML = document.getElementById('street_input').value
            document.getElementById(area_output_id + incremented_id).innerHTML = document.getElementById('area_input').value
            document.getElementById(landmark_output_id + incremented_id).innerHTML = document.getElementById('landmark_input').value
            document.getElementById(city_output_id + incremented_id).innerHTML = document.getElementById('city_input').value
            document.getElementById(pcode_output_id + incremented_id).innerHTML = document.getElementById('pcode_input').value
            document.getElementById(region_output_id + incremented_id).innerHTML = document.getElementById('region_input').value
            $('#shippingAddress_added-'+incremented_id).prop("hidden", true);
            $('#shipping_address_info').css("display", "none");
        }
        
    }
    document.getElementById(street_output_id).innerHTML = document.getElementById('street_input').value
    document.getElementById(area_output_id).innerHTML = document.getElementById('area_input').value
    document.getElementById(landmark_output_id).innerHTML = document.getElementById('landmark_input').value
    document.getElementById(city_output_id).innerHTML = document.getElementById('city_input').value
    document.getElementById(pcode_output_id).innerHTML = document.getElementById('pcode_input').value
    document.getElementById(region_output_id).innerHTML = document.getElementById('region_input').value
    $('#EditShipAddr').modal('hide');

    edit_address_item_num = ''
}

// Function to display edited shipping address in Shipping details section
function select_address(address_id) {
    var id = address_id;
    var split_id = id.split("-");
    var address_index = split_id[1];

    address_numb = document.getElementById('addr_num-' + address_index).innerHTML;
    street = document.getElementById('street-' + address_index).innerHTML;
    area = document.getElementById('area-' + address_index).innerHTML;
    landmark = document.getElementById('landmark-' + address_index).innerHTML;
    city = document.getElementById('city-' + address_index).innerHTML;
    postalcode = document.getElementById('postal_code-' + address_index).innerHTML;
    region = document.getElementById('region-' + address_index).innerHTML;

    var address_number_id = 'address_number';
    var street_output_id = 'street_output';
    var area_output_id = 'area_output';
    var landmark_output_id = 'landmark_output';
    var city_output_id = 'city_output';
    var pcode_output_id = 'pcode_output';
    var region_output_id = 'region_output';

    var header_level_address_number = $('#address_number').html();

    if (change_address_item_num != '') {
        address_number_id += '_' + change_address_item_num;
        street_output_id += change_address_item_num;
        area_output_id += change_address_item_num;
        landmark_output_id += change_address_item_num;
        city_output_id += change_address_item_num;
        pcode_output_id += change_address_item_num;
        region_output_id += change_address_item_num;

        document.getElementById(address_number_id).innerHTML = address_numb;
        document.getElementById(street_output_id).innerHTML = street;
        document.getElementById(area_output_id).innerHTML = area;
        document.getElementById(landmark_output_id).innerHTML = landmark;
        document.getElementById(city_output_id).innerHTML = city;
        document.getElementById(pcode_output_id).innerHTML = postalcode;
        document.getElementById(region_output_id).innerHTML = region;
        
        var item_level_address_number = $('#'+address_number_id).html();
        if(item_level_address_number == header_level_address_number){
            $('#shippingAddress_added-'+change_address_item_num).prop("hidden", true);
            $('#shipping_address_info').css("display", "none");
        } else {
            $('#shippingAddress_added-'+change_address_item_num).prop("hidden", false);
            $('#shipping_address_info').css("display", "block");
        }
        change_address_item_num = '';
    } else if (change_address_item_num == '') {
        $('#address_number').html(address_numb)
        for (i = 0; i < cart_length; i++) {
            incremented_id = i + 1
            document.getElementById(address_number_id + '_' + incremented_id).innerHTML = address_numb;
            document.getElementById(street_output_id + incremented_id).innerHTML = street;
            document.getElementById(area_output_id + incremented_id).innerHTML = area;
            document.getElementById(landmark_output_id + incremented_id).innerHTML = landmark;
            document.getElementById(city_output_id + incremented_id).innerHTML = city;
            document.getElementById(pcode_output_id + incremented_id).innerHTML = postalcode;
            document.getElementById(region_output_id + incremented_id).innerHTML = region;
            $('#shippingAddress_added-'+incremented_id).prop("hidden", true);
            $('#shipping_address_info').css("display", "none");
        }
        document.getElementById(address_number_id).innerHTML = address_numb;
        document.getElementById(street_output_id).innerHTML = street
        document.getElementById(area_output_id).innerHTML = area
        document.getElementById(landmark_output_id).innerHTML =landmark
        document.getElementById(city_output_id).innerHTML = city
        document.getElementById(pcode_output_id).innerHTML = postalcode
        document.getElementById(region_output_id).innerHTML = region
    }
    $('#ChngShipAddr').modal('hide');
}


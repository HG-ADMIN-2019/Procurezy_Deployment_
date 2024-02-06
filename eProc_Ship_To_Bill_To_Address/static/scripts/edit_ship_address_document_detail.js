// Function to display edit shipping address pop-up in sc second step
function shippingAddress() {
    $('#EditShipAddr').modal('show')

    // street_output_id = 'ScAddresses-street-'
    // area_output_id = 'ScAddresses-area-'
    // landmark_output_id = 'ScAddresses-landmark-'
    // city_output_id = 'ScAddresses-city-'
    // pcode_output_id = 'ScAddresses-postal_code-'
    // region_output_id = 'ScAddresses-region-'

    if (edit_address_item_num == '') {
        var street = document.getElementById('ScAddresses-street-' + GLOBAL_HEADER_LEVEL_ADDR_GUID).innerHTML;
        var area = document.getElementById('ScAddresses-area-' + GLOBAL_HEADER_LEVEL_ADDR_GUID).innerHTML;
        var landmark = document.getElementById('ScAddresses-landmark-' + GLOBAL_HEADER_LEVEL_ADDR_GUID).innerHTML;
        var city = document.getElementById('ScAddresses-city-' + GLOBAL_HEADER_LEVEL_ADDR_GUID).innerHTML;
        var pcode = document.getElementById('ScAddresses-postal_code-' + GLOBAL_HEADER_LEVEL_ADDR_GUID).innerHTML;
        var region = document.getElementById('ScAddresses-region-' + GLOBAL_HEADER_LEVEL_ADDR_GUID).innerHTML;    
    } else if (edit_address_item_num != '') {
        var street = document.getElementById('ScAddresses-street-' + rendered_addr_guid[edit_address_item_num - 1]).innerHTML;
        var area = document.getElementById('ScAddresses-area-' + rendered_addr_guid[edit_address_item_num - 1]).innerHTML;
        var landmark = document.getElementById('ScAddresses-landmark-' + rendered_addr_guid[edit_address_item_num - 1]).innerHTML;
        var city = document.getElementById('ScAddresses-city-' + rendered_addr_guid[edit_address_item_num - 1]).innerHTML;
        var pcode = document.getElementById('ScAddresses-postal_code-' + rendered_addr_guid[edit_address_item_num - 1]).innerHTML;
        var region = document.getElementById('ScAddresses-region-' + rendered_addr_guid[edit_address_item_num - 1]).innerHTML;    
    }

    document.getElementById('street_input').value = street
    document.getElementById('area_input').value = area
    document.getElementById('landmark_input').value = landmark
    document.getElementById('city_input').value = city
    document.getElementById('pcode_input').value = pcode
    document.getElementById('region_input').value = region
}

// Function to display edited shipping address in Shipping details section
function submitAddress() {

    is_special_character = false;

    special_character_class = document.getElementsByClassName('hg_special_character');
    for (i = 0; i < special_character_class.length; i++) {
        value = special_character_class[i].value;
        check_value = validateAddressField(value);
        if (!check_value) {
            is_special_character = true;
        }
    }

    if (is_special_character) {
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
 

    var get_item_guid =  get_item_guid_edit(edit_row_index);

    street_output_id = 'ScAddresses-street-'
    area_output_id = 'ScAddresses-area-'
    landmark_output_id = 'ScAddresses-landmark-'
    city_output_id = 'ScAddresses-city-'
    pcode_output_id = 'ScAddresses-postal_code-'
    region_output_id = 'ScAddresses-region-'
    // remove on change class for Sc address popup
    $("#street_input").removeClass("sc_field_change")
    $("#area_input").removeClass("sc_field_change")
    $("#landmark_input").removeClass("sc_field_change")
    $("#city_input").removeClass("sc_field_change")
    $("#pcode_input").removeClass("sc_field_change")
    $("#region_input").removeClass("sc_field_change")

    // Update Item level address change on pop up
    if (edit_address_item_num != '') {
        document.getElementById(street_output_id + rendered_addr_guid[edit_address_item_num - 1]).innerHTML = document.getElementById('street_input').value
        document.getElementById(area_output_id + rendered_addr_guid[edit_address_item_num - 1]).innerHTML = document.getElementById('area_input').value
        document.getElementById(landmark_output_id + rendered_addr_guid[edit_address_item_num - 1]).innerHTML = document.getElementById('landmark_input').value
        document.getElementById(city_output_id + rendered_addr_guid[edit_address_item_num - 1]).innerHTML = document.getElementById('city_input').value
        document.getElementById(pcode_output_id + rendered_addr_guid[edit_address_item_num - 1]).innerHTML = document.getElementById('pcode_input').value
        document.getElementById(region_output_id + rendered_addr_guid[edit_address_item_num - 1]).innerHTML = document.getElementById('region_input').value


        // add on change class to Sc Item level addr updated field
        $('#' + street_output_id + rendered_addr_guid[edit_address_item_num - 1]).addClass("sc_field_change")
        $('#' + area_output_id + rendered_addr_guid[edit_address_item_num - 1]).addClass("sc_field_change")
        $('#' + landmark_output_id + rendered_addr_guid[edit_address_item_num - 1]).addClass("sc_field_change")
        $('#' + city_output_id + rendered_addr_guid[edit_address_item_num - 1]).addClass("sc_field_change")
        $('#' + pcode_output_id + rendered_addr_guid[edit_address_item_num - 1]).addClass("sc_field_change")
        $('#' + region_output_id + rendered_addr_guid[edit_address_item_num - 1]).addClass("sc_field_change")

        $('#shippingAddress_added-'+get_item_guid).css("display", "block");

    }
    // on edit in header level address, update item level and header level  address
    else if (edit_address_item_num == '') {
        document.getElementById(street_output_id + GLOBAL_HEADER_LEVEL_ADDR_GUID).innerHTML = document.getElementById('street_input').value
        document.getElementById(area_output_id + GLOBAL_HEADER_LEVEL_ADDR_GUID).innerHTML = document.getElementById('area_input').value
        document.getElementById(landmark_output_id + GLOBAL_HEADER_LEVEL_ADDR_GUID).innerHTML = document.getElementById('landmark_input').value
        document.getElementById(city_output_id + GLOBAL_HEADER_LEVEL_ADDR_GUID).innerHTML = document.getElementById('city_input').value
        document.getElementById(pcode_output_id + GLOBAL_HEADER_LEVEL_ADDR_GUID).innerHTML = document.getElementById('pcode_input').value
        document.getElementById(region_output_id + GLOBAL_HEADER_LEVEL_ADDR_GUID).innerHTML = document.getElementById('region_input').value

        // add on change class to Sc Header level addr updated field
        $('#' + street_output_id + GLOBAL_HEADER_LEVEL_ADDR_GUID).addClass("sc_field_change")
        $('#' + area_output_id + GLOBAL_HEADER_LEVEL_ADDR_GUID).addClass("sc_field_change")
        $('#' + landmark_output_id + GLOBAL_HEADER_LEVEL_ADDR_GUID).addClass("sc_field_change")
        $('#' + city_output_id + GLOBAL_HEADER_LEVEL_ADDR_GUID).addClass("sc_field_change")
        $('#' + pcode_output_id + GLOBAL_HEADER_LEVEL_ADDR_GUID).addClass("sc_field_change")
        $('#' + region_output_id + GLOBAL_HEADER_LEVEL_ADDR_GUID).addClass("sc_field_change")

        for (i = 0; i < cart_length; i++) {
            incremented_id = i + 1
            document.getElementById(street_output_id + rendered_addr_guid[i]).innerHTML = document.getElementById('street_input').value
            document.getElementById(area_output_id + rendered_addr_guid[i]).innerHTML = document.getElementById('area_input').value
            document.getElementById(landmark_output_id + rendered_addr_guid[i]).innerHTML = document.getElementById('landmark_input').value
            document.getElementById(city_output_id + rendered_addr_guid[i]).innerHTML = document.getElementById('city_input').value
            document.getElementById(pcode_output_id + rendered_addr_guid[i]).innerHTML = document.getElementById('pcode_input').value
            document.getElementById(region_output_id + rendered_addr_guid[i]).innerHTML = document.getElementById('region_input').value

            // add on change class to Sc Item level addr updated field
            $('#' + street_output_id + rendered_addr_guid[edit_address_item_num - 1]).addClass("sc_field_change")
            $('#' + area_output_id + rendered_addr_guid[edit_address_item_num - 1]).addClass("sc_field_change")
            $('#' + landmark_output_id + rendered_addr_guid[edit_address_item_num - 1]).addClass("sc_field_change")
            $('#' + city_output_id + rendered_addr_guid[edit_address_item_num - 1]).addClass("sc_field_change")
            $('#' + pcode_output_id + rendered_addr_guid[edit_address_item_num - 1]).addClass("sc_field_change")
            $('#' + region_output_id + rendered_addr_guid[edit_address_item_num - 1]).addClass("sc_field_change")

        }

        $('#shippingAddress_added-'+get_item_guid).css("display", "none");
    }
    $('#EditShipAddr').modal('hide')
    edit_address_item_num = ''
}
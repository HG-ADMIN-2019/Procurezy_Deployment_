// Function to display edit shipping address pop-up in sc second step
function shippingAddress() {
    street_output_id = 'street_output'
    area_output_id = 'area_output'
    landmark_output_id = 'landmark_output'
    city_output_id = 'city_output'
    pcode_output_id = 'pcode_output'
    region_output_id = 'region_output'
    if (edit_address_item_num != '') {
        street_output_id += edit_address_item_num
        area_output_id += edit_address_item_num
        landmark_output_id += edit_address_item_num
        city_output_id += edit_address_item_num
        pcode_output_id += edit_address_item_num
        region_output_id += edit_address_item_num
    }

    $('#EditShipAddr').modal('show');
    document.getElementById('street_input').value = document.getElementById(street_output_id).innerHTML
    document.getElementById('area_input').value = document.getElementById(area_output_id).innerHTML
    document.getElementById('landmark_input').value = document.getElementById(landmark_output_id).innerHTML
    document.getElementById('city_input').value = document.getElementById(city_output_id).innerHTML
    document.getElementById('pcode_input').value = document.getElementById(pcode_output_id).innerHTML
    document.getElementById('region_input').value = document.getElementById(region_output_id).innerHTML
}

$('.hg_edit_address').bind('input', function () {
    if (edit_address_item_num == '') {
        for (i = 0; i < cart_length; i++) {
            incremented_id = i + 1
            $('#address_number_' + incremented_id).html('')
        }
    } else {
        $('#address_number_' + edit_address_item_num).html('')
    }
});
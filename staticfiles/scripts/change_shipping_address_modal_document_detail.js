// datatable plugin for change shipping address pop-up
$(document).ready( function () {
    $('.mydatatable').DataTable({
        "ordering": false,
        "scrollY": "320px",
        "scrollCollapse": true,
    });
} );

// global var : stores the address id of the changed address at item level 
var changed_item_level_address_id = '';

function select_address(address_id) {
    get_count = $('[id^="ScAddresses-street-"]');
    address_guid_at_header = '';
    address_guid_at_item = '';

    if (change_address_item_num === '') {
        for (i = 0; i < get_count.length; i++) {
            if (i === 0) {
                address_guid_at_header = get_count[i].id.split('-')[2];
                update_address_data(address_id, address_guid_at_header);
            } else {
                address_guid_at_item = get_count[i].id.split('-')[2];
                update_address_data(address_id, address_guid_at_item);
            }
        }
    } else {
        update_address_data(address_id, change_address_item_num);
        var get_item_guid =  get_item_guid_edit(edit_row_index);
        var header_level_address_number = $('#ScAddresses-address_number-' + GLOBAL_HEADER_LEVEL_ADDR_GUID).html();
    
        if(changed_item_level_address_id == header_level_address_number){
            $('#shippingAddress_added-'+get_item_guid).css("display", "none");
        } else {
            $('#shippingAddress_added-'+get_item_guid).css("display", "block");
        }
    }
    change_address_item_num = '';
    $('.modal').modal('hide');
}

const update_address_data = (address_id, address_guid) => {
    
    address = address_id.split('-')[1]
    address_number_element = document.getElementById('ScAddresses-address_number-' + address_guid)
    street_element = document.getElementById('ScAddresses-street-' + address_guid)
    area_element = document.getElementById('ScAddresses-area-' + address_guid)
    landmark_element = document.getElementById('ScAddresses-landmark-' + address_guid)
    city_element = document.getElementById('ScAddresses-city-' + address_guid)
    region_element = document.getElementById('ScAddresses-region-' + address_guid)
    postal_code_element = document.getElementById('ScAddresses-postal_code-' + address_guid)

    address_number_element.innerHTML = $('#addr_num-' + address).html()
    street_element.innerHTML = $('#street-' + address).html()
    area_element.innerHTML = $('#area-' + address).html()
    landmark_element.innerHTML = $('#landmark-' + address).html()
    city_element.innerHTML = $('#city-' + address).html()
    region_element.innerHTML = $('#region-' + address).html()
    postal_code_element.innerHTML = $('#postal_code-' + address).html()

    address_number_element.classList.add('sc_field_change')
    street_element.classList.add('sc_field_change')
    area_element.classList.add('sc_field_change')
    landmark_element.classList.add('sc_field_change')
    city_element.classList.add('sc_field_change')
    region_element.classList.add('sc_field_change')
    postal_code_element.classList.add('sc_field_change')

    changed_item_level_address_id = address_number_element.innerHTML;
}

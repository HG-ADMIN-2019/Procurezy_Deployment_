nav_bar_user_settings();

var GLOBAL_DEFAULT_INPUT_DIV_ID = ['default_div_id_acc','default_div_id_cc','default_div_id_wbs',
                        'default_div_id_io','default_div_id_asset','default_div_id_doc_type','edit_purch_settings']
var GLOBAL_SELECT_DROP_DOWN_DIV_ID = ['purch_cancel', 'save_user_settings_attr', 'shipping_addr_actions', 'invoice_addr_actions',
                    'acc_div_id','cc_div_id','wbs_div_id','or_div_id','asset_div_id','doc_type_div_id']

$("#edit_purch_settings").click(function () {
    $("select.form-control.pur_set_slct").each(function (_inx, _ele) { $(_ele).prop('disabled', false) })
    display_elements(null, GLOBAL_SELECT_DROP_DOWN_DIV_ID)
    hide_elements(null,GLOBAL_DEFAULT_INPUT_DIV_ID)
});


function display_elements(prefix, ele_ids) {
    try {
        if (!!prefix) {
            ele_ids.forEach((ele_id) => { $("#" + prefix + ele_id).removeClass('d-none') })
        } else {
            ele_ids.forEach((ele_id) => { $("#" + ele_id).removeClass('d-none') })
        }
    } catch (error) {
        console.log(error)
        return
    }
}


function hide_elements(prefix, ele_ids) {
    try {
        if (!!prefix) {
            ele_ids.forEach((ele_id) => { $("#" + prefix + ele_id).addClass('d-none') })
        } else {
            ele_ids.forEach((ele_id) => { $("#" + ele_id).addClass('d-none') })
        }
    } catch (error) {
        console.log(error)
        return
    }
}

$("#purch_cancel").click(function () {
    toggle_purhase_actions()
});


function toggle_purhase_actions() {
    $("select.form-control.pur_set_slct").each(function (_inx, _ele) { $(_ele).prop('disabled', true) })
    display_elements(null, GLOBAL_DEFAULT_INPUT_DIV_ID)
    hide_elements(null,GLOBAL_SELECT_DROP_DOWN_DIV_ID )
}


var GLOBAL_ID_PURCHASE_SETTINGS_IGNORE_LIST = []
$('select').on('change', function () {
    element_id = this.id
    var sc_id = $(this).attr("id");
    $(this).addClass('drop_down_change_class');

});


// Function to display Select shipping address pop-up in Purchase Settings in Shipping Addr
function select_address(address_id) {
    var id = address_id;
    var split_id = id.split("-");
    var address_index = split_id[1];
    address_numb = document.getElementById('addr_num-' + address_index).innerHTML
    $('#DEL_ADDR').addClass('drop_down_change_class');
    street = document.getElementById('street-' + address_index).innerHTML
    area = document.getElementById('area-' + address_index).innerHTML
    landmark = document.getElementById('landmark-' + address_index).innerHTML
    city = document.getElementById('city-' + address_index).innerHTML
    postalcode = document.getElementById('postal_code-' + address_index).innerHTML
    region = document.getElementById('region-' + address_index).innerHTML
    $('#ChngShipAddr').modal('hide');
    document.getElementById('DEL_ADDR').innerHTML = address_numb
    document.getElementById('shipping_street_output').innerHTML = street
    document.getElementById('shipping_area_output').innerHTML = area
    document.getElementById('shipping_landmark_output').innerHTML = landmark
    document.getElementById('shipping_city_output').innerHTML = city
    document.getElementById('shipping_pcode_output').innerHTML = postalcode
    document.getElementById('shipping_region_output').innerHTML = region
}


// Function to display Select shipping address pop-up in Purchase Settings Invoice Addr
function select_invoice_address(address_id) {
    var id = address_id;
    var split_id = id.split("-");
    var address_index = split_id[1];

    address_numb = document.getElementById('addr_num-' + address_index).innerHTML
    $('#INV_ADDR').addClass('drop_down_change_class');
    street = document.getElementById('street-' + address_index).innerHTML
    area = document.getElementById('area-' + address_index).innerHTML
    landmark = document.getElementById('landmark-' + address_index).innerHTML
    city = document.getElementById('city-' + address_index).innerHTML
    postalcode = document.getElementById('postal_code-' + address_index).innerHTML
    region = document.getElementById('region-' + address_index).innerHTML
    $('#ChngInvcAddr').modal('hide');
    document.getElementById('INV_ADDR').innerHTML = address_numb
    document.getElementById('invoice_street_output').innerHTML = street
    document.getElementById('invoice_area_output').innerHTML = area
    document.getElementById('invoice_landmark_output').innerHTML = landmark
    document.getElementById('invoice_city_output').innerHTML = city
    document.getElementById('invoice_pcode_output').innerHTML = postalcode
    document.getElementById('invoice_region_output').innerHTML = region
}


function update_default(attr_id,attr_val){
    var html_option = '';
    var default_value  = '';
    switch(attr_id) {
        case 'ACC_CAT':
            default_value = attr_val
            $('#input_id_acc').val(attr_val)
            var select_value = $("#"+ attr_id).val();
            if (select_value !==attr_val){
                $("#"+ attr_id +"option[value=attr_val]").remove();
                html_option = '<option value="'+ attr_val +'">' + attr_val + '</option>'
                $("#"+attr_id).prepend(html_option);
            }
            break;
        case 'CT_CTR':
            default_value = attr_val
             $('#input_id_cc').val(default_value)
            var select_value = $("#"+ attr_id).val();
            if (select_value !== default_value){
                $("#"+ attr_id +"option[value=default_value]").remove();
                html_option = '<option value="'+ default_value +'">' + default_value + '</option>'
                $("#"+attr_id).prepend(html_option);
            }
            break;
        case 'WBS_ELEM':
            default_value = attr_val
             $('#input_id_wbs').val(default_value)
            var select_value = $("#"+ attr_id).val();
            if (select_value !== default_value){
                $("#"+ attr_id +"option[value=default_value]").remove();
                html_option = '<option value="'+ default_value +'">' + default_value + '</option>'
                $("#"+attr_id).prepend(html_option);
            }
            break;
        case 'INT_ORD':
            default_value = attr_val
             $('#input_id_io').val(default_value)
            var select_value = $("#"+ attr_id).val();
            if (select_value !== default_value){
                $("#"+ attr_id +"option[value=default_value]").remove();
                html_option = '<option value="'+ default_value +'">' + default_value + '</option>'
                $("#"+attr_id).prepend(html_option);
            }
            break;
        case 'AS_SET':
            default_value = attr_val
             $('#input_id_asset').val(default_value)
            var select_value = $("#"+ attr_id).val();
            if (select_value !== default_value){
                $("#"+ attr_id +"option[value=default_value]").remove();
                html_option = '<option value="'+ default_value +'">' + default_value + '</option>'
                $("#"+attr_id).prepend(html_option);
            }
            break;
        case 'DEF_DOC_SEARCH':
            default_value = attr_val
             $('#input_id_doc_type').val(default_value)
            var select_value = $("#"+ attr_id).val();
            if (select_value !== default_value){
                $("#"+ attr_id +"option[value=default_value]").remove();
                html_option = '<option value="'+ default_value +'">' + default_value + '</option>'
                $("#"+attr_id).prepend(html_option);
            }
            break;
        case 'DEL_ADDR':
            default_delivery_addr = attr_val
            break;
        case 'INV_ADDR':
            default_inv_addr = attr_val
            break;
        default:
            break;
    }
}

var GLOBAL_ADDR_ID = ['INV_ADDR','DEL_ADDR']

// Function to update/save purchase setup
$("#save_user_settings_attr").click(function () {
    var formData = new FormData();
    purch_attr_dict = {}
    var attr_val = '';
    $(".drop_down_change_class").each(function () {

        attr_val = ''
        var drop_down_id = $(this).attr("id");
        select_val =  this.value ;
        if (GLOBAL_ADDR_ID.includes(drop_down_id) ){
            select_val = this.innerHTML ;
        }
        if (select_val){
            attr_val = select_val.split(' - ')[0]
            purch_attr_dict[drop_down_id] = attr_val
            formData.append('update_default', JSON.stringify(purch_attr_dict))
        }
    })

    ajax_save_user_setting_attr(formData);

    $(".drop_down_change_class").each(function () {
        attr_val = ''
        var drop_down_id = $(this).attr("id");
        select_val =  this.value ;
        update_default(drop_down_id,select_val)
        $(this).removeClass('drop_down_change_class');
    })

    document.getElementById('user_setting_update_success').innerHTML = response.message;
    $('#user_setting_update_success').show();
    toggle_purhase_actions()

});


function get_porg_pgrp(selected_option,onchange_action){
    let org_structure_data = {};
    org_structure_data.onchange_action = onchange_action;
    org_structure_data.selected_drop_down_value = selected_option.value;

    var org_data_result = ajax_get_porg_pgrp(org_structure_data);

    if(org_data_result) {
        var porg_html ='';
        var pgrp_html = '';
        if (onchange_action == "company_code"){
            $.each(response.porg_detail, function (i, item) {
                porg_html += '<option value="' + item.porg_id + '">' + item.porg_description + '</option>';
            });
            $("#porg_select_id").empty();
            $("#porg_select_id").append(porg_html);
        }
        $.each(response.pgroup_detail, function (i, item) {
            pgrp_html += '<option value="' + item.pgroup_id + '">' + item.pgroup_description + '</option>';
        });
        $("#pgroup_select_id").empty();
        $("#pgroup_select_id").append(pgrp_html);
    }
    else {
        console.log(response);
    }

}
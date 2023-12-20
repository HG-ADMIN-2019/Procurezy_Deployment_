//=================================================== start acc next and previous =========================================

function show_acc_div() {
    $(".class_sc_acc").hide();
    $(".class_sc_acc:eq(" + acc_visible_div + ")").show();
}

show_acc_div();

function acc_next() {
    if (acc_visible_div == $(".class_sc_acc").length - 1) {
        acc_visible_div = 0;
    }
    else {
        acc_visible_div++;
    }
    show_acc_div();
}

function acc_previous() {
    if (acc_visible_div == 0) {
        acc_visible_div = $(".class_sc_acc").length - 1;
    }
    else {
        acc_visible_div--;
    }
    show_acc_div();
}
//=================================================== end acc next and previous =========================================

//=================================================== start addr next and previous =========================================
function show_addr_div() {
    $(".class_addr").hide();
    $(".class_addr:eq(" + addr_visible_div + ")").show();
}
show_addr_div();

function addr_next() {
    if (addr_visible_div == $(".class_addr").length - 1) {
        addr_visible_div = 0;
    }
    else {
        addr_visible_div++;
    }
    show_addr_div();
}

function addr_previous() {
    if (addr_visible_div == 0) {
        addr_visible_div = $(".class_addr").length - 1;
    }
    else {
        addr_visible_div--;
    }
    show_addr_div();
}
    //=================================================== end addr next and previous =========================================

//========================================start display detail =================================================

function on_click_item_display_detail(button) {
    if (button) {
        item_num_id = button;
        eform_display = true;
        item_no_call_off = item_num_id.split("_");
        item_detail_visible_div = parseInt(item_no_call_off[0]) - 1;
        sc_calloff = item_no_call_off[1];
        show_item_detail_div();
        // display_acc_onselect(rendered_acc[item_detail_visible_div]);
        document.getElementById('id_display_item_detail').style.display = "block";
        $("body, html").animate({
            scrollTop: $('#id_display_item_detail').offset().top,
        }, 1000 );
    
    }
}
    //========================================end display detail =================================================

//=================================================== Start ON CLICK OF ITEM TAB  =========================================
function open_item_details(evt, detail_tab_name) {
    if (detail_tab_name === "approval_process_summary") {
        if (edit_flag) {

            approve_tab_click_trigger_wf(evt, detail_tab_name,'APPROVE_TYPE');
        }
    }
}

function display_tab(evt, detail_tab_name) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("hg_tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("hg_tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].style.background = '#FFFFFF'
        tablinks[i].style.color = '#007BFF'
    }
    GLOBAL_TAB_ID = detail_tab_name;
    document.getElementById(detail_tab_name).style.display = "block";
    try {
        evt.target.style.background = '#007BFF';
        evt.target.style.color = '#FFFFFF';
    } catch (error) {

    }
}

//=================================================== End Item and acc details tab  =========================================

//=================================================== Start note tab  =========================================
function sup_int_note_tab(evt, cityName) {
    var i, tabcontent, note_tab;
    sup_int_note = document.getElementsByClassName("hg_sup_int_note");
    for (i = 0; i < sup_int_note.length; i++) {
        sup_int_note[i].style.display = "none";
    }
    note_tab = document.getElementsByClassName("note_type");
    for (i = 0; i < note_tab.length; i++) {
        note_tab[i].style.backgroundColor = '#FFFFFF'
        note_tab[i].style.color = '#000000'
    }
    document.getElementById(cityName).style.display = "block";
    evt.target.style.backgroundColor = "#007bff";
    evt.target.style.color = '#FFFFFF'
}
    //=================================================== End note tab  =========================================

    //=================================================== Start Item next and prev details tab  =========================================

function show_item_detail_div() {

    $(".hg_class_item_data").hide();
    $(".hg_class_prod_desc").hide();
    $(".hg_class_sc_acc_details").hide();
    $(".hg_supp_note_content").hide();
    $(".hg_int_note_content").hide();
    $(".dummy_eform_class").hide();
    $(".hg_attachment_content").hide();
    $(".hg_class_del_addrs").hide();
    $(".hg_class_attachement").hide();
    $(".hg_supplier_class").hide();
    $(".hg_class_item_data:eq(" + item_detail_visible_div + ")").show();
    $(".hg_class_prod_desc:eq(" + item_detail_visible_div + ")").show();
    $(".hg_class_sc_acc_details:eq(" + item_detail_visible_div + ")").show();
    $(".hg_supp_note_content:eq(" + item_detail_visible_div + ")").show();
    $(".hg_int_note_content:eq(" + item_detail_visible_div + ")").show();
    $(".hg_attachment_content:eq(" + item_detail_visible_div + ")").show();
    $(".hg_class_del_addrs:eq(" + item_detail_visible_div + ")").show();
    $(".hg_class_attachement:eq(" + item_detail_visible_div + ")").show();
    $(".hg_supplier_class:eq(" + item_detail_visible_div + ")").show();
    item_num = item_detail_visible_div + 1;
    if (rendered_eform[item_detail_visible_div] !== "None") {
        $('#eform_tab').show();
        $('.hg_class_eform').hide()
        $("#display_eform-" + rendered_item_guid[item_detail_visible_div]+"-"+item_detail_visible_div).show()
        if (GLOBAL_TAB_ID == "eForm"){
            document.getElementById("eForm").style.display = "block";
        }
    }
    else{

        //document.getElementById(GLOBAL_TAB_ID).style.display = "none";
        $('#eform_tab').hide();
        $('.hg_class_eform').hide()
        if (GLOBAL_TAB_ID == "eForm"){
            GLOBAL_TAB_ID ="item_data"
            document.getElementById("item_tab_id").style.background = '#007BFF';
            document.getElementById("item_tab_id").style.color = '#FFFFFF';
            document.getElementById("eform_tab").style.background = '#FFFFFF';
            document.getElementById("eform_tab").style.color = '#007BFF';
            document.getElementById("item_data").style.display = "block";


        }

    }
    if (edit_flag) {
        // Item data
        if(editable_flag){
        $('.pr_lead_time').prop('disabled', false)
        $("#ScItem-purch_grp-" + rendered_item_guid[item_detail_visible_div]).prop("disabled", false);
        $("#ScItem-silent_po-" + rendered_item_guid[item_detail_visible_div]).prop("disabled", false);
        $("#ScItem-silent_po-" + rendered_item_guid[item_detail_visible_div]).prop("disabled", false);
        $("#ScItem-catalog_qty-" + rendered_item_guid[item_detail_visible_div]).prop("disabled", false);
        $("#ScItem-quantity-" + rendered_item_guid[item_detail_visible_div]).prop("disabled", false);
        $("#ScItem-goods_recep-" + rendered_item_guid[item_detail_visible_div]).prop("disabled", false);
        $("#ScItem-goods_marking-" + rendered_item_guid[item_detail_visible_div]).prop("disabled", false);
        // Accounting data
        $("#ScAccounting-acc_cat-" + rendered_acc_guid[item_detail_visible_div]).prop("disabled", false);
        $("#ScAccounting-cost_center-" + rendered_acc_guid[item_detail_visible_div]).prop("disabled", false);
        $("#ScAccounting-asset_number-" + rendered_acc_guid[item_detail_visible_div]).prop("disabled", false);
        $("#ScAccounting-internal_order-" + rendered_acc_guid[item_detail_visible_div]).prop("disabled", false);
        $("#ScAccounting-wbs_ele-" + rendered_acc_guid[item_detail_visible_div]).prop("disabled", false);
        $("#ScAccounting-account_assign_value-" + rendered_acc_guid[item_detail_visible_div]).prop("disabled", false);
        //$("#ScAccounting-gl_acc_num-" + rendered_acc_guid[item_detail_visible_div]).prop("disabled", false);
        // delivery address
        $("#ScAddresses-name1-" + rendered_sc_addr[item_detail_visible_div]).prop("disabled", false);
        $("#ScAddresses-name2-" + rendered_sc_addr[item_detail_visible_div]).prop("disabled", false);
        $("#ScAddresses-fax_number-" + rendered_sc_addr[item_detail_visible_div]).prop("disabled", false);
        $("#ScAddresses-street-" + rendered_sc_addr[item_detail_visible_div]).prop("disabled", false);
        $("#ScAddresses-area-" + rendered_sc_addr[item_detail_visible_div]).prop("disabled", false);
        $("#ScAddresses-landmark-" + rendered_sc_addr[item_detail_visible_div]).prop("disabled", false);
        $("#ScAddresses-city-" + rendered_sc_addr[item_detail_visible_div]).prop("disabled", false);
        $("#ScAddresses-region-" + rendered_sc_addr[item_detail_visible_div]).prop("disabled", false);
        $("#ScAddresses-country_code-" + rendered_sc_addr[item_detail_visible_div]).prop("disabled", false);
        $("#ScAddresses-language_id-" + rendered_sc_addr[item_detail_visible_div]).prop("disabled", false);
        $("#ScAddresses-mobile_number-" + rendered_sc_addr[item_detail_visible_div]).prop("disabled", false);
        $("#ScAddresses-telephone_number-" + rendered_sc_addr[item_detail_visible_div]).prop("disabled", false);
        $("#ScAddresses-email-" + rendered_sc_addr[item_detail_visible_div]).prop("disabled", false);
        $("#ScAddresses-postalcode-" + rendered_sc_addr[item_detail_visible_div]).prop("disabled", false);

        //Internal and external note
        $("#Notes-note_text-" + rendered_int_note[item_detail_visible_div] + "-I").prop("disabled", false);
        $("#Notes-note_text-" + rendered_supp_note[item_detail_visible_div] + "-S").prop("disabled", false);
        //supplier data
        $("#ScItem-supplier_id-" + rendered_item_guid[item_detail_visible_div] + "-drop").prop("disabled", false);
        $("#ScItem-pref_supplier-" + rendered_item_guid[item_detail_visible_div] + "-drop").prop("disabled", false);
        $("#ScItem-supplier_id-" + rendered_item_guid[item_detail_visible_div]).prop("disabled", false);
        $("#ScItem-pref_supplier-" + rendered_item_guid[item_detail_visible_div]).prop("disabled", false);
        $("#ScItem-supplier_id-" + rendered_item_guid[item_detail_visible_div] + "-drop-ft").prop("disabled", false);

        if (rendered_call_off[item_detail_visible_div] === "01" || rendered_call_off[item_detail_visible_div] === "02") {
        //if (sc_calloff === "Catalog" || sc_calloff === "Freetext") {
            $("#ScItem-payment_term-" + rendered_item_guid[item_detail_visible_div]).prop("disabled", false);
        }
        if (rendered_call_off[item_detail_visible_div] == '03') {
            $("#ScItem-description-" + rendered_item_guid[item_detail_visible_div]).prop("disabled", false);
            $("#ScItem-price-" + rendered_item_guid[item_detail_visible_div]).prop("disabled", false);
            $("#ScItem-price_unit-" + rendered_item_guid[item_detail_visible_div]).prop("disabled", false);
        }

    }
    }
}



show_item_detail_div();
function item_detail_next(button) {
    current_item_num = parseInt(button.id);
    var item_count = rendered_call_off.length;
    if (current_item_num >= item_count) {
        current_item_num = 0;
    }
    sc_calloff = rendered_call_off[current_item_num];
    sc_acc_cat = rendered_acc[current_item_num];

    var item_count = $(".hg_class_item_data").length - 1
    if (item_detail_visible_div == $(".hg_class_item_data").length - 1) {
        item_detail_visible_div = 0;
    }
    else {
        item_detail_visible_div++;
    }
    show_item_detail_div();
}


function item_detail_previous(button) {
    current_item_num = parseInt(button.id) - 1;
    var item_count = rendered_call_off.length;
    if (current_item_num == -1) {
        current_item_num = item_count - 1;
    }
    sc_calloff = rendered_call_off[current_item_num]
    if (item_detail_visible_div == 0) {
        item_detail_visible_div = $(".hg_class_item_data").length - 1;
    }
    else {
        item_detail_visible_div--;
    }
    show_item_detail_div();
}


//=================================================== End Item next and prev details tab  =========================================
//======================================================== start Function to toggle note type textarea ================================
function selectNoteType(data) {
    var getNotebtnClass1 = data.className.split(" ")[0]
    var getNotebtnClass2 = data.className.split(" ")[1]
    var activeNoteBtn = document.getElementsByClassName(hg_getNotebtnClass1);
    var noteBtnId = data.id
    var textareaId = document.getElementById(getNotebtnClass2);
    var textareaClass = textareaId.className;
    var hideableNoteText = document.getElementsByClassName(hg_textareaClass);


    for (var i = 0; i < hideableNoteText.length; i++) {
        var current_element = hideableNoteText[i].id
        if (current_element == getNotebtnClass2) {
            hideableNoteText[i].style.display = 'block';
        } else {
            hideableNoteText[i].style.display = 'none';
        }
    }

    for (var i = 0; i < activeNoteBtn.length; i++) {
        var current_button = activeNoteBtn[i].id
        if (current_button == noteBtnId) {
            activeNoteBtn[i].style.backgroundColor = ' #ffb957';
        } else {
            activeNoteBtn[i].style.backgroundColor = 'rgb(248, 245, 245)';
        }
    }

}
//======================================================== end Function to toggle note type textarea ================================

//==================================== START ON CLICK OF CANCEL BUTTON======================================================================
$("#id_cancel_sc").on("click", function () {

    eform_display = true;
    edit_flag = false;
    document.getElementById('add_id').style.display = 'none';
    document.getElementById('edit_div_id').style.display = 'none';
    document.getElementById('display_div_id').style.display = 'block';
    $(".action_class").prop("hidden", true);
    $(".action_column_id").prop("hidden", true);
    for (i = 0; i < rendered_item_guid.length; i++) {

        // Item data
        $("#ScItem-purch_grp-" + rendered_item_guid[i]).prop("disabled", true);
        $("#ScItem-silent_po-" + rendered_item_guid[i]).prop("disabled", true);
        $("#ScItem-silent_po-" + rendered_item_guid[i]).prop("disabled", true);
        $("#ScItem-catalog_qty-" + rendered_item_guid[i]).prop("disabled", true);
        $("#ScItem-quantity-" + rendered_item_guid[i]).prop("disabled", true);
        $("#ScItem-goods_recep-" + rendered_item_guid[i]).prop("disabled", true);
        $("#ScItem-item_del_date-" + rendered_item_guid[i]).prop("disabled", true);
        $("#ScItem-goods_marking-" + rendered_item_guid[i]).prop("disabled", true);
        // Accounting data
        $("#ScAccounting-dist_perc-" + rendered_acc_guid[i]).prop("disabled", true);
        $("#ScAccounting-acc_cat-" + rendered_acc_guid[i]).prop("disabled", true);
        $("#ScAccounting-cost_center-" + rendered_acc_guid[i]).prop("disabled", true);
        $("#ScAccounting-asset_number-" + rendered_acc_guid[i]).prop("disabled", true);
        $("#ScAccounting-internal_order-" + rendered_acc_guid[i]).prop("disabled", true);
        $("#ScAccounting-wbs_ele-" + rendered_acc_guid[i]).prop("disabled", true);
        $("#ScAccounting-account_assign_value-" + rendered_acc_guid[i]).prop("disabled", true);
        //$("#ScAccounting-gl_acc_num-" + rendered_acc_guid[i]).prop("disabled", true);
        // delivery address
        $("#ScAddresses-name1-" + rendered_sc_addr[i]).prop("disabled", true);
        $("#ScAddresses-name2-" + rendered_sc_addr[i]).prop("disabled", true);
        $("#ScAddresses-fax_number-" + rendered_sc_addr[i]).prop("disabled", true);
        $("#ScAddresses-street-" + rendered_sc_addr[i]).prop("disabled", true);
        $("#ScAddresses-area-" + rendered_sc_addr[i]).prop("disabled", true);
        $("#ScAddresses-landmark-" + rendered_sc_addr[i]).prop("disabled", true);
        $("#ScAddresses-city-" + rendered_sc_addr[i]).prop("disabled", true);
        $("#ScAddresses-region-" + rendered_sc_addr[i]).prop("disabled", true);
        $("#ScAddresses-country_code-" + rendered_sc_addr[i]).prop("disabled", true);
        $("#ScAddresses-language_id-" + rendered_sc_addr[i]).prop("disabled", true);
        $("#ScAddresses-mobile_number-" + rendered_sc_addr[i]).prop("disabled", true);
        $("#ScAddresses-telephone_number-" + rendered_sc_addr[i]).prop("disabled", true);
        $("#ScAddresses-email-" + rendered_sc_addr[i]).prop("disabled", true);
        $("#ScAddresses-postalcode-" + rendered_sc_addr[i]).prop("disabled", true);
        //Internal and external note
        $("#Notes-note_text-" + rendered_int_note[i] + "-I").prop("disabled", true);
        $("#Notes-note_text-" + rendered_supp_note[i] + "-S").prop("disabled", true);
        //supplier data
        $("#ScItem-supplier_id-" + rendered_item_guid[i] + "-drop").prop("disabled", true);
        $("#ScItem-supplier_id-" + rendered_item_guid[i]).prop("disabled", true);
        $("#ScItem-pref_supplier-" + rendered_item_guid[i]).prop("disabled", true);
        $("#ScItem-supplier_id-" + rendered_item_guid[i] + "-drop-ft").prop("disabled", true);

        $("#ScItem-payment_term-" + rendered_item_guid[i]).prop("disabled", true);
        $("#ScItem-description-" + rendered_item_guid[i]).prop("disabled", true);
        $("#ScItem-price-" + rendered_item_guid[i]).prop("disabled", true);
        $("#ScItem-price_unit-" + rendered_item_guid[i]).prop("disabled", true);
    }

    document.getElementById('id_display_item_detail').style.display = "none";

});
//==================================== END ON CLICK OF CANCEL BUTTON======================================================================

function get_data_for_check() {
    var data_for_check = new Array()
    var supplier_id = '';
    var change_acc_value_id = '';
    supplier = $("[id^=supp-]")
    adr_num = $("[id^=address_number_]")
    for (i = 0; i < supplier.length; i++) {
        data = {}
        incremented_i = i + 1
        var supp_id = supplier[i].id;
        // var address_info = 'ScAddresses-address_number-'+rendered_addr_guid[i];
        var acc_info = 'ScAccounting-acc_cat-' + rendered_acc_guid[i];
        var acc_acc_cat = (document.getElementById(acc_info).value).split(' - ')[0]
        data.acc_acc_cat = acc_acc_cat.replace(/\s/g, '')
        switch (data.acc_acc_cat) {
            case "CC":
                change_acc_value_id = 'ScAccounting-cost_center-';
                break;
            case "WBS":
                change_acc_value_id = 'ScAccounting-wbs_ele-';
                break;
            case "OR":
                change_acc_value_id = 'ScAccounting-internal_order-';
                break;
            case "AS":
                change_acc_value_id = 'ScAccounting-asset_number-';
                break;
            default:
        }
        var get_delivery_address_class = document.getElementsByClassName('address_number_check')
        for(del_addr = 0; del_addr < get_delivery_address_class.length; del_addr++) {
            data.address_number = get_delivery_address_class[del_addr].value;
        }
        var acc_val_info = change_acc_value_id + rendered_acc_guid[i];
        var gl_num_info = 'ScAccounting-gl_acc_num-' + rendered_acc_guid[i];
        var prod_cat_info = 'prod_cat_id-' + rendered_item_guid[incremented_i - 1];
        supplier_info = document.getElementById(supp_id).innerHTML;
        data.item_num = incremented_i
        supplier_name = supplier_info.split(' - ')[1]
        // if(supplier_name === 'None'){
        //     supplier_name = document.getElementById('ScItem-supplier_id-' + rendered_item_guid[incremented_i - 1] + '-drop').value
        // }
        data.supplier_name = supplier_name
        //data.address_number = '';
        acc_acc_cat = (document.getElementById(acc_info).value).split(' - ')[0]
        data.acc_acc_cat = acc_acc_cat.replace(/\s/g, '');
        acc_acc_val = (document.getElementById(acc_val_info).value).split(' - ')[0]
        data.acc_acc_val = acc_acc_val.replace(/\s/g, '');
        data.gl_acc_num = (document.getElementById(gl_num_info).value).split(' - ')[0]
        data.prod_cat = (document.getElementById(prod_cat_info).innerHTML)
        delivery_date = document.getElementById('item_del_date-' + rendered_item_guid[i]).innerHTML
        data.delivery_date = delivery_date
        create_id = 'product_id-' + incremented_i + '-'
        get_product_ids = $('[id^="' + create_id + '"]')
        if(get_product_ids.length > 0){
            split_array = get_product_ids[0].id.split('-')
            data.product_id = split_array[2]
            data.lead_time  = split_array[3]
            data.item_price = document.getElementById("price-"+rendered_item_guid[i]).innerHTML
            data.quantity = document.getElementById("catalog_qty-"+rendered_item_guid[i]).innerHTML
        }
        var internal_note = document.getElementById("Notes-note_text-"+rendered_int_note[i] + '-I').value
        var supplier_note = document.getElementById("Notes-note_text-" + rendered_supp_note[i] + "-S").value
        remove_special_characters(internal_note, supplier_note, incremented_i)
        data.item_guid = rendered_item_guid[i]
        data_for_check.push(data)
    }
    return data_for_check
}


// on click of edit, update delivery date and display  save,check, submit,cancel button
$("#id_edit_sc").on("click", function () {
    $('#add_info').modal('show');
});


$("#add_info_ok").on("click", function () {
    $('#add_info').modal('hide');
    update_delivery_date('on_click_edit', null)
});

const document_edit_mode = () => {
    get_call_offs = document.querySelectorAll("[class*=call_off]");
    for(let call_off_item=0; call_off_item<get_call_offs.length; call_off_item++){
        class_list = get_call_offs[call_off_item].className; 
        class_name = class_list.split(' ')[1];
        call_off_type = class_name.split('-')[1]
        if(call_off_type === '01'){
            $('.call_off-'+ call_off_type +'-acc_asgn_cat').prop('disabled', true);
            $('.call_off-'+ call_off_type +'-cc').prop('disabled', true);
            $('.call_off-'+ call_off_type +'-as').prop('disabled', true);
            $('.call_off-'+ call_off_type +'-or').prop('disabled', true);
            $('.call_off-'+ call_off_type +'-wbs').prop('disabled', true);
            $('.call_off-'+ call_off_type +'-gl_account').prop('disabled', true);
            $('.call_off-'+ call_off_type +'-gl_desc').prop('disabled', true);
        } else if(call_off_type == '03'){
            $('.call_off-PR-description').prop('disabled', false);
            $('.call_off-'+ call_off_type +'-acc_asgn_cat').prop('disabled', false);
            $('.call_off-'+ call_off_type +'-cc').prop('disabled', false);
            $('.call_off-'+ call_off_type +'-as').prop('disabled', false);
            $('.call_off-'+ call_off_type +'-or').prop('disabled', false);
            $('.call_off-'+ call_off_type +'-wbs').prop('disabled', false);
            $('.call_off-'+ call_off_type +'-gl_account').prop('disabled', false);
            $('.call_off-'+ call_off_type +'-gl_desc').prop('disabled', false);
        }
            
       
    }
    $('#approver_text').prop('disabled', false);
    $('.hide_in_display_mode').show()
    $('#id_edit_sc').hide()
    $('#document_header').html('Complete Shopping Cart')
    var atLeastOneIsChecked = $('input[name="select_item"]:checked').length;
    if (atLeastOneIsChecked > 0) {
        $('#delete_item_button').attr('hidden', false)
    }
    $('#change_shipping_address_button').attr('hidden', false)
    edit_flag = true;
    eform_display = true;
    document.getElementById('add_id').style.display = 'inline-block';
    //document.getElementById('display_div_id').style.display = 'none';
    $(".action_class").prop("hidden", false);
    $(".action_column_id").prop("hidden", false);
    show_item_detail_div();
    $('.read_only_field').prop('disabled', true)
    // $('#table_header_action').show();
    // $('.table_body_action_icons').show();
    $('.sc-completion-item-delete-icon').toggle();
    
}


// remove bootstrap alert classes on close
$('#ChngShipAddr').on('hidden.bs.modal', function (e) {
    $('.mydatatable').DataTable().destroy()
})


//==================================== START ON CHANGE OF ACCOUNT ASSIGNMENT CATEGORY ======================================================================

// On change of Account Assignment Category in item level, display its respective value
var acc_field_item_guid = ''


function display_acc_onselect(acc) {
    field_id = acc_field_item_guid
    selectid = parseInt(item_detail_visible_div) + 1;
    abc = 'id_asset' + selectid;
    if (acc === 'AS') {
        $('#input_asset'+selectid).empty()
        input_as = ''
        document.getElementById('id_asset' + selectid).style.display = 'block';
        document.getElementById('id_cost_center' + selectid).style.display = 'none';
        document.getElementById('id_int_ord' + selectid).style.display = 'none';
        document.getElementById('id_wbs' + selectid).style.display = 'none';
        
        input_as = '<input type="text" id="ScAccounting-asset_number-'+field_id+'" name="AS" class="hg_modal_select_field form-control" value="Select Asset Value" onclick="open_account_assign_values_modal(this)">'
        $('#input_asset'+selectid).append(input_as);

    }
    if (acc === 'CC') {
        $('#input_costcenter'+selectid).empty()
        input_as = ''
        document.getElementById('id_asset' + selectid).style.display = 'none';
        document.getElementById('id_cost_center' + selectid).style.display = 'block';
        document.getElementById('id_int_ord' + selectid).style.display = 'none';
        document.getElementById('id_wbs' + selectid).style.display = 'none';

        input_as = '<input type="text" id="ScAccounting-cost_center-'+field_id+'" name="CC" class="hg_modal_select_field form-control" value="Select Cost Center Value" onclick="open_account_assign_values_modal(this)">'
        $('#input_costcenter'+selectid).append(input_as);
    }
    if (acc === 'OR') {
        $('#input_intorder'+selectid).empty()
        input_as = ''
        document.getElementById('id_asset' + selectid).style.display = 'none';
        document.getElementById('id_cost_center' + selectid).style.display = 'none';
        document.getElementById('id_int_ord' + selectid).style.display = 'block';
        document.getElementById('id_wbs' + selectid).style.display = 'none';

        input_as = '<input type="text" id="ScAccounting-internal_order-'+field_id+'" name="OR" class="hg_modal_select_field form-control" value="Select Internal Order Value" onclick="open_account_assign_values_modal(this)">'
        $('#input_intorder'+selectid).append(input_as);
    }
    if (acc === 'WBS') {
        $('#input_wbs'+selectid).empty()
        input_as = ''
        document.getElementById('id_asset' + selectid).style.display = 'none';
        document.getElementById('id_cost_center' + selectid).style.display = 'none';
        document.getElementById('id_int_ord' + selectid).style.display = 'none';
        document.getElementById('id_wbs' + selectid).style.display = 'block';

        input_as = '<input type="text" id="ScAccounting-wbs_ele-'+field_id+'" name="WBS" class="hg_modal_select_field form-control" value="Select WBS Value" onclick="open_account_assign_values_modal(this)">'
        $('#input_wbs'+selectid).append(input_as);
    }
}
//==================================== END ON CHANGE OF ACCOUNT ASSIGNMENT CATEGORY ======================================================================


//========================================================= START ON CLICK OF SUBMIT ============================================================
$("#id_submit_sc").on("click", function () {
    get_supplier_class = document.getElementsByClassName('check_supplier')
    var supplier_error_message = ''
    for(i = 0; i < get_supplier_class.length; i++){
        supplier_id = get_supplier_class[i].value 
        item_number = rendered_item_guid.indexOf((get_supplier_class[i].id).split('-')[2])
        if(supplier_id == 'None' || supplier_id == ''){
              
                            var msg = "JMSG004";
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

                           var display8 = msg_type.messages_id_desc;
            supplier_error_message += 'Error at item ' + (item_number + 1) + display8 + "supplier"
        }
    }
    if(supplier_error_message != ''){
        $('#sc_error_messages').html(supplier_error_message)
        $('#sc_error_messages').show()
        return
    }
    check_shopping_cart('submit', 'sc_data', highest_item_acc_asgn_cat, highest_item_change_acc_value);
});

//========================================================= END ON CLICK OF SUBMIT ============================================================


//======================================================== start on change in ACC ==============================================
function get_changed_input_value(changed_id) {
    var changed_val = '';
    var quantity_class_name = changed_id.attr('class');
    if (quantity_class_name === "sc_changed") {
        changed_val = changed_id.val();
    }
    return changed_val
}

function get_item_detail() {
    var quantity = [];
    var price_unit = [];
    var price = [];
    var overall_limit = [];
    var catalog_qty = [];
    $.each(rendered_item_guid, function (index, item_guid) {
        // quantity
        quant_val = $("#ScItem-quantity-" + item_guid).val()
        // get catalog quantity value
        catalog_qty_val = $("#ScItem-catalog_qty-" + item_guid).val()
        if (catalog_qty_val === undefined) {
            catalog_qty_val = 0;
        }
        catalog_qty.push(catalog_qty_val);
        if (quant_val === undefined) {
            quant_val = catalog_qty_val;
        }
        quantity.push(quant_val);

        // get price unit value
        price_unit_val = $("#ScItem-price_unit-" + item_guid).val()
        if (price_unit_val === undefined) {
            price_unit_val = 1;
        }
        price_unit.push(price_unit_val);

        // get price value
        price_val = $("#ScItem-price-" + item_guid).val()
        if (price_val === undefined) {
            price_val = 1;
        }
        price.push(price_val);

        // get overall_limit value
        overall_limit_val = $("#ScItem-overall_limit-" + item_guid).val()
        if (overall_limit_val === undefined) {
            overall_limit_val = 0;
        }
        overall_limit.push(overall_limit_val);


    });
    return [quantity, price_unit, price, overall_limit, catalog_qty];
}

function get_acc_detail() {
    var acc_val = [];
    var acc_cat = [];
    var acc_val_desc = ''
    $.each(rendered_acc_guid, function (index, accounting_guid) {
        acc_desc = $("#ScAccounting-acc_cat-" + accounting_guid).val();

        acc_default = acc_desc.split(" - ")
        acc_cat.push(acc_default[0]);
        switch (acc_default[0]) {
            case "CC":
                acc_val_desc = $("#ScAccounting-cost_center-" + accounting_guid).val();
                break;
            case "WBS":
                acc_val_desc = $("#ScAccounting-wbs_ele-" + accounting_guid).val();
                break;
            case "OR":
                acc_val_desc = $("#ScAccounting-internal_order-" + accounting_guid).val();
                break;
            case "AS":
                acc_val_desc = $("#ScAccounting-asset_number-" + accounting_guid).val();
                break;
            default:
        }
        var acc_default_val = acc_val_desc.split(' - ');
        acc_val.push(acc_default_val[0]);
    });
    return [acc_cat, acc_val]
}

//======================================================== end on change in ACC ==============================================

// Function to delete item
let delete_item_guid = '';
const display_delete_popup = (item_guid) => {
    delete_item_guid = item_guid;
    $('#delete_popup').modal('show');
}

// Start of Checkbox section
var display_item_detail_id = ''

// const checkbox_onchange = (element) => {

//     if ($(element).prop("checked") == true) {
//         get_id = element.id
//         GLOBAL_ID_IGNORE_LIST.push(get_id)
//         check_box_id = element.id.split('-')
//         display_item_detail_id = check_box_id[1]
//         delete_item_guid = check_box_id[2]
//         if (edit_flag) {
//             $('#delete_item_button').attr('hidden', false)
//         }
//         $('#display_item_detail_button').attr('hidden', false)
//     } else {
//         $('#delete_item_button').attr('hidden', true)
//         $('#display_item_detail_button').attr('hidden', true)
//         display_item_detail_id = ''
//         delete_item_guid = ''
//         $('#id_display_item_detail').hide()
//     }
// }


$("input:checkbox").on('click', function () {
    // in the handler, 'this' refers to the box clicked on
    var $box = $(this);

    if ($box.is(":checked")) {
        // the name of the box is retrieved using the .attr() method
        // as it is assumed and expected to be immutable
        var group = "input:checkbox[name='" + $box.attr("name") + "']";
        // the checked state of the group/box on the other hand will change
        // and the current value is retrieved using .prop() method
        $(group).prop("checked", false);
        $box.prop("checked", true);
    } else {
        $box.prop("checked", false);
    }
});
// End of checkbox section


const sc_completion_ui_checks = () => {
    var get_delivery_address_class = document.getElementsByClassName('address_number_check')
    var get_multiple_account_asign_type = document.getElementsByClassName('check_multiple_account_asign_type')
    var address_number_array = new Array();
    var account_asign_type_array = new Array();
    var account_asign_value_array = new Array();
    var warning_messages = '';
    for(i = 0; i < get_delivery_address_class.length; i++) {
        address_number_array.push(get_delivery_address_class[i].value)
    }
    is_multiple_delivery_addresses = address_number_array.every( (val, i, arr) => val === arr[0] )
    if(!is_multiple_delivery_addresses){
                  
                    var msg = "JMSG026";
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
                  var display = msg_type.messages_id_desc;
                   warning_messages += display;

    }
    for(i = 0; i < get_multiple_account_asign_type.length; i++) {
        var decide_id = ''
        account_assignment_type = get_multiple_account_asign_type[i].value
        account_assignment_type_id = get_multiple_account_asign_type[i].id
        accounting_guid = account_assignment_type_id.split('-')[2]

        account_asign_type_array.push(account_assignment_type)
        account_assignment_type_split = account_assignment_type.split(' - ')[0]
        if(account_assignment_type_split == 'CC'){
            decide_id = 'cost_center'
        } else if(account_assignment_type_split == 'AS') {
            decide_id = 'asset_number'
        } else if(account_assignment_type_split == 'OR'){
            decide_id = 'internal_order'
        } else if(account_assignment_type_split == 'WBS'){
            decide_id = 'wbs_ele'
        }

        var account_asign_value = document.getElementById('ScAccounting-' + decide_id + '-' + accounting_guid).value
        account_asign_value_array.push(account_asign_value)
    }
    is_multiple_account_asign_type = account_asign_type_array.every( (val, i, arr) => val === arr[0] )
    if(!is_multiple_account_asign_type){
               
                    var msg = "JMSG047";
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
                  var display = msg_type.messages_id_desc;
                  warning_messages += display;

    } else {
        is_multiple_account_assignment_value = account_asign_value_array.every( (val, i, arr) => val === arr[0] )
        if(!is_multiple_account_assignment_value){
              
                    var msg = "JMSG048";
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
                     var display5 = msg_type.messages_id_desc;
                    warning_messages += display5;

        }
    }

    if(warning_messages == ''){
        $('sc_warning_messages').hide()
    } else {
        $('#sc_warning_messages').html(warning_messages)
        $('#sc_warning_messages').show()
    }

    var error_messages = ''

    for(j = 0; j < internal_supplier_error_itemNumber.length; j++ ) {
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

           var display5 = msg_type.messages_id_desc;
          error_messages += 'Error at item ' + internal_supplier_error_itemNumber[j] + ': ' + display5 + "Internal or supplier note" + '<br>'

    }

    return error_messages
}



// Function to open Change GL account number pop up modal
gl_account_value_field_id = ''
function open_change_gl_account_modal(data){
    $('#change_gl_account_modal').modal('show');
    gl_account_value_field_id = data
}

// Function to update GL account number
$('#select_gl_account').click(function(){
    $('#select_gl_account_table TBODY TR').each(function(){
        var row = $(this);
        var check = row.find("TD").eq(0).find('input[type="radio"]').is(':checked');
        if (check){
            gl_acc_value = row.find("TD").eq(1).text();
            document.getElementById(gl_account_value_field_id).value = gl_acc_value;
            $("#"+gl_account_value_field_id).addClass('sc_changed');
        }
        
    });
});


// Function to open Change supplier pop up modal
change_supplier_field_id = ''
function open_change_supplier_modal(data){
    setTimeout(function() {
        $('.select_supplier_datatable').DataTable( {
            "scrollY": "300px",
            "scrollCollapse": true,
        } );
    }, 500);
    $('#change_supplier_modal').modal('show');
    change_supplier_field_id = data
}

// Function to update supplier number
$('#select_supplier_value').click(function(){
    $('#select_supplier_table TBODY TR').each(function(){
        var row = $(this);
        var check = row.find("TD").eq(0).find('input[type="radio"]').is(':checked');
        if (check){
            select_supplier_value = row.find("TD").eq(1).text();
            supplier_id = select_supplier_value.split('-')[0].trim()
            update_supplier_item_guid = change_supplier_field_id.split('-')[2]
            $('#supp-' + update_supplier_item_guid).html('by - ' + supplier_id)
            document.getElementById(change_supplier_field_id).value = select_supplier_value;
            $("#"+change_supplier_field_id).addClass('sc_changed');
            update_delivery_date('on_select_supplier', null)
        }
        
    });
});

// remove bootstrap alert classes on close
$('#change_supplier_modal').on('hidden.bs.modal', function (e) {
    $('.select_supplier_datatable').DataTable().destroy()
})


account_assignment_value_field_id = ''

function open_account_assign_values_modal(data) {
    $('#select_acc_tbody').empty();
    $('#acc_assign_type').empty();
    var acc_type = data.name
    var selected_value = data.value
    account_assignment_value_field_id = data.id
    var tbody_content = ''

    $.each(accout_assigment_values, function (i, acc_values) {
        if (acc_values.account_assign_cat == acc_type){
            tbody_content += '<tr> <td><input type="radio" name="select_value"></td> <td>'+ acc_values.append_val +'</td> </tr>'
        }
    });
    $('#select_acc_tbody').append(tbody_content)

    if (acc_type == 'CC'){
        $('#acc_assign_type').html('Cost Center value')
    }else if (acc_type == 'WBS'){
        $('#acc_assign_type').html('WBS value')
    }else if (acc_type == 'AS'){
        $('#acc_assign_type').html('Asset value')
    }else if (acc_type == 'OR'){
        $('#acc_assign_type').html('Internal Order value')
    }
    $('#change_account_assignment_modal').modal('show');
}


// Trigger Function on select of account assignmnt value in change account assignmnt values popup
$('#select_account_assignment_value').click(function(){
    $('#select_acc_table TBODY TR').each(function(){
        var row = $(this);
        var check = row.find("TD").eq(0).find('input[type="radio"]').is(':checked');
        if (check){
            select_account_assignment_value = row.find("TD").eq(1).text();
            document.getElementById(account_assignment_value_field_id).value = select_account_assignment_value;
            $("#"+account_assignment_value_field_id).addClass('sc_changed');
        }

    })
})


$('#change_shipping_address_button').click(function(){
    setTimeout(function(){
        $('.mydatatable').DataTable({
            "scrollY": "320px",
            "scrollCollapse": true,
        });
    },500);
});

var addr_loop_counter = ''
function select_addr_radio_btn(data){
    GLOBAL_ID_IGNORE_LIST.push(data)
    addr_loop_counter = data.split('-')[1]
}


//  Trigger Function on select of shipping address in change shipping address pop-up
$('#select_shipping_address').click(function(){
    var address_name = $('#address_name-'+addr_loop_counter).text();
    var name = address_name.split(' - ')
    var name1 = name[0]
    var name2 = name[1]
    var address_email = $('#address_email-'+addr_loop_counter).text();
    var addr_num = $('#addr_num-'+addr_loop_counter).text();
    var street = $('#street-'+addr_loop_counter).text();
    var area = $('#area-'+addr_loop_counter).text();
    var landmark = $('#landmark-'+addr_loop_counter).text();
    var city = $('#city-'+addr_loop_counter).text();
    var postal_code = $('#postal_code-'+addr_loop_counter).text();
    var region = $('#region-'+addr_loop_counter).text();
    $("#ScAddresses-name1-" + rendered_sc_addr[item_detail_visible_div]).val(name1);
    $("#ScAddresses-name1-" + rendered_sc_addr[item_detail_visible_div]).addClass('sc_changed');
    $("#ScAddresses-name2-" + rendered_sc_addr[item_detail_visible_div]).val(name2);
    $("#ScAddresses-name2-" + rendered_sc_addr[item_detail_visible_div]).addClass('sc_changed');
    $("#ScAddresses-email-" + rendered_sc_addr[item_detail_visible_div]).val(address_email);
    $("#ScAddresses-email-" + rendered_sc_addr[item_detail_visible_div]).addClass('sc_changed');
    $("#ScAddresses-street-" + rendered_sc_addr[item_detail_visible_div]).val(street);
    $("#ScAddresses-street-" + rendered_sc_addr[item_detail_visible_div]).addClass('sc_changed');
    $("#ScAddresses-area-" + rendered_sc_addr[item_detail_visible_div]).val(area);
    $("#ScAddresses-area-" + rendered_sc_addr[item_detail_visible_div]).addClass('sc_changed');
    $("#ScAddresses-landmark-" + rendered_sc_addr[item_detail_visible_div]).val(landmark);
    $("#ScAddresses-landmark-" + rendered_sc_addr[item_detail_visible_div]).addClass('sc_changed');
    $("#ScAddresses-city-" + rendered_sc_addr[item_detail_visible_div]).val(city);
    $("#ScAddresses-city-" + rendered_sc_addr[item_detail_visible_div]).addClass('sc_changed');
    $("#ScAddresses-postalcode-" + rendered_sc_addr[item_detail_visible_div]).val(postal_code);
    $("#ScAddresses-postalcode-" + rendered_sc_addr[item_detail_visible_div]).addClass('sc_changed');
    $("#ScAddresses-region-" + rendered_sc_addr[item_detail_visible_div]).val(region);
    $("#ScAddresses-region-" + rendered_sc_addr[item_detail_visible_div]).addClass('sc_changed');

    $('#ChngShipAddr').modal('hide');
})


// Script from sc item details.html
function add_item_to_saved_cart(item_type) {
    doc_number_encrypted = doc_number_encrypted;
    url_remove_display = location.href.split('/')
    url_remove_display.pop()
    url_remove_display = url_remove_display.join('/')
    localStorage.setItem('opened_document-' + doc_number_encrypted, url_remove_display)

    if (item_type === '01') {
        url = '/shop/products_services/All/' + 'doc_number-' + doc_number_encrypted
        location.href = url
    }
    if (item_type === '02') {
        url = '/shop/products_services/All/' + 'doc_number-' + doc_number_encrypted
        location.href = url
    }
    if (item_type === '03') {
        url = '/add_item/purchase_requisition/' + 'doc_number-' + doc_number_encrypted
        location.href = url
    }
}


// Function to delete item in cart
function delete_cart_item() {
    if (delete_item_guid) {
        $('#delete_popup').modal('hide');
        delete_item_data = {};
        delete_item_data.del_item_guid = delete_item_guid;
        delete_item_data.total_value = document.getElementById('ScHeader-total_value-' + GLOBAL_HEADER_GUID).innerHTML;
        delete_item_data.header_guid = document.getElementById('header_guid').value;
        
        OpenLoaderPopup();

        $.ajax({
            type: 'POST',
            url: ajax_delete_cart_item_url,
            data: delete_item_data,
            success: function(response){
                if (response.count === 0) {
                    window.opener.location.reload();
                    window.close();
                } else {
                    document.getElementById("ScHeader-total_value-" + GLOBAL_HEADER_GUID).innerHTML = response.total_value;
                    var get_item_number = $("[id^=item_number_]");
                    var row = document.getElementById(delete_item_guid);
                    row.parentNode.removeChild(row);
                }
                // loader keeps running in bg while page refreshes
                location.reload();
                window.opener.location.reload();
            },
            error: function(error) {
                console.log(error);
                CloseLoaderPopup();
            },
        });
    };
};

function update_description(id){
    var desc = $('#'+id).val()
    $('#sc_item_description-'+rendered_item_guid[item_detail_visible_div]).html(desc)

}


// $( "#item_approval_overview" ).click(function() {
//     alert( "Handler for .click() called." );
//     approve_tab_click_trigger_wf(evt, detail_tab_name,'APPROVE_TYPE');
//   });
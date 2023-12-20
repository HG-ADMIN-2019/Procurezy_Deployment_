var main_table_low_value = [];
var encrypted_supplier

// Global variable - supplier id
var global_supplier_id = document.getElementById('supplier_id').value

// Global variable - delete supplier purchasing info
var delete_supp_purch_data = []

// Global variable - supplier purchasing data
var supplier_org_data = new Array();
$("#display_basic_org_table TBODY TR").each(function() {
    var row = $(this);
    var save_supp_org_data = {};
    save_supp_org_data.supp_id = global_supplier_id;
    save_supp_org_data.supp_org_guid = row.find("TD").eq(0).text().trim();
    save_supp_org_data.porg_id = row.find("TD").eq(1).text().trim();
    save_supp_org_data.currency_id = row.find("TD").eq(2).text().trim();
    save_supp_org_data.payment_term = row.find("TD").eq(3).text().trim();
    save_supp_org_data.incoterm = row.find("TD").eq(4).text().trim();
    save_supp_org_data.gr_inv_vrf = row.find("TD").eq(5).find('input[type="checkbox"]').is(':checked');
    save_supp_org_data.inv_conf_exp = row.find("TD").eq(6).find('input[type="checkbox"]').is(':checked');
    save_supp_org_data.gr_conf_exp = row.find("TD").eq(7).find('input[type="checkbox"]').is(':checked');
    save_supp_org_data.po_resp = row.find("TD").eq(8).find('input[type="checkbox"]').is(':checked');
    save_supp_org_data.ship_notif_exp = row.find("TD").eq(9).find('input[type="checkbox"]').is(':checked');
    save_supp_org_data.purch_block = row.find("TD").eq(10).find('input[type="checkbox"]').is(':checked');
    supplier_org_data.push(save_supp_org_data)
    console.log(save_supp_org_data)
})


// Makes the supplier basic data fields editable
function edit_basic_supp_data(){
    $('#supplier_basic_update_success').hide();
    $(".hg_edit_display_mode").prop( "disabled", false );
    if(GLOBAL_ACTION != 'CREATE'){
            $("#supplier_id").prop( "disabled", true );
            $("#sbd_edit_button").prop("hidden", true);
            $("#cancel_button").prop("hidden", false);
            document.getElementById('cancel_button').style.display = 'block';
            document.getElementById('sbd_save_cancel_button').style.display = 'block';
            $("#working_days").show();
            $("#working_days").prop("hidden", false);
            $("#working_days_id").prop("hidden", true);
    }
    $("#edit_mode").show();
    document.getElementById('display_mode').style.display = 'none' ;
    $("#working_days_id").prop("hidden", false);
     $("#edit_mode").prop("hidden", false);
     var num = w_days.match(/\d/g);
     $("select[id=working_days_id]").val(num);
     $('#working_days_id').selectpicker('refresh');
    document.getElementById('sbd_edit_button').style.display = 'none' ;
     $("#cancel_button").prop("hidden", false);
    $("#sbd_edit_button").prop("hidden", true);
    document.getElementById('sbd_save_cancel_button').style.display = 'block';
    $("#sbd_save_cancel_button").prop("hidden", false);
    values_reload();
}

// onclick of cancel button functionality
function cancel_basic_details(){
    $(".hg_edit_display_mode").prop("disabled", true);
    document.getElementById('sbd_save_cancel_button').style.display = 'none'
    document.getElementById('cancel_button').style.display = 'none'
    document.getElementById('sbd_edit_button').style.display = 'block'
    document.getElementById('display_mode').style.display = 'block';
    document.getElementById('edit_mode').style.display = 'none';
    $('#working_days_id').selectpicker('refresh');
    var result = get_working_day_val();
    $("#working_days_id").val(result);
    $("#edit_mode").prop("disabled", true);
    $("#sbd_edit_button").prop("hidden", false);
    get_values_onerror();
    $('#image-preview').hide();
    $('#image-preview3').show();
    var output = document.getElementById('image-preview3');
    if(!(img_url == '')){
        output.src = img_url;
    }
}

function get_working_day_val(){
    var wday_array = [];
        wday_array = w_days.split(",");
        var num = w_days.match(/\d/g);
        return num;
}
// Function to edit supplier purchasing details data
function edit_supp_org(){
    var supp_org_body_data = '';
// -----------------------------------------------
    $('#display_basic_org_table').DataTable().destroy();
    $('#supp_org_body').empty();
    var edit_basic_data = '';
    $.each(rendered_supp_org_data, function (i, item) {
         var gr_inv_vrf_checkbox = '';
        if (item.ir_gr_ind){
            gr_inv_vrf_checkbox += '<input type="checkbox"  checked disabled>'
        } else gr_inv_vrf_checkbox += '<input type="checkbox" disabled>'

        var inv_conf_exp_checkbox = '';
        if(item.ir_ind){
            inv_conf_exp_checkbox += '<input type="checkbox"  checked disabled>'
        } else inv_conf_exp_checkbox += '<input type="checkbox" disabled>'

        var gr_conf_exp_checkbox = '';
        if(item.gr_ind){
            gr_conf_exp_checkbox += '<input type="checkbox"  checked disabled>'
        } else gr_conf_exp_checkbox += '<input type="checkbox" disabled>'

        var po_resp_checkbox = '';
        if(item.po_resp){
            po_resp_checkbox += '<input type="checkbox"  checked disabled>'
        } else po_resp_checkbox += '<input type="checkbox" disabled>'

        var ship_notif_exp_checkbox = ''
        if(item.ship_notif_exp){
            ship_notif_exp_checkbox += '<input type="checkbox"  checked disabled>'
        } else ship_notif_exp_checkbox += '<input type="checkbox" disabled>'

        var purch_block_checkbox = ''
        if(item.purch_block){
            purch_block_checkbox += '<input type="checkbox"  checked disabled>'
        } else purch_block_checkbox += '<input type="checkbox" disabled>'

        edit_basic_data += '<tr><td class="class_select_checkbox"><input class="checkbox_check"  onclick="valueChanged()" type="checkbox"></td>'+
         '<td hidden>'+item.guid+'</td>'+
         '<td>'+item.porg_id+'</td>'+
         '<td>'+item.currency_id_id+'</td>'+
         '<td>'+item.payment_term_key+'</td>'+
         '<td>'+item.incoterm_key_id+'</td>'+
         '<td>'+gr_inv_vrf_checkbox+'</td>'+
         '<td>'+inv_conf_exp_checkbox+'</td>'+
         '<td>'+gr_conf_exp_checkbox+'</td>'+
         '<td>'+po_resp_checkbox+'</td>'+
         '<td>'+ship_notif_exp_checkbox+'</td>'+
         '<td>'+purch_block_checkbox+'</td></tr>';
    });
    $('#supp_org_body').append(edit_basic_data);
    $("#hg_select_checkbox").prop("hidden", true);
    $("#id_check_all").prop("hidden", false);
    $(".class_select_checkbox").prop("hidden", true);
//    $('input:checkbox').removeAttr('checked');
    $('#id_edit_data').show();
    $('#id_cancel_data').hide();
    $('#id_delete_data').hide();
    $('#id_copy_data').hide();
    $('#id_update_data').hide();
    $('#id_save_confirm_popup').modal('hide');
    $('#id_delete_confirm_popup').modal('hide');
    table_sort_filter('display_basic_org_table');
}

// Function to cancel Edit operation
function cancel_supp_org_data(){
    display_supp_org_header = ''
    display_supp_org_body = ''
    $('#supp_org_header').empty();
    $('#supp_org_body').empty();
    display_supp_org_header = '<tr> <th>Purchasing organisation</th> <th>PO Currency</th> <th>Payment Terms</th> <th>Incoterm</th> <th>GR based invoice verification</th> <th>Invoice confirmation expected</th> <th>GR confirmation expected</th> <th>PO response</th> <th>Shipping notification expected</th> <th>Purchase block</th></tr>'
    $.each(supplier_org_data, function(index, data){
        var gr_inv_vrf_checkbox = ''
        if (data.gr_inv_vrf==true){
            gr_inv_vrf_checkbox += '<input type="checkbox" checked disabled>'
        } else gr_inv_vrf_checkbox += '<input type="checkbox" disabled>'

        var inv_conf_exp_checkbox = ''
        if(data.inv_conf_exp==true){
            inv_conf_exp_checkbox += '<input type="checkbox" checked disabled>'
        } else inv_conf_exp_checkbox += '<input type="checkbox" disabled>'

        var gr_conf_exp_checkbox = ''
        if(data.gr_conf_exp==true){
            gr_conf_exp_checkbox += '<input type="checkbox" checked disabled>'
        } else gr_conf_exp_checkbox += '<input type="checkbox" disabled>'

        var po_resp_checkbox = ''
        if(data.po_resp==true){
            po_resp_checkbox += '<input type="checkbox" checked disabled>'
        } else po_resp_checkbox += '<input type="checkbox" disabled>'

        var ship_notif_exp_checkbox = ''
        if(data.ship_notif_exp==true){
            ship_notif_exp_checkbox += '<input type="checkbox" checked disabled>'
        } else ship_notif_exp_checkbox += '<input type="checkbox">'

        var purch_block_checkbox = ''
        if(data.purch_block==true){
            purch_block_checkbox += '<input type="checkbox" checked disabled>'
        } else purch_block_checkbox += '<input type="checkbox" disabled>'

        display_supp_org_body += '<tr> <td hidden>'+data.supp_org_guid+'</td> <td>'+data.porg_id+'</td> <td>'+data.currency_id+'</td> <td>'+data.payment_term+'</td> <td>'+data.incoterm+'</td> <td>'+gr_inv_vrf_checkbox+'</td> <td>'+inv_conf_exp_checkbox+'</td> <td>'+gr_conf_exp_checkbox+'</td> <td>'+po_resp_checkbox+'</td> <td>'+ship_notif_exp_checkbox+'</td> <td>'+purch_block_checkbox+'</td></tr> '
    });

    $('#supp_org_header').append(display_supp_org_header);
    $('#supp_org_body').append(display_supp_org_body);
    document.getElementById("id_edit_data").style.display = "block";
    document.getElementById("supp_org_cancel_save").style.display = "none";
}


var supplierid = global_supplier_id;

   // Validation function
function save_basic_form_validation(){
        var is_valid = true;
        var save_form_errors = ''
        var mailformat = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;

        var err_text1 = '';
        var temp = document.getElementsByClassName('mandatory_fields');
        var drp_down = document.getElementsByClassName('dropdown_fields');
        for (var i = 0; i<temp.length; i++) {
            if(temp[i].nodeName == "SELECT"){
                if((temp[i].value == "") || (temp[i].value == null)){
                    err_text1 = temp[i].parentNode.children[0].innerHTML;
                    var display_id = temp[i].nextElementSibling.id;
                    $('#'+display_id).prop('hidden', false);
                    $('#temp[i].nextElementSibling.id').html("required");
                    document.getElementById(temp[i].nextElementSibling.id).innerHTML = err_text1 + " required";
                    is_valid = false;
                }
                else{ $('#temp[i].nextElementSibling.id').prop('hidden', true);
                }
            }
            else if(temp[i].nodeName == "INPUT"){
                var data = temp[i].value;
                var count = data.split('**').length - 1;
                if(temp[i].value == ''){
                    var err_text = temp[i].parentNode.children[0].innerHTML;
                    $(".error_message").prop("hidden", false);
                    temp[i].nextElementSibling.innerHTML = err_text + " required";
                   is_valid = false;
                }
                else if((count >= 1) || (data.includes('*'))){
                    var err_text = temp[i].parentNode.children[0].innerHTML;
                    $(".error_message").prop("hidden", false);
                    var display_id = temp[i].nextElementSibling.id;
                    $('#'+display_id).prop('hidden', false);
                    document.getElementById(display_id).style.display = "block";
                    temp[i].nextElementSibling.innerHTML = "Please enter valid value";
                   is_valid = false;
                }
                else if((temp[i].value.length < 3) || ((count >= 1) || (data == '*'))){
                    var err_text = temp[i].parentNode.children[0].innerHTML;
                    $(".error_message").prop("hidden", false);
                    var display_id = temp[i].nextElementSibling.id;
                    $('#'+display_id).prop('hidden', false);
                    document.getElementById(display_id).style.display = "block";
                    temp[i].nextElementSibling.innerHTML = "Please enter min 3 chars for "+ err_text;
                   is_valid = false;
                }
                else if(temp[i].id == 'email_id'){
                    var mailformat = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
                     if (!(temp[i].value).match(mailformat)) {
                            valid_data = false
                             var msg = "JMSG002";
                             var msg_type ;
                             msg_type = message_config_details(msg);
                             var display1 = msg_type.messages_id_desc;
                             $(".error_message").prop("hidden", false);
                            var display_id = temp[i].nextElementSibling.id;
                            $('#'+display_id).prop('hidden', false);
                            document.getElementById(display_id).style.display = "block";
                            temp[i].nextElementSibling.innerHTML = display1 + " for Email Id";
                           is_valid = false;
                     }
                }
            }
            }
            for (var i = 0; i<drp_down.length; i++) {
                if(drp_down[i].nodeName == "SELECT"){
                    if((drp_down[i].value == "") || (drp_down[i].value == null)){
                        err_text1 = drp_down[i].parentNode.children[0].innerHTML;
                        var display_id = drp_down[i].nextElementSibling.id;
                        $('#'+display_id).prop('hidden', false);
                        $('#drp_down[i].nextElementSibling.id').html("required");
                        document.getElementById(drp_down[i].nextElementSibling.id).innerHTML = err_text1 + " required";
                        is_valid = false;
                    }
                    else{ $('#drp_down[i].nextElementSibling.id').prop('hidden', true);
                    }
                }
            }
        return is_valid
    }

function data_validation(formdata){
    var save_form_errors = ''
    var valid_data = true;
    var mailformat = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
     if (!(formdata.get("email_id")).match(mailformat)) {
            valid_data = false
             var msg = "JMSG002";
             var msg_type ;
             msg_type = message_config_details(msg);
             $("#error_msg_id").prop("hidden", false)
             var display1 = msg_type.messages_id_desc;
            save_form_errors += display1 + " for Email Id";
            document.getElementById("save_error_div").innerHTML = save_form_errors;
             setTimeout(function() {
                   CloseLoaderPopup();
             }, 500);
        }
    return valid_data;
}

function enable_disable(action){
    $(".dummy_ft_button_class").hide();
    if(action == 'EDIT'){
        $("#ft_save").show();
        $("#ft_cancel").show();
        $('.toggle_mode').prop('disabled', false)
    }
    else{
        $("#ft_edit").show();
        $('.toggle_mode').prop('disabled', true)
    }
}


// Function for add a new row data
function new_row_data(){
    basic_add_new_html = '<tr><td><input type="checkbox" class="checkbox_check" onclick="valueChanged();" required></td>'+
    '<td hidden><input type="text" name="supp_org_guid"></td>'+
    '<td><select class="form-control"  type="text"  name="porg_id" style="text-transform:uppercase;">'+porg_opt+'</select></td>'+
    '<td><select class="form-control" type="text"  name="currency_id">'+currency_opt1+'</select></td>'+
    '<td><select style="width:auto;" class="form-control" type="text"  name="payment_term">'+payterm_opt+'</select></td>'+
    '<td><select style="width:auto;" class="form-control" type="text"  name="incoterm">'+incoterm_opt+'</select></td>'+
    '<td><input class="checkbox-size" type="checkbox"  name="gr_inv_vrf_checkbox" required></td>'+
    '<td><input class="checkbox-size" type="checkbox"  name="inv_conf_exp_checkbox" required></td>'+
    '<td><input class="checkbox-size" type="checkbox"  name="gr_conf_exp_checkbox" required></td>'+
    '<td><input class="checkbox-size" type="checkbox"  name="po_resp_checkbox" required></td>'+
    '<td><input class="checkbox-size" type="checkbox"  name="ship_notif_exp_checkbox" required></td>'+
    '<td><input class="checkbox-size" type="checkbox"  name="purch_block_checkbox" required></td>'+
    '<td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
    $('#id_popup_tbody').append(basic_add_new_html);
}
//onclick of cancel display the table in display mode............
function display_basic_db_data() {
    $('#display_basic_org_table').DataTable().destroy();
    $('#supp_org_body').empty();
    var edit_basic_data = '';
    $.each(rendered_supp_org_data, function (i, item) {
        var gr_inv_vrf = '', inv_conf_exp = '', gr_conf_exp = '', po_resp = '', ship_notif_exp='', purch_block='';
        if (item.gr_ind == true){
                gr_inv_vrf = '<input type="checkbox" name="gr_inv_vrf" value="" checked disabled>'
        } else{
                gr_inv_vrf = '<input type="checkbox" name="gr_inv_vrf" value="" disabled>'
        }
        if (item.ir_ind == true){
                inv_conf_exp = '<input type="checkbox" name="inv_conf_exp" value="" checked disabled>'
        } else{
                inv_conf_exp = '<input type="checkbox" name="inv_conf_exp" value="" disabled>'
        }
         if (item.ir_gr_ind == true){
                gr_conf_exp = '<input type="checkbox" name="gr_conf_exp" value="" checked disabled>'
        } else{
                gr_conf_exp = '<input type="checkbox" name="gr_conf_exp" value="" disabled>'
        }
         if (item.po_resp == true){
                po_resp = '<input type="checkbox" name="po_resp" value="" checked disabled>'
        } else{
                po_resp = '<input type="checkbox" name="po_resp" value="" disabled>'
        }
        if (item.ship_notif_exp == true){
                ship_notif_exp = '<input type="checkbox" name="ship_notif_exp" value="" checked disabled>'
        } else{
                ship_notif_exp = '<input type="checkbox" name="ship_notif_exp" value="" disabled>'
        }
        if (item.purch_block == true){
                purch_block = '<input type="checkbox" name="purch_block" value="" checked disabled>'
        } else{
                purch_block = '<input type="checkbox" name="purch_block" value="" disabled>'
        }
        edit_basic_data += '<tr><td class="class_select_checkbox"><input class="checkbox_check" onclick="valueChanged()" type="checkbox" required></td>'+
        '<td>' + item.porg_id + '</td>'+
        '<td>' + item.currency_id + '</td>'+
        '<td>' + item.payment_term_key + '</td>'+
        '<td>' + item.incoterm_key + '</td>'+
        '<td>' + gr_inv_vrf + '</td>'+
        '<td>' + inv_conf_exp + '</td>'+
        '<td>' + gr_conf_exp+ '</td>'+
        '<td>' + po_resp + '</td>'+
        '<td>' + ship_notif_exp + '</td>'+
        '<td>' + purch_block + '</td>'+
        '</tr>';
    });
    $('#supp_org_body').append(edit_basic_data);
    $("#hg_select_checkbox").prop("hidden", true);
    $(".class_select_checkbox").prop("hidden", true);
//    $('input:checkbox').removeAttr('checked');
    $('#id_edit_data').show();
    $('#id_cancel_data').hide();
    $('#id_delete_data').hide();
    $('#id_copy_data').hide();
    $('#id_update_data').hide();
    $('#id_save_confirm_popup').modal('hide');
    $('#id_delete_confirm_popup').modal('hide');
    $('#id_check_all').hide();
    table_sort_filter('display_basic_org_table');
}
// Function to get the selected row data
function get_selected_row_data(){
    $("#display_basic_org_table TBODY TR").each(function () {
        var row = $(this);
        var supp_arr_obj ={};
        supp_arr_obj.del_ind = row.find("TD").eq(0).find('input[type="checkbox"]').is(':checked');
        if(supp_arr_obj.del_ind){
            supp_arr_obj.supp_id = supplierid;
        supp_arr_obj.supp_org_guid = row.find("TD").eq(1).html();
        supp_arr_obj.porg_id = row.find("TD").eq(2).html();
        supp_arr_obj.currency_id = row.find("TD").eq(3).html();
        supp_arr_obj.payment_term = row.find("TD").eq(4).html();
        supp_arr_obj.incoterm = row.find("TD").eq(5).html();
        supp_arr_obj.gr_inv_vrf = row.find("TD").eq(6).find('input[type="checkbox"]').is(':checked');
        supp_arr_obj.inv_conf_exp = row.find("TD").eq(7).find('input[type="checkbox"]').is(':checked');
        supp_arr_obj.gr_conf_exp = row.find("TD").eq(8).find('input[type="checkbox"]').is(':checked');
        supp_arr_obj.po_resp = row.find("TD").eq(9).find('input[type="checkbox"]').is(':checked');
        supp_arr_obj.ship_notif_exp = row.find("TD").eq(10).find('input[type="checkbox"]').is(':checked');
        supp_arr_obj.purch_block = row.find("TD").eq(11).find('input[type="checkbox"]').is(':checked');
            main_table_supp_checked.push(supp_arr_obj);
        }
    });
}

// on click update icon display the selected checkbox data to update
function onclick_update_button() {
    GLOBAL_ACTION = "UPDATE"
    onclick_copy_update_button("UPDATE")
    document.getElementById("id_del_add_button").style.display = "none";
}

// on click add icon display the row in to add the new entries
function add_popup_row() {
    $("#error_msg_id").css("display", "none")
    basic_add_new_html = '';
    var display_db_data = '';
    $('#id_popup_table').DataTable().destroy();
    $(".modal").on("hidden.bs.modal", function () {
        $("#id_error_msg").html(" ");
    });
    new_row_data();   // Add a new row in popup
    if (GLOBAL_ACTION == "country_upload") {
        $(".class_del_checkbox").prop("hidden", false);
        $("#id_del_ind_checkbox").prop("hidden", false);
    }
    table_sort_filter('id_popup_table');
    $('#delete_data').hide()
}

function values_reload(){
    localStorage.setItem("supplier_guid", document.getElementById("supplier_guid").value);
    localStorage.setItem("supplier_image_id", document.getElementById("supplier_image_id").value);
    localStorage.setItem("supplier_id", document.getElementById("supplier_id").value);
    localStorage.setItem("supplier_type", document.getElementById("supplier_type").value);
    localStorage.setItem("supplier_regnum", document.getElementById("supplier_regnum").value);
    localStorage.setItem("name1", document.getElementById("name1").value);
    localStorage.setItem("name2", document.getElementById("name2").value);
    localStorage.setItem("city_id", document.getElementById("city_id").value);
    localStorage.setItem("postal_code_id", document.getElementById("postal_code_id").value);
    localStorage.setItem("street_id", document.getElementById("street_id").value);
    localStorage.setItem("country_code_id", document.getElementById("country_code_id").value);
    localStorage.setItem("currency_id", document.getElementById("currency_id").value);
    localStorage.setItem("language_id", document.getElementById("language_id").value);
    localStorage.setItem("landline_id", document.getElementById("landline_id").value);
    localStorage.setItem("mobile_num_id", document.getElementById("mobile_num_id").value);
    localStorage.setItem("fax_id", document.getElementById("fax_id").value);
    localStorage.setItem("email_id", document.getElementById("email_id").value);
     localStorage.setItem("search_term1_id", document.getElementById("search_term1_id").value);
    localStorage.setItem("search_term2_id", document.getElementById("search_term2_id").value);
    localStorage.setItem("working_days_id", $('#working_days_id').val());
    localStorage.setItem("working_days", $('#working_days').val());
    localStorage.setItem("duns_number_id", document.getElementById("duns_number_id").value);
    localStorage.setItem("output_medium_id", document.getElementById("output_medium_id").value);
}
function get_values_onerror(){
    var wdy = localStorage.getItem("working_days");
    $('#supplier_guid').val(localStorage.getItem("supplier_guid"));
//   $('#supplier_image_id').val(localStorage.getItem("supplier_image_id"));
   $('#supplier_id').val(localStorage.getItem("supplier_id"));
    $('#supplier_type').val(localStorage.getItem("supplier_type"));
   $('#supplier_regnum').val(localStorage.getItem("supplier_regnum"));
   $('#name1').val(localStorage.getItem("name1"));
    $('#name2').val(localStorage.getItem("name2"));
   $('#city_id').val(localStorage.getItem("city_id"));
   $('#postal_code_id').val(localStorage.getItem("postal_code_id"));
    $('#street_id').val(localStorage.getItem("street_id"));
   $('#country_code_id').val(localStorage.getItem("country_code_id")).attr('selected', 'selected');
   $('#currency_id').val(localStorage.getItem("currency_id")).attr('selected', 'selected');
    $('#language_id').val(localStorage.getItem("language_id")).attr('selected', 'selected');
    $('#landline_id').val(localStorage.getItem("landline_id"));
   $('#mobile_num_id').val(localStorage.getItem("mobile_num_id"));
   $('#fax_id').val(localStorage.getItem("fax_id"));
   $('#email_id').val(localStorage.getItem("email_id"));
   $('#search_term1_id').val(localStorage.getItem("search_term1_id"));
   $('#search_term2_id').val(localStorage.getItem("search_term2_id"));
    $('#working_days_id').val(localStorage.getItem("working_days_id"));
    $('#working_days').val(localStorage.getItem("working_days"));
   $('#duns_number_id').val(localStorage.getItem("duns_number_id"));
   $('#output_medium_id').val(localStorage.getItem("output_medium_id"));
   wday_array = wdy.split(",");
   var num = wdy.match(/\d/g);
   if(!(num == null)){
   $("select[id=working_days]").val(num);
   $('#working_days').selectpicker('refresh');
   }
//   return false;
}
// Function to get main table data
function get_main_table_data() {
    main_table_low_value = [];
    $('#display_basic_org_table').DataTable().destroy();
    $("#display_basic_org_table TBODY TR").each(function() {
        var row = $(this);
        var main_attribute = {};
        main_attribute.porg_id = row.find("TD").eq(2).html();
        main_table_low_value.push(main_attribute.porg_id);
    });
    table_sort_filter('display_basic_org_table');
}
function display_error_message(error_message){
    $('#error_message').text(error_message);
    document.getElementById("error_message").style.color = "Red";
    $("#error_msg_id").css("display", "block")
//    $('#id_save_confirm_popup').modal('hide');
    $('#supplierOrgModal').modal('show');
}
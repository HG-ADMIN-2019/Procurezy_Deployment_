  $(document).ready(function(){
    
      $("#supplier_form_reset").click(function(){
        $('#configform')[0].reset();
        $('#myModal').modal('hide');
      });
    
      $('#nav_menu_items').remove();
      $("body").css("padding-top", "3.7rem");
      $('.multiple_select').selectpicker();
  });


  var global_supplier_id = document.getElementById('id_supp_id')

  // Function to register supplier org data
function save_supplier_org_details() {
  var global_supplier_id = document.getElementById('id_supplier_id').value
  console.log(global_supplier_id);
  var supplier_org_data = new Array();
  $("#supp_org_details TBODY TR").each(function() {
      var row = $(this);
      var save_supp_org_data = {};
      save_supp_org_data.supp_id        = global_supplier_id;
      save_supp_org_data.porg_id        = row.find("TD").eq(0).find("select option:selected").val();
      save_supp_org_data.currency_id    = row.find("TD").eq(1).find("select option:selected").val();
      save_supp_org_data.payment_term   = row.find("TD").eq(2).find("select option:selected").val();
      save_supp_org_data.incoterm1      = row.find("TD").eq(3).find("select option:selected").val();;
      save_supp_org_data.gr_inv_vrf     = row.find("TD").eq(4).find('input[type="checkbox"]').is(':checked');
      save_supp_org_data.inv_conf_exp   = row.find("TD").eq(5).find('input[type="checkbox"]').is(':checked');
      save_supp_org_data.gr_conf_exp    = row.find("TD").eq(6).find('input[type="checkbox"]').is(':checked');
      save_supp_org_data.po_resp        = row.find("TD").eq(7).find('input[type="checkbox"]').is(':checked');
      save_supp_org_data.ship_notif_exp = row.find("TD").eq(8).find('input[type="checkbox"]').is(':checked');
      save_supp_org_data.purch_block    = row.find("TD").eq(9).find('input[type="checkbox"]').is(':checked');
      supplier_org_data.push(save_supp_org_data)
  })
  console.log(supplier_org_data)

  ajax_save_supplier_org_details(save_supp_org_data);

  document.getElementById('supplier_org_success').innerHTML = response.message;
  $('#supplier_org_success').show();

}


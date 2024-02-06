// Script to generate sort and filter feature for tables
$(document).ready( function() {
//  table_sort_filter_export_excel();
  $('#name1').val(localStorage.getItem("fname"));
  $('#name2').val(localStorage.getItem("lname"));
  $('#supplier_id').val(localStorage.getItem("supp_id"));
  $('#email').val(localStorage.getItem("supp_email"));
  $('#supplier_type').val(localStorage.getItem("supp_type"));
  $('#city').val(localStorage.getItem("city_code"));
  $('#country_code').val(localStorage.getItem("country_id"));
  $('#porg').val(localStorage.getItem("supp_porg"));
  if(localStorage.getItem("supp_purchase_block") == "true"){
        $('#purchase_block').prop("checked", true)
   }
   else{ $('#purchase_block').prop("checked", false)}
    if(form_method == 'GET'){
        $('#name1').val("");
        $('#name2').val("");
        $('#supplier_id').val("");
        $('#email').val("");
        $('#supplier_type').val("");
        $('#city').val("");
        $('#country_code').val("");
        $('#porg').val("");
        $('#purchase_block').prop("checked", false);
    }
  nav_bar_admin();
});

$("#porg").change(function () {
    if(document.getElementById("porg").value != ''){
         $('#porg_change').prop("hidden", false)
    }
    else
    {
        $('#porg_change').prop("hidden", true)
    }
})
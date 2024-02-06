$(document).ready(function(){
  $("#system_settings_form_reset").click(function(){
    $('#SystemSettingform')[0].reset();
    $('#myModal').modal('hide');
    $( "#guid").prop( "hidden", true );
  });

  $('#nav_menu_items').remove();
  $("body").css("padding-top", "3.7rem");
});

function edit_mode()
{
    $('.toggle_field').prop('disabled', false);
}

function cancel_mode()
{
    $('.toggle_field').prop('disabled', true);
    $( "#edit_sys_settings").prop( "hidden", false );
    $( "#save_sys_settings").prop( "hidden", true );
    $( "#cancel_sys_settings").prop( "hidden", true );
}

function onclick_edit()
{
    edit_mode();
    $( "#edit_sys_settings").prop( "hidden", true );
    $( "#save_sys_settings").prop( "hidden", false );
    $( "#cancel_sys_settings").prop( "hidden", false );

}

$('#acct_assignment_category').on('change', function(){
   this.value = this.checked ? 1 : 0;
});
$('#purchase_group').on('change', function(){
   this.value = this.checked ? 1 : 0;
});
$('#edit_address').on('change', function(){
   this.value = this.checked ? 1 : 0;
});
$('#recently_viewed_items').on('change', function(){
   this.value = this.checked ? 1 : 0;
});
$('#frequently_purchased_items').on('change', function(){
   this.value = this.checked ? 1 : 0;
});
$('#change_shipping_address').on('change', function(){
   this.value = this.checked ? 1 : 0;
});
 $('#limit_item').on('change', function(){
   this.value = this.checked ? 1 : 0;
});
 $('#add_favourites').on('change', function(){
   this.value = this.checked ? 1 : 0;
});

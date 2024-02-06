$(document).ready(function () {
    $('#nav_menu_items').remove();
    $("body").css("padding-top", "3.7rem");
    $('#display_basic_table').DataTable();
    table_sort_filter('display_basic_table');
});

//hide the myModal popup: Implemented Dependency delete purpose
function hideModal() {
    $('#myModal').modal('hide');
}

// Function to display button based on action
function display_button() {
    if (GLOBAL_ACTION == "DELETE") {
        $('#delete_data').show();
        $('#save_id').hide();
        document.getElementById("id_del_add_button").style.display = "none";
    } else if (GLOBAL_ACTION == "Update") {
        $('#delete_data').hide();
        $('#id_update_data').show();
    }else {
        $('#delete_data').hide();
        $('#save_id').show();
        document.getElementById('save_id').style.visibility = 'visible';
    }
}

var currPageStartIdx, currPageEndIdx, page_num=0, checked_flag=0;
// Function called on pagination
  $('#display_basic_table').on( 'page.dt', function () {
  checked_flag =0;
      var table = $('#display_basic_table').DataTable();
      var info = table.page.info();
      page_num = info.page;
      var res = table.rows().nodes();
      currPageStartIdx = info.start;
     currPageEndIdx = info.end;
      for (var i = currPageStartIdx; i < currPageEndIdx; i++) {
            if(res[i].children[0].childNodes[0].checked){
            checked_flag =1;
            }
       }
      if(checked_flag){
        $('#selectAll').prop('checked', true);
         $('#id_delete_data').show();
         $('#id_copy_data').show();
         $('#id_update_data').show();
      }
      else
      {
        $('#selectAll').prop('checked', false);
         $('#id_delete_data').hide();
         $('#id_copy_data').hide();
         $('#id_update_data').hide();
      }
});

// on click edit icon display the data in edit mode
function onclick_edit_button() {
    //display the add,cancel and upload buttons and select all checkbox,select heading and checkboxes for each row
    $('#display_basic_table').DataTable().destroy();
    $("#hg_select_checkbox").prop("hidden", false);
    $(".class_select_checkbox").prop("hidden", false);
    $(".checkbox_check").prop("hidden", false);
    $(".checkbox_check").show();
    if($('#selectAll').is(':checked')){
         $("#selectAll").prop("checked", false);
         $(".checkbox_check").prop("checked", false);
    }
    //hide the edit,delete,copy and update buttons
    $('#id_cancel_data').show();
    $('#id_edit_data').hide();
    $('#id_check_all').show();
    table_sort_filter('display_basic_table');
}
var table = $('#display_basic_table').DataTable();
 var rows_selected = [];
//onclick of select all checkbox
$('#display_basic_table tbody').on('click', 'input[class="checkbox_check"]', function(e){
     var table = $('#display_basic_table').DataTable();
      var $row = $(this).closest('tr');
      // Get row data
      var data = table.row($row).data();
      // Get row ID
      var rowId = data[0];
      // Determine whether row ID is in the list of selected row IDs
      var index = $.inArray(rowId, rows_selected);
      // If checkbox is checked and row ID is not in list of selected row IDs
      if(this.checked && index === -1){
         rows_selected.push(rowId);
      // Otherwise, if checkbox is not checked and row ID is in list of selected row IDs
      } else if (!this.checked && index !== -1){
         rows_selected.splice(index, 1);
      }
      if(this.checked){
         $row.addClass('selected');
      } else {
         $row.removeClass('selected');
      }
      // Update state of "Select all" control
//      updateDataTableSelectAllCtrl(table);
      // Prevent click event from propagating to parent
      e.stopPropagation();
   });
   // Handle click on table cells with checkboxes
//   $('#display_basic_table').on('click', 'tbody td, thead th:first-child', function(e){
//      $(this).parent().find('input[class="checkbox_check"]').trigger('click');
//   });
   // Handle click on "Select all" control
   $('thead input[id="selectAll"]', table.table().container()).on('click', function(e){
      if(this.checked){
         $('#display_basic_table tbody input[class="checkbox_check"]:not(:checked)').trigger('click');
      } else {
         $('#display_basic_table tbody input[class="checkbox_check"]:checked').trigger('click');
      }
      // Prevent click event from propagating to parent
      e.stopPropagation();
   });
   // Handle table draw event
   table.on('draw', function(){
      // Update state of "Select all" control
      updateDataTableSelectAllCtrl(table);
//      e.stopPropagation();
   });
    function updateDataTableSelectAllCtrl(table){
       var $table             = table.table().node();
       var $chkbox_all        = $('tbody input[class="checkbox_check"]', $table);
       var $chkbox_checked    = $('tbody input[class="checkbox_check"]:checked', $table);
       var chkbox_select_all  = $('thead input[id="selectAll"]', $table).get(0);

       // If none of the checkboxes are checked
       if($chkbox_checked.length === 0){
          chkbox_select_all.checked = false;
          if('indeterminate' in chkbox_select_all){
             chkbox_select_all.indeterminate = false;
          }
       // If all of the checkboxes are checked
       } else if ($chkbox_checked.length === $chkbox_all.length){
          chkbox_select_all.checked = true;
          if('indeterminate' in chkbox_select_all){
             chkbox_select_all.indeterminate = false;
          }
       } else {
          chkbox_select_all.checked = true;
          if('indeterminate' in chkbox_select_all){
             chkbox_select_all.indeterminate = true;
          }
   }
}

//------------------------------------------
//onclick of checkbox display delete,update and copy Buttons
function valueChanged() {
    if ($('.checkbox_check').is(":checked")) {
        $('#id_delete_data').show();
        $('#id_copy_data').show();
        $('#id_update_data').show();
    } else {
        $('#id_delete_data').hide();
        $('#id_copy_data').hide();
        $('#id_update_data').hide();
    }
}

//onclick of checkbox enable delete button in popup -> Dependency delete
function enableDeleteButton() {
    var $popupCheckboxes = $('#id_popup_tbody input[type="checkbox"]');
    var $deleteButton = $('#delete_data');
    // Check if any checkbox is checked in the popup
    var anyCheckboxChecked = $popupCheckboxes.is(":checked");
    // Enable or disable the delete button based on whether any checkbox is checked
    $deleteButton.prop('disabled', !anyCheckboxChecked || $popupCheckboxes.length === 0);
}


//onclick of delete,delete the row.
function application_settings_delete_Row(myTable) {
    $('#id_popup_table').DataTable().destroy();
    var uncheck_count=0

     try {
        $("#id_popup_table TBODY TR").each(function() {
            var row = $(this);
            var checked = row.find("TD").eq(0).find('input[type="checkbox"]').is(':checked')
            if (!(row.find("TD").eq(0).find('input[type="checkbox"]').is(':checked'))){
                uncheck_count ++;
            }
        });
        if (uncheck_count==0){
            $('#myModal').modal('hide');
            $('#delete_not_possible').modal('show');
        }
        else{
            var table = document.getElementById(myTable);
            var rowCount = table.rows.length;
            for (var i = 0; i < rowCount; i++) {
                var row = table.rows[i];
                var chkbox = row.cells[0].childNodes[0];
                if (null != chkbox && true == chkbox.checked) {
                    table.deleteRow(i);
                    rowCount--;
                    i--;
                }
            }
            $("#id_delete_currency").hide();
            $("#id_copy_currency").hide();
            $("#id_update_currency").hide();
            $("#error_msg_id").css("display", "none");
            table_sort_filter_popup('id_popup_table');
            return rowCount;
        }

    } catch (e) {
        alert(e);
    }
}


function display_popup(){
    $('#delete_not_possible').modal('hide');
    $('#myModal').modal('show');

}

// Function to display Description based on element Id
function display_message(id, description){
                $('#'+id).html(description);
                $('#'+id).css("display", "block");
                $('#id_save_confirm_popup').modal('hide');
                $('#myModal').modal('show');

}

//// Function to hide and display save related popups
//$('#save_id').click(function () {
//    $('#myModal').modal('hide');
//    $('#id_save_confirm_popup').modal('show');
//});

function get_message_details(msgId){
    var msg_type ;
    msg_type = message_config_details(msgId);
    $("#error_msg_id").prop("hidden", false);
    if(msg_type.message_type == "ERROR"){
        display_message("error_msg_id", msg_type.messages_id_desc)
    }
    else if(msg_type.message_type == "WARNING"){
     display_message("id_warning_msg_id", msg_type.messages_id_desc)
    }
    else if(msg_type.message_type == "INFORMATION"){
     display_message("id_info_msg_id", msg_type.messages_id_desc)
    }
}

// Function for close window button
function window_close() {
     window.history.back();
      var preUrl = document.referrer;
      window.open('', '_self', '').close();
      if (preUrl == null)
             return "The previous page url is empty";
     else
             return preUrl;
}
// Success response function
function success_response(Response){
     $('#success_msg_id').text(Response[1])
    $("#err_msg_app_settings_t").prop("hidden", false)
    table_sort_filter('id_popup_table');
     // function to display success msg based on sys setting msg interval time
    message_display_time();
}
// Function to hide the error message in data upload pop up
function cancel_upload(){
    $("#id_error_msg_upload").prop("hidden",true);
    $('#id_data_upload').modal('hide');
}
function display_file_select_error(){
    $("#id_error_msg_upload").prop("hidden",false);
    var msg = "JMSG110";
    var msg_type ;
    msg_type = message_config_details(msg);
    get_message_details(msg); // Get message details
    var display = msg_type.messages_id_desc;
    document.getElementById("id_error_msg_upload").innerHTML = display;
    document.getElementById("id_error_msg_upload").style.color = "Red";
    $('#id_data_upload').modal('show');
}
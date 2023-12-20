 // Script to generate sort and filter feature for tables
 $(document).ready( function() {
   nav_bar_timesheet();
   $('#add_update_project_name').val(localStorage.getItem("project_name"));
   $('#add_update_project_description').val(localStorage.getItem("project_desc"));
//   $('#start date').val(localStorage.getItem("start date"));
//   $('#end date').val(localStorage.getItem("end date"));
//   $('#user_type').val(localStorage.getItem("user_type"));
   $('#add_update_project_id').val(localStorage.getItem("project_id"));
   table_sort_filter_basic("project_main_table_id")
});

//onclick of upload button display id_data_upload popup and set GLOBAL_ACTION button value
function onclick_upload_button() {
    GLOBAL_ACTION = "project_upload"
  //  $("#user_tab_tbody").empty();
    $('#id_data_upload').modal('show');
    document.getElementById('id_file_data_upload').value = "";
}
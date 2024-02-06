// Script to generate sort and filter feature for tables
$(document).ready( function() {
    table_sort_filter();
    $('.multiple_select').selectpicker();
    if(form_method == ''){
        $("#status").val('')
        $("#id_time_frame").val('Today');
    }
    else
    {
        $('#status').val(localStorage.getItem("status"));
           var time = localStorage.getItem("status");
           if(!(time == null)){
            time_array = time.split(",");
            var num = time.match(/\d/g);
            $("select[id=status]").val(time_array);
            $('#status').selectpicker('refresh');
            }
            else{
                $("select[id=status]").val('');
            }
    }
});

nav_bar_approvals();

$('#search_button_id').click(function () {
    OpenLoaderPopup();
})


// Function which runs ajax script on click approve or reject button
function approve_status(value){
    OpenLoaderPopup();
    var manage_multi_status = {}
    manage_multi_status['status'] = value.id;

    $.ajax({
        type: 'POST',
        url: ajax_approval_button_url,
        data: JSON.stringify(manage_multi_status),
        success: function (response) {
            location.reload();
        },
        error: function (response) {
            console.log(response);
        }
    })
}


// Function to display notes
function approver_note(data){

    var get_text_data = {};
    get_text_data.get_approver_text = 'get_approver_text';
    get_text_data.header_guid = data.split("-")[1];

    var approver_text_result = ajax_get_approver_note(get_text_data)

    if(approver_text_result) {
        console.log(response.approver_note)
        if(response.approver_note === ""){
            $('#approval_note').empty();
            $('#approval_note').append("<h4><span class='badge badge-light'>No approver note available</span></h4>");
            $('#approver_note_modal').modal('show');
        } else {
            $('#approval_note').empty();
            $('#approval_note').append(response.approver_note);
            $('#approver_note_modal').modal('show');
        }
        
    }
    
}
function set_values(){
    localStorage.setItem("status", $('#status').val());
}
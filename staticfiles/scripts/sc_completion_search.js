    //Display submenu  for purchaser and purchaser assist role
    nav_bar_purchaser();

    $(document).ready(function() {
        var time_array = [];
        if(form_method == ''){
            document.getElementById("description").value = '';
            document.getElementById("doc_number").value = '';
            document.getElementById("changed_by").value = '';
             document.getElementById("created_at").value = 'Today';
        }
        else{
            $('#description').val(localStorage.getItem("description"));
           $('#doc_number').val(localStorage.getItem("doc_number"));
           $('#changed_by').val(localStorage.getItem("changed_by"));
           $('#created_at').val(localStorage.getItem("created_at"));
           var time = localStorage.getItem("created_at");
           if(!(time == null)){
            time_array = time.split(",");
            var num = time.match(/\d/g);
            $("select[id=created_at]").val(time_array);
            $('#created_at').selectpicker('refresh');
            }
            else{
                $("select[id=created_at]").val('Today');
            }
        }
        $('.table_sort_filter_pagination').DataTable( {
            "lengthChange": false,
            "searching":   false,
            "ordering": false,
            "info":     false
        });

    });

    $('.multiple_select').selectpicker();
    $('#search_button_id').click(function () {
        OpenLoaderPopup();
    })
    function set_values()
    {
    localStorage.setItem("description", document.getElementById("description").value);
    localStorage.setItem("doc_number", document.getElementById("doc_number").value);
    localStorage.setItem("changed_by", document.getElementById("changed_by").value);
    localStorage.setItem("created_at", $('#created_at').val());
    }
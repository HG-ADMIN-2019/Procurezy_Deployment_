    nav_bar_shop();
    let url = window.location.href;
    is_edit = false;
    split_url = url.split('/');
    last_index = split_url.slice(-1)[0];
    let document_number = 'create';

    if(last_index.includes('doc_number')){
        is_edit = true
        document_number = last_index.split('-')[1]
    }

    $(document).ready(function (){
        if(is_edit){
            no_slide_menu_style()
               
            var msg = "JMSG033";
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

            $('#edit_message').html(display + document_number_decrypted + '<a href="#" onclick="go_back_to_sc()"> go back to shopping cart</a>')
            $('#edit_message').show()
        }
    })
    
    // Function to open and initiate data-table for Product category table
    $('#choose_product_cat').click(function(){
        $('#select_prod_cat_modal').modal('show');
        setTimeout(function() {
            $('.prod_cat_datatable').DataTable( {
                "scrollY": "300px",
                "scrollCollapse": true,
            } );
        }, 500);
    })

    // Function to update Product category value
    $('#select_product_category').click(function(){
        var prod_cat_value = ''
        $('#product_category_table TBODY TR').each(function(){
            var row = $(this);
            var check = row.find("TD").eq(0).find('input[type="radio"]').is(':checked');
            if (check){
                prod_cat_id = row.find("TD").eq(1).text();
                prod_cat_desc = row.find("TD").eq(2).text();
                prod_cat_value = prod_cat_id.concat(' - ', prod_cat_desc);

                document.getElementById('choose_product_cat').value = prod_cat_value;
                $('#select_prod_cat_modal').modal('hide');
            }
        });
        $('.prod_cat_datatable').DataTable().destroy()
    });

    const go_back_to_sc = () => {
        get_document_url = localStorage.getItem('opened_document-' + document_number);
        location.href = get_document_url + '/edit';
    }

    $('#id_supplier').click(function(){
        setTimeout(function() {
            $('.select_supplier_datatable').DataTable( {
                "scrollY": "300px",
                "scrollCollapse": true,
            } );
        }, 500);
        $('#select_supplier_modal').modal('show');
    })

    // Function to update supplier value
    supplier_id = ''

    $('#select_supplier').click(function(){
        $('#supplier_table TBODY TR').each(function(){
            var row = $(this);
            var check = row.find("TD").eq(0).find('input[type="radio"]').is(':checked');

            if (check){
                supplier_desc = row.find("TD").eq(1).text();
                supplier_id = row.find("TD").eq(2).text();
                document.getElementById('id_supplier').value = supplier_id +' - '+supplier_desc;
                $('#select_supplier_modal').modal('hide');
            }
        });
    });
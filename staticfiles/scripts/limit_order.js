nav_bar_shop()


// $('#limit_form').submit(function (e) {
//     e.preventDefault();

//     item_name = document.getElementById("id_item_name").value
//     prod_cat = (document.getElementById("prod_cat_limit").value).split(' - ')[0]
//     currency = document.getElementById("id_currency").value
//     overall_limit = document.getElementById("id_overall_limit").value
//     expected_value = document.getElementById("id_expected_value").value
//     required = document.getElementById("id_required").value
//     from_date = document.getElementById("id_from_date").value
//     to_date = document.getElementById("id_to_date").value
//     on_date = document.getElementById("id_on_date").value
//     follow_up_action = $('input[name="follow_up_actions"]:checked').val();

//     limit_order_data = {};
//     limit_order_data.description = item_name;
//     limit_order_data.prod_cat = prod_cat;
//     limit_order_data.currency = currency;
//     limit_order_data.overall_limit = overall_limit;
//     limit_order_data.expected_value = expected_value;
//     limit_order_data.required = required;
//     limit_order_data.start_date = from_date;
//     limit_order_data.end_date = to_date;
//     limit_order_data.item_del_date = on_date;
//     limit_order_data.follow_up_action =  follow_up_action;
//     limit_order_data.call_off= 'Limit';

//     // Form validations for limit if errors display's relevant messages
//     is_valid = limit_item_validation(item_name, prod_cat, currency, supplier_id, follow_up_action, required, from_date, to_date, on_date, overall_limit, expected_value);
//     if (is_valid != true) {
//         document.getElementById('limit_errors').innerHTML = is_valid;
//         $('#limit_errors').show()
//         scroll_top()
//         return false;
//     } else {
//         $('#limit_errors').hide()
//     }

//     var limit_order_result = ajax_submit_limit_form(limit_order_data);

//     if(limit_order_result){
//         $('#limit_form').trigger("reset");
//         counter = document.getElementById('cart_counter').innerHTML
//         document.getElementById('limit_errors').innerHTML = '';
//         item_added_to_cart_success_popup();
//         $('#cart_counter').html(parseInt(counter) + 1)
//         supplier_id = ''
//     }
// });

const required_onchange = () => {
    value = $('#id_required').val();
    $("#id_required").width('74%')
    $('.required_date').hide()
    if (value == 'Between') {
        $('#div_from_date').show()
        $('#div_to_date').show()
    } else if (value == 'From') {
        $('#div_from_date').show()
    } else if (value == 'On') {
        $('#div_on_date').show()
    } else {
        $('.required_date').hide()
        $("#id_required").width('24%')
    }

}

// Function to open and initiate data-table for Product category table
$('#prod_cat_limit').click(function(){
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
            prod_cat_value = prod_cat_id.concat(' - ', prod_cat_desc)

            document.getElementById('prod_cat_limit').value = prod_cat_value;
            $('#select_prod_cat_modal').modal('hide');
        }
    });
})

// Function to open and initiate data-table for supplier table
$('#supp_id_limit').click(function(){
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
            document.getElementById('supp_id_limit').value = supplier_desc;
            $('#select_supplier_modal').modal('hide');
        }
    });
});
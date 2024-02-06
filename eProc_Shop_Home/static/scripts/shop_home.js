var document_number = 'create';
is_edit = false;
var GLOBAL_EFORM_FLAG
$(document).ready(function(){
    generic_carousel_slider_products();
    generic_carousel_slider_fav_sc();
    $('#nav_menu_items').remove();

});

function generic_carousel_slider_products() {
    $(".generic_carousel_slider_products").owlCarousel({
        items:5,
        navigation:true,
        navigationText:['<i class="fas fa-chevron-left" aria-hidden="true"></i>','<i class="fas fa-chevron-right" aria-hidden="true"></i>'],
        responsive: true,
    });
}

function generic_carousel_slider_fav_sc() {
    $(".generic_carousel_slider_fav_sc").owlCarousel({
        items:4,
        navigation:true,
        navigationText:['<i class="fas fa-chevron-left" aria-hidden="true"></i>','<i class="fas fa-chevron-right" aria-hidden="true"></i>'],
        responsive: true,
    });
}

function TriggerOutlook() {        

    var body = '';
    var email = "{{support_email.org_support_email}}";
    var subject = "Majjaka Customer Support";

    window.location.href = "mailto:"+email+"?"
}   


 // Delete favourite shopping cart
 let delete_favourite_cart_num = '';
 function FavScDelete(fav_cart_num) {
    delete_favourite_cart_num = fav_cart_num;
    $('#delete-favourite-cart-popup').modal('show');
}


function delete_favourite_cart () {
    let data = {}
    data.fav_cart_num = delete_favourite_cart_num
    ajax_delete_favourite_shopping_cart(data)
    $('#delete-favourite-cart-popup').modal('hide');
    $("#fav_sc_card_"+delete_favourite_cart_num).remove();
}

// Delete recently viewed items
function RviDelete(item_prod_id) {
    event.preventDefault();
   
    let data = {}
    data.item_prod_id = item_prod_id
    OpenLoaderPopup();
    $.ajax({
        type: 'POST',
        url: ajax_delete_rvi_url,
        data: data,
        success: function (response) {
            $("#rvi_card_"+item_prod_id).remove();
            if(response.recently_viewed_count == 0){
                document.getElementById("recently_viewed_product").style.display = "none";
            }
            CloseLoaderPopup();
        }, 
        error: function(response) {
            console.log(response);
        }
    });

}

var GLOBAL_QUANTITY = 0;
var GLOBAL_FROM_ID = '';
var GLOBAL_EFORM_GUID = []



function add_freetext(supplier_id,prd_id, price){
 let catalog_item = {};
    catalog_item["prod_cat"] = prd_id;
    catalog_item['call_off'] = '02';
    catalog_item["quantity"] = 1;
    catalog_item["document_number"] = document_number;
    catalog_item["supplier_id"] = supplier_id;
    catalog_item["eform_data"] = 'create';
    catalog_item["price"] = price;
    catalog_url = '/add_item/update_or_create_item/' + document_number;

    var add_catalog_response = ajax_add_catalog_item(catalog_url, catalog_item);

    if(add_catalog_response) {
        if (!is_edit) {
            if(response.cart_count){
                counter = document.getElementById('cart_counter').innerHTML
                $('#cart_counter').html(parseInt(counter)+1)
                item_added_to_cart_success_popup()
            } else if(response.error) {
                alert( response.error)
            }
        } else {
            $('#confirm_add_item').modal('show')
        }
        $('document').find('input:number').val('');
    }
}

// Function to ADD TO CART from veiw product details pop up
function add_catalog_popup(){
    let catalog_item = {};
    catalog_item["prod_id"] = GLOBAL_PRODUCT_ID;
    catalog_item["call_off"] = '01'
    catalog_item["quantity"] = document.getElementById("id_quantity").value;
    catalog_item['eform_id'] = ''
    catalog_item['eform_detail'] = ''
    catalog_item['item_total_value'] = $("#id_price").text();
    let header_guid = '';
    var eform_check =true

//    if(is_edit){
//        header_guid = window.sessionStorage.getItem('sc_header_guid');
//    }
    catalog_item["document_number"] = document_number;
    if(GLOBAL_EFORM_FLAG){
        catalog_item['eform_id'] = document.getElementById("eform_id").textContent;
        eform_check = validate_eform()
        catalog_item['eform_detail'] = get_eform_data()
        catalog_item['quantity_guid'] = GLOBAL_QUANTITY.eform_field_config_guid
    }

    if(eform_check){
        var add_catalog_response = ajax_catalog_product(catalog_item);

        if (add_catalog_response) {
            if (!is_edit) {
                if(response.cart_count){
                    //counter = document.getElementById('cart_counter').innerHTML
                    CartCounterView(response.cart_count);
                    item_added_to_cart_success_popup();
                }
            } else {
                $('#confirm_add_item').modal('show')
            }
            $('document').find('input:number').val('');
        }
    }
    else{
        alert("please enter all fields")
    }
}

//validate eform data
function validate_eform(){
    var check_flag = true
    $('.dummy_eform_class').each(function() {
        if(this.value === "") {
            check_flag = false
        }
    });
    return check_flag
}

// get eform data
function get_eform_data(){
    var eform_data = []
    $('.dummy_eform_class').each(function() {
        var eform_data_dictionary ={}
        var option_value = this.value
        if(GLOBAL_EFORM_FLAG)
        {
            drop_down = option_value.split("|")
            if (drop_down.length == 3 ){
                eform_data_dictionary = {'pricing_type':'WITHOUT_PRICING','eform_field_data':drop_down[1],
                'variant_config_guid':this.id,'eform_id':GLOBAL_FROM_ID,'eform_field_name':drop_down[0],
                'eform_field_count':drop_down[2]}
            }
            else{
                eform_data_dictionary = {'pricing_type':drop_down[1],'eform_field_data':drop_down[3],'eform_field_name':drop_down[0],
                'pricing_data':drop_down[2],'variant_config_guid':this.id ,'eform_id':GLOBAL_FROM_ID,'eform_field_count':drop_down[5]}
            }

        }
        eform_data.push(eform_data_dictionary)
    });
    return eform_data
}

function add_favourite_cart(fav_cart_num){
    let data = {}
    data.fav_cart_num = fav_cart_num
    response = ajax_add_fav_cart(data)
    item_added_to_cart_success_popup()
    $('#cart_counter').html(response.cart_count)

}
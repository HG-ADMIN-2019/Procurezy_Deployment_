let url = window.location.href
is_edit = false
split_url = url.split('/')
last_index = split_url.slice(-1)[0]
let document_number = 'create';
var GLOBAL_EFORM_FLAG = false
var GLOBAL_EFORM_GUID = []
var GLOBAL_BASE_PRICE = 0
var GLOBAL_QUANTITY = []
var GLOBAL_FROM_ID = ''
if(last_index.includes('doc_number')){
    is_edit = true
    document_number = last_index.split('-')[1]
    $('#quick_links_catalog').css('pointer-events', 'none')
}

$(document).ready(function() {
    nav_bar_shop();

    $("#product_detail_popup").on("contextmenu",function(){
        return false;
    });
 
    $('.collapse').on('hidden.bs.collapse', function (){
        $(this).parent().find('.fa-chevron-up').css({'transform': 'rotateZ(180deg)'})
    }).on('shown.bs.collapse', function (){
        $(this).parent().find('.fa-chevron-up').css({'transform': 'rotateZ(0deg)'})
    });
 
    // localStorage.removeItem("previously_selected_link");
    // $('.sidenav__listitem').removeClass('sidenav__listitem-active');
    // document.getElementById('sidenav__listitem-shop').classList.add('sidenav__listitem-active');
    // localStorage.setItem("previously_selected_link", "sidenav__listitem-shop");
})

//  To be reviewed
$('button').hover(function () {
    let titlename= $(this).text();
    this.title = titlename;
});

// on click of purchase requition in quick links
const purchase_requisition_url = () => {
    url = '/add_item/purchase_requisition/' + document_number
    location.href = url
}

//############################### START ONCLICK OF INPUT TEXT IN SEARCH FIELD ##############################################
function open_search_modal(){
    if(GLOBAL_SEARCH_TYPE){
        $("#button_action").css("display", "none");
    }
    else{
        $("#button_action").css("display", "block");
    }
    // $("#prod_service_search").modal('toggle');
}
//############################### END ONCLICK OF INPUT TEXT IN SEARCH FIELD ##############################################

//################################## START SEARCH TYPE ###############################################################

function search_type(data) {
    var result = data.value;
    GLOBAL_PROD_SEARCH_TYPE = data.value;
    var search_ele = "<button style='cursor: auto;' class='btn btn-light mr-2' id='catalog_filter_select_value' value="+
     result + ">" + result +"<span style='cursor: pointer; margin-left: 5px;' aria-hidden='true' onclick='hg_search_term_close()'>&times;</span></button>"
    $("#catalog_filter_select").html(search_ele)
}

function hg_search_term_close() {
    GLOBAL_PROD_SEARCH_TYPE = 'ALL';
    $("#catalog_filter_select_value").remove()
}
//################################## END SEARCH TYPE ###############################################################

// Function to toggle between product selection tabs
function openTab(evt, tabName) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("product-selection-tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("hg_tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
}

// Function to generate url in products result filter card
const generate_url = (selected_catalog, type, id) => {
    if(document_number != 'create'){
        send_doc_number = 'doc_number-' + document_number;
    } else {
        send_doc_number = document_number ;
    }
    var selected_classfication_text = $('#text-'+id).text();
    $(".prod-classification-select-link").removeClass("active");
    sessionStorage.setItem("prod_classification_select_id", id);
    sessionStorage.setItem("prod_classification_select_type", type);
    sessionStorage.setItem("prod_classification_select_text", selected_classfication_text);

    url = '/shop/products_services/' + selected_catalog + '/' + type + '/' + id + '/' + send_doc_number;
    location.href = url;
}

$(document).ready(function(){
    var previously_selected_classification_link_id = sessionStorage.getItem('prod_classification_select_id');
    var previously_selected_classification_link_type = sessionStorage.getItem('prod_classification_select_type');

    if(previously_selected_classification_link_id) {
        $(".prod-classification-select-link").removeClass("active");

        if(previously_selected_classification_link_type == 'prod_category'){
            $('#classification-' + previously_selected_classification_link_type + "-" + previously_selected_classification_link_id).addClass("active");
        } else if(previously_selected_classification_link_type == 'supplier') {
            $('#classification-' + previously_selected_classification_link_type + "-" + previously_selected_classification_link_id).addClass("active");
        }

        display_result_text()
        
    }
})


function display_result_text() {
    var get_hild_text = $('.prod-classification-select-link.active').children().first().text();
    $('#results-text').text(get_hild_text);
}


// Function to generate url for freetext form
const freetext_url = (encrypted_freetext_id) => {
    if(document_number != 'create') {
        send_doc_number = 'doc_number-' + document_number;
        ViewFreetextItemWindow(send_doc_number, encrypted_freetext_id);
        
    } else {
        send_doc_number = document_number;
        get_freetext_url = '/add_item/free_text/' + encrypted_freetext_id + '/' + send_doc_number
        window.open(get_freetext_url);
    }
    
}

// Function to go back to previosly opend document 
const go_back_to_sc = () => {
    get_document_url = localStorage.getItem('opened_document-' + document_number)
    location.href = get_document_url + '/edit'
}
const go_back_to_sc_search = (encrypt_doc_num) => {
    get_document_url = localStorage.getItem('opened_document-' + encrypt_doc_num)
    location.href = get_document_url + '/edit'
}


//###################################################### START VIEW CATALOG DETAIL POPUP ############################################

function change_price(price_value){
    var select_price_option = price_value.split('|')
    var price = ''
    quantity = document.getElementById("id_quantity").value
    if (select_price_option[1]=='VARIANT_BASE_PRICING'){
        $("#id_prod_desc").text(select_price_option[6] + ' ');
        price = select_price_option[2]
        let quantity_range = get_price_range(quantity)
            console.log(quantity_range)
        var price_percentage = get_percentage_by_quantity(quantity_range)
        if(quantity_range !== 0){
            GLOBAL_BASE_PRICE = parseFloat(price)*(100- (parseFloat(price_percentage)))/100
        }
        else{
            GLOBAL_BASE_PRICE = parseFloat(price)
        }

        var item_price = GLOBAL_BASE_PRICE
        $('.dummy_eform_class').each(function() {
            var select_value = this.value
            var select_value_split = select_value.split('|')
            if (select_value_split[1]=='VARIANT_ADDITIONAL_PRICING'){
                item_price = calculate_item_value_based_on_operator(select_value_split[2],select_value_split[4],item_price)
            }
       });
       item_price = item_price *parseInt(quantity)
        $("#id_price").text(item_price);
    }
    if((select_price_option[1]=='VARIANT_ADDITIONAL_PRICING')||(select_price_option[1]=='QUANTITY_BASED_DISCOUNT')){
        var item_price = GLOBAL_BASE_PRICE
        $('.dummy_eform_class').each(function() {
            var select_value = this.value
            var select_value_split = select_value.split('|')
            if (select_value_split[1]=='VARIANT_ADDITIONAL_PRICING'){
                item_price = calculate_item_value_based_on_operator(select_value_split[2],select_value_split[4],item_price)
            }
       });
       item_price = parseFloat(item_price)*parseInt(quantity)
        $("#id_price").text(item_price);
    }

}



//###########################  start based on selected operator get sign #######################3
function calculate_item_value_based_on_operator(differential_value,operator,item_price){
    var item_value = 0;
    switch(operator){
        case 'PLUS':
            item_value = parseInt(item_price)+parseInt(differential_value)
            break;
        case 'MINUS':
            item_value = parseInt(item_price)-parseInt(differential_value)
            break;
        case 'PERCENTAGE':
            item_value = (parseInt(item_price)*(100 - parseInt(differential_value)))/100
            break;
        default:
            break;

    }
    return item_value

}
//########################### end based on selected operator get sign #######################3


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

    if(is_edit){
        header_guid = window.sessionStorage.getItem('sc_header_guid');
    }
    catalog_item["document_number"] = document_number;
    if(GLOBAL_EFORM_FLAG){
        catalog_item['eform_id'] = eform_id
        eform_check = validate_eform()
        catalog_item['eform_detail'] = get_eform_data()
        catalog_item['quantity_guid'] = GLOBAL_QUANTITY.eform_field_config_guid
    }

    if(eform_check){
        var add_catalog_response = ajax_catalog_product(catalog_item);

        if (add_catalog_response) {
        $('#prod_detail_popup').modal('hide');
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
           
        var msg = "JMSG007";
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
       var display5 = msg_type.messages_id_desc;
        alert(display5+ "all fields")
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
    $('.dummy_class_price_data').each(function() {
        var eform_data_dictionary ={};
        var selected_price_id = this.id;
        drop_down = selected_price_id.split("-");
        //eform_detail = get_eform_ui_detail(drop_down[1],drop_down[2])
        eform_data_dictionary = {'pricing_type':drop_down[0],
                                    'variant_config_guid':drop_down[1],
                                    'eform_id':GLOBAL_FROM_ID,
                                    'product_eform_pricing_guid':drop_down[2]}

        eform_data.push(eform_data_dictionary)
    });
    $('.dummy_eform_class').each(function() {
        var eform_data_dictionary ={}
        var selected_price_id = this.value
        drop_down = selected_price_id.split("-")
        eform_data_dictionary = {'pricing_type':drop_down[0],
                                 'variant_config_guid':drop_down[1],
                                 'eform_id':GLOBAL_FROM_ID,
                                 'data':drop_down[2],
                                 'product_eform_pricing_guid':''}
        eform_data.push(eform_data_dictionary)
    });
    return eform_data
}

function get_eform_ui_detail(eform_config_guid,eform_pricing_guid){
    var eform_detail = {}
    $.each(eform_detail, function (i, eform_config) {
        if(eform_config.eform_field_config_guid==eform_config_guid){
             $.each(eform_config.pricing, function (i, eform_pricing) {
                if (eform_pricing.product_eform_pricing_guid == eform_pricing_guid){
                    eform_detail = eform_pricing
                }
             });

        }
    });
    return eform_detail
}



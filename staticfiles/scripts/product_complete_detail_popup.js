var eform_detail
var eform_id
var product_price
var GLOBAL_QUANTITY 
var prod_image_data =''
var GLOBAL_BASE_PRICE 

function view_detail(prd_detail, prd_catalog_id){
    GLOBAL_PRODUCT_ID = prd_detail;
    OpenLoaderPopup();
    product_cat_id={}
    product_cat_id["prod_id"] = prd_detail;
    product_cat_id["catalog_id"] = prd_catalog_id
    GLOBAL_FROM_ID = ''
    var view_detail_response = ajax_view_prod_detail(product_cat_id);
    var response = view_detail_response.prod_detail[0]
    var discount_data_dictionary = view_detail_response.quantity_dictionary;
    if(response) {
        currency_id = response[0].currency_id
        $("#id_currency").text(response[0].currency_id + ' ');
        $("#id_prod_desc").text(response[0].long_desc);
        $("#id_prod_desc").attr("disabled", "disabled");
        $("#id_desc").text(response[0].short_desc + ' ');
        $("#id_lead_time").text(response[0].lead_time);
        $("#id_lot_size").text(response[0].price_unit);
        $("#id_quantity").val("1");
        $("#id_unspsc_cat").text(response[0].unspsc);
        $("#eform_id").text(response[0].eform_id);
        $("#id_price").text(response[0].price);
        $("#min_order_qty_popup").text(response[0].quantity_min);
        $("#lead_time_popup").text(response[0].lead_time);
        GLOBAL_BASE_PRICE = response[0].price;
        $("#id_unit").text(response[0].unit);
        $("#id_supp").text(response[0].supplier_id);
        eform_detail = view_detail_response.eform_detail;
        eform_id = response[0].variant_id;
        if (eform_id){
            GLOBAL_EFORM_FLAG = true
        }
        else{
            GLOBAL_EFORM_FLAG = false
        }
        product_price = response[0].price;
        GLOBAL_QUANTITY = view_detail_response.quantity_dictionary
        var product_specification = view_detail_response.product_specification
        GLOBAL_FROM_ID = response[0].eform_id
        $('#discount_info_body').empty();
        $('#eform_body').empty();
        $('#vwbp_options_body').empty();
        $('#vwap_options_body').empty();
        // update_eform_data(eform_detail)
        $('#vwobp_dropdown_body').empty();
        create_eform_fields(eform_detail);

        if( Object.keys(discount_data_dictionary).length !== 0) {
            var discount_pricing_data = discount_data_dictionary.variant_data
            display_discount_inforrmation(discount_pricing_data);
        }
        if (product_specification.length != 0){
            update_product_specification(product_specification);
        }
        else{
            document.getElementById('prod_spec_div_id').style.display = 'none';
        }
        static_url = '/media/';
        prod_img_detail = view_detail_response.prod_img_detail

        if (prod_img_detail[0]){
            $('#image_featured').attr('src',static_url+ prod_img_detail[0].image_url);
        }
        else{
            $('#image_featured').attr('src',"/static/images/no-image-cropped.png");
        }
        for(i=0; i<prod_img_detail.length; i++){
            var num = i+1
            var num_increment = num.toString()
            var image_id = '#img_'+num_increment
            if (prod_img_detail[i]){
                $(image_id).attr('src',static_url+ prod_img_detail[i].image_url);
            }
            else{
                $(image_id).attr('src',"/static/images/no-image-cropped.png");
            }
        }

        image_visible_div = 0
        // show_image_div()
        $('#prod_detail_popup').modal('show');
        CloseLoaderPopup();
    }
}




function update_eform_data(eform_configured){
    console.log(eform_configured);
    if (eform_configured.length > 0) {
        GLOBAL_EFORM_FLAG = true
        $('#eform_body').empty()
        var div_content = '';
        $.each(eform_configured, function (index, value) {
            var line_separator = '';
            eform_field_datatype = value['eform_field_datatype']
            eform_field_name = value['eform_field_name']
            eform_field_count = value['eform_field_count']
            required_flag = value['required_flag']
            var eform_guid = value['eform_field_config_guid']
            GLOBAL_EFORM_GUID.push(eform_guid)
            if ((index + 1) % 2 == 0) {
                line_separator = '<div class="w-100"></div>'
            }

            var options = ''

            if (eform_field_datatype == 'DROPDOWN') {
				var eform_field_data = value['eform_field_data']
				if (eform_field_data){
                    get_dropdown = eform_field_data.split('|~#')
                }
                else{
                    get_dropdown = eform_field_data
                }
				var eform_price_flag = value['price_flag']
				if(eform_price_flag){
                    get_dropdown_price = value['pricing']
                }
                else{
                    get_dropdown_price = []
                }

                var product_description =''
				if(get_dropdown_price.length>0){
					for (i = 0; i < get_dropdown_price.length; i++) {
					    var price_dictionary = get_dropdown_price[i]
					    if ((price_dictionary['pricing_type'] == 'VARIANT_BASE_PRICING') && (price_dictionary['pricing_data_default'] == true)){
					        GLOBAL_BASE_PRICE = price_dictionary['price']
					        //$("#id_desc").text(get_dropdown_price[0].product_description + ' ');
					    }
					    if (price_dictionary['pricing_type'] == 'VARIANT_BASE_PRICING'){
					        $("#id_prod_desc").text(get_dropdown_price[0].product_description + ' ');
					        product_description = price_dictionary['product_description']
					        console.log(price_dictionary)
					    }
					    else{
					        product_description = '';
					    }


						options += '<option value="' + eform_field_name + '|' + price_dictionary['pricing_type'] + '|'+price_dictionary['price']+'|'+price_dictionary['pricing_data']+'|'+price_dictionary['operator']+'|'+eform_field_count+'|'+product_description+'">' + price_dictionary['pricing_data'] + ' </option>'

					}
				}
				else{
				    options = '<option value="" selected>Select</option>'
					for (i = 0; i < get_dropdown.length; i++)
					{
						options += '<option value="' + eform_field_name + '|' + get_dropdown[i] + '|'+eform_field_count+'">' + get_dropdown[i] + ' </option>'
					}

				}


                if (get_dropdown_price.length>0){
                div_content = '<div id="array_index-' + index + '" class="form-group col-6"><label  for="' + eform_field_name + '">' + eform_field_name + ':' + '</label><span id="span_' + eform_field_name + '" ></span><br><select id="' + eform_guid + '" class="form-control toggle_mode '+value['drop_down_type']+' dummy_eform_class" onchange = "change_price(this.value)">' + options + '</select></div>' + line_separator
                }
                else{
                div_content = '<div id="array_index-' + index + '" class="form-group col-6"><label  for="' + eform_field_name + '">' + eform_field_name + ':' + '</label><span id="span_' + eform_field_name + '" ></span><br><select id="' + eform_guid + '" class="form-control toggle_mode '+value['drop_down_type']+' dummy_eform_class">' + options + '</select></div>' + line_separator
                }
            }
            else if (eform_field_datatype == 'checkbox') {
                div_content = '<div id="array_index-' + index + '" class="form-group col-6"><label  for="' + eform_field_name + '">' + eform_field_name + ':' + '</label><span id="span_' + eform_field_name + '" ></span><br><input class="form-control toggle_mode dummy_eform_class" type="' + eform_field_datatype + '"><button style="margin-top:0.5rem" id="' + eform_field_name + '-' + index + '" type="button" onclick="remove_element(this.id)"  class="btn btn-danger btn-sm btn-delete"><i class="far fa-trash-alt"></i></button></div>' + line_separator
            }
            else {
                div_content = '<div id="array_index-' + index + '" class="form-group col-6"><label  for="' + eform_field_name + '">' + eform_field_name + ':' + '</label><span id="span_' + eform_field_name + '" ></span><br><input class="form-control toggle_mode dummy_eform_class" type="' + eform_field_datatype + '"><button style="margin-top:0.5rem" id="' + eform_field_name + '-' + index + '" type="button" onclick="remove_element(this.id)"  class="btn btn-danger btn-sm btn-delete"><i class="far fa-trash-alt"></i></button></div>' + line_separator
            }

            $('#eform_body').append(div_content)
            if (required_flag) {
                document.getElementById('span_' + eform_field_name).classList.add("hg_required")
                // $('#span_' + eform_field_name).html('*')
            }
        });
        $('#eform_details').show()
    }
}


function update_product_specification(product_specification){
    $('#product_spec_main_tbody').empty();
    var prod_spec_main_html = ''
    $.each(product_specification, function (i, item) {
        prod_spec_main_html += '<tr ><td>' + item.product_info_key + '</td><td>' + item.product_info_value + '</td></tr>';
    });
    $('#product_spec_main_tbody').append(prod_spec_main_html);
    document.getElementById('prod_spec_div_id').style.display = 'block';
}
//onclick of upload button display id_data_upload popup and set GLOBAL_ACTION button value
function onclick_upload_button() {
    GLOBAL_ACTION = "product_upload"
    $("#id_popup_tbody").empty();
    $('#id_data_upload').modal('show');
    document.getElementById('id_file_data_upload').value = "";
}

var image_thumbnail = document.getElementsByClassName('image-thumbnail');
var image_thumbnail_select = document.getElementsByClassName('prod-img-selected');

for(i=0; image_thumbnail.length > i; i++){

    image_thumbnail[i].addEventListener('click', function(){

        if(image_thumbnail_select.length > 0){
            image_thumbnail_select[0].classList.remove('prod-img-selected');
        };
        this.classList.add('prod-img-selected');
        var new_src = this.src;
        document.getElementById('image-featured').src = new_src;
    });

};

// Funtion to create eform fields
const create_eform_fields = (eform_detail) => {
    eform_detail.forEach(eform_data => {
        console.log(eform_detail)
        var variant_type = eform_data.dropdown_pricetype;
        var eform_field_config_guid = eform_data.variant_config_guid;
        var eform_field_variant_options = eform_data.variant_data.split('|~#');
       
        if(variant_type == 'VARIANT_WITHOUT_PRICING') {
            
            $('#product-detail-section__vwobp').show();
            var vwobp_options = '<option value="" selected>Select</option>';
            
            eform_field_variant_options.forEach(variant_options => {
                vwobp_options += '<option value="VARIANT_WITHOUT_PRICING-'+eform_field_config_guid+'-'+variant_options+'">'+variant_options+'</option>'
            })
            data =  '<div class="col-sm-6">'+
                    '<h5>'+eform_data.variant_name+'</h5>'+
                    '<select class="form-control dummy_eform_class">'+ vwobp_options + '</select>'+
                    '</div>'
            $('#vwobp_dropdown_body').append(data);
        }

        else if(variant_type == 'VARIANT_BASE_PRICING') {
            $('#product-detail-section__vwbp').show();
            $('#product-detail-section__vwbp-field-name').html(eform_data.variant_name);
            var vwbp_options_body = ''
            eform_data.pricing.forEach(variant_data_type => {
                var default_card_class = ''
                if(variant_data_type.pricing_data_default == true) {
                    default_card_class = 'selected-vwbp dummy_class_price_data'
                }
                
                vwbp_options_body += '<div class="col-sm-4 select-option-item" >'+ 
                    '<div class="select-option-item__card '+default_card_class+'" id="VARIANT_BASE_PRICING-'+eform_field_config_guid+'-'+variant_data_type.product_eform_pricing_guid+'"  onclick="update_price(this.id)">'+
                    '<div class="select-option-item__card-body">'+
                    '<span class="card-main-text">'+variant_data_type.pricing_data+'</span>'+
                    '<span class="card-sub-text">'+variant_data_type.product_description+', '+variant_data_type.price+'</span>'+
                    '</div>'+
                    '</div>'+
                    '</div>'
            });
            $('#vwbp_options_body').append(vwbp_options_body);
        }

        else if(variant_type == 'VARIANT_ADDITIONAL_PRICING') {
            $('#product-detail-section__vwap').show();
            $('#product-detail-section__vwap-field-name').html(eform_data.eform_field_name);
            var vwap_options_body = ''
            eform_data.pricing.forEach(variant_data_type => {
                var default_card_class = ''
                if(variant_data_type.pricing_data_default == true) {
                    default_card_class = 'selected-vwap dummy_class_price_data'
                }
                
                vwap_options_body += '<div class="col-sm-3 select-option-item" >'+ 
                    '<div class="select-option-item__card '+default_card_class+'" id="VARIANT_ADDITIONAL_PRICING-'+eform_field_config_guid+'-'+variant_data_type.product_eform_pricing_guid+'"  onclick="update_price(this.id)">'+
                    '<div class="select-option-item__card-body">'+
                    '<span class="card-main-text">'+variant_data_type.pricing_data+'</span>'+
                    '<span class="card-sub-text"> + '+variant_data_type.price+'</span>'+
                    '</div>'+
                    '</div>'+
                    '</div>'
            });
            $('#vwap_options_body').append(vwap_options_body);
        }
    }); 
}


const display_discount_inforrmation = (discount_pricing_data) => {
    $('#product-detail-section__discount').show();
    var discount_info_body = '';
    discount_pricing_data.forEach(dicount_data => {
        discount_info_body += '<div class="discount-label-text">'+
                                    '<i class="material-icons">discount</i>'+
                                    '<span>'+dicount_data.discount_percentage_value+'% off on minimum '+dicount_data.discount_min_quantity+' quantity</span>'+
                               '</div>'
    })
    $('#discount_info_body').append(discount_info_body);
}



function update_price(price_value){
    var select_price_option = price_value.split('-')
    var price = get_price(select_price_option[1],select_price_option[2])
    quantity = document.getElementById("id_quantity").value
    if (select_price_option[0]=='VARIANT_BASE_PRICING'){
        remove_base_class()
        $("#"+price_value).addClass("selected-vwbp")
        $("#"+price_value).addClass("dummy_class_price_data")

        //$("#id_prod_desc").text(select_price_option[6] + ' ');
        //price = select_price_option[2]
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
        $('.selected-vwap').each(function() {
            var select_value = this.id
            var select_value_split = select_value.split('-')
            if (select_value_split[0]=='VARIANT_ADDITIONAL_PRICING'){
                var additional_price = get_price(select_value_split[1],select_value_split[2])
                item_price = calculate_item_value_based_on_operator(additional_price,'PLUS',item_price)
            }
       });
       item_price = item_price *parseInt(quantity)
        $("#id_price").text(item_price);
    }
    if(select_price_option[0]=='VARIANT_ADDITIONAL_PRICING'){
        remove_additional_class(select_price_option[1])
        $("#"+price_value).addClass("selected-vwap")
        $("#"+price_value).addClass("dummy_class_price_data")
        var item_price = GLOBAL_BASE_PRICE
        $('.selected-vwap').each(function() {
            var select_value = this.id
            var select_value_split = select_value.split('-')
            if (select_value_split[0]=='VARIANT_ADDITIONAL_PRICING'){
                var additional_price = get_price(select_value_split[1],select_value_split[2])
                item_price = calculate_item_value_based_on_operator(additional_price,'PLUS',item_price)
            }
       });
       item_price = parseFloat(item_price)*parseInt(quantity)
        $("#id_price").text(item_price);
    }

}

function get_price(eform_config_guid,eform_pricing_guid){
    var price = 0
    $.each(eform_detail, function (i, eform_config) {
        if(eform_config.variant_config_guid==eform_config_guid){
             $.each(eform_config.pricing, function (i, eform_pricing) {
                if (eform_pricing.product_eform_pricing_guid == eform_pricing_guid){
                    price = eform_pricing.price
                }
             });

        }
    });
    return price
}

function remove_base_class(){
    $('.selected-vwbp').each(function() {
        $(this).removeClass("selected-vwbp");
        $(this).removeClass("dummy_class_price_data");
    });
}

function remove_additional_class(eform_config_guid){
    $.each(eform_detail, function (i, eform_config) {
        if(eform_config.variant_config_guid==eform_config_guid){
             $.each(eform_config.pricing, function (i, eform_pricing) {
                var id_value = 'VARIANT_ADDITIONAL_PRICING-'+eform_config.variant_config_guid+'-'+eform_pricing.product_eform_pricing_guid+'';
                $("#"+id_value ).removeClass("selected-vwap");
                $("#"+id_value).removeClass("dummy_class_price_data")
             });

        }
    });
}

var quantity_range = '';
function get_price_range(quantity){
    var range = 0
    var min  = 0
    var range_flag = false
    var max_flag = false
    var max_quantity =0
    var price_percentage =0
    $.each(GLOBAL_QUANTITY.variant_data, function (i, item) {
        if((GLOBAL_QUANTITY.variant_data.length)==(i)){
            max_quantity = parseFloat(9999999999999999999999999)
            max_flag = true
        }
        else{
            max_quantity = item.discount_min_quantity
        }

        range_flag = inRange(parseFloat(quantity),min,parseFloat(max_quantity)-1)
        if(range_flag){

            var range = min
            console.log("retutn 1")
            quantity_range = min
            return quantity_range
        }
        else{
             if((GLOBAL_QUANTITY.variant_data.length-1)==(i))
            {
                if(parseFloat(quantity) >= parseFloat(max_quantity))
                {
                console.log("retutn 2")
                quantity_range = max_quantity
                price_percentage = item.discount_percentage_value
                    return quantity_range
                }
            }
            else{
                min =item.discount_min_quantity
            }
        }
    });
    return quantity_range
 }
function get_percentage_by_quantity(quantity_range){
    if(GLOBAL_QUANTITY.length != 0){
         for(var i=0; i<GLOBAL_QUANTITY.variant_data.length; i++ ){
            if (quantity_range == GLOBAL_QUANTITY.variant_data[i].discount_min_quantity){
                return GLOBAL_QUANTITY.variant_data[i].discount_percentage_value;
            }
        }
    }
    return 0
}


function inRange(x, min, max) {
    return ((x-min)*(x-max) <= 0);
}


var quantity_flag = true
function on_change_quantity(action){

    var range = 0
    var min  = 0
    var range_flag = false
    quantity_flag = true
    var quantity_range = 0
    var price_percentage = 0
    quantity = document.getElementById("id_quantity").value
    if(!quantity){
        quantity = 1
        document.getElementById("catalog_quantity").value = quantity
    }
    if(parseInt(quantity) == 0){
        quantity = 1
        document.getElementById("catalog_quantity").value = quantity
    }
    if (action == 'INCREMENT'){
        quantity = parseInt(quantity)+1;
    }
    else if(action == 'DECREMENT'){
        if(parseInt(quantity) > 1)
        {
            //quantity_flag = false
            quantity = parseInt(quantity)-1;
        }
    }
    if (quantity_flag){
        if(GLOBAL_QUANTITY.length != 0){
            quantity_range = get_price_range(quantity)
        }
        //var without_discount = GLOBAL_BASE_PRICE
        console.log(without_discount)
        if(GLOBAL_QUANTITY.length != 0){
            price_percentage = get_percentage_by_quantity(quantity_range)
        }
        $('.selected-vwbp').each(function() {
                var select_value = this.id
                var select_value_split = select_value.split('-')
                if (select_value_split[0]=='VARIANT_BASE_PRICING'){
                    GLOBAL_BASE_PRICE = get_price(select_value_split[1],select_value_split[2])
                }
           });
           var without_discount = GLOBAL_BASE_PRICE
        if(quantity_range !== 0)
        {
            GLOBAL_BASE_PRICE = GLOBAL_BASE_PRICE*(100 - parseFloat(price_percentage))/100
        }
        var item_price = GLOBAL_BASE_PRICE
        console.log(item_price)
            $('.selected-vwap').each(function() {
                var select_value = this.id
                var select_value_split = select_value.split('-')
                if (select_value_split[0]=='VARIANT_ADDITIONAL_PRICING'){
                    var additional_price = get_price(select_value_split[1],select_value_split[2])
                    item_price = calculate_item_value_based_on_operator(additional_price,'PLUS',item_price)
                    without_discount = calculate_item_value_based_on_operator(additional_price,'PLUS',without_discount)
                }
           });
           var item_total_price = item_price*parseInt(quantity)
           var without_discount_total_price = without_discount*parseInt(quantity)
           var save = parseFloat(without_discount_total_price) - parseFloat(item_total_price);
           $("#id_discount").empty();
           if (price_percentage == 0){
                $("#id_discount").empty();
           }
           else{
            var text = '<span  class="hg_subtext_color"><del>'+ without_discount_total_price +'</del>('+ price_percentage +'%) Save '+ save +'</span>';
                $("#id_discount").append(text);
           }

           console.log(item_price)
            $("#id_price").text(item_total_price);
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


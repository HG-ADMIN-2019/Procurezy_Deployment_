    // on click of save in Account Assignment popup - Update respective Account assignment Data
function change_account_assignment_category() {
        var item_details = [];
        var total_value = $('#ScHeader-total_value-' + GLOBAL_HEADER_GUID).text();
        primary_account_assignment_type = $('#select_acc_type').val();
        primary_account_assignment_value = document.getElementById(primary_account_assignment_type).value;
        gl_account = $('#select_gl_acc_num').val();
        acc_asign_class = document.getElementsByClassName('account_assignment_secondary');
        secondary_account_assignment = '';
        var get_item_guid =  get_item_guid_edit(edit_row_index);

        for(i=0; i< acc_asign_class.length; i++){
            account_assignment_id = acc_asign_class[i].id
            account_assignment_value = acc_asign_class[i].value
            if(primary_account_assignment_type != account_assignment_id){
                if(account_assignment_value != ''){
                    secondary_account_assignment +=  '<div><h5 class="hg_display_inline"><span class="change_header">'+ account_assignment_id +'</span></h5>'  + ': ' + '<span class="hg_display_inline">'+ account_assignment_value +'</span></div>'
                }
            }

        }
        if(GLOBAL_ACCOUNTING_DATA_CHANGE_TYPE == 'header'){
            $('#secondary_accounting_data_header').html(secondary_account_assignment);
            $('#ScAccounting-acc_cat-' + GLOBAL_HEADER_LEVEL_ACC_GUID).html(primary_account_assignment_type)
            $('#ScAccounting-acc_val-' + GLOBAL_HEADER_LEVEL_ACC_GUID).html(primary_account_assignment_value)
            $('#id_acc_title').html(get_title[primary_account_assignment_type] + ':')
            //$('#gl_account_header').html(gl_account);
            $('#ScAccounting-acc_cat-' + GLOBAL_HEADER_LEVEL_ACC_GUID).addClass('sc_field_change');
            $('#ScAccounting-acc_val-' + GLOBAL_HEADER_LEVEL_ACC_GUID).addClass('sc_field_change');
            get_all_item_level_ids = $('[id^="ScAccounting-gl_acc_num-"]')
            for(i=0; i< get_all_item_level_ids.length; i++){
                item_detail = {}
                item_detail.item_value = $('#ScIem-value-'+rendered_item_guid[i]).text();
                item_detail.prod_cat = document.getElementById('prod_cat_id-'+rendered_item_guid[i]).innerHTML
                item_details.push(item_detail)
                account_assignment_guid = get_all_item_level_ids[i].id.split('-')[2]
                $('#ScAccounting-acc_cat-' + account_assignment_guid).html(primary_account_assignment_type)
                $('#id_acc_title-' + account_assignment_guid).html(get_title[primary_account_assignment_type] + ':')
                $('#ScAccounting-acc_val-' + account_assignment_guid).html(primary_account_assignment_value)
                //$('#ScAccounting-gl_acc_num-' + account_assignment_guid).html(gl_account)
                $('#secondary_accounting-' + account_assignment_guid).html(secondary_account_assignment)
                $('#ScAccounting-acc_cat-' + account_assignment_guid).addClass('sc_field_change');
                $('#ScAccounting-acc_val-' + account_assignment_guid).addClass('sc_field_change');
                $('#accounting_added-'+rendered_item_guid[i]).css("display", "none");
            }

            // If header level account assignment category and value is not equal to highest item account assignment and value then trigger work flow
            if(primary_account_assignment_type != highest_item_acc_asgn_cat || primary_account_assignment_value != highest_item_change_acc_value){
                highest_item_acc_asgn_cat = primary_account_assignment_type.split(' - ')[0].trim()
                highest_item_change_acc_value = primary_account_assignment_value.split(' - ')[0].trim()
                //check_shopping_cart('approval_workflow', '', primary_account_assignment_type, primary_account_assignment_value)
                trigger_wf_acc(primary_account_assignment_type, primary_account_assignment_value,item_details,total_value,GLOBAL_REQUESTER_USER_NAME,GLOBAL_SC_CO_CODE)

            }
        } else {
            $('#ScAccounting-acc_cat-' + GLOBAL_ACCOUNTING_DATA_CHANGE_GUID).html(primary_account_assignment_type);
            $('#id_acc_title-' + GLOBAL_ACCOUNTING_DATA_CHANGE_GUID).html(get_title[primary_account_assignment_type] + ':');
            $('#ScAccounting-acc_val-' + GLOBAL_ACCOUNTING_DATA_CHANGE_GUID).html(primary_account_assignment_value);
            $('#ScAccounting-gl_acc_num-' + GLOBAL_ACCOUNTING_DATA_CHANGE_GUID).html(gl_account);
            $('#secondary_accounting-' + GLOBAL_ACCOUNTING_DATA_CHANGE_GUID).html(secondary_account_assignment);
            $('#ScAccounting-acc_cat-' + GLOBAL_ACCOUNTING_DATA_CHANGE_GUID).addClass('sc_field_change');
            $('#ScAccounting-acc_val-' + GLOBAL_ACCOUNTING_DATA_CHANGE_GUID).addClass('sc_field_change');

            var item_level_acc_cat = primary_account_assignment_type;
            var item_level_acc_val = primary_account_assignment_value;

            var header_leve_acc_cat = $('#ScAccounting-acc_cat-' + GLOBAL_HEADER_LEVEL_ACC_GUID).html();
            var header_leve_acc_val = $('#ScAccounting-acc_val-' + GLOBAL_HEADER_LEVEL_ACC_GUID).html();
            if(item_level_acc_cat == header_leve_acc_cat || item_level_acc_val==header_leve_acc_val){
                $('#accounting_added-'+get_item_guid).css("display", "none");
            } else {
                $('#accounting_added-'+get_item_guid).css("display", "block");
            }

            if(edit_row_index == GLOBAL_HIGHEST_VALUE_ITEM_ROW){
                if(primary_account_assignment_type != highest_item_acc_asgn_cat || primary_account_assignment_value != highest_item_change_acc_value){
                    highest_item_acc_asgn_cat = primary_account_assignment_type.split(' - ')[0].trim()
                    highest_item_change_acc_value = primary_account_assignment_value.split(' - ')[0].trim()
                    //check_shopping_cart('approval_workflow', '', primary_account_assignment_type, primary_account_assignment_value)
                    trigger_wf_acc(primary_account_assignment_type, primary_account_assignment_value,item_details,total_value,GLOBAL_REQUESTER_USER_NAME,GLOBAL_SC_CO_CODE)

                }
            }
        }

        GLOBAL_ACCOUNTING_DATA_CHANGE_TYPE = '';
        GLOBAL_ACCOUNTING_DATA_CHANGE_GUID = '';
        $('#change_acc_cat').modal('hide')
    }

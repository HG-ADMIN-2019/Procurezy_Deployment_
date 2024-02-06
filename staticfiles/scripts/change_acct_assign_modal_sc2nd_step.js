    // Function to temporary change account assignment details on selecting from pop-up
    function change_account_assignment_category() {
        var item_details = [];
        var change_acc_type_id = 'change_acc_type'
        var change_acc_value_id = 'change_acc_value'
        var gl_acc_val_id = 'gl_acc_val'
        var secondary_acc_assign_cat_id = 'item_secondary_acc_assign_category'
        var acc_cat = document.getElementById('select_acc_type').value;
        var selected_gl_acc_num = document.getElementById('select_gl_acc_num').value;
        var total_value    = document.getElementById("total_cart_value").innerHTML
        var acc_val = '';
        var account_assignment_cat = acc_cat.split(' - ')[0]
        if(account_assignment_cat=='CC'){
            acc_val = document.getElementById('CC').value
        } else if (account_assignment_cat=='AS'){
            acc_val = document.getElementById('AS').value
        }else if (account_assignment_cat=='WBS'){
            acc_val = document.getElementById('WBS').value
        }else if (account_assignment_cat=='OR'){
            acc_val = document.getElementById('OR').value
        }

        acc_asign_class = document.getElementsByClassName('account_assignment_secondary')
        secondary_account_assignment = '';
        for(i=0; i< acc_asign_class.length; i++){
            account_assignment_id = acc_asign_class[i].id
            account_assignment_value = acc_asign_class[i].value
            if(account_assignment_cat != account_assignment_id){
                if(account_assignment_value != ''){
                    secondary_account_assignment +=  account_assignment_id  + ': ' + account_assignment_value + '<br>'
                }
            }

        }
        console.log("edit")
        console.log(edit_account_assignment_cat)
        if (edit_account_assignment_cat != ''){
            change_acc_type_id  += '_'+edit_account_assignment_cat
            change_acc_value_id += '_'+edit_account_assignment_cat
            gl_acc_val_id       += '_'+edit_account_assignment_cat
            secondary_acc_assign_cat_id += '_'+edit_account_assignment_cat
            document.getElementById(gl_acc_val_id).innerHTML = selected_gl_acc_num;
            $('#accounting_added-'+edit_account_assignment_cat).prop("hidden", false);
            $('#cost_objects_info').css("display", "block");
        }
        if (edit_account_assignment_cat == ''){
            document.getElementById(change_acc_type_id).innerHTML = acc_cat
            document.getElementById(change_acc_value_id).innerHTML = acc_val


            for(i=0;i<cart_length;i++){
                incremented_id = i+1
                item_detail = {}
                item_detail.item_value = document.getElementById('item_value_'+sc_item_guid[i]).innerHTML
                item_detail.prod_cat = document.getElementById('prod_cat_'+incremented_id).innerHTML
                item_details.push(item_detail)

                document.getElementById('change_acc_type_'+incremented_id).innerHTML = acc_cat
                document.getElementById('change_acc_value_'+incremented_id).innerHTML = acc_val

                $('#secondary_acc_ass_cat_section').html('');
                $('#secondary_acc_ass_cat_section').html(secondary_account_assignment);
                document.getElementById('item_secondary_acc_assign_category_'+incremented_id).innerHTML = secondary_account_assignment;
                $('#accounting_added-'+incremented_id).prop("hidden", true);
                $('#cost_objects_info').css("display", "none");
            }

            trigger_wf_acc(acc_cat, acc_val,item_details,total_value,requester_user_name,rendered_default_company_code)
        }


            //document.getElementById(gl_acc_val_id).innerHTML = selected_gl_acc_num
            document.getElementById(change_acc_type_id).innerHTML = acc_cat
            document.getElementById(change_acc_value_id).innerHTML = acc_val
            //document.getElementById(gl_acc_val_id).innerHTML = selected_gl_acc_num
            $('#change_acc_cat').modal('hide');
            document.getElementById(secondary_acc_assign_cat_id).innerHTML = secondary_account_assignment


            if(highest_value_item_number == edit_account_assignment_cat){
                highest_item_acc_asgn_cat = acc_cat
                highest_item_change_acc_value = acc_val
                trigger_wf_acc(acc_cat, acc_val,item_details,total_value,requester_user_name,rendered_default_company_code)
                 //check_shopping_cart('approval_workflow', 'sc_data', acc_cat, acc_val)
            }
            edit_account_assignment_cat = ''
        //$('#hg_loader').modal('hide');
    }


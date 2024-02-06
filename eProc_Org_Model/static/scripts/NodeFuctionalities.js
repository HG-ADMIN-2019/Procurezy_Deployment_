var GLOBAL_USER_STATUS = ''
var GLOBAL_USER_ID_LIST = []
var GLOBAL_ONCLICK_NODE_GUID = ''
var GLOBAL_DIV_ID = ''

// on click of create in create node popup,this function saves node name in orgmodel db table
function createNode() {
    let new_node_name = ""
    new_node_name = $("#AddNodeName").val().trim();
    if (!new_node_name) {
        return $("#addNodeAlertMsg").removeAttr('hidden').css("display", "block")
            .removeClass("alert-success")
            .addClass("alert-danger")
            .text(OrgMessageConstants.JMSG003);

        //  var msg = "JMSG012";
        //  var msg_type ;
        //  msg_type = message_config_details(msg);
        //  $("#error_msg_id").prop("hidden", false)
        //  var display2 = msg_type.messages_id_desc[0];
        //  .text(display2);
    }
    else {
        $("#addNodeAlertMsg").text("").css("display", "none")
    }
    node = nodeTypes;
    let new_node_parent = new_node_parent_mapId;
    let parent_pk = NodeGuidByMapId(jsonData, new_node_parent);
    if (parent_pk == undefined) {
        let root_pk = rootRef(orgs, new_node_parent)
        console.log(root_pk)
        parent_pk = root_pk;
    }
    let sel = document.getElementById('NodeTypesoptions');
    let opt_selected = sel.options[sel.selectedIndex];
    /* Calling ApI of Add Node */
    let addNodeInput = {
        "name": new_node_name,
        "node_type": opt_selected.value,
        "parent_node": parent_pk,
        "root_node_object_id": ROOT_NODE_OBJECT_ID
    };
    var AddNodeResult = node_create_ajax_call(addNodeInput);
    if (AddNodeResult.error)
    {
        $('#error_message').text(AddNodeResult.error);
        document.getElementById("error_message").style.color = "Red";
        $("#error_msg_id").css("display", "block")
    }
    else{
        var nodeResult = typeof (AddNodeResult);
        if (!AddNodeResult.hasOwnProperty('error')) {
            $("#ConfirmationPopUp").css("display", "none")
            $("#createNodeBtn").hide()
            $("#addNodeAlertMsg").css("display", "block").removeClass('alert-danger').addClass("alert-success").text(`Node type ${opt_selected.value} with Name ${new_node_name} created successfully.`);
            $("#modalAddNode").modal('hide');
            if (new_node_arrow_class == "material-icons-outlined remove_circle") {
                //Displaying of the newly added node in tree structure
                if (new_node_append_ul === undefined || new_node_append_ul === " ") {
                    var ul = document.createElement("ul");
                    ul.id = "subnode" + subInc;
                    subInc++;
                    new_node_append_ul = ul.id;
                    document.getElementById(new_node_create_ul).appendChild(ul);
                }

                var lis = document.createElement('li')
                var liId = AddNodeResult[0].fields.name + "new";
                lis.id = liId;
                lis.setAttribute('value', AddNodeResult[0].pk) //map_id
                lis.setAttribute('class', 'branch')
                document.getElementById(new_node_append_ul).appendChild(lis);


                var idiv = document.createElement('div');
                idiv.id = AddNodeResult[0].pk; //map_id
                document.getElementById(liId).appendChild(idiv);

                var node_t = AddNodeResult[0].fields.node_type
                if (node_t != 'USER') {
                    var iElement = document.createElement('i');
                    iElement.setAttribute('value', AddNodeResult[0].pk) //map_id
                    iElement.id = liId + "i";
                    iElement.className = "material-icons-outlined add_circle";
                    iElement.append('add_circle');
                    iElement.style.fontSize="18px";
                    document.getElementById(liId).appendChild(iElement);
                }
                var icon_container = document.createElement('span');
                icon_container.className = "tree-icon-container";
                var icon = document.createElement('i')
                icon.className = setNodeType(node_t); //node_type
                icon_container.appendChild(icon)

                document.getElementById(liId).appendChild(icon_container);

                var li = document.createElement("span");
                li.setAttribute('id', "child" + "new");
                // add tree option to support customize right click
                if (node_t != "USER") {
                    li.setAttribute('class', 'treeOptions');
                }
                var liData = AddNodeResult[0].fields.name + " ";
                li.innerHTML = liData;
                li.classList.add('tree-node-name');
                document.getElementById(liId).appendChild(li);


                var json_child = { model: AddNodeResult[0].model, pk: AddNodeResult[0].pk, fields: AddNodeResult[0].fields };
                if (jsonData.includes(json_child) === false) {
                    jsonData.push(json_child);
                }
            }
            nodeDuplicateInd = " ";
            new_node_pId = " ";
            //            new_node_append_ul = " ";
            //            new_node_arrow_class = " ";

        }
        else {
            new_node_pId = " ";
            new_node_append_ul = " ";
            let result_msg = "Node type " + opt_selected.text + " " + new_node_name + " cannot be added under " + new_node_pId + " - " + AddNodeResult.error
            $("#addNodeAlertMsg").css("display", "block").removeClass("alert-success").addClass("alert-danger").text(result_msg);
        }
    }

}


//** Getting Guid using MapId **//

function NodeGuidByMapId(jsonData, NodeMap) {
    for (var i = 0; i < jsonData.length; i++) {
        if (NodeMap == jsonData[i].pk) {
            return jsonData[i].fields.node_guid;
        }
    }
}

// Get the guid of the root node from the list of orgs json data 
function rootRef(jsonData, nodeName) {
    for (var i = 0; i < jsonData.length; i++) {
        if (nodeName == jsonData[i].fields.name) {
            return jsonData[i].pk;
        }
    }
}
// Get the guid of the root node from the list of orgs json data
function get_org_name_object_id(jsonData, nodeName) {
    for (var i = 0; i < jsonData.length; i++) {
        if (nodeName == jsonData[i].fields.name) {
            return jsonData[i].fields.object_id;
        }
    }
}

function get_org_name_obj_id(jsonData, nodeName) {
    for (var i = 0; i < jsonData.length; i++) {
        if (nodeName == jsonData[i].fields.name) {
            return jsonData[i].fields.object_id;
        }
    }
}

// Delete node functionality from the tree structure
// This function deletes node in db and remove that node in tree structure
function on_click_delete_confirmation_popup() {
    let delete_guid = NodeGuidByMapId(jsonData, delete_element_value)
    //let urlLinkDeleteNode = 'node/delete';
    let deleteNodeInput = {
        "pk": delete_element_value
    };
    var AddNodeResult = node_delete_ajax_call(deleteNodeInput);

    if (AddNodeResult.error) {
        $("#deleteNodeAlertMsg").removeAttr('hidden')
            .css("display", "block").removeClass("alert-success")
            .addClass("alert-danger")
            .text(OrgMessageConstants.JMSG010);
        $("#Delete_Confirmation_PopUp").css("display", "none")
        $("#Delete_Node_Yes").hide()

    }
    else {
        $("#org-list").empty();
        update_root_node_search_drop_down(AddNodeResult);
        $("#deleteNodeAlertMsg").removeAttr('hidden')
            .css("display", "block")
            .removeClass("alert-danger").addClass("alert-success")
            .text(OrgMessageConstants.JMSG009);
        $("#Delete_Confirmation_PopUp").css("display", "none")
        $("#Delete_Node_Yes").hide()
        $("#Delete_Node_No").hide()
        $("#Delete_Node_ok").show()
        $(delete_li).empty();
        $(delete_li).remove();
        if (delete_element_value == GLOBAL_ONCLICK_UPDATE_OBJ_ID) {
            var parent_object_id = get_parent_object_id(delete_element_value)
            get_node_details(parent_object_id);
            //hide basic and attribute detais
            //document.getElementById("BasicData").style.display = "none"
            //document.getElementById("attribute_overview").style.display = "none"
            // clear_basic_details_fields()
        }


    }
    delete_element_value = " ";
}



// add user id to the list
function assign_unassign(assign_id) {
    input_id = assign_id.id
    if(assign_id.checked == true){
//    if ($("#" + input_id).prop("checked") == true) {
        if (!(GLOBAL_USER_ID_LIST.includes(input_id))) {
            GLOBAL_USER_ID_LIST.push(input_id)
        }
    }
}

// Saving assign unassign  user
function save_assign_unassign_status() {
    var index = -1
    let save_check = "";
    let user_list = [];
    let get_users = document.getElementsByClassName("users_assign")
    GLOBAL_ONCLICK_NODE_GUID = NodeGuidByMapId(jsonData, delete_element_value);


    if (!GLOBAL_USER_ID_LIST) {
        alert(OrgMessageConstants["JMSG011"])
        $("#modal_users").modal("toggle");

    }
    else {
        let data = {
            "node_action": GLOBAL_USER_STATUS,
            "user_id_list": GLOBAL_USER_ID_LIST,
            "node_guid": GLOBAL_ONCLICK_NODE_GUID,
            "root_node_object_id": ROOT_NODE_OBJECT_ID
        }

        //let users_api = "users/save_assign_unassign_user"
        // let result = save_assign_unassign_ajax_call(data)

        $.ajax({
            type: 'POST',
            url: save_assign_unassign_ajax_call_url,
            data: JSON.stringify(data),
            success: function(result){
                console.log(result)
                if (a_un_arrow == "material-icons-outlined remove_circle") {
                    let check_ul_exists = delete_li.children.length
                    if (check_ul_exists > 4) {
                        let get_existing_ul = delete_li.children[4].id
                        let users_array = [];
                        let get_users_list = document.getElementById(get_existing_ul).children
                        for (let i = 0; i < get_users_list.length; i++) {
                            let get_value = get_users_list[i].value
                            //get users from the json data and delete from global json
                            for (let j = 0; j < jsonData.length; j++) {
                                if (jsonData[j].pk == get_value) {
                                    jsonData.splice(j, 1);
                                }
                            }
                        }
                        $("#" + get_existing_ul).empty();
                        $("#" + get_existing_ul).remove();
                        $("#modal_users").modal("toggle");
                        let get_guid = NodeGuidByMapId(jsonData, delete_element_value);
                        let get_li_id = delete_li.id
                        getChild(get_guid, get_li_id)
        
                    }
                }
                else {
                    let check_ul_exists = delete_li.children.length
                    if (check_ul_exists > 4) {
                        let get_existing_ul = delete_li.children[4].id
                        let users_array = [];
                        let get_users_list = document.getElementById(get_existing_ul).children
                        for (let i = 0; i < get_users_list.length; i++) {
                            let get_value = get_users_list[i].value
                            //get users from the json data and delete from global json
                            for (let j = 0; j < jsonData.length; j++) {
                                if (jsonData[j].pk == get_value) {
                                    jsonData.splice(j, 1);
                                }
                            }
                        }
                        $("#" + get_existing_ul).empty();
                        $("#" + get_existing_ul).remove();
                    }
                    $("#modal_users").modal("toggle");
                }
                
                CloseLoaderPopup();
            },
            error: function(xhr, resp, text) {
                console.log((xhr.responseText));
            },
        });
    }
}

function get_parent_object_id(object_id) {
    var parent_object_id = ''
    for (var i = 0; i < jsonData.length; i++) {
        if (object_id == jsonData[i].pk) {
            var parent_guid = jsonData[i].fields.parent_node_guid;
            break
        }
    }
    for (var i = 0; i < jsonData.length; i++) {
        if (parent_guid == jsonData[i].fields.node_guid) {
            parent_object_id = jsonData[i].pk;
            return parent_object_id
        }
    }
    parent_object_id = ROOT_NODE_OBJECT_ID
    return parent_object_id
}
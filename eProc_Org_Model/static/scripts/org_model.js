// **-------------------------------Start of declaring constant------------------------------** //
// **--------------------------------End of declaring constant-------------------------------** //

// **---------------------------Start of declaring Global variables--------------------------** //
var valid = false;               // Var for orgName validation
var rootName = " ";                // Var to store the rootName
var subInc = 1;                 // Var to increment the subNodes id in tree structure
var jsonData = [];               // Var to store the jsonData of tree
var nodeId = [];              // Var to store the node id to check the length of children
var nodeDuplicateInd = " ";
var new_node_parent_mapId = " ";
var new_node_pId = " ";
var nodes = [];
//################################ START INITIALIZING BASIC DATA FIELD VARIABLE #######################################
var GLOBAL_BD_NAME_VALUE = ''
var GLOBAL_CC_ID_VALUE = ''
var GLOBAL_CC_NAME1_VALUE = ''
var GLOBAL_CC_NAME2_VALUE = ''
var GLOBAL_PORG_ID_VALUE = ''
var GLOBAL_PORG_DESC_VALUE = ''
var GLOBAL_PGRP_ID_VALUE = ''
var GLOBAL_PGRP_DESC_VALUE = ''
var GLOBAL_USER_FIRST_NAME_VALUE = ''
var GLOBAL_USER_LAST_NAME_VALUE = ''
var GLOBAL_USER_EMAIL_ID_VALUE = ''
var GLOBAL_NODE_DETAIL_EXISTS = false
var GLOBAL_NODE_DETAIL = {}
var GLOBAL_ATTRIBUTE_ID_LIST = []
var CENTRALIZE_PURCH_LEVEL_FLAG = false

//################################ END INITIALIZING BASIC DATA FIELD VARIABLE #######################################
// Tab Variabls
var tabPriKey = " ";                     // var for saving the edited basic data details
var node_type = " ";                   // var for saving the edited basic data details
var DetailsTabPK = " ";                 // Var for displaying details tab
var DetailsTabmapid = " ";              // Var for displaying details tab
var DetailsTabNodeType = " ";           // Var for displaying details tab
var DetailsInd = " ";
var new_node_append_ul = " ";          //var for add node - existing ul id
var new_node_create_ul = " "           //var for add node - new ul id
var orgs = [];
var new_node_arrow_class = " ";
var delete_element_value = " ";
var delete_li = " ";
var comp_check = " ";
var porg_check = " ";
var pgrp_check = " ";
var modify_popup_add_new_line = '';
var add_popup_add_new_line = '';
var ext_add_new_line = '';
var resp_add_new_line = '';

//---------------------Before/after edit variables check-------------------------------//
var basic_node_name = "";
var details_name1 = " ";
var details_name2 = " ";
var details_des = " ";
var details_obj_id = " ";
var basic_tab_edited_saved = " ";
var control_multiple_request = " ";
//---------------------Assign/Unassign user nodes global variables------------------------//
var a_un_arrow = ""; //on right click get arrow id
var a_us_check = "";
var search_started = "";

// on click of create organization( create root node)
function create_organization() {
    var orgname = document.getElementById("orgName").value;
    if (orgname === undefined || orgname === "") {
        $("#orgErrMsg").removeAttr('hidden')
            .css("display", "block")
            .removeClass("alert-success")
            .addClass("alert-danger")
            .text(OrgMessageConstants.JMSG001);
    }
    else if (!(orgname.match(/^[0-9a-zA-Z \_\s]+$/))) {
        $("#orgErrMsg").removeAttr('hidden')
            .css("display", "block")
            .removeClass("alert-success")
            .addClass("alert-danger")
            .text(OrgMessageConstants.JMSG002);

    }
    else if (orgname.length > 0) {
        if (orgname[0].match(/^[_]*$/)) {
            $("#orgErrMsg").removeAttr('hidden')
                .css("display", "block")
                .removeClass("alert-success")
                .addClass("alert-danger")
                .text(OrgMessageConstants.JMSG003);
        }
        else if (orgname[0].match(/^[0-9]*$/)) {
            $("#orgErrMsg").removeAttr('hidden')
                .css("display", "block")
                .removeClass("alert-success")
                .addClass("alert-danger")
                .text(OrgMessageConstants.JMSG003);

        }
        else if (orgname.length < 3) {
            $("#orgErrMsg").removeAttr('hidden')
                .css("display", "block")
                .removeClass("alert-success")
                .addClass("alert-danger")
                .text(OrgMessageConstants.JMSG005);
        }
        else {
            valid = true;
            var orgname = document.getElementById("orgName").value;
            var orgCreate = {
                "org_name": orgname
            };
            var data = create_org_ajax_call(orgCreate)
            if (data.error !== undefined) {
                $("#orgErrMsg").removeAttr('hidden')
                    .css("display", "block")
                    .removeClass("alert-success")
                    .addClass("alert-danger")
                    .text(data.error || OrgMessageConstants.JMSG006);
            }
            else {
                var updateOrgLst = document.getElementById("org-list");
                var element = document.createElement("option");
                element.text = document.getElementById("orgName").value.toUpperCase();
                element.value = document.getElementById("orgName").value.toUpperCase();
                updateOrgLst.appendChild(element);

                $("#orgErrMsg").removeAttr('hidden')
                    .css("display", "block")
                    .removeClass("alert-danger")
                    .addClass("alert-success")
                    .text(OrgMessageConstants.JMSG007);
                $("#creOrgCreBtn").hide()
                var json_child = { model: data[0].model, pk: data[0].pk, fields: data[0].fields };
                if (orgs.includes(json_child) === false) {
                    orgs.push(json_child);
                }
            }
        }
    }
}
// **End of validations for org create** //

// **Start of navbar datalist function** //

function update_root_node_search_drop_down(org_list) {
    orgs = org_list
    var out = ' ';
    for (var i = 0; i < orgs.length; i++) {
        out += orgs[i].fields.name + '<br>';
        var optElement = document.createElement('option');
        optElement.text = orgs[i].fields.name;
        optElement.value = orgs[i].fields.name;
        document.getElementById("org-list").appendChild(optElement);
    }

}

//on select of root node drop down
function on_select_root_node_drop_down(event) {
    $("#org_search_modal").modal('toggle');
    rootName = "";
    $("#hg_org_search_term").val(event.target.value)
    root_node = document.getElementById("root-node")
    if (root_node) {
        document.getElementById("root-node").innerHTML = "";
    }
    else {
        var root_li = '<li id="root-node" class="branch"><i class="indicator glyphicon glyphicon-minus-sign"></i></li>'
        $("#tree_Structure").append(root_li);
    }
    // clear tree structure
    $("[id^=subnode]").empty();
    $("[id^=subnode]").remove();
    $("[id^=node_tree]").empty();
    $("[id^=node_tree]").remove();

    //hide basic and attribute detais
    document.getElementById("BasicData").style.display = "none"
    document.getElementById("attribute_overview").style.display = "none"

    // create root node
    nodeId = [];
    var val = document.getElementById("org-list").value;
    var opts = document.getElementById('org-list').childNodes;
    for (var i = 0; i < opts.length; i++) {
        if (opts[i].value === val) {
            rootName = opts[i].value;
            var spanElement = document.createElement("span");
            spanElement.id = opts[i].value;
            spanElement.className = "treeOptions";
            spanElement.classList.add("tree-node-name");
            document.getElementById("root-node").append(spanElement);

            var iElement = document.createElement('i');
            iElement.id = "rootNodeId";
            iElement.className = "material-icons-outlined remove_circle";
            iElement.append('remove_circle');
            iElement.style.fontSize = "18px";
            document.getElementById(spanElement.id).appendChild(iElement);
            var icon_container = document.createElement('span');
            icon_container.className = "tree-icon-container";
            var icon = document.createElement('i')
            icon.className = "fa fa-sitemap text-primary";
            icon_container.appendChild(icon)
            document.getElementById(spanElement.id).appendChild(icon_container);
            document.getElementById(spanElement.id).append(opts[i].value);

            jsonData = [];
            var orgChildGuid = rootRef(orgs, rootName)
            var object_id = get_org_name_object_id(orgs, rootName)
            ROOT_NODE_OBJECT_ID = object_id
            document.getElementById("root-node").value = object_id
            //get children
            getChild(orgChildGuid, "tree_Structure");
        }
    }
}


// **Start of getting a node reference from node name ** //
function getNodeRef(jsonData, nodeName) {
    for (var i = 0; i < jsonData.length; i++) {
        if (nodeName == jsonData[i].pk) { //map_id
            return jsonData[i].pk;
        }
    }
}
// **End of getting a node reference from node name ** //

// **Start of getting a icon based on the node type** //
function setNodeType(nodeType) {
    var nodeIcon = " ";
    var x = nodeType;
    switch (x) {
        case "CCODE":
            nodeIcon = "fa fa-building tree-icon__company";
            break;
        case "PORG":
            nodeIcon = "fa fa-industry tree-icon__purch-org";
            break;
        case "PGRP":
            nodeIcon = "fas fa-object-ungroup tree-icon__purch-group";
            break;
        case "PLANT":
            nodeIcon = "fa fa-industry tree-icon__plant";
            break;
        case "NODE":
            nodeIcon = "fas fa-layer-group tree-icon__nodes";
            break;
        case "USER":
            nodeIcon = "fa fa-user tree-icon__user";
            break;
        case "RNODE":
            nodeIcon = "fa fa-sitemap text-primary";
            break;
        default:
            break;
    }
    return nodeIcon;
}
// **End of getting a icon based on the node type ** //

// **Start of getting a subsequent children to a tree structure** //
function getChild(pk, listId) {
    var dataj = []
    if (jsonData.length > 0) {
        for (var k = 0; k < jsonData.length; k++) {

            if (pk == jsonData[k].fields.parent_node_guid) {
                console.log("exists")
                nodeDuplicateInd = "X";
                break;
            }

        }
    }


    if (nodeDuplicateInd != "X") {
        var nodeGet = {
            "guid": pk
        };

        nodes = nodeTypes;
        testApi(nodeGet, listId)
    }

    else {
        var rlist = " "
        var ilist = " "
        var rlist_id = $(this)[0].parent.childId
        if (rlist_id == 'rootNodeId') {
            let root_ref = document.getElementById(rlist_id)
            root_ref = root_ref.parentElement.parentElement.id
            let root_sib = document.getElementById(root_ref).nextElementSibling.id
            rlist = root_sib
        }
        else {
            rlist = document.getElementById(rlist_id).getElementsByTagName('ul')[0].id;
        }
        ilist = document.getElementById(rlist).getElementsByTagName("li");

        for (var i = 0; i < ilist.length; i++) {
            display = ilist[i].style.display
            $(ilist[i]).toggle();
        }
        nodeDuplicateInd = " ";
    }
}
// **End of getting a subsequent children to a tree structure** //
// **-------------------------End of tree structure tree view class--------------------------** //

//Finding the guid based on the map ID
function nodeRefNodeType(jsonData, node_object_id) {
    for (let i = 0; i < jsonData.length; i++) {
        if (node_object_id == jsonData[i].pk) {
            return jsonData[i].fields.node_type;
            break;
        }
    }
}

// disable all fields from the field_id_list
function disable_fields(field_id_list) {
    $.each(field_id_list, function (i, item) {
        $("#" + item).prop("readonly", true);
        $("#" + item).css("background", "#d7d7d7");

    });
}

//disable all fields from the field_id_list
function enable_fields(field_id_list) {
    $.each(field_id_list, function (i, item) {
        $("#" + item).prop("readonly", false);
        $("#" + item).css("background", "white");
    });
}

// Remove d-none to display elements in element_id_list
function display_elements(prefix, element_id_list) {
    try {
        element_id_list.forEach((element_id) => { $("#" + prefix + element_id).removeClass('d-none') })
    } catch (error) {
        console.log(error)
        return
    }
}

// add d-none to hide elements in element_id_list
function hide_elements(prefix, element_id_list) {
    console.log('hide_elements')
    try {
        element_id_list.forEach((element_id) => { $("#" + prefix + element_id).addClass('d-none') })
    } catch (error) {
        console.log(error)
        return
    }
}

// on click edit/cancel in basic details
function button_action(button_type) {
    node_type_disable_fields_list = get_field_id_list(button_type)
    if (button_type == 'EDIT') {
        if (GLOBAL_ON_DOUBLE_CLICK_NODE_TYPE == 'RNODE') {
            GLOBAL_ROOT_NODE_NAME = $("#BDname").val()
        }
        display_ele("#tab_save")
        display_ele("#tab_cancel")
        hide_ele("#tab_edit")
        enable_fields(node_type_disable_fields_list)
    }
    else if (button_type == 'CANCEL') {
        disable_fields(node_type_disable_fields_list)
        display_ele("#tab_edit")
        hide_ele("#tab_cancel")
        hide_ele("#tab_save")
    }
}

// get basic field id list based on node type
function get_field_id_list(button_type) {
    var node_type_disable_fields_list = []
    let node_type = GLOBAL_ON_DOUBLE_CLICK_NODE_TYPE;
    x = node_type
    switch (x) {
        case "CCODE":
            if (button_type == 'EDIT') {
                $("#select_cc_id").prop("disabled", false);
            }
            else {
                $("#select_cc_id").prop("disabled", true);
            }
            //node_type_disable_fields_list = ['cc_id','cc_name1','cc_name2']
            //if (!GLOBAL_NODE_DETAIL_EXISTS){
            //  node_type_disable_fields_list.push('select_cc_id')
            //}
            node_type_disable_fields_list.push('select_cc_id')
            GLOBAL_CC_ID_VALUE = $("#cc_id").val()
            GLOBAL_CC_NAME1_VALUE = $("#cc_name1").val()
            GLOBAL_CC_NAME2_VALUE = $("#cc_name2").val()

            break;
        case "PORG":
            if (button_type == 'EDIT') {
                $("#select_porg_id").prop("disabled", false);
            }
            else {
                $("#select_porg_id").prop("disabled", true);
            }
            //node_type_disable_fields_list = ['porg_id','POrg_desc']
            //if (!GLOBAL_NODE_DETAIL_EXISTS){
            //    node_type_disable_fields_list.push('select_porg_id')
            //}
            node_type_disable_fields_list.push('select_porg_id')
            GLOBAL_PORG_ID_VALUE = $("#porg_id").val()
            GLOBAL_PORG_DESC_VALUE = $("#POrg_desc").val()

            break;
        case "PGRP":
            if (button_type == 'EDIT') {
                $("#select_pgrp_id").prop("disabled", false);
            }
            else {
                $("#select_pgrp_id").prop("disabled", true);
            }
            //node_type_disable_fields_list = ['pgrp_id','Pgrp_desc']
            //if (!GLOBAL_NODE_DETAIL_EXISTS){
            //  node_type_disable_fields_list.push('select_pgrp_id')
            //}
            node_type_disable_fields_list.push('select_pgrp_id')
            GLOBAL_PGRP_ID_VALUE = $("#pgrp_id").val()
            GLOBAL_PGRP_DESC_VALUE = $("#Pgrp_desc").val()

            break;
        default:
            break;
    }
    node_type_disable_fields_list.push('BDname')
    GLOBAL_BD_NAME_VALUE = $("#BDname").val()
    return node_type_disable_fields_list
}

// on click of Cancel button in basic details
function cancel_fun() {
    let node_type = GLOBAL_ON_DOUBLE_CLICK_NODE_TYPE;
    x = node_type
    $("#BDname").val(GLOBAL_BD_NAME_VALUE)
    switch (x) {
        case "CCODE":
            $("#cc_id").val(GLOBAL_CC_ID_VALUE)
            $("#cc_name1").val(GLOBAL_CC_NAME1_VALUE)
            $("#cc_name2").val(GLOBAL_CC_NAME2_VALUE)

            break;
        case "PORG":
            $("#porg_id").val(GLOBAL_PORG_ID_VALUE)
            $("#POrg_desc").val(GLOBAL_PORG_DESC_VALUE)

            break;
        case "PGRP":
            $("#pgrp_id").val(GLOBAL_PGRP_ID_VALUE)
            $("#Pgrp_desc").val(GLOBAL_PGRP_DESC_VALUE)

            break;
        case "USER":
            $("#user_first_name").val(GLOBAL_USER_FIRST_NAME_VALUE)
            $("#user_last_name").val(GLOBAL_USER_LAST_NAME_VALUE)
            $("#user_email_id").val(GLOBAL_USER_EMAIL_ID_VALUE)

            break;
        default:
            break;
    }
    button_action('CANCEL')
}


//on creating node, this function validates node
function node_ID_validation(node_id_value) {
    if (!(node_id_value.match(/^[a-zA-Z0-9]*$/))) {
        //contains special characters
        return false
    }
    else {
        // does not contain special characters
        return true
    }
}


// Closing the basic details tab
function refreshBD() {
    $('#modal_Basic_Detail').modal('hide')
    document.getElementById("BD").style.display = "none";
    document.getElementById("BD_result").innerHTML = " ";
}

//**//    End of Details Data Tab    //**//

// **---------------------------------------End of Tabs--------------------------------------** //



var GLOBAL_ONCLICK_UPDATE_OBJ_ID = " ";
var GLOBAL_ON_DOUBLE_CLICK_NODE_TYPE = '';
var GLOBAL_ROOT_NODE_NAME = '';
var obj_id_node_type = " ";
var porg_id = '';
var cocode_values = '';

function create_main_table(attr_level_detail) {

    var type_val = '';
    var default_value = '';
    var inherit_value = '';
    var exclude_value = '';
    var resp_modify = '';
    var resp_attr_html = '';
    var ext_modify = '';
    var ext_attr_html = '';
    var ext_inherit_value = '';
    var add_resp_attr = '';
    var cocode_drop_down = '';

    var company_detail = '';
    GLOBAL_ATTRIBUTE_ID_LIST = []
    $('#main_table_body').empty();
    $('#responsibility_body').empty();
    $("#extend_attr_table").find("tr:gt(0)").remove();
    if (attr_level_detail) {
        attr_level_value = attr_level_detail.attr_value_list;
        org_comp_dropdown_list = attr_level_detail.org_comp_dropdown_list;
        CENTRALIZE_PURCH_LEVEL_FLAG = attr_level_detail.centralize_purch_level_flag;
        if ((GLOBAL_ON_DOUBLE_CLICK_NODE_TYPE == 'PGRP') || (GLOBAL_ON_DOUBLE_CLICK_NODE_TYPE == 'PORG')) {
            cocode_values = get_cocode_drop_down(org_comp_dropdown_list, CENTRALIZE_PURCH_LEVEL_FLAG);
        }
        $.each(attr_level_value, function (i, item) {
            GLOBAL_ATTRIBUTE_ID_LIST.push(item.attribute_id)
            if (CENTRALIZE_PURCH_LEVEL_FLAG) {
                company_detail = '<select class="form-control" disabled><option value="' + item.extended_value + '" >' + item.extended_value + '</option></select>'
            }
            else {
                company_detail = '<input type="text" value=' + item.extended_value + ' disabled>';
            }
            if (item.attribute_id == "RESP_PROD_CAT") {


                resp_modify = '<a onclick=clone_resp_table_row() id="' + item.attr_level_guid + '" class="org-table-action-icon" title="Add new row"><i class="fa fa-plus text-primary"></i></a>  <a onclick="remove_resp_Row(this)" id="' + item.attr_level_guid + '" class="org-table-action-icon" title="Delete Row"><i class="fa fa-trash text-primary"></i></a>';
                resp_attr_html += '<tr id="resp_attr_tr"><td><input type="number" class="form-control" onkeypress="return event.charCode >= 48" min="0" name="from" value="' + item.low + '" required></td><td><input type="number" class="form-control" onkeypress="return event.charCode >= 48" min="0" name="from" value="' + item.high + '" required></td><td> ' + company_detail + ' </td><td> ' + resp_modify + ' </td></tr>';
                resp_add_new_line = '<tr id="resp_attr_tr"><td><input type="number" class="form-control" onkeypress="return event.charCode >= 48" min="0" name="from" value="' + item.low + '" required></td><td><input type="number" class="form-control" onkeypress="return event.charCode >= 48" min="0" name="from" value="' + item.high + '" required></td><td> ' + cocode_values + ' </td><td> ' + resp_modify + ' </td></tr>';
            }
            else if (item.attribute_id == "PROD_CAT") {

                if (item.object_id == GLOBAL_ONCLICK_UPDATE_OBJ_ID) {
                    ext_inherit_value = '<input  type="checkbox" name="inherit" value="inherit">';
                }
                else {
                    ext_inherit_value = '<input disabled type="checkbox" name="inherit" value="inherit" checked>';
                }
                ext_modify = '<a onclick="clone_ext_table_row();" id="' + item.attr_level_guid + '" class="org-table-action-icon" title="Add new row"><i class="fa fa-plus text-primary"></i></a>  <a onclick="remove_ext_Row(this)" id="' + item.attr_level_guid + '" class="org-table-action-icon" title="Delete Row"><i class="fa fa-trash text-primary"></i></a>';
                ext_attr_html += '<tr id="extend_attr_tr"><td><input type="number" class="form-control" onkeypress="return event.charCode >= 48" min="0" name="from" value="' + item.low + '" required></td><td><input type="number" class="form-control" onkeypress="return event.charCode >= 48" min="0" name="from" value="' + item.high + '" required></td><td> ' + company_detail + ' </td><td> ' + ext_inherit_value + ' </td><td> ' + ext_modify + ' </td></tr>';
                ext_add_new_line = '<tr id="extend_attr_tr"><td><input type="number" class="form-control" onkeypress="return event.charCode >= 48" min="0" name="from" value="' + item.low + '" required></td><td><input type="number" class="form-control" onkeypress="return event.charCode >= 48" min="0" name="from" value="' + item.high + '" required></td><td> ' + cocode_values + ' </td><td> ' + ext_inherit_value + ' </td><td> ' + ext_modify + ' </td></tr>'
            }
            else {
                default_value = '';
                inherit_value = '';
                if (item.attr_level_default) {
                    default_value = ' <input disabled type="checkbox" name="Default" value="' + item.attr_level_default + '" checked>';
                }
                else {
                    default_value = '<input disabled type="checkbox" name="Default" value="' + item.attr_level_default + '">';
                }
                if (item.object_id == GLOBAL_ONCLICK_UPDATE_OBJ_ID) {
                    inherit_value = '<input disabled type="checkbox" name="inherit" value="inherit">';
                }
                else {
                    inherit_value = '<input disabled type="checkbox" name="inherit" value="inherit" checked>';
                }
                if (item.attr_level_exclude) {
                    exclude_value = ' <input disabled type="checkbox" name="exclude" value="' + item.attr_level_exclude + '" checked>';
                }
                else {
                    exclude_value = '<input disabled type="checkbox"  name="exclude" value="' + item.attr_level_exclude + '">';
                }
                modify = '<a onclick=get_selected_attr_list(this.className) id="' + item.attr_level_guid + '" class="' + item.attribute_id + '" ><i class="far fa-edit text-primary"></i></a>';

                type_val += '<tr><td contenteditable="false" hidden>' + item.attribute_id + '</td><td contenteditable="false">' + item.attribute_name + '</td><td contenteditable="false">' + item.low + '</td><td>' + item.attribute_value_desc + '</td><td>' + default_value + '</td><td>' + inherit_value + '</td><td>' + exclude_value + '</td><td>' + modify + '</td><td hidden>' + item.object_id + '</td><td>' + item.org_node_name + '</td></tr>';
            }
        });
        console.log(GLOBAL_ON_DOUBLE_CLICK_NODE_TYPE)
        $('#main_table_body').append(type_val);
        $('#responsibility_body').append(resp_attr_html);
        $('#extend_attr_table').append(ext_attr_html);
        $("#org_attribute_overview").removeClass("d-none")
        // if prod cat not present in attr level table
        if (GLOBAL_ON_DOUBLE_CLICK_NODE_TYPE != 'PORG') {
            document.getElementById("ext_attr_errmsg").innerHTML = 'Extended  Product Category Not Applicable';
            document.getElementById('ext_error_div').style.display = 'block';
            document.getElementById('ext_porg_id').style.display = 'none';
        }
        else {
            porg_id = $("#select_porg_id").val()
            if (!(ext_attr_html)) {

                add_ext_attr = '<tr id="extend_attr_tr"><td><input type="number" class="form-control" name="from" required></td><td><input type="number" class="form-control" name="to" required></td><td> ' + cocode_values + ' </td><td><input disabled type="checkbox" name="inherit" value="inherit"></td><td><a onclick="clone_ext_table_row()" title="Add new row"><i class="fa fa-plus text-primary"></i></a> </td></tr>';
                ext_add_new_line = '<tr id="extend_attr_tr"><td><input type="number" class="form-control" name="from" required></td><td><input type="number" class="form-control" name="to" required></td><td> ' + cocode_values + ' </td><td><input disabled type="checkbox" name="inherit" value="inherit"></td><td><a onclick="clone_ext_table_row()" title="Add new row"><i class="fa fa-plus text-primary"></i></a> <a onclick="remove_ext_Row(this)" id="ext_new" title="Delete row"><i class="fa fa-trash text-primary"></i></a></td></tr>';
                $('#extend_attr_body').append(add_ext_attr);
            }
            document.getElementById('ext_porg_id').style.display = 'block';
            document.getElementById('ext_error_div').style.display = 'none';
            document.getElementById('company_id').style.display = 'block';
            document.getElementById('non_company_id').style.display = 'none';

        }
        if (GLOBAL_ON_DOUBLE_CLICK_NODE_TYPE != 'PGRP') {
            document.getElementById("resp_msg").innerHTML = 'Responsibility Not Applicable';
            document.getElementById('non_pgrp').style.display = 'block';
            document.getElementById('resp_pgrp').style.display = 'none';
        }
        else {
            if (resp_attr_html) {
                document.getElementById('resp_pgrp').style.display = 'block';
                document.getElementById('non_pgrp').style.display = 'none';
            }
            else {
                add_resp_attr = '<tr><td><input type="number" class="form-control" name="from" required></td><td><input type="number" class="form-control" name="to" required></td><td> ' + cocode_values + ' </td><td><a onclick=clone_resp_table_row() ><i class="fa fa-plus text-primary"></i></a></td></tr>';
                resp_add_new_line = '<tr><td><input type="number" class="form-control" name="from" required></td><td><input type="number" class="form-control" name="to" required></td><td> ' + cocode_values + ' </td><td><a onclick=clone_resp_table_row() ><i class="fa fa-plus text-primary"></i></a> <a onclick=remove_resp_Row(this) ><i class="fa fa-trash text-primary"></i></a></td></tr>';
                $('#responsibility_body').append(add_resp_attr);
                document.getElementById('resp_pgrp').style.display = 'block';
                document.getElementById('non_pgrp').style.display = 'none';
            }
        }
    }
    document.getElementById("attribute_overview").style.display = "block"
}


function onchange_node_id_dropdown(option_val) {
    opt_val = option_val.value
    var node_details = GLOBAL_NODE_DETAIL
    x = GLOBAL_ON_DOUBLE_CLICK_NODE_TYPE
    switch (x) {
        case "CCODE":
            $.each(node_details, function (i, item) {
                if (item.company_id == opt_val) {
                    $("#cc_name1").val(item.name1)
                    $("#cc_name2").val(item.name2)
                    GLOBAL_CC_NAME1_VALUE = item.name1
                    GLOBAL_CC_NAME2_VALUE = item.name2

                }
            });
            if (opt_val == '') {
                $("#cc_name1").val('')
                $("#cc_name2").val('')
                GLOBAL_CC_NAME1_VALUE = ''
                GLOBAL_CC_NAME2_VALUE = ''
            }
            break;
        case "PORG":
            $.each(node_details, function (i, item) {
                if (item.porg_id == opt_val) {
                    $("#POrg_desc").val(item.description)
                    GLOBAL_PORG_DESC_VALUE = item.description
                }

            });

            if (opt_val == '') {
                $("#POrg_desc").val('')
                GLOBAL_PORG_DESC_VALUE = ''
            }
            break;
        case "PGRP":
            $.each(node_details, function (i, item) {
                if (item.pgroup_id == opt_val) {
                    $("#Pgrp_desc").val(item.description)
                    GLOBAL_PGRP_DESC_VALUE = item.description

                }
            });
            if (opt_val == '') {
                $("#Pgrp_desc").val('')
                GLOBAL_PGRP_DESC_VALUE = ''
            }
            break;
        default:
            break;
        // code block
    }


}

// get company code drop down for responsibility tab in org attributes
function get_cocode_drop_down(org_comp_dropdown_list, centralize_purch_level_flag) {
    var cocode_values = ''
    var cocode_drop_down = ''
    if (centralize_purch_level_flag) {
        $.each(org_comp_dropdown_list, function (i, item) {
            cocode_drop_down += '<option value="' + item + '" >' + item + '</option>';
        })
        cocode_values = '<select class="form-control">' + cocode_drop_down + '</select>'
    }
    else {
        console.log("org_comp_dropdown_list")
        console.log(org_comp_dropdown_list)
        cocode_values = '<input type="text" value=' + org_comp_dropdown_list[0] + ' disabled>';
    }
    return cocode_values
}

// on double click of node hid all button in basic details and display button based on node type
function initial_display_hide_button(node_type) {
    // display none to
    hide_ele("#tab_save")
    hide_ele("#tab_cancel")
    hide_ele("#tab_edit")
    hide_ele("#basic_details_button")
    switch (node_type) {
        case "CCODE":
        case "PORG":
        case "PGRP":
        case "PLANT":
        case "NODE":
        case "RNODE":
            display_ele("#tab_edit")
            display_ele("#basic_details_button")
            break;
        default:
            break;
    }

}

//on double click of node, display edit button
function on_edit_display_hide_button() {
    hide_ele("#tab_save");
    hide_ele("#tab_cancel");
    hide_ele("#tab_edit");
    display_ele("#tab_edit");
}

//on click of save basic details, it saves basic data in to db
async function on_click_save_basic_details() {
    OpenLoaderPopup()
    let details_edit_input = "";
    let details_edit_link = " ";
    let details_edit_data = '';
    let node_type = GLOBAL_ON_DOUBLE_CLICK_NODE_TYPE;
    let check_edited = " ";
    node_name = $("#BDname").val()
    details_edit_input = {}
    details_edit_input.node_name = node_name
    details_edit_input.node_detail_flag = GLOBAL_NODE_DETAIL_EXISTS
    details_edit_input.object_id = GLOBAL_ONCLICK_UPDATE_OBJ_ID
    details_edit_input.node_type = node_type
    switch (node_type) {
        case "CCODE":
            let name1 = $("#cc_name1").val().trim()
            let name2 = $("#cc_name2").val().trim()
            let object_id = $("#select_cc_id").val().trim()
            if (node_ID_validation(object_id) == false) {
                details_edit_data = "Company ID should not consists of special characters"
            }
            else {
                details_edit_input.name1 = name1
                details_edit_input.name2 = name2
                details_edit_input.company_id = object_id
                org_name = await save_basic_details_ajax_call(details_edit_input);
                update_org_node_name(org_name.org_model_name)
                node_type_disable_fields_list = ['cc_id', 'cc_name1', 'cc_name2', 'select_cc_id', 'BDname']
                disable_fields(node_type_disable_fields_list)
                on_edit_display_hide_button()
                CloseLoaderPopup();
            }

            break;
        case "PORG":
            let porg_description = $("#POrg_desc").val().trim()
            let porg_id = $("#select_porg_id").val().trim()
            if (node_ID_validation(porg_id) == false) {
                details_edit_data = "Porg ID should not consists of special characters"
            }
            else {
                details_edit_input.description = porg_description
                details_edit_input.porg_id = porg_id
                org_name = await save_basic_details_ajax_call(details_edit_input);
                update_org_node_name(org_name.org_model_name)
                node_type_disable_fields_list = ['porg_id', 'POrg_desc', 'select_porg_id', 'BDname']
                disable_fields(node_type_disable_fields_list)
                on_edit_display_hide_button()
                CloseLoaderPopup();
            }

            break;
        case "PGRP":
            let pgrp_description = (document.getElementById("Pgrp_desc").value).trim()
            let pgrp_id = (document.getElementById("select_pgrp_id").value).trim()
            if (node_ID_validation(pgrp_id) == false) {
                details_edit_data = "Pgrp ID should not consists of special characters"
            }
            else {
                details_edit_input.description = pgrp_description
                details_edit_input.pgrp_id = pgrp_id
                org_name = await save_basic_details_ajax_call(details_edit_input);
                update_org_node_name(org_name.org_model_name)
                node_type_disable_fields_list = ['pgrp_id', 'Pgrp_desc', 'select_pgrp_id', 'BDname']
                disable_fields(node_type_disable_fields_list)
                on_edit_display_hide_button()
                CloseLoaderPopup();
            }

            break;
        case "NODE":
        case "RNODE":
            org_name = await save_basic_details_ajax_call(details_edit_input);
            update_org_node_name(org_name.org_model_name)
            update_root_node_in_root_node_search(org_name.org_model_name)
            node_type_disable_fields_list = ['BDname']
            disable_fields(node_type_disable_fields_list)
            on_edit_display_hide_button()
            CloseLoaderPopup();
            break;
        default:
            break;
    }
    let AddResult = document.getElementById("BD_result")
    if (details_edit_data) {
        AddResult.innerHTML = details_edit_data;
        AddResult.style.color = "red"

    }
    else {
        details_result = ("Data saved successfully")
        AddResult.innerHTML = details_result
        AddResult.style.color = "green"
    }
    $('#modal_Basic_Detail').modal('show')
    document.getElementById("BD").style.display = "block";

}

//on change in node name, update tree structure
function update_org_node_name(org_model_name) {
    var update_ele = document.getElementById(basic_element_id);
    if (basic_element_id != "root-node") {
        update_ele.children[3].innerHTML = org_model_name;
    }
    else {
        update_ele.children[0].lastChild.nodeValue = org_model_name;
    }
    basic_node_name = org_model_name;
    for (var i = 0; i < jsonData.length; i++) {
        if (jsonData[i].pk == GLOBAL_ONCLICK_UPDATE_OBJ_ID) {
            jsonData[i].fields.name = org_model_name[0];
        }
    }
}

function update_root_node_in_root_node_search(root_node_name) {
    $('#org-list option[value="' + GLOBAL_ROOT_NODE_NAME + '"]').remove()
    html_option_default = '<option value="' + root_node_name + '" selected>' + root_node_name + '</option>'
    $("#org-list").prepend(html_option_default);
    $("#org-list")[0].options[0].selected = true;
    for (var i = 0; i < orgs.length; i++) {
        if (orgs[i].fields.object_id == GLOBAL_ONCLICK_UPDATE_OBJ_ID) {
            orgs[i].fields.name = root_node_name
        }
    }
}


// otp input fields with backspace
// document.addEventListener("DOMContentLoaded", function(event) {

//     function OTPInput() {
//         const inputs = document.querySelectorAll('#otp > *[id]');
//         for (let i = 0; i < inputs.length; i++) {
//             inputs[i].addEventListener('keydown', function(event) {
//                 if (event.key==="Backspace" ) {
//                     inputs[i].value='' ; if (i !==0) inputs[i - 1].focus();
//                 } else {
//                     if (i===inputs.length - 1 && inputs[i].value !=='' ) {
//                         return true;
//                     } else if (event.keyCode> 47 && event.keyCode < 58) {
//                         inputs[i].value=event.key;
//                         if (i !==inputs.length - 1) inputs[i + 1].focus(); event.preventDefault();
//                     } else if (event.keyCode> 64 && event.keyCode < 91) {
//                         inputs[i].value=String.fromCharCode(event.keyCode);
//                         if (i !==inputs.length - 1) inputs[i + 1].focus(); event.preventDefault();
//                     }
//                 }
//             });
//         }
//     }
//     OTPInput();
// });

// <!-- <i class="fa fa-pencil-square-o text-primary"></i> -->
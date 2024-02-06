//********************************************
$(document).ready(function () {
    nav_bar_admin();
    table_sort_filter_export_excel();

    $('#hg_approval_report_search').click(function () {
        $('#hg_loader').modal('show');
    });

    $('.multiple_select').selectpicker();
    $('.multiple_select').selectpicker('val', selected_status_value);
    $('#acc_assgn_cat').val(selected_status_value).attr('selected', 'selected');
});

//********************************************
window.onbeforeunload = function () {
    sessionStorage.setItem("COMP_CODE", $('#id_comp_code_app').val());
    sessionStorage.setItem("ACC_ASSGN_CAT", $('#acc_assgn_cat').val());
}

//********************************************
window.onload = function () {
    comp_code = sessionStorage.getItem("COMP_CODE");
    acc_assgn_cat = sessionStorage.getItem("ACC_ASSGN_CAT");
    $('#id_comp_code_app').val(comp_code).attr('selected', 'selected');
    $('#acc_assgn_cat').val(acc_assgn_cat).attr('selected', 'selected');
}

//********************************************
function resetCompanyCodeDropdown() {
    var companyCodeDropdown = document.getElementById('id_comp_code_app');
    if (companyCodeDropdown) {
        companyCodeDropdown.selectedIndex = 0;
    }
}

//********************************************
window.onload = function () {
    resetCompanyCodeDropdown();
}

//********************************************
$('#hg_approval_report_search').click(function () {
    OpenLoaderPopup();
});

//********************************************
$(document).ready(function () {
    $('.multiple_select').selectpicker();

    $('#hg_approval_report_search').click(function () {
        $('#table-container').show();
        OpenLoaderPopup();

        var selectedCompany = $('#id_comp_code_app').val();
        var selectedCategories = $('#acc_assgn_cat').val();

        var selectedData = {
            company: selectedCompany,
            categories: selectedCategories
        };

        localStorage.setItem("selectedData", JSON.stringify(selectedData));
    });

    var selectedDataJSON = localStorage.getItem("selectedData");
    if (selectedDataJSON) {
        var selectedData = JSON.parse(selectedDataJSON);

        if (selectedData.company) {
            $('#id_comp_code_app').val(selectedData.company);
        }

        if (selectedData.categories) {
            $('#acc_assgn_cat').selectpicker('val', selectedData.categories);
        }
    }
});

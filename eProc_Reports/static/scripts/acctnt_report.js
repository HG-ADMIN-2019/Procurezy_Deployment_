$(document).ready(function () {
    table_sort_filter_export_excel();
    nav_bar_admin();
    $('#hg_accnt_report_search').click(function () {
        $('#hg_loader').modal('show');
    });
});

window.onbeforeunload = function () {
    sessionStorage.setItem("COMP_CODE", $('#id_comp_code_app').val());
    sessionStorage.setItem("ACC_ASSGN_CAT", $('#id_acc_assgn_cat').val());
    sessionStorage.setItem("LANG", $('#id_language').val());
};

$('#hg_accnt_report_search').click(function () {
    OpenLoaderPopup();
});

$(document).ready(function () {
    $('#clear_filters_button').click(function () {
        $('#id_comp_code_app').val(null);
        $('#id_acc_assgn_cat').val(null);
        $('#id_language').val(null);
        localStorage.removeItem("COMP_CODE");
        localStorage.removeItem("ACC_ASSGN_CAT");
        localStorage.removeItem("LANG");
        $('.multiple_select').selectpicker('refresh');
    });
});

$('#id_language').on('change', function () {
    var selectedValue = $(this).val();
    localStorage.setItem("LANG", selectedValue);
});

$(document).ready(function () {
    var lang = localStorage.getItem("LANG");
    if (lang !== null) {
        $('#id_language').val(lang);
    }
});

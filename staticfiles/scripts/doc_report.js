//********************************************
function search_click() {
    $("#err_msg").prop("hidden", false);
}

// Function to store the selected values when the form is submitted
$('#hg_doc_report_search').click(function () {
    sessionStorage.setItem("DOC_TYPE", $('#id_doc_type').val());
    sessionStorage.setItem("COMPANY", $('#id_company_code').val());

    // Store the supplier field value
    sessionStorage.setItem("SUPPLIER", $('#supplier').val());
});

// Function to retrieve and apply the stored values when the page loads
$(document).ready(function () {
    var storedDocType = sessionStorage.getItem("DOC_TYPE");
    var storedCompany = sessionStorage.getItem("COMPANY");

    if (storedDocType) {
        $('#id_doc_type').val(storedDocType);
    }

    if (storedCompany) {
        $('#id_company_code').val(storedCompany);
    }

    // Retrieve and apply the "Supplier" field value
    var storedSupplier = sessionStorage.getItem("SUPPLIER");
    if (storedSupplier) {
        $('#supplier').val(storedSupplier);
    }
});

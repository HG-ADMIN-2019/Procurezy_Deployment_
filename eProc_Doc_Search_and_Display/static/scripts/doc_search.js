$(document).ready(function(){

    nav_bar_shop();

    // sidenav code
    // localStorage.removeItem("previously_selected_link");
    // $('.sidenav__listitem').removeClass('sidenav__listitem-active');
    // document.getElementById('sidenav__listitem-shop').classList.add('sidenav__listitem-active');

    // Accordian on expand and collapse indicate respective icon
    $('.collapse').on('shown.bs.collapse', function (){
        $(this).parent().find('.fa-plus').removeClass('fa-plus').addClass('fa-minus');
    }).on('hidden.bs.collapse', function (){
        $(this).parent().find('.fa-minus').removeClass('fa-minus').addClass('fa-plus');
    })

    // Datatable plugin
    $('.table_sort_filter_pagination').DataTable( {
        "lengthChange": false,
        "searching":   false,
        "ordering": false,
        "info":     false
    } );

    // Bootstrap-select plugin being called to render multiselect dropdown 
    $('.multiple_select').selectpicker();
    $('.multiple_select').selectpicker('val', selected_status_value);

});

function get_pgrp_user(button_id){
    pgrp_id = button_id.id;
}

// Function to expand and collapse accordian
function displayToggle(element) {
    id = element.id.split('-')[1]
    element.dataset.target = '#collapseSearch'+id
}

$('#search_button_id').click(function () {
    OpenLoaderPopup();
})
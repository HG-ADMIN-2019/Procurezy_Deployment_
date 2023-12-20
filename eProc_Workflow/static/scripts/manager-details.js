function show_manager_detail(id) {
    sc_app_guid_data = {};
    sc_app_guid_data['guid'] = id;

    ajax_get_manager_detail(sc_app_guid_data)

    $('#manager_detail_body').empty();
    trHTML = '<tr></tr>';
    $.each(response, function (i, sc_app) {
        trHTML += '<tr><td>' + sc_app.fields.app_desc + '</td><td >' + sc_app.fields.step_num + '</td><td>' + sc_app.fields.proc_lvl_sts + '</td><td>' + sc_app.fields.app_sts + '</td><td>' + sc_app.fields.app_id + '</td><td>' + sc_app.fields.proc_time + '</td><td>' + sc_app.fields.received_time + '</td></tr>';
    });
    $('#manager_detail_body').append(trHTML);
    $('#manager-detail-popup').modal('show');

}
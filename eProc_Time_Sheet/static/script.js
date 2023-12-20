// Timesheet related

// Global Variables
var empty_select = '<option value="">Select</option>'
var project_category_dropdown = '';
var available_project_category_array = new Array();
var holiday_list_global;
var weekend_in_days_global;
var is_current_week = true;

const daysInWeek = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'];

const day_number_object = {
    'monday': 1,
    'tuesday': 2,
    'wednesday': 3,
    'thursday': 4,
    'friday': 5,
    'saturday': 6,
    'sunday': 7
}

const determine_week_day_by_number = {
    1: 'monday',
    2: 'tuesday',
    3: 'wednesday',
    4: 'thursday',
    5: 'friday',
    6: 'saturday',
    7: 'sunday'
}

function insert_timesheet_row(day) {
    var lastid = $("." + day + ":last").attr("id");
    var split_id = lastid.split("_");
    var nextindex = Number(split_id[1]) + 1;

    // Adding new div
    $("." + day + ":last").after('<div class="hg_card_outer_div input_timesheet_form ' + day + '" id="' + day + '_' + nextindex + '"></div>');
    // Adding element to <div>
    new_row = ' <div style="float: left; padding-top: 35px;"> <button type="button" class="btn btn-danger hg_hide_display_mode btn-circle btn-sm" id="' + day + '-' + nextindex + '" onclick="remove_timesheet_row(this.id);"><i class="fa fa-minus" aria-hidden="true"></i></button></div><div class="hg_project_category"><label>Select Category:</label><select onchange="update_project_categories_onchange(this)" id="category_' + day + '_' + nextindex + '" name="category" class="form-control category_' + day + ' project_category"><option>Select</option>' + project_category_dropdown + '</select></div><div class="hg_timespent_div"><label>Time spent:</label><br><input type="" class="form-control timespent_' + day + '_' + nextindex + '" placeholder="Enter time spent"></div><div class="hg_task_div"><label>Task:</label><br><textarea class="form-control task_' + day + '_' + nextindex + '" rows="1" cols="50"></textarea></div>'
    $("#" + day + "_" + nextindex).append(new_row);
    test_class = document.getElementsByClassName('category_monday')
}

function remove_timesheet_row(id) {
    var split_id = id.split("-");
    var day = split_id[0];
    var deleteindex = split_id[1];
    $("#" + day + "_" + deleteindex).remove();
}

const update_project_categories_onchange = (element) => {
    selected_value = element.value;
    select_id = element.id
    day = select_id.split('_')[1]
    card_number = select_id[select_id.length - 1]
    select_class = select_id.substring(0, select_id.length - 2)
    test = $('[id^="' + select_class + '"]')
    timespent_class = 'timespent_' + day + '_' + card_number
    task_class = 'task_' + day + '_' + card_number
    set_timespent_id = document.getElementsByClassName(timespent_class)[0].setAttribute('id', 'timespent-' + selected_value + '-' + day)
    set_task_id = document.getElementsByClassName(task_class)[0].setAttribute('id', 'task-' + selected_value + '-' + day)
    for (i = 0; i < test.length; i++) {
        dynamic_card_id = test[i].id
        dynamic_card_number = dynamic_card_id[dynamic_card_id.length - 1]
        if (card_number !== dynamic_card_number) {
            if (document.getElementById(dynamic_card_id).value == selected_value) {
                alert(selected_value + ' is already selected');
                document.getElementById(select_id).selectedIndex = 0;
                document.getElementsByClassName(timespent_class)[0].setAttribute('id', '')
                document.getElementsByClassName(task_class)[0].setAttribute('id', '')
            }
        }
    }
}


const get_timesheet_data = () => {
    var final_array = new Array();
    for (i = 0; i < available_project_category_array.length; i++) {
        var timesheet_week_data = {};
        project_category = project_category_array[i]
        timespent_ids = 'timespent-' + project_category + '-';
        project_cat_based_id = $('[id^="' + timespent_ids + '"]')
        for (j = 0; j < project_cat_based_id.length; j++) {
            timespent_id = project_cat_based_id[j].id
            day = timespent_id.split('-').slice(-1)[0]
            timespent = document.getElementById(timespent_id).value
            task = document.getElementById('task-' + project_category + '-' + day).value
            timesheet_week_data['effort' + day_number_object[day]] = timespent
            timesheet_week_data['description' + day_number_object[day]] = task
        }
        timesheet_week_data['project_category'] = project_category
        if (Object.keys(timesheet_week_data).length > 1) {
            final_array.push(timesheet_week_data)
        }
    }
    final_array.push({
        'project_id': document.getElementById('project_id').innerHTML,
        'project_description': document.getElementById('project_desc').innerHTML,
        'start_date': document.getElementById('project_start_date').innerHTML,
        'end_date': document.getElementById('project_end_date').innerHTML,
        'monday': document.getElementById('date_monday').innerHTML,
        'tuesday': document.getElementById('date_tuesday').innerHTML,
        'wednesday': document.getElementById('date_wednesday').innerHTML,
        'thursday': document.getElementById('date_thursday').innerHTML,
        'friday': document.getElementById('date_friday').innerHTML,
        'saturday': document.getElementById('date_saturday').innerHTML,
        'sunday': document.getElementById('date_sunday').innerHTML,
        'week_number': document.getElementById('week_number').innerHTML
    })
    return final_array;
}

const get_project_details = () => {
    var url = $("#get_project_detail_btn").attr("data-url");
    project_category_dropdown = '';
    var project_id = document.getElementById("choose_project").value;
    if (!project_id) {
        alert('Please select project')
        return
    }
    $.ajax({
        type: "POST",
        url: url,
        data: {
            project_id: project_id,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        success: function (context) {
            remove_previous_divs()
            clear_values()
            edit_mode()
            $('#display_timesheet_buttons').html('')
            number_of_previous_timesheets = context.project_data_list.length
            previous_timesheet_guid = context.project_data_list
            var generate_icons = ''
            for (i = 0; i < number_of_previous_timesheets; i++) {
                generate_icons += '<button id="' + previous_timesheet_guid[i]['guid'] + '" class="btn btn-primary" onclick="get_previous_week_timesheet(this.id)" data-url="/timesheet/display-timesheet/">Week' + previous_timesheet_guid[i]['week_number'] + '</button>'
            }
            $('#display_timesheet_buttons').html(generate_icons)
            display_current_week_data(context)
            $('#save_timesheet_btn').attr('hidden', false)
            $('#display_current_week').attr('hidden', true)
            $('#edit_timesheet_btn').attr('hidden', false)
        },
        error: function (context) {
            alert(context.responseJSON.error_message)
        }
    })
}

function save_timesheet_data() {
    const save_url = $("#save_timesheet_btn").attr("data-url");
    var data = get_timesheet_data()
    $.ajax({
        type: "POST",
        url: save_url,
        data: JSON.stringify(data),
        success: function (context) {
            alert('Data saved successfully')
            display_mode()
        }
    })
}

function edit_timesheet_btn() {
    const edit_mode = $("#edit_timesheet_btn").attr("data-url");
    var data = get_timesheet_data()
    $.ajax({
        type: "POST",
        url: save_url,
        data: JSON.stringify(data),
        success: function (context) {
            alert('Data saved successfully')
            display_mode()
        }
    })
}

const display_current_week_data = (context) => {
    weekend_in_days_global = context.weekend_in_days
    $('#project_val').empty()
    document.getElementById("project_val").innerHTML = '<div>Start Date : ' + '<span id="project_start_date">' + context.project_start_date + '</span>' + '<br>' + 'End Date: <span id="project_end_date">' + context.project_end_date + '</span></div>';
    var det_div = document.getElementById("project_det_div");
    det_div.style.display = "block";
    project_category_array = context.project_categories
    project_category_class = document.getElementsByClassName('project_category')
    for (i = 0; i < project_category_array.length; i++) {
        project_category_dropdown += '<option value="' + project_category_array[i] + '">' + project_category_array[i] + '</option>'
        available_project_category_array.push(project_category_array[i])
    }

    for (j = 0; j < project_category_class.length; j++) {
        project_category_class[j].innerHTML = empty_select + project_category_dropdown
    }
    document.getElementById("project_id").innerHTML = context.project_id;
    document.getElementById("project_desc").innerHTML = context.project_description;
    for (i = 0; i < context.weekend_in_days.length; i++) {
        document.getElementById('update_holiday_' + context.weekend_in_days[i]).innerHTML = 'Weekend'
    }

    holiday_list = context.holiday_list
    holiday_list_global = holiday_list
    get_date_id = $('[id^="date_"]')
    for (i = 0; i < get_date_id.length; i++) {
        date_id = get_date_id[i].id
        day = date_id.split('_')[1]
        date = $('#' + date_id).html()
        if (holiday_list.includes(date)) {
            $('#update_holiday_' + day).html('Holiday')
        }
    }
}

const get_previous_week_timesheet = (element_id) => {
    const previous_week_url = $("#" + element_id).attr("data-url");
    $.ajax({
        type: "POST",
        url: previous_week_url,
        data: {
            'project_data_guid': element_id,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        success: function (context) {
            remove_previous_divs()
            clear_values()
            $('#display_current_week').attr('hidden', false)
            $('#save_timesheet_btn').attr('hidden', true)
            dates = context.previous_week_data['dates']
            $.each(dates, function (index, value) {
                day_number = index + 1
                date_day = determine_week_day_by_number[day_number]
                $('#date_' + date_day).html(value)
                if (holiday_list_global.includes(value)) {
                    $('#update_holiday_' + date_day).html('Holiday')
                } else {
                    if (!weekend_in_days_global.includes(date_day)) {
                        $('#update_holiday_' + date_day).html('')
                    }
                }
            });

            for (i = 0; i < daysInWeek.length; i++) {
                day = daysInWeek[i]
                day_data = context.previous_week_data[day]
                for (j = 0; j < day_data.length; j++) {
                    if (j != 0) {
                        insert_timesheet_row(day)
                    }
                    project_category = day_data[j]['project_category']
                    effort = day_data[j]['effort']
                    description = day_data[j]['description']
                    document.getElementById('category_' + day + '_' + (j + 1)).value = project_category
                    document.getElementsByClassName('timespent_' + day + '_' + (j + 1))[0].value = effort
                    document.getElementsByClassName('task_' + day + '_' + (j + 1))[0].value = description
                }
            }
            display_mode()
        }
    })
}

const display_mode = () => {
    $('input, textarea, .project_category').prop('disabled', true)
    $('.hg_hide_display_mode').hide()
}

const edit_mode = () => {
    $('input, textarea, .project_category').prop('disabled', false)
    $('.hg_hide_display_mode').show()
}

const remove_previous_divs = () => {
    $.each(daysInWeek, function (index, value) {
        id = value + '_'
        get_previous_div_ids = $('[id^="' + id + '"]')
        for (j = 0; j < get_previous_div_ids.length; j++) {
            if (j != 0) {
                $('#' + get_previous_div_ids[j].id).remove()
            }
        }
    });
}

const clear_values = () => {
    $('input, textarea, .project_category').val('')
}

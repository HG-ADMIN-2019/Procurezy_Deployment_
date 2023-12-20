
//To show supplier field only for purchase order
function docchanged(doc_type){
    display_status(doc_type)
}

// To get attachments
function get_attach(path){
$.ajax({
    type: 'POST',
        url: 'attachments',
        data: {
        'file_path':path,
        'csrfmiddlewaretoken': $("input[name='csrfmiddlewaretoken']").val(),
        },
        success: function (data) {
            $("#attach_col").empty();
            $("#attach_col").html(data);
        }
      });
}

// To get PO preview
function get_pdf(path){
var new_div=document.createElement('div');
new_div.innerHTML=document.getElementById('popdf_col').innerHTML;
new_div.id='hide_'+no_of_hide;
no_of_hide+=1;
document.getElementById('up-hide-div').appendChild(new_div);
$.ajax({
    type: 'POST',
        url: 'attachments',
        data: {
        'file_path':path,
        'csrfmiddlewaretoken': $("input[name='csrfmiddlewaretoken']").val(),
        },
        success: function (data) {
          $("#popdf_col").empty();
          $("#popdf_col").html(data);
        }
      });
}

// creating the backlink for PO preview
function up_hide_div(){
    if(no_of_hide>0){
        no_of_hide-=1;
        $("#popdf_col").empty();
        var remdiv=document.getElementById('hide_'+no_of_hide);
        document.getElementById('popdf_col').appendChild(remdiv);
    }
}

// Select - Notes tab selection start
function openEvent(evt, eventName) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(eventName).style.display = "block";
    evt.currentTarget.className += " active";
    }
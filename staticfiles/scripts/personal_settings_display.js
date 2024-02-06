$(document).ready(function () {
  nav_bar_user_settings();

  if (action == 'Save') {
    display_elements('', ['save_id', 'cancel_id', 'change_password'])
    hide_elements('', ['edit_id'])
  }
  if (action == 'Edit') {
    display_elements('', ['edit_id'])
    hide_elements('', ['save_id', 'cancel_id', 'change_password'])
  }

  function display_elements(prefix, ele_ids) {
    try {
      ele_ids.forEach((ele_id) => { $("#" + prefix + ele_id).removeClass('d-none') })
    } catch (error) {
      console.log(error)
      return
    }
  }

  function hide_elements(prefix, ele_ids) {
    try {
      ele_ids.forEach((ele_id) => { $("#" + prefix + ele_id).addClass('d-none') })
    } catch (error) {
      console.log(error)
      return
    }
  }

  console.log(action)

});

// Buttons added with an event-listener to trigger popup-loader on click
var buttons = document.getElementsByClassName('pop-up-loader');
for(var i=0; i<buttons.length; i++){
  buttons[i].addEventListener("click", function(){ OpenLoaderPopup(); })
}
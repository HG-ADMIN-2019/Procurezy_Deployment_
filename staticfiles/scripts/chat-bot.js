// Collapsible
var coll = document.getElementsByClassName("collapsible");

for (let i = 0; i < coll.length; i++) {
    coll[i].addEventListener("click", function () {
        this.classList.toggle("active");

        var content = this.nextElementSibling;

        if (content.style.maxHeight) {
            content.style.maxHeight = null;
        } else {
            content.style.maxHeight = content.scrollHeight + "px";
        }

    });
}
 var coll = document.getElementsByClassName("togButton");
var i;

for (i = 0; i < coll.length; i++) {
  coll[i].addEventListener("click", function() {
    this.classList.toggle("active");
    var content = this.nextElementSibling;
    if ($('.togCheck').is(':hidden')) {
      content.style.display = "none";
    } else {
      content.style.display = "block";
    }
//       setTimeout(() => {
//       $("#content_id").toggle("slow");
//    }, 5000)
  });
}

function getTime() {
    let today = new Date();
    hours = today.getHours();
    minutes = today.getMinutes();

    if (hours < 10) {
        hours = "0" + hours;
    }

    if (minutes < 10) {
        minutes = "0" + minutes;
    }

    let time = hours + ":" + minutes;
    return time;
}

// Gets the first message
function firstBotMessage() {
    let firstMessage = "How can we help you?"
    document.getElementById("botStarterMessage").innerHTML = '<p class="botText"><span>' + firstMessage + '</span></p>';

    let time = getTime();

    $("#chat-timestamp").append(time);
    document.getElementById("userInput").scrollIntoView(false);
}

firstBotMessage();

// Retrieves the response
function getHardResponse(userText) {
    let botResponse = getBotResponse(userText);
    let botHtml = '<p class="botText"><span>' + botResponse + '</span></p>';
    $("#chatbox").append(botHtml);
}
function getBotResponse(input) {
    let keyword_arr = ["hi", "hello", "shopping cart", "order"];

    if (keyword_arr.includes(input) || (input == "")) {

    }
    $("#chatbox").append(input);
    document.getElementById("chat-bar-bottom").scrollIntoView(true);
}

//Gets the text text from the input box and processes it
function getResponse() {
    let userText = $("#textInput").val();
       let keyword_arr = ["hi", "hello", "shopping cart", "order"];

    if (keyword_arr.includes(userText) || (userText == "")) {
        $("#first_msg").prop("hidden", false);

    }
    $("#textInput").val("");
    document.getElementById("chat-bar-bottom").scrollIntoView(true);


}
function product_service(){
     let productHtml = '<p id="id_search" class="botText botTextSub"><a class="userText" href="https://eprocure.gov.in/eprocure/app;" target="_blank">' + "- Search Products/Services" +  '</a></p>';
     $("#chatbox").append(productHtml);
     let freetextHtml = '<p  class="botText botTextSub"><a class="userText" href="https://eprocure.gov.in/eprocure/app;" target="_blank">' + "- Freetext" +  '</a></p>';
     $("#chatbox").append(freetextHtml);
     let prHtml = '<p  class="botText botTextSub"><a class="userText" href="https://eprocure.gov.in/eprocure/app;" target="_blank">' + "- Purchase Requisition" +  '</a></p>';
     $("#chatbox").append(prHtml);
    document.getElementById("chat-bar-bottom").scrollIntoView(true);
}
function personalize(){
     const container = document.getElementById('chatbox');
//     const p1 = document.createElement('p');
//     const p2 = document.createElement('p');
//     p1.innerHTML = '<p id="id_search" class="botText botTextSub"><a class="userText" href="https://eprocure.gov.in/eprocure/app;" target="_blank">' + "- Search Products/Services" +  '</a></p>';
//     p2.innerHTML = '<p id="id_search" class="botText botTextSub"><a class="userText" href="https://eprocure.gov.in/eprocure/app;" target="_blank">' + "- Search Products/Services" +  '</a></p>';
//    container.replaceChildren(p1, p2);
//    container.textContent = '';
    let productHtml = '<p id="id_search" class="botText botTextSub"><a class="userText" href="https://eprocure.gov.in/eprocure/app;" target="_blank">' + "- Search Products/Services" +  '</a></p>';
     $("#chatbox").append(productHtml);
     let freetextHtml = '<p  class="botText botTextSub"><a class="userText" href="https://eprocure.gov.in/eprocure/app;" target="_blank">' + "- Freetext" +  '</a></p>';
     $("#chatbox").append(freetextHtml);
     let prHtml = '<p  class="botText botTextSub"><a class="userText" href="https://eprocure.gov.in/eprocure/app;" target="_blank">' + "- Purchase Requisition" +  '</a></p>';
     $("#chatbox").append(prHtml);
 document.getElementById("chat-bar-bottom").scrollIntoView(true);
}
// Handles sending text via button clicks
function buttonSendText(sampleText) {
    let userHtml = '<p class="userText"><span>' + sampleText + '</span></p>';

    $("#textInput").val("");
    $("#chatbox").append(userHtml);
    document.getElementById("chat-bar-bottom").scrollIntoView(true);

    //Uncomment this if you want the bot to respond to this buttonSendText event
<!--     setTimeout(() => {-->
<!--         getHardResponse(sampleText);-->
<!--     }, 1000)-->
}

function sendButton() {
    getResponse();
}

function heartButton() {
    buttonSendText("Heart clicked!")
}

// Press enter to send a message
$("#textInput").keypress(function (e) {
    if (e.which == 13) {
        getResponse();
    }
});
function close_window(){
    localStorage.setItem("chatVisible", "False");
    $("#bot_popup_id").hide();
}
let currentRecipient = '';
let chatInput = $('#chat-input');
let chatButton = $('#btn-send');
let userList = $('#user-list');
let messageList = $('#messages');

function updateUserList() {
    $.getJSON('api/v1/user/', function (data) {
        userList.children('.user').remove();
        for (let i = 0; i < data.length; i++) {
            const userItem = `<a class="list-group-item user">${data[i]['username']}</a>`;
            $(userItem).appendTo('#user-list');
        }
        $('.user').click(function () {
            userList.children('.active').removeClass('active');
            let selected = event.target;
            $(selected).addClass('active');
            setCurrentRecipient(selected.text);
        });
    });
}

function drawMessage(message) {
    let position = 'left';
    const date = new Date(message.timestamp);
    if (message.user === currentUser) position = 'right';
    const messageItem = `
            <li class="message ${position}">
                <div class="avatar">${message.user}</div>
                    <div class="text_wrapper">
                        <div class="text">${message.body}<br>
                            <span class="small">${date}</span>
                    </div>
                </div>
            </li>`;
    $(messageItem).appendTo('#messages');
}

function getConversation(recipient) {
    $.getJSON(`/api/v1/message/?target=${recipient}`, function (data) {
        messageList.children('.message').remove();
        for (let i = data['results'].length - 1; i >= 0; i--) {
            drawMessage(data['results'][i]);
        }
        messageList.animate({scrollTop: messageList.prop('scrollHeight')});
    });

}

function getMessageById(message) {
    id = JSON.parse(message).message
    $.getJSON(`/api/v1/message/${id}/`, function (data) {
        if (data.user === currentRecipient ||
            (data.recipient === currentRecipient && data.user == currentUser)) {
            drawMessage(data);
        }
        messageList.animate({scrollTop: messageList.prop('scrollHeight')});
    });
}

function sendMessage(recipient, body) {
    $.post('/api/v1/message/', {
        recipient: recipient,
        body: body
    }).fail(function () {
        alert('Error! Check console!');
    });
    getConversation(recipient);
}

function setCurrentRecipient(username) {
    currentRecipient = username;
    getConversation(currentRecipient);
    enableInput();
}


function enableInput() {
    chatInput.prop('disabled', false);
    chatButton.prop('disabled', false);
    chatInput.focus();
}

function disableInput() {
    chatInput.prop('disabled', true);
    chatButton.prop('disabled', true);
}

$(document).ready(function () {
    updateUserList();
    disableInput();


var ws = 'ws://'
if (window.location.protocol === 'ws://127.0.0.1:8000/'){
    ws = 'wss://'
}

    var socket = new WebSocket('ws://127.0.0.1:8000/ws', 'echo-protocol');

    chatInput.keypress(function (e) {
        if (e.keyCode == 13)
            chatButton.click();
    });

    chatButton.click(function () {
        if (chatInput.val().length > 0) {
            sendMessage(currentRecipient, chatInput.val());
            chatInput.val('');
        }
    });

    socket.onmessage = function (e) {
        getMessageById(e.data);
        console.log("message", e)
    var chatData = JSON.parse(e.data)
    if ($("#username").val() === chatData.username){
	   chatHolder.append(
	   	"<div class='d-flex justify-content-start mb-4'>"+
	   	            "<div class='img_cont_msg'>" +
	   	                "<img src='https://vignette.wikia.nocookie.net/tomandjerry/images/5/5f/JerryMouse.png/revision/latest?cb=20140723114908' class='rounded-circle user_img_msg'>"+
	   	            "</div>"+
	   	            "<div class='msg_cotainer'>" +
	   	                chatData.message +
	   	            "</div>" +
	   	         "</div>"
	 )
    }
    else{
    	chatHolder.append(
    	"<div class='d-flex justify-content-end mb-4'>"+
	   	            "<div class='msg_cotainer_send'>" +
	   	                chatData.message  +
	   	                "<span class='msg_time_send'>8:40 AM, Today</span>" +
	   	            "</div>" +
	   	            "<div class='img_cont_msg'>" +
	   	                "<img src='https://upload.wikimedia.org/wikipedia/en/f/f6/Tom_Tom_and_Jerry.png' class='rounded-circle user_img_msg'>"+
	   	            "</div>"+
	   	         "</div>"
	   	         )
    }
    };




    socket.onopen = function(e){
        console.log("open", e)
        var formData = $("#form");
        formData.submit(function(event){
            event.preventDefault();
            // prevents form from being submitted by default if socket is connected
            // default action will still work if socket is not connecting
            var msgData = $("#id_message").val()
            // chatHolder.append("<li> S: " + msgData + " via " + $("#username").val() + "</li>")
            msgText = {
                'message': msgData
            }
            socket.send(JSON.stringify(msgText))
            formData[0].reset()
        })
    }
});



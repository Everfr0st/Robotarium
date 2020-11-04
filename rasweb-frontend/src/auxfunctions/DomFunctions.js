export function setDialogPosition(username) {
    try {
        let div_user = document.getElementById("user_" + username);
        let dialog_userdiv = document.getElementById("dialog_" + username);
        console.log(div_user, dialog_userdiv)
        if (dialog_userdiv != null) {
            console.log(dialog_userdiv)

            let divuser_position = div_user.getBoundingClientRect();
            let dialogposition = {
                top: (divuser_position.top + divuser_position.bottom) / 2 - (0.40 * 285),
                left: divuser_position.left - 290,
            };

            dialog_userdiv.style = `
            top:${dialogposition.top}px;
            left: ${dialogposition.left}px;
            max-width: 290px;
            width: 295px;
            max-height: 285px;
            z-index: 1000;
            transition: all ease 500ms;
            display: block;`;
        }
    } catch {
    }
}

export function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}





/*@click = function (e) {
    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;
    chatSocket.send(JSON.stringify({
        'message': message
    }));
    messageInputDom.value = '';
};*/
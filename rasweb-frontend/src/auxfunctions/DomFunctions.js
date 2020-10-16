export function setDialogPosition(username) {
    try {
        let div_user = document.getElementById("user_" + username);
        let dialog_userdiv = document.getElementById("dialog_" + username);

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
      display: block;
      `;
    } catch { }
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
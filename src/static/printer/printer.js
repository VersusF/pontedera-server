let token = "";

async function login() {
    const pwd = document.getElementById("input_password").value;
    const baseurl = document.location.origin;
    try {
        const { data } = await axios.post(baseurl + "/printer/login", {
            password: pwd,
        });
        token = data.token;
        toastSuccess("Benvenuto");
        afterLogin();
    } catch (error) {
        toastError("Password errata");
    }
}

function afterLogin() {
    const loginDiv = document.getElementById("login");
    const mainDiv = document.getElementById("main");
    loginDiv.style.display = "none";
    mainDiv.style.display = "block";
}

/**
 * @param {string} msg 
 */
function toastError(msg) {
    toast(msg, "#ec0941", "#ebebfa");
}

/**
 * @param {string} msg 
 */
function toastSuccess(msg) {
    toast(msg, "#82ff9e", "#1b1a2c");
}

/**
 * @param {string} msg 
 */
function toastWarn(msg) {
    toast(msg, "#ecd509", "#1b1a2c");
}

/**
 * 
 * @param {string} msg 
 * @param {string} bgColor 
 * @param {string} textColor 
 */
function toast(msg, bgColor, textColor) {
    const toast = document.getElementById('toast');
    toast.style.backgroundColor = bgColor;
    toast.style.color = textColor;
    toast.innerHTML = msg;
    toast.classList.replace('toast-hidden', 'toast-shown');
    setTimeout(() => toast.classList.replace('toast-shown', 'toast-hidden'), 1500);
}
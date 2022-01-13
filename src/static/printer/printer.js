let token = "";

function init() {
    document.getElementById("input_password").addEventListener("keyup", event => {
        if (event.key === "Enter") {
            login();
        }
    });
}

async function login() {
    const pwd = document.getElementById("input_password").value;
    const baseurl = document.location.origin;
    try {
        const { data } = await axios.post(baseurl + "/printer/login", {
            password: pwd,
        });
        token = data.token;
        afterLogin().then(() => {
            toastSuccess("Benvenuto");
        }).catch(() => {
            toastError("Errore interno");
        });
    } catch (error) {
        toastError("Password errata");
    }
}

async function afterLogin() {
    const loginDiv = document.getElementById("login");
    const mainDiv = document.getElementById("main");
    loginDiv.style.display = "none";
    mainDiv.style.display = "block";

    const baseurl = document.location.origin;
    const queuedRequest = await axios.get(baseurl + "/printer/queued-jobs", {
        headers: {
            "auth": token
        }
    });
    addJobsToTable("queued-jobs", queuedRequest.data.jobs);

    const printedRequest = await axios.get(baseurl + "/printer/printed-jobs", {
        headers: {
            "auth": token
        }
    });
    addJobsToTable("printed-jobs", printedRequest.data.jobs);
}

/**
 * @param {string} tableId 
 * @param {{ timestamp: number, filename: string, copies: number }[]} jobs 
 */
function addJobsToTable(tableId, jobs) {
    const queuedTable = document.getElementById(tableId);
    for (const j of jobs) {
        const row = document.createElement("tr");
        const dateCell = document.createElement("td");
        dateCell.innerHTML = j.timestamp;
        row.appendChild(dateCell);

        const nameCell = document.createElement("td");
        nameCell.innerHTML = j.filename;
        row.appendChild(nameCell);

        const copiesCell = document.createElement("td");
        copiesCell.innerHTML = j.copies;
        row.appendChild(copiesCell);

        queuedTable.appendChild(row);
    }
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
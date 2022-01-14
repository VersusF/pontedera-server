const SESSION_STORAGE_TOKEN_KEY = "token";

const axiosClient = axios.create({
    baseURL: window.location.origin + "/printer",
});

function init() {
    document.getElementById("input_password").addEventListener("keyup", event => {
        if (event.key === "Enter") {
            login();
        }
    });
    // Check if old token is still valid
    const oldToken = sessionStorage.getItem(SESSION_STORAGE_TOKEN_KEY) || "";
    axiosClient.get("/check-token", {
        headers: { auth: oldToken }
    }).then(() => {
        // Old token is still valid
        axiosClient.defaults.headers.common.auth = oldToken;
        afterLogin().catch(e => {
            console.error(e);
            sessionStorage.removeItem(SESSION_STORAGE_TOKEN_KEY);
            toastError("Errore interno");
        });
    }).catch(() => {
        // Old token is not valid, show login screen
        const loginDiv = document.getElementById("login");
        loginDiv.style.display = "block";
    });
}

async function login() {
    const pwd = document.getElementById("input_password").value;
    try {
        const { data } = await axiosClient.post("/login", {
            password: pwd,
        });
        sessionStorage.setItem(SESSION_STORAGE_TOKEN_KEY, data.token);
        axiosClient.defaults.headers.common.auth = data.token;
        afterLogin().then(() => {
            toastSuccess("Benvenuto");
        }).catch(e => {
            console.error(e);
            toastError("Errore interno");
        });
    } catch (e) {
        console.error(e);
        toastError("Password errata");
    }
}

async function afterLogin() {
    const loginDiv = document.getElementById("login");
    const mainDiv = document.getElementById("main");
    loginDiv.style.display = "none";
    mainDiv.style.display = "block";

    const baseurl = document.location.origin;
    const queuedRequest = await axiosClient.get("/queued-jobs");
    addJobsToTable("queued-jobs", queuedRequest.data.jobs);

    const printedRequest = await axiosClient.get("/printed-jobs");
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

function updateFilename() {
    const label = document.getElementById("p-input-filename");
    const fileInput = document.getElementById("input-print-file").files[0];
    label.innerHTML = fileInput.name;
}

function submit() {
    // TODO: implement me
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
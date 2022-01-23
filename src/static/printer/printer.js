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
    await refresh();
}

async function refresh() {
    const queuedRequest = await axiosClient.get("/queued-jobs");
    document.getElementById("queued-jobs").innerHTML = "";
    addJobsToTable("queued-jobs", queuedRequest.data.jobs, true);

    const printedRequest = await axiosClient.get("/printed-jobs");
    document.getElementById("printed-jobs").innerHTML = "";
    addJobsToTable("printed-jobs", printedRequest.data.jobs, false);
}

/**
 * @param {string} tableId 
 * @param {{ timestamp: number, filename: string, copies: number }[]} jobs 
 * @param {boolean} trashButton whether to include button to delete the job
 * @param {boolean} prepend whether to prepnd to the table instead of append 
 */
function addJobsToTable(tableId, jobs, trashButton = false, prepend = false) {
    const queuedTable = document.getElementById(tableId);
    for (const j of jobs) {
        const row = document.createElement("tr");
        const dateCell = document.createElement("td");
        dateCell.innerHTML = luxon.DateTime
            .fromMillis(parseInt(j.timestamp))
            .toFormat("dd/LL/yyyy HH:mm");
        row.appendChild(dateCell);

        const nameCell = document.createElement("td");
        nameCell.innerHTML = j.filename;
        row.appendChild(nameCell);

        const copiesCell = document.createElement("td");
        copiesCell.innerHTML = j.copies;
        row.appendChild(copiesCell);

        if (trashButton) {
            const trashCell = document.createElement("td");
            trashCell.innerHTML = '<span class="material-icons trash-icon">delete_outline</span>';
            trashCell.addEventListener("click", () => _deleteQueuedJob(j.timestamp));
            row.appendChild(trashCell);
        }

        if (prepend) {
            queuedTable.prepend(row);
        } else {
            queuedTable.appendChild(row);
        }
    }
}

/**
 * Delete a queued job from server
 * @param {number} jobId 
 */
async function _deleteQueuedJob(jobId) {
    try {
        await axiosClient.delete("/queued-jobs/" + jobId);
        await refresh();
        toastSuccess("Lavoro rimosso dalla coda");
    } catch (e) {
        toastError("Errore rimuovendo il lavoro dalla coda");
    }
}

function updateFilename() {
    const label = document.getElementById("p-input-filename");
    const fileInput = document.getElementById("input-print-file").files[0];
    label.innerHTML = fileInput.name;
}

async function submit() {
    const fileInput = document.getElementById("input-print-file").files[0];
    const copies = parseInt(document.getElementById("input-copies").value);

    if (isNaN(copies) || copies < 1 || copies > 100) {
        toastWarn("Copie non valide");
        return;
    }
    if (fileInput == null) {
        toastWarn("File non valido");
        return;
    }

    try {
        const data = new FormData();
        data.append("copies", copies);
        data.append("print_file", fileInput);
        const { data: { job } } = await axiosClient.post("/submit", data);
        addJobsToTable("queued-jobs", [job], true, true);
        toastSuccess("File aggiunto alla coda di stampa");
    } catch (e) {
        toastError("Errore inviando il file");
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
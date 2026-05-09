const API_URL = "http://localhost:8000";

function getToken() {
    return localStorage.getItem("access_token");
}

function setToken(token) {
    localStorage.setItem("access_token", token);
}

function clearToken() {
    localStorage.removeItem("access_token");
}

async function login() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const message = document.getElementById("login-message");

    try {
        const response = await fetch(`${API_URL}/auth/login`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                username,
                password
            })
        });

        if (!response.ok) {
            throw new Error("Usuario o password incorrecto");
        }

        const data = await response.json();

        setToken(data.access_token);

        document.getElementById("login-section").classList.add("hidden");
        document.getElementById("dashboard-section").classList.remove("hidden");

        message.textContent = "";

    } catch (error) {
        message.textContent = error.message;
    }
}

function logout() {
    clearToken();

    document.getElementById("login-section").classList.remove("hidden");
    document.getElementById("dashboard-section").classList.add("hidden");
    document.getElementById("output").textContent = "";
}

async function apiGet(endpoint) {
    const token = getToken();

    const response = await fetch(`${API_URL}${endpoint}`, {
        method: "GET",
        headers: {
            "Authorization": `Bearer ${token}`
        }
    });

    if (!response.ok) {
        throw new Error(`Error consumiendo ${endpoint}`);
    }

    return await response.json();
}

async function loadProducts() {
    const output = document.getElementById("output");

    try {
        const data = await apiGet("/products");
        output.textContent = JSON.stringify(data, null, 2);
    } catch (error) {
        output.textContent = error.message;
    }
}

async function loadStock() {
    const output = document.getElementById("output");

    try {
        const data = await apiGet("/stock");
        output.textContent = JSON.stringify(data, null, 2);
    } catch (error) {
        output.textContent = error.message;
    }
}

async function loadMovements() {
    const output = document.getElementById("output");

    try {
        const data = await apiGet("/movements");
        output.textContent = JSON.stringify(data, null, 2);
    } catch (error) {
        output.textContent = error.message;
    }
}
document.addEventListener("DOMContentLoaded", onDeviceReady, false);

function onDeviceReady() {
    const apiUrl = "http://192.168.1.1:8000/app/login";

    const email=document.getElementById("email");
    const password=document.getElementById("password");

    document.getElementById("loginBTN").addEventListener("click", (e) => {
        e.preventDefault();
        
        fetch(apiUrl, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ 
                email: email.value,
                password: password.value
             })
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                window.location.href = "AuthorizedPage.html";
            } else {
                document.getElementById("result").innerText = data.message || "Błąd logowania!";
            }
        })
        .catch(err => {
            console.error("Błąd:", err);
            document.getElementById("result").innerText = "Błąd połączenia!";
        });
    });
}

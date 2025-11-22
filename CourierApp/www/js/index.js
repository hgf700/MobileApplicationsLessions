document.addEventListener("deviceready", onDeviceReady, false);

function onDeviceReady() {
    const apiUrl = "http://192.168.1.1:8000/action";

    document.getElementById("actionBtn").addEventListener("click", () => {

        fetch(apiUrl, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: "Kliknięto przycisk!" })
        })
        .then(res => res.json())
        .then(data => {
            document.getElementById("result").innerText =
                "Backend odpowiedział: " + JSON.stringify(data);
        })
        .catch(err => {
            console.error("Błąd:", err);
            document.getElementById("result").innerText = "Błąd połączenia!";
        });
    });
}

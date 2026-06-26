const encryptBtn = document.getElementById("encryptBtn");

encryptBtn.onclick = async () => {
    const num1 = document.getElementById("num1").value;
    const num2 = document.getElementById("num2").value;
    const num3 = document.getElementById("num3").value;

    if (!num1 || !num2 || !num3) {
        alert("Please enter all three numbers");
        return;
    }

    encryptBtn.disabled = true;
    encryptBtn.textContent = "Processing...";

    try {
        const res = await fetch("http://127.0.0.1:5000/process", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ numbers: [num1, num2, num3] })
        });

        const data = await res.json();
        console.log("Server Response:", data);

        if (data.error) {
            alert("Error: " + data.error);
        } else {
            // --- Artificial delay ---
            const delay = ms => new Promise(resolve => setTimeout(resolve, ms));
            await delay(12000);  // 12 seconds delay

            document.getElementById("enc1").innerText = data.encrypted_numbers[0].substring(0, 80) + "...";
            document.getElementById("enc2").innerText = data.encrypted_numbers[1].substring(0, 80) + "...";
            document.getElementById("enc3").innerText = data.encrypted_numbers[2].substring(0, 80) + "...";
            document.getElementById("encSum").innerText = data.encrypted_sum.substring(0, 80) + "...";
            document.getElementById("decSum").innerText = data.decrypted_sum.toFixed(6);
        }

    } catch (err) {
        console.error(err);
        alert("Failed to fetch from backend");
    } finally {
        encryptBtn.disabled = false;
        encryptBtn.textContent = "Encrypt & Send";
    }
};

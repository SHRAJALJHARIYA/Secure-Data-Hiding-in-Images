function decryptMessage() {
    let formData = new FormData();
    formData.append("image", document.getElementById("imageUploadDecrypt").files[0]);
    formData.append("key", document.getElementById("decryptionKey").value);

    fetch("/decrypt", { method: "POST", body: formData })
        .then(response => response.json())
        .then(data => {
            if (data.decrypted_message) {
                document.getElementById("decryptedMessage").innerText = "Decrypted Message: " + data.decrypted_message;
            } else {
                alert("Decryption failed! Invalid key.");
            }
        })
        .catch(error => console.error("Error:", error));
}

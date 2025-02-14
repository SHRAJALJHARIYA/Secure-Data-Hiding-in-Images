function encryptMessage() {
    let formData = new FormData();
    formData.append("image", document.getElementById("imageUpload").files[0]);
    formData.append("message", document.getElementById("secretMessage").value);
    formData.append("key", document.getElementById("encryptionKey").value);

    fetch("/encrypt", { method: "POST", body: formData })
        .then(response => response.json())
        .then(data => {
            if (data.encrypted_image) {
                alert("Encryption successful! Download the encrypted image.");
                window.open(data.encrypted_image, "_blank");
            } else {
                alert("Encryption failed.");
            }
        })
        .catch(error => console.error("Error:", error));
}

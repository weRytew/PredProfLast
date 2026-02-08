function Main(){
    const regButton = document.getElementById('buttonForReg')
    regButton.addEventListener('click', goToRegPage)
    document.getElementById('regForm').addEventListener('submit', e => {
        e.preventDefault();

        const data = {
            name: document.getElementById('name').value,
            password: document.getElementById('password').value,
            tel: document.getElementById('email').value,
            agree: document.getElementById('soglashenie').value
        }
        console.log(data)

        sendForm(data);
    });

    async function sendForm(data) {
        const res = await fetch('/registration', {
            method: 'POST',
            headers: {'Content-type': 'application/json'},
            body: JSON.stringify(data)
        });

        const result = await res.json();
        if (result.message == "Success!"){
            window.location.href = result.nextPage
        }
        if (result.message == "error"){
            const errorTeg = document.getElementById('ErrorText')
            errorTeg.textContent = result.error
            errorTeg.style.display = 'block'
        }
    }
    function goToRegPage() {
        window.location.href = "/"
    }
}

window.onload = Main;
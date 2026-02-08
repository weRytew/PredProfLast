function Main(){

    async function sendData(data) {
        return await fetch('/', {
            method: 'POST',
            body: data,
        })
    }

    async function handleFormSubmit(event) {
        event.preventDefault()
        const data = new FormData(event.target)
        const response = await sendData(data)
        const result = await response.json();
        if (result.message == "Success!"){
            window.location.href = result.nextPage
        }
        else {
            const errorTeg = document.getElementById('ErrorText')
            errorTeg.textContent = "неправильный username или пароль"
            errorTeg.style.display = 'block'
        }
    }

    function goToRegPage() {
        window.location.href = "/registration"
    }

    const applicantForm = document.getElementById('regForm')
    const regButton = document.getElementById('buttonForReg')
    applicantForm.addEventListener('submit', handleFormSubmit)
    regButton.addEventListener('click', goToRegPage)
}

window.onload = Main;
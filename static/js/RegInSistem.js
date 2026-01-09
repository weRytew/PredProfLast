function Main(){

    async function sendData(data) {
        return await fetch('/registration', {
            method: 'POST',
            body: data,
        })
    }

    async function handleFormSubmit(event) {
        event.preventDefault()
        const data = new FormData(event.target)
        console.log(Array.from(data.entries()))
        const response = await sendData(data)
        const result = await response.json();
        if (result.message == "Success!"){
            window.location.href = result.nextPage
        }
        else {
            const errorTeg = document.getElementById('ErrorText')
            errorTeg.textContent = "этот username уже занят"
        }

        console.log(result)
    }

    function goToRegPage() {
        window.location.href = "/"
    }

    const applicantForm = document.getElementById('enterForm')
    const regButton = document.getElementById('buttonForEnter')
    applicantForm.addEventListener('submit', handleFormSubmit)
    regButton.addEventListener('click', goToRegPage)
}

window.onload = Main;
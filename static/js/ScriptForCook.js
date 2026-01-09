//function Main(){
//
//    async function sendData(data) {
//        return await fetch('/admin/<name>/<password>', {
//            method: 'POST',
//            body: data,
//        })
//    }
//
//    async function handleFormSubmit(event) {
//        event.preventDefault()
//        const data = new FormData(event.target)
//        const response = await sendData(data)
//        const result = await response.json();
//    }
//
//    const applicantForm = document.getElementById('textForm')
//    const sendButton = document.getElementById('sendApplications')
//    applicantForm.addEventListener('submit', handleFormSubmit)
//}
//
//window.onload = Main;
function Main(){
//    function getManu(){
//        fetch("/manu/value")
//            .then(response => response.json())
//            .then(data => {
//                const manuList = data.manu;
//                return manuList;
//            })
//            .then(manuList => {
//                console.log(manuList)
//                const tableManuZ = document.getElementById('menuTableZ')
//                const tableManuO = document.getElementById('menuTableO')
//                const arrayWithIDday = ["monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
//                const arrayWithTrans = ["понедельник", "вторник", "среда", "четверг", "пятница", "суббота", "воскресенье"]
//                for (let i = 0; i < arrayWithIDday.length; i++){
//                    newtr = document.createElement("tr")
//                    newtr.id = arrayWithIDday[i]
//                    flag = false
//                    for (let j = 0; j < manuList.length; j++){
//                        if (arrayWithTrans[i] == manuList[j][0] && manuList[j][1] == "завтрак"){
//                            flag = true
//                            for (let y = 0; y < manuList[j].length; y++){
//                                if (y != 1){
//                                    newth = document.createElement("th")
//                                    newth.textContent = manuList[j][y]
//                                    newtr.appendChild(newth)
//                                }
//                            }
//                        }
//                        if (flag){
//                            break
//                        }
//                    }
//                    if (flag){
//                        newth = document.createElement("input")
//                        newth.type="checkbox"
//                        newth.id = arrayWithIDday[i] + "Z"
//                        newtr.appendChild(newth)
//                        tableManuZ.appendChild(newtr)
//                    }
//                }
//                for (let i = 0; i < arrayWithIDday.length; i++){
//                    newtr = document.createElement("tr")
//                    newtr.id = arrayWithIDday[i]
//                    flag = false
//                    for (let j = 0; j < manuList.length; j++){
//                        if (arrayWithTrans[i] == manuList[j][0] && manuList[j][1] == "обед"){
//                            flag = true
//                            for (let y = 0; y < manuList[j].length; y++){
//                                if (y != 1){
//                                    newth = document.createElement("th")
//                                    newth.textContent = manuList[j][y]
//                                    newtr.appendChild(newth)
//                                }
//                            }
//                        }
//                        if (flag){
//                            break
//                        }
//                    }
//                    if (flag){
//                        newth = document.createElement("input")
//                        newth.type="checkbox"
//                        newth.id = arrayWithIDday[i] + "O"
//                        newtr.appendChild(newth)
//                        tableManuO.appendChild(newtr)
//                    }
//                }
//            })
//            .catch(error => console.error(error));
//    }

    function rendorTable(manuList){
        console.log(manuList)
        const tableManuZ = document.getElementById('menuTableZ')
        const tableManuO = document.getElementById('menuTableO')
        const arrayWithIDday = ["monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        const arrayWithTrans = ["понедельник", "вторник", "среда", "четверг", "пятница", "суббота", "воскресенье"]
        for (let i = 0; i < arrayWithIDday.length; i++){
            newtr = document.createElement("tr")
            newtr.id = arrayWithIDday[i]
            flag = false
            for (let j = 0; j < manuList.length; j++){
                if (arrayWithTrans[i] == manuList[j][0] && manuList[j][1] == "завтрак"){
                    flag = true
                    for (let y = 0; y < manuList[j].length; y++){
                        if (y != 1 && y != 5){
                            newth = document.createElement("th")
                            newth.textContent = manuList[j][y]
                            newtr.appendChild(newth)
                        }
                    }
                }
                if (flag){
                    break
                }
            }
            if (flag){
                newth = document.createElement("input")
                newth.type = "checkbox"
                newth.name = arrayWithIDday[i] + "Z"
                newth.id = arrayWithIDday[i] + "Z"
                newtr.appendChild(newth)
                tableManuZ.appendChild(newtr)
            }
        }
        for (let i = 0; i < arrayWithIDday.length; i++){
            newtr = document.createElement("tr")
            newtr.id = arrayWithIDday[i]
            flag = false
            for (let j = 0; j < manuList.length; j++){
                if (arrayWithTrans[i] == manuList[j][0] && manuList[j][1] == "обед"){
                    flag = true
                    for (let y = 0; y < manuList[j].length; y++){
                        if (y != 1 && y != 5){
                            newth = document.createElement("th")
                            newth.textContent = manuList[j][y]
                            newtr.appendChild(newth)
                        }
                    }
                }
                if (flag){
                    break
                }
            }
            if (flag){
                newth = document.createElement("input")
                newth.type="checkbox"
                newth.name = arrayWithIDday[i] + "O"
                newth.id = arrayWithIDday[i] + "O"
                newtr.appendChild(newth)
                tableManuO.appendChild(newtr)
            }
        }
    }

//    function makeFormForPay(manuList){
//        const tableManuO = document.getElementById('formaForPayFood')
//        const arrayWithIDday = ["monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
//        const arrayWithTrans = ["понедельник", "вторник", "среда", "четверг", "пятница", "суббота", "воскресенье"]
//        for(let i = 0; i < arrayWithIDday.length; i++){
//            newLable = document.createElement("label")
//            newLable.textContent =
//        }
//    }

    async function getManu(){
        const response = await fetch("/manu/value")
        const data = await response.json()
        const manuList = data.manu
        return manuList
    }

    // Использование:
    async function main() {
            const manuList = await getManu()
            rendorTable(manuList)
    }

//    async function sendData(data) {
//        return await fetch('/', {
//            method: 'POST',
//            body: data,
//        })
//    }
//
//    async function handleFormSubmit(event) {
//        event.preventDefault()
//        const data = new FormData(event.target)
////        console.log(Array.from(data.entries()))
//        const response = await sendData(data)
//        const result = await response.json();
//        if (result.message == "Success!"){
//            window.location.href = result.nextPage
//        }
//        else {
//            const errorTeg = document.getElementById('ErrorText')
//            errorTeg.textContent = "неправильный username или пароль"
//        }
//
////        console.log(result)
//    }
    main()
//    const applicantForm = document.getElementById('formForPay')
//    applicantForm.addEventListener('submit', handleFormSubmit)

//    getManu()
}

window.onload = Main;
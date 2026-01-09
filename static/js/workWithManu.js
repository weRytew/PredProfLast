function Main(){
    function rendorTable(manuList){
        console.log(manuList)
        const tableManuZ = document.getElementById('menuTableZ')
        const tableManuO = document.getElementById('menuTableO')
        const arrayWithIDday = ["monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        const arrayWithTrans = ["понедельник", "вторник", "среда", "четверг", "пятница", "суббота", "воскресенье"]
        const numbersArray = [1, 5, 6]
        for (let i = 0; i < arrayWithIDday.length; i++){
            newtr = document.createElement("tr")
            newtr.id = arrayWithIDday[i]
            flag = false
            for (let j = 0; j < manuList.length; j++){
                if (arrayWithTrans[i] == manuList[j][0] && manuList[j][1] == "завтрак"){
                    flag = true
                    for (let y = 0; y < manuList[j].length; y++){
                        if (!numbersArray.includes(y)){
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
                        if (!numbersArray.includes(y)){
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

    async function getManu(){
        const response = await fetch("/manu/value")
        const data = await response.json()
        const manuList = data.manu
        return manuList
    }

    async function main() {
            const manuList = await getManu()
            rendorTable(manuList)
    }

    main()
}

window.onload = Main;
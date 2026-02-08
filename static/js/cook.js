function Main(){
    document.getElementById('addFood').addEventListener('submit', e => {
        e.preventDefault();

        const data = {}
        const arrayWithIDday = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        const nameZnach = ["ZorOZ", "ZorOO", "ZorOD", "Meal", "Col", "FirstCost", "Cost"]
        for (let i = 0; i < 7; i++){
            const znach = {}
            let put = false
            for (let j = 0; j < 7; j++){
                if (j == 0 || j == 1){
                    if (document.getElementById(arrayWithIDday[i] + nameZnach[j]).checked && put == false){
                        znach["ZorO"] = document.getElementById(arrayWithIDday[i] + nameZnach[j]).value
                        put = true
                    }
                }
                else{
                    if (put == false){
                        put = true
                        znach["ZorO"] = "Nothing"
                    }
                    if (j == 2){
                        znach["ZorOD"] = document.getElementById(arrayWithIDday[i] + nameZnach[j]).checked
                    }
                    else{
                        znach[arrayWithIDday[i] + nameZnach[j]] = document.getElementById(arrayWithIDday[i] + nameZnach[j]).value
                    }
                }
            }
            data[arrayWithIDday[i]] = znach
        }
        sendForm(data);
    });

    async function sendForm(data) {
        const res = await fetch('/addFood1', {
            method: 'POST',
            headers: {'Content-type': 'application/json'},
            body: JSON.stringify(data)
        });
        try {
            const result = await res.json();
            if (result.message == "error") {
                const errorTeg = document.getElementById('ErrorText')
                errorTeg.textContent = result.error
                errorTeg.style.display = 'block'
            }
        } catch (error) {
            location.reload()
        }
    }
}

window.onload = Main;
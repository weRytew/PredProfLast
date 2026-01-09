function Main(){
    const buttonCreate = document.getElementById('create')

    buttonCreate.addEventListener("click", async function (){
        try {
            const response = await fetch('/download-report', {
                method: 'POST'
            });

            if (!response.ok) {
                throw new Error(`Ошибка: ${response.status}`);
            }

            // Получаем файл как Blob
            const blob = await response.blob();

            // Создаём ссылку для скачивания
            const url = window.URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = url;
            link.download = 'report.xlsx';  // Имя файла
            document.body.appendChild(link);
            link.click();  // Автоскачивание

            // Очистка памяти
            document.body.removeChild(link);
            window.URL.revokeObjectURL(url);

        } catch (error) {
            console.error('Ошибка скачивания:', error);
        }
    })
}

window.onload = Main;
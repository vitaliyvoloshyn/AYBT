const url = 'http://localhost:8000';
const btn = document.getElementById("btn_pay");
btn.addEventListener("click", () => {
    try {
      const response = fetch(url, {
        method: 'POST', // или 'PUT'
        body: JSON.stringify(consolidate_data()), // данные могут быть 'строкой' или {объектом}!
        headers: {
          'Content-Type': 'application/json'
        }
      });

    } catch (error) {
      console.error('Ошибка:', error);
    }
})

function consolidate_data() {
    sum = {};
    try {
        for (let i = 1; ;i++) {
            obj = document.getElementById(`sum_${i}`);
            if (Number(obj.value) != 0) {
                sum[`counter_${i}`] = Number(obj.value);
            }
        }
        } catch (error) {
            return sum;
        }
}

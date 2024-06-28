let tariff_type = document.getElementById("tariff_type")
let counter = document.getElementById("counter")
tariff_type.addEventListener("change", () => {
if (tariff_type.value == 1){
    counter.disabled = true
} else if (tariff_type.value == 2){
    counter.disabled = false
} else if (tariff_type.value == 3){
    counter.disabled = true
}
})

let isCounterCheckbox = document.getElementById("categoryIsCounter");
let counterName = document.getElementById("counterName");
let counterIndicator = document.getElementById("counterIndicator");
let counterUnit = document.getElementById("counterUnit")



isCounterCheckbox.addEventListener("change", () => {
if (isCounterCheckbox.checked) {
counterName.disabled = false;
counterIndicator.disabled = false;
counterUnit.disabled = false;
} else {
counterName.disabled = true;
counterIndicator.disabled = true;
counterUnit.disabled = true;
counterIndicator.value = "";
counterName.value = "";
counterUnit.value = "Виберіть зі списку одиницю виміру...";
}});

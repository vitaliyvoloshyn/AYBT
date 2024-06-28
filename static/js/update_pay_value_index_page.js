const totalSum = document.getElementById('total_sum');
let updateInputs = [];
let i = 1;
try {
        for (let i = 1; ;i++) {
          let input = document.getElementById(`sum_${i}`);
        input.addEventListener("change", () => {
            totalSum.value = updateTotalValue();
});

        updateInputs.push(input);
    }}    catch (error) {}


function updateTotalValue() {
    let res = 0;
    updateInputs.forEach(function(item, i, updateInputs) {
    res += Number(item.value);

});
return res;
}
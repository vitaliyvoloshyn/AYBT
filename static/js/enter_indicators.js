let counters = []
counter_{{i}}_prev_ind
counter_{{i}}_cur_ind
counter_{{i}}_using

try {
        for (let i = 1; ;i++) {
            prev = document.getElementById(`counter_${i}_prev_ind`);
            cur = document.getElementById(`counter_${i}_cur_ind`);
            use = document.getElementById(`counter_${i}_using`);

            cur.onchange = function() {
                if (cur.value <= 0){
                    use.value = ""
                    cur.value = ""
                } else if ((counter1_cur_ind.value - counter1_prev_ind.value) < 0){
                    counter1_using.value = ""
                    counter1_cur_ind.value = ""
                } else {
                counter1_using.value = counter1_cur_ind.value - counter1_prev_ind.value
                };
            };

            counters.push(
                {prev: prev, cur: cur, use: use}
            )
        }
        } catch (error) {
        }



let counter1_prev_ind = document.getElementById("counter_1_prev_ind");
let counter1_cur_ind = document.getElementById("counter_1_cur_ind");
let counter1_using = document.getElementById("counter_1_using");

counter1_cur_ind.onchange = function() {
    if (counter1_cur_ind.value <= 0){
        counter1_using.value = ""
        counter1_cur_ind.value = ""
    } else if ((counter1_cur_ind.value - counter1_prev_ind.value) < 0){
        counter1_using.value = ""
        counter1_cur_ind.value = ""
    } else {
    counter1_using.value = counter1_cur_ind.value - counter1_prev_ind.value
	};
};


let counter2_prev_ind = document.getElementById("counter_2_prev_ind");
let counter2_cur_ind = document.getElementById("counter_2_cur_ind");
let counter2_using = document.getElementById("counter_2_using");

counter2_cur_ind.onchange = function() {
    if (counter2_cur_ind.value <= 0){
        counter2_using.value = ""
        counter2_cur_ind.value = ""
    } else if ((counter2_cur_ind.value - counter2_prev_ind.value) < 0){
        counter2_using.value = ""
        counter2_cur_ind.value = ""

    } else {
    counter2_using.value = counter2_cur_ind.value - counter2_prev_ind.value
	};
};


let counter3_prev_ind = document.getElementById("counter_3_prev_ind");
let counter3_cur_ind = document.getElementById("counter_3_cur_ind");
let counter3_using = document.getElementById("counter_3_using");

counter3_cur_ind.onchange = function() {
    if (counter3_cur_ind.value <= 0){
        counter3_using.value = ""
        counter3_cur_ind.value = ""
    } else if ((counter3_cur_ind.value - counter3_prev_ind.value) < 0){
        counter3_using.value = ""
        counter3_cur_ind.value = ""

    } else {
    counter3_using.value = counter3_cur_ind.value - counter3_prev_ind.value
	};
};


let counter4_prev_ind = document.getElementById("counter_4_prev_ind");
let counter4_cur_ind = document.getElementById("counter_4_cur_ind");
let counter4_using = document.getElementById("counter_4_using");

counter4_cur_ind.onchange = function() {
    if (counter4_cur_ind.value <= 0){
        counter4_using.value = ""
        counter4_cur_ind.value = ""
    } else if ((counter4_cur_ind.value - counter4_prev_ind.value) <= 0){
        counter4_using.value = ""
        counter4_cur_ind.value = ""
    } else {
    counter4_using.value = counter4_cur_ind.value - counter4_prev_ind.value
	};
};
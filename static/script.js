function lightDark() {
    const lightButton = document.getElementById("lightButton");
    document.body.classList.toggle("dark-mode");
    lightButton.classList.toggle("light-button");
    lightButton.classList.toggle("dark-button");
  
    if (lightButton.innerHTML == "☼") {
        lightButton.innerHTML = "<i class='fa-regular fa-moon fa-sm'></i>"
    } else {
        lightButton.innerHTML = "☼"
    }
}

function add_entry(name_1, name_2, score_1, score_2) {
	const new_entry = document.createElement("div");
	const name_div = document.createElement("div");
	const score_div = document.createElement("div");
	document.body.appendChild(new_entry);
	new_entry.appendChild(name_div);
	new_entry.appendChild(score_div);
	new_entry.classList.toggle("entry");
	name_div.classList.toggle("names");
	score_div.classList.toggle("score");

    const name1 = document.createElement("span");
    const name2 = document.createElement("span");
    name1.innerText = name_1;
    name2.innerText = name_2;
    name_div.appendChild(name1);
    name_div.appendChild(name2);
    name1.classList.toggle("name-left");
    name2.classList.toggle("name-right");

    const score1 = document.createElement("span");
    const dash = document.createElement("span");
    const score2 = document.createElement("span");
    score1.innerText = score_1;
    dash.innerText = "-";
    score2.innerText = score_2;
    score_div.appendChild(score1);
    score_div.appendChild(dash);
    score_div.appendChild(score2);
    score1.classList.toggle("name-left");
    score2.classList.toggle("name-right");
}

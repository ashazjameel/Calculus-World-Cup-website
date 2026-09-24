function lightDark() {
    const lightButton = document.getElementById("lightButton");
    document.body.classList.toggle("dark-mode");
    lightButton.classList.toggle("light-button");
    lightButton.classList.toggle("dark-button");
  
    if (lightButton.innerHTML == "☼") {
        lightButton.innerHTML = "☾"
    } else {
        lightButton.innerHTML = "☼"
    }
}

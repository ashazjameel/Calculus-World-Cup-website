function lightDark() {
  document.body.classList.toggle("dark-mode");
  document.getElementById("lightButton").classList.toggle("light-button");
  document.getElementById("lightButton").classList.toggle("dark-button");
}

function fetchData() {
  fetch("/api/test")
    .then(response => alert(response));
}

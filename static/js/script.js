const darkModeBtn = document.querySelector("input[type=checkbox]");

if (localStorage.getItem("darkModeOn")) {
  document.body.className = "dark-mode";
  darkModeBtn.checked = true;
}

darkModeBtn.addEventListener("click", () => {
  if (darkModeBtn.checked === true) {
    document.body.className = "dark-mode";
  } else {
    document.body.className = "";
  }

  if (darkModeBtn.checked === true) {
    localStorage.setItem("darkModeOn", "on");
  } else {
    localStorage.removeItem("darkModeOn");
  }
});

const days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
function display_ct5() {
  var x = new Date();

  var x1 =
    x.getDate() +
    "/" +
    x.getMonth() +
    "/" +
    x.getFullYear() +
    " " +
    days[x.getDay()];
  x1 = x1 + " - " + x.getHours() + ":" + x.getMinutes() + ":" + x.getSeconds();
  document.getElementById("ct5").innerHTML = x1;
  display_c5();
}
function display_c5() {
  var refresh = 1000; // Refresh rate in milli seconds
  mytime = setTimeout("display_ct5()", refresh);
}
display_c5();

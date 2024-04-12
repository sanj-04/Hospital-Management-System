
const carouselItems = document.querySelectorAll('.carousel-item');
let currentIndex = 0;

function showNextItem() {
  carouselItems[currentIndex].classList.remove('active');
  currentIndex = (currentIndex + 1) % carouselItems.length;
  carouselItems[currentIndex].classList.add('active');
}

setInterval(showNextItem, 1000); // Change image every 5 seconds

function toggleMenu() {
  var x = document.getElementsByClassName("navbar-right")[0];
  if (x.className === "navbar-right") {
      x.className += " responsive";
  } else {
      x.className = "navbar-right";
  }
}


// Get the registration popup
var registerPopup = document.getElementById("register-popup");
var registerLink = document.querySelector(".navbar-links a.register-link");
var closeButton = document.querySelector(".register-popup .close-button");
registerLink.onclick = function() {
  registerPopup.style.display = "block";
}
closeButton.onclick = function() {
  registerPopup.style.display = "none";
}
window.onclick = function(event) {
  if (event.target == registerPopup) {
    registerPopup.style.display = "none";
  }
}

// Get the login popup
var loginPopup = document.getElementById("login-popup");
var loginLink = document.querySelector(".navbar-links a.login-link");
var closeButton = document.querySelector(".login-popup .close-button");
loginLink.onclick = function() {
  loginPopup.style.display = "block";
}
closeButton.onclick = function() {
  loginPopup.style.display = "none";
}
window.onclick = function(event) {
  if (event.target == loginPopup) {
    loginPopup.style.display = "none";
  }
}

// the forgot password popup
var loginPopup = document.getElementById("login-popup");
var forgotPasswordPopup = document.getElementById("forgot-password-popup");

// Function to show the forgot password popup
function showForgotPasswordPopup() {
  forgotPasswordPopup.style.display = "block";
}

// Function to close the forgot password popup
function closeForgotPasswordPopup() {
  forgotPasswordPopup.style.display = "none";
}
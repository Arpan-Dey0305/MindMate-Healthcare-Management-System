function switchTab(button, role) {
  document.querySelectorAll(".tab-btn").forEach((btn) => {
    btn.classList.remove("active");
  });

  button.classList.add("active");

  console.log(role);
}

function togglePassword() {
  let password = document.getElementById("password");

  if (password.type === "password") {
    password.type = "text";
  } else {
    password.type = "password";
  }
}
function showRegister() {
  const form = document.getElementById("loginForm");
  const nameGroup = document.getElementById("nameGroup");
  const mobileGroup = document.getElementById("mobileGroup");
  const submitBtn = document.getElementById("submitBtn");
  const registerText = document.getElementById("registerText");

  form.action = "/user-signup";
  nameGroup.style.display = "flex";
  mobileGroup.style.display = "flex";
  submitBtn.innerText = "Register";
  registerText.innerText = "Already have an account?";
}
function switchToUserLogin() {
  const form = document.getElementById("loginForm");

  form.action = "/user-login";

  document.getElementById("nameGroup").style.display = "none";
  document.getElementById("mobileGroup").style.display = "none";
  document.getElementById("submitBtn").innerText = "Log In";

  const usernameInput = document.getElementById("username");
  usernameInput.type = "email";
  usernameInput.name = "email";
  usernameInput.placeholder = "Email";

  document.querySelector(".tabs").classList.remove("admin-active");

  document
    .querySelectorAll(".tab-btn")
    .forEach((btn) => btn.classList.remove("active"));
  document.querySelectorAll(".tab-btn")[0].classList.add("active");
}

function switchToAdminLogin() {
  const form = document.getElementById("loginForm");

  form.action = "/admin-login";

  document.getElementById("nameGroup").style.display = "none";
  document.getElementById("mobileGroup").style.display = "none";
  document.getElementById("submitBtn").innerText = "Admin Log In";

  const usernameInput = document.getElementById("username");
  usernameInput.type = "text";
  usernameInput.name = "username";
  usernameInput.placeholder = "Admin Username";

  document.querySelector(".tabs").classList.add("admin-active");

  document
    .querySelectorAll(".tab-btn")
    .forEach((btn) => btn.classList.remove("active"));
  document.querySelectorAll(".tab-btn")[1].classList.add("active");
}

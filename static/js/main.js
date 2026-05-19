"use strict";

function toggleNav() {
  document.querySelector(".nav-links").classList.toggle("show");
}

document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".nav-links a").forEach(function (link) {
    link.addEventListener("click", function () {
      document.querySelector(".nav-links").classList.remove("show");
    });
  });

  var darkToggle = document.getElementById("darkToggle");
  if (darkToggle) {
    var stored = localStorage.getItem("polarpurse-dark");
    if (stored === "true") {
      document.documentElement.classList.add("dark");
      darkToggle.innerHTML = '<i class="fa fa-sun"></i>';
    }

    darkToggle.addEventListener("click", function () {
      var html = document.documentElement;
      html.classList.toggle("dark");
      var isDark = html.classList.contains("dark");
      localStorage.setItem("polarpurse-dark", isDark);
      darkToggle.innerHTML = isDark
        ? '<i class="fa fa-sun"></i>'
        : '<i class="fa fa-moon"></i>';
    });
  }
});

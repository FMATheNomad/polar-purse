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
});

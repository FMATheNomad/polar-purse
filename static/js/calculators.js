"use strict";

function showError(el, msg) {
  el.innerHTML = '<p class="text-red-500 font-semibold">' + msg + "</p>";
}

function showResult(el, html) {
  el.innerHTML = html;
}

async function apiPost(url, data) {
  const resp = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return resp.json();
}

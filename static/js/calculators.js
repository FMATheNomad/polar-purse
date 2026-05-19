"use strict";

function showError(el, msg) {
  el.classList.remove("hidden");
  el.className = "bg-red-50 border border-red-300 rounded p-4 text-center";
  el.innerHTML = '<p class="text-red-600 font-bold">' + escapeHtml(msg) + "</p>";
}

function showResult(el, html, isError) {
  el.classList.remove("hidden");
  if (isError) {
    el.className = "bg-red-50 border border-red-300 rounded p-4 text-center";
  } else {
    el.className = "bg-emerald-50 border border-emerald-300 rounded p-4 text-center";
  }
  el.innerHTML = html;
}

function escapeHtml(str) {
  var div = document.createElement("div");
  div.appendChild(document.createTextNode(str));
  return div.innerHTML;
}

function setLoading(btn, loading) {
  if (loading) {
    btn.disabled = true;
    btn.innerHTML =
      '<i class="fa fa-spinner fa-spin mr-2"></i>Memproses...';
  } else {
    btn.disabled = false;
    btn.innerHTML = "Hitung";
  }
}

async function apiPost(url, data) {
  var controller = new AbortController();
  var timeout = setTimeout(function () {
    controller.abort();
  }, 15000);

  try {
    var resp = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
      signal: controller.signal,
    });
    clearTimeout(timeout);
    var json = await resp.json();
    if (!resp.ok) {
      throw new Error(json.message || "Terjadi kesalahan server");
    }
    return json;
  } catch (err) {
    clearTimeout(timeout);
    if (err.name === "AbortError") {
      throw new Error("Request timeout — server tidak merespon");
    }
    throw new Error(err.message || "Gagal terhubung ke server");
  }
}

document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll("input, select").forEach(function (el) {
    el.addEventListener("keydown", function (e) {
      if (e.key === "Enter") {
        var btn = this.closest(".calculator-card")?.querySelector(".calc-btn");
        if (btn) btn.click();
      }
    });
  });
});

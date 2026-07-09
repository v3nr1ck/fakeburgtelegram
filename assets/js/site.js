(function () {
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.querySelector(".nav-row");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      nav.classList.toggle("show");
    });
  }

  document.querySelectorAll(".nav-item > button").forEach(function (btn) {
    btn.addEventListener("click", function (e) {
      if (window.matchMedia("(max-width: 900px)").matches) {
        e.preventDefault();
        var item = btn.parentElement;
        item.classList.toggle("open");
      }
    });
  });

  var form = document.querySelector(".search-form");
  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var q = (form.querySelector("input") || {}).value || "";
      q = q.trim().toLowerCase();
      if (!q) return;
      window.location.href = "/search/?q=" + encodeURIComponent(q);
    });
  }

  document.querySelectorAll("form[data-static]").forEach(function (f) {
    f.addEventListener("submit", function (e) {
      e.preventDefault();
      var msg = f.querySelector(".form-success");
      if (msg) {
        msg.hidden = false;
      } else {
        alert("Thanks — this demo form does not send email yet. Copy your text and email the newsroom from the Contact page.");
      }
      f.reset();
    });
  });
})();

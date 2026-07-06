/* APS Group — inner-page interactions (tabs). No external libraries. */
(function () {
  "use strict";
  /* Contact page: switch the embedded map when an office is selected. */
  (function () {
    var map = document.querySelector("[data-office-map]");
    if (!map) return;
    var cards = Array.prototype.slice.call(document.querySelectorAll(".office-card"));
    cards.forEach(function (card) {
      card.addEventListener("click", function () {
        var q = card.getAttribute("data-map-q");
        if (!q) return;
        map.src = "https://maps.google.com/maps?q=" + q + "&z=14&hl=ar&output=embed";
        cards.forEach(function (c) {
          var on = c === card;
          c.classList.toggle("is-active", on);
          c.setAttribute("aria-pressed", on ? "true" : "false");
        });
      });
    });
  })();

  document.querySelectorAll("[data-tabs]").forEach(function (tabs) {
    var btns = Array.prototype.slice.call(tabs.querySelectorAll("[data-tab]"));
    var panels = Array.prototype.slice.call(tabs.querySelectorAll("[data-panel]"));
    btns.forEach(function (btn) {
      btn.addEventListener("click", function () {
        var i = btn.getAttribute("data-tab");
        btns.forEach(function (b) {
          var on = b.getAttribute("data-tab") === i;
          b.classList.toggle("is-active", on);
          b.setAttribute("aria-selected", on ? "true" : "false");
        });
        panels.forEach(function (p) {
          p.classList.toggle("is-active", p.getAttribute("data-panel") === i);
        });
      });
    });
  });

  /* FAQ accordion: one open at a time within each category. */
  document.querySelectorAll(".acc-q").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var item = btn.closest(".acc-item");
      var isOpen = item.classList.contains("is-open");
      var group = btn.closest(".accordion");
      if (group) {
        group.querySelectorAll(".acc-item.is-open").forEach(function (o) {
          o.classList.remove("is-open");
          var q = o.querySelector(".acc-q");
          if (q) q.setAttribute("aria-expanded", "false");
        });
      }
      item.classList.toggle("is-open", !isOpen);
      btn.setAttribute("aria-expanded", !isOpen ? "true" : "false");
    });
  });

  /* Industries marquee: manual left/right arrows. First click freezes the
     auto-scroll in place, then each click steps one card. Arrows are bound by
     scroll DIRECTION (left arrow reveals items to the left, right arrow to the
     right), so they read correctly in both Arabic (RTL) and English (LTR). The
     track holds two identical halves, so we wrap by half-width for a seamless loop. */
  (function () {
    var section = document.querySelector(".sectors");
    var marquee = section && section.querySelector(".sectors__marquee[data-marquee]");
    if (!marquee) return;
    var track = marquee.querySelector(".sectors__track");
    var leftBtn = section.querySelector("[data-sectors-left]");
    var rightBtn = section.querySelector("[data-sectors-right]");
    if (!track || (!leftBtn && !rightBtn)) return;
    var manual = false, x = 0, halfW = 0;

    function currentX() {
      var t = getComputedStyle(track).transform;
      var m = t && t.match(/matrix\(([^)]+)\)/);
      return m ? (parseFloat(m[1].split(",")[4]) || 0) : 0;
    }
    function cardW() {
      var card = track.querySelector(".sector-card");
      return card ? card.getBoundingClientRect().width + 2 : 300; // +2px divider
    }
    function engage() {
      if (manual) return;
      x = currentX();
      halfW = track.scrollWidth / 2;
      track.style.animation = "none";
      track.style.transform = "translateX(" + x + "px)";
      void track.offsetWidth; // reflow so the transition starts from the frozen spot
      track.style.transition = "transform .55s cubic-bezier(.4,0,.2,1)";
      manual = true;
    }
    function step(dir) {
      engage();
      x += dir * cardW();
      track.style.transform = "translateX(" + x + "px)";
    }
    track.addEventListener("transitionend", function (e) {
      if (e.propertyName !== "transform") return;
      var nx = x;
      if (nx <= -halfW) nx += halfW;
      else if (nx > 0) nx -= halfW;
      if (nx !== x) {
        x = nx;
        var keep = track.style.transition;
        track.style.transition = "none";
        track.style.transform = "translateX(" + x + "px)";
        void track.offsetWidth;
        track.style.transition = keep;
      }
    });
    // Left arrow → reveal items toward the left (x increases);
    // right arrow → reveal items toward the right (x decreases).
    if (leftBtn) leftBtn.addEventListener("click", function () { step(1); });
    if (rightBtn) rightBtn.addEventListener("click", function () { step(-1); });
  })();
})();

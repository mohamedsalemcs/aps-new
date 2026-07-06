// Visual card editor + live preview for the custom CMS section editors.
// Each editor root: [data-editor="projects|systems|partners|guiding|facts"].
(function () {
  function ready(fn) {
    if (document.readyState !== 'loading') fn();
    else document.addEventListener('DOMContentLoaded', fn);
  }

  function esc(s) {
    return (s || '').replace(/[&<>"]/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c];
    });
  }

  // Preview renderers per kind. `d` = { <field>: value, image: src }.
  var RENDER = {
    projects: {
      show: function (d) { return d.name || d.image; },
      html: function (d) {
        return '<div class="pv-proj">' + (d.image ? '<img src="' + d.image + '">' : '') +
          '<span class="pv-proj__o"></span><div class="pv-proj__b">' +
          (d.sector ? '<span class="pv-proj__sec">' + esc(d.sector) + '</span>' : '') +
          '<div class="pv-proj__name">' + esc(d.name || 'بدون اسم') + '</div></div></div>';
      }
    },
    systems: {
      show: function (d) { return d.name || d.image; },
      html: function (d) {
        return '<div class="pv-sys"><div class="pv-sys__m">' +
          (d.image ? '<img src="' + d.image + '">' : '') + '</div>' +
          '<div class="pv-sys__n">' + esc(d.name || 'بدون اسم') + '</div></div>';
      }
    },
    partners: {
      show: function (d) { return d.image; },
      html: function (d) {
        return '<div class="pv-logo">' + (d.image ? '<img src="' + d.image + '">' : '') + '</div>';
      }
    },
    guiding: {
      show: function (d) { return d.title || d.text || d.iconimg || d.icon; },
      html: function (d) {
        var ic;
        if (d.iconimg) ic = '<img src="' + d.iconimg + '" style="width:24px;height:24px;object-fit:contain">';
        else if (d.icon) ic = '<svg style="width:24px;height:24px;stroke:currentColor;fill:none;stroke-width:1.8"><use href="/static/icons/sprite.svg#i-' + esc(d.icon) + '"></use></svg>';
        else ic = '●';
        return '<div class="pv-guide"><div class="pv-guide__ic">' + ic + '</div>' +
          '<div class="pv-guide__t">' + esc(d.title || 'عنوان') + '</div>' +
          '<div class="pv-guide__x">' + esc(d.text || '') + '</div></div>';
      }
    },
    facts: {
      show: function (d) { return d.value || d.label; },
      html: function (d) {
        return '<div class="pv-fact"><div class="pv-fact__v">' + esc(d.value || '0') + esc(d.suffix || '') +
          '</div><div class="pv-fact__l">' + esc(d.label || '') + '</div></div>';
      }
    },
    lifecycle: {
      show: function (d) { return d.title || d.no; },
      html: function (d) {
        return '<div class="pv-phase"><span class="pv-phase__no num">' + esc(d.no || '') + '</span>' +
          '<div class="pv-phase__t">' + esc(d.title || 'مرحلة') + '</div></div>';
      }
    },
    steps: {
      show: function (d) { return d.title || d.text; },
      html: function (d) {
        return '<div class="pv-step"><div class="pv-step__t">' + esc(d.title || 'خطوة') + '</div>' +
          '<div class="pv-step__x">' + esc(d.text || '') + '</div></div>';
      }
    },
    channels: {
      show: function (d) { return d.label || d.value || d.icon || d.iconimg; },
      html: function (d) {
        var ic;
        if (d.iconimg) ic = '<img src="' + d.iconimg + '" style="width:22px;height:22px;object-fit:contain">';
        else if (d.icon) ic = '<svg style="width:22px;height:22px;stroke:currentColor;fill:none;stroke-width:1.8"><use href="/static/icons/sprite.svg#i-' + esc(d.icon) + '"></use></svg>';
        else ic = '●';
        return '<div class="pv-guide"><div class="pv-guide__ic">' + ic + '</div>' +
          '<div class="pv-guide__t">' + esc(d.label || 'قناة') + '</div>' +
          '<div class="pv-guide__x">' + esc(d.value || '') + '</div></div>';
      }
    },
    office: {
      show: function (d) { return d.name || d.address; },
      html: function (d) {
        return '<div class="pv-office"><div class="pv-office__h">' +
          '<span class="pv-office__n">' + esc(d.name || 'مكتب') + '</span>' +
          (d.tag ? '<span class="pv-office__tag">' + esc(d.tag) + '</span>' : '') + '</div>' +
          '<div class="pv-office__a">' + esc(d.address || '') + '</div>' +
          (d.phone ? '<div class="pv-office__c">' + esc(d.phone) + '</div>' : '') + '</div>';
      }
    },
    heroslide: {
      show: function (d) { return d.title || d.eyebrow || d.image; },
      html: function (d) {
        return '<div class="pv-guide" style="text-align:right">' +
          (d.image ? '<img src="' + d.image + '" style="width:100%;height:96px;object-fit:cover;border-radius:8px;margin-bottom:8px">' : '') +
          (d.eyebrow ? '<div class="pv-guide__x" style="color:var(--b);font-weight:800;margin-bottom:2px">' + esc(d.eyebrow) + '</div>' : '') +
          '<div class="pv-guide__t">' + esc(d.title || 'عنوان الشريحة') + '</div>' +
          '<div class="pv-guide__x">' + esc(d.subtitle || '') + '</div></div>';
      }
    },
    industry: {
      show: function (d) { return d.name || d.image; },
      html: function (d) {
        return '<div class="pv-proj">' + (d.image ? '<img src="' + d.image + '">' : '') +
          '<span class="pv-proj__o"></span><div class="pv-proj__b">' +
          (d.tags ? '<span class="pv-proj__sec">' + esc(d.tags) + '</span>' : '') +
          '<div class="pv-proj__name">' + esc(d.name || 'قطاع') + '</div>' +
          (d.desc ? '<div style="font-size:.72rem;color:#e6edf6;margin-top:4px;line-height:1.5">' + esc(d.desc) + '</div>' : '') +
          '</div></div>';
      }
    },
    badge: {
      show: function (d) { return d.label || d.icon; },
      html: function (d) {
        var ic = d.icon ? '<svg style="width:16px;height:16px;stroke:currentColor;fill:none;stroke-width:1.8"><use href="/static/icons/sprite.svg#i-' + esc(d.icon) + '"></use></svg>' : '';
        return '<span class="pv-badge">' + ic + '<span>' + esc(d.label || 'شارة') + '</span></span>';
      }
    }
  };

  ready(function () { document.querySelectorAll('[data-editor]').forEach(initEditor); });

  function initEditor(root) {
    var kind = root.dataset.editor;
    var renderer = RENDER[kind] || RENDER.projects;
    var wrap = root.querySelector('[data-cards]');
    var prefix = wrap.dataset.prefix;
    var total = document.getElementById('id_' + prefix + '-TOTAL_FORMS');
    var tpl = wrap.querySelector('template[data-empty]');
    var addTile = root.querySelector('[data-add]');
    var pvGrid = root.querySelector('[data-pv-grid]');
    var pvEmpty = root.querySelector('[data-pv-empty]');

    function collect(card) {
      var d = {};
      card.querySelectorAll('[data-f]').forEach(function (w) {
        var el = w.querySelector('input, textarea, select');
        d[w.dataset.f] = el ? (el.value || '').trim() : '';
      });
      var img = card.querySelector('[data-drop] img');
      d.image = img ? img.src : '';
      var ic = card.querySelector('[data-icon] img');
      d.iconimg = ic ? ic.src : '';
      return d;
    }

    function renderPreview() {
      // header preview
      root.querySelectorAll('[data-pv]').forEach(function (src) {
        var out = root.querySelector('[data-pv-out="' + src.dataset.pv + '"]');
        if (out) {
          var input = src.querySelector('input, textarea') || src;
          out.textContent = (input.value || input.textContent || '').trim();
        }
      });
      if (!pvGrid) return;
      pvGrid.innerHTML = '';
      var shown = 0;
      root.querySelectorAll('[data-card]').forEach(function (card) {
        if (card.classList.contains('is-deleted')) return;
        var d = collect(card);
        if (!renderer.show(d)) return;
        shown++;
        var frag = document.createElement('div');
        frag.innerHTML = renderer.html(d);
        pvGrid.appendChild(frag.firstElementChild);
      });
      if (pvEmpty) pvEmpty.style.display = shown ? 'none' : '';
    }

    function showFile(drop, file) {
      if (!drop) return;
      var img = drop.querySelector('img');
      if (!img) { img = document.createElement('img'); drop.appendChild(img); }
      img.src = URL.createObjectURL(file);
      var ph = drop.querySelector('.drop__ph'); if (ph) ph.style.display = 'none';
      var edit = drop.querySelector('.drop__edit'); if (edit) edit.style.display = '';
      renderPreview();
    }

    function wireCard(card) {
      // Wire every image drop-zone in the card (a hero slide has up to three).
      card.querySelectorAll('[data-drop]').forEach(function (drop) {
        var fileInput = drop.querySelector('input[type=file]');
        if (!fileInput) return;
        ['dragenter', 'dragover'].forEach(function (e) {
          drop.addEventListener(e, function (ev) { ev.preventDefault(); drop.classList.add('is-over'); });
        });
        ['dragleave', 'drop'].forEach(function (e) {
          drop.addEventListener(e, function (ev) { ev.preventDefault(); drop.classList.remove('is-over'); });
        });
        drop.addEventListener('drop', function (ev) {
          if (ev.dataTransfer && ev.dataTransfer.files.length) {
            fileInput.files = ev.dataTransfer.files;
            showFile(drop, fileInput.files[0]);
          }
        });
        fileInput.addEventListener('change', function () {
          if (fileInput.files.length) showFile(drop, fileInput.files[0]);
        });
      });
      var del = card.querySelector('[data-del]');
      var delBox = card.querySelector('input[type=checkbox][name$="-DELETE"]');
      if (del) {
        del.addEventListener('click', function () {
          if (delBox) delBox.checked = true;
          card.classList.add('is-deleted');
          renderPreview();
        });
      }
      // reorder up/down (swaps DOM position; order is renumbered on submit)
      card.querySelectorAll('[data-move]').forEach(function (mb) {
        mb.addEventListener('click', function () {
          var up = mb.dataset.move === 'up';
          var sib = card;
          do { sib = up ? sib.previousElementSibling : sib.nextElementSibling; }
          while (sib && (!sib.matches('[data-card]') || sib.classList.contains('is-deleted')));
          if (!sib) return;
          if (up) card.parentNode.insertBefore(card, sib);
          else card.parentNode.insertBefore(sib, card);
          renderPreview();
        });
      });
      card.querySelectorAll('input, textarea, select').forEach(function (inp) {
        inp.addEventListener('input', renderPreview);
        inp.addEventListener('change', renderPreview);
      });
    }

    if (addTile && tpl && total) {
      addTile.addEventListener('click', function () {
        var i = parseInt(total.value, 10);
        var html = tpl.innerHTML.replace(/__prefix__/g, i);
        var frag = document.createElement('div');
        frag.innerHTML = html.trim();
        var card = frag.firstElementChild;
        wrap.querySelector('[data-cardlist]').appendChild(card);
        total.value = i + 1;
        wireCard(card);
        var first = card.querySelector('[data-f] input, [data-f] textarea');
        if (first) first.focus();
        renderPreview();
      });
    }

    var form = root.closest('form');
    if (form) {
      form.addEventListener('submit', function () {
        var n = 0;
        root.querySelectorAll('[data-card]').forEach(function (card) {
          if (card.classList.contains('is-deleted')) return;
          var ord = card.querySelector('input[name$="-order"]');
          if (ord) ord.value = n++;
        });
      });
    }

    root.querySelectorAll('[data-card]').forEach(wireCard);
    renderPreview();
  }
})();

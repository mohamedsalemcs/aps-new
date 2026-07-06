// Custom CMS admin — dynamic inline formsets (add / mark-for-delete).
document.addEventListener('DOMContentLoaded', function () {

  // ---- nice confirmation modal (replaces native confirm) ----
  var modal = null;
  function apsConfirm(msg, onOk) {
    if (!modal) {
      modal = document.createElement('div');
      modal.className = 'm-modal';
      modal.innerHTML = '<div class="m-modal__box"><div class="m-modal__ic m-modal__ic--warn">' +
        '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg></div>' +
        '<div class="m-modal__t">تأكيد الإجراء</div><div class="m-modal__m" data-msg></div>' +
        '<div class="m-modal__act"><button type="button" class="btnm btnm--ghost" data-cancel>إلغاء</button>' +
        '<button type="button" class="btnm btnm--danger" data-ok>تأكيد</button></div></div>';
      document.body.appendChild(modal);
      modal.addEventListener('click', function (e) { if (e.target === modal || e.target.hasAttribute('data-cancel')) close(); });
    }
    modal.querySelector('[data-msg]').textContent = msg;
    var okBtn = modal.querySelector('[data-ok]');
    var fresh = okBtn.cloneNode(true); okBtn.replaceWith(fresh);
    fresh.addEventListener('click', function () { close(); onOk(); });
    modal.classList.add('open');
    function close() { modal.classList.remove('open'); }
  }
  window.apsConfirm = apsConfirm;
  document.querySelectorAll('[data-confirm]').forEach(function (el) {
    el.addEventListener('click', function (ev) {
      ev.preventDefault(); ev.stopPropagation();
      apsConfirm(el.getAttribute('data-confirm'), function () {
        if (el.tagName === 'A') { window.location.href = el.getAttribute('href'); return; }
        var form = el.closest('form');
        if (form) {
          if (el.name) { var hid = document.createElement('input'); hid.type = 'hidden'; hid.name = el.name; hid.value = el.value || ''; form.appendChild(hid); }
          form.submit();
        }
      });
    });
  });

  document.querySelectorAll('[data-formset]').forEach(function (fs) {
    var prefix = fs.dataset.prefix;
    var total = fs.querySelector('#id_' + prefix + '-TOTAL_FORMS');
    var rows = fs.querySelector('.fs__rows');
    var tpl = fs.querySelector('.fs__empty');
    var addBtn = fs.querySelector('[data-add-row]');

    if (addBtn && total && tpl && rows) {
      addBtn.addEventListener('click', function () {
        var i = parseInt(total.value, 10);
        var html = tpl.innerHTML.replace(/__prefix__/g, i);
        var wrap = document.createElement('div');
        wrap.innerHTML = html.trim();
        var node = wrap.firstElementChild;
        node.querySelector('.fs__no').textContent = i + 1;
        rows.appendChild(node);
        total.value = i + 1;
      });
    }

    // Visually flag rows marked for deletion.
    fs.addEventListener('change', function (e) {
      if (e.target.name && e.target.name.endsWith('-DELETE')) {
        var row = e.target.closest('.fs__row');
        if (row) row.classList.toggle('to-delete', e.target.checked);
      }
    });
  });

  // Make every card collapsible (title chevron toggles the body).
  var ICON = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><path d="M6 9l6 6 6-6"/></svg>';
  document.querySelectorAll('.m-card').forEach(function (card) {
    if (card.dataset.noCollapse !== undefined) return;
    var title = card.querySelector(':scope > .m-card__title');
    if (!title) return;
    var hint = card.querySelector(':scope > .m-card__hint');
    var anchor = hint || title;
    var body = document.createElement('div');
    body.className = 'm-card__body';
    var n = anchor.nextSibling;
    while (n) { var next = n.nextSibling; body.appendChild(n); n = next; }
    card.appendChild(body);
    var btn = document.createElement('button');
    btn.type = 'button'; btn.className = 'm-card__toggle'; btn.setAttribute('aria-label', 'طيّ/فتح');
    btn.innerHTML = ICON;
    btn.addEventListener('click', function () { card.classList.toggle('is-collapsed'); });
    card.appendChild(btn);
  });

  // Content tabs (e.g. page-content | SEO).
  document.querySelectorAll('[data-tabs]').forEach(function (nav) {
    var root = nav.closest('[data-tabroot]') || document;
    nav.querySelectorAll('[data-tab]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var key = btn.dataset.tab;
        nav.querySelectorAll('[data-tab]').forEach(function (b) { b.classList.toggle('is-active', b === btn); });
        root.querySelectorAll('[data-tabpanel]').forEach(function (p) { p.classList.toggle('is-active', p.dataset.tabpanel === key); });
      });
    });
  });

  // Clean image dropboxes (drag-drop + instant preview of the current image).
  document.querySelectorAll('[data-dropbox]').forEach(function (box) {
    var inp = box.querySelector('input[type=file]');
    var ctl = box.closest('.imgctl, .iconctl');
    if (!inp || !ctl) return;
    var icon = ctl.classList.contains('iconctl');
    function show() {
      if (!inp.files || !inp.files[0]) return;
      var url = URL.createObjectURL(inp.files[0]);
      var cur = ctl.querySelector(icon ? '.iconctl__cur' : '.imgctl__cur');
      if (icon) { cur.innerHTML = '<img src="' + url + '" alt="">'; }
      else { var img = document.createElement('img'); img.className = 'imgctl__cur'; img.src = url; cur.replaceWith(img); }
      // Optionally mirror into a live-preview image (data-dropbox-pv="<element id>").
      var pvId = box.getAttribute('data-dropbox-pv');
      if (pvId) { var pel = document.getElementById(pvId); if (pel) pel.src = url; }
    }
    ['dragenter', 'dragover'].forEach(function (e) { box.addEventListener(e, function (ev) { ev.preventDefault(); box.classList.add('is-over'); }); });
    ['dragleave', 'drop'].forEach(function (e) { box.addEventListener(e, function (ev) { ev.preventDefault(); box.classList.remove('is-over'); }); });
    box.addEventListener('drop', function (ev) { if (ev.dataTransfer && ev.dataTransfer.files.length) { inp.files = ev.dataTransfer.files; show(); } });
    inp.addEventListener('change', show);
  });

  // Split section editors into two columns: form (5) | sticky preview (7).
  document.querySelectorAll('form[data-editor], form[data-split]').forEach(function (form) {
    var pv = form.querySelector(':scope > .pv');
    if (!pv) return;
    var ed = document.createElement('div'); ed.className = 'ed';
    var col1 = document.createElement('div'); col1.className = 'ed__form';
    var col2 = document.createElement('div'); col2.className = 'ed__preview';
    form.querySelectorAll(':scope > .m-card').forEach(function (card) { col1.appendChild(card); });
    col2.appendChild(pv);
    ed.appendChild(col1); ed.appendChild(col2);
    var actions = form.querySelector(':scope > .m-actions');
    if (actions) form.insertBefore(ed, actions); else form.appendChild(ed);
  });

  // Unsaved-changes indicator in the fixed savebar (dot + text; dirty on first edit).
  (function () {
    var bar = document.querySelector('.m-savebar');
    if (!bar) return;
    var form = bar.closest('form') || document.querySelector('form[method="post"], form[method="POST"]');
    if (!form) return;
    var status = document.createElement('span');
    status.className = 'm-savebar__status';
    status.setAttribute('aria-live', 'polite');
    status.innerHTML = '<span class="m-savebar__dot"></span><span class="m-savebar__stxt"></span>';
    bar.insertBefore(status, bar.querySelector('.btnm') || null);
    var txt = status.querySelector('.m-savebar__stxt');
    var dirty = false;
    function render() {
      bar.classList.toggle('is-dirty', dirty);
      txt.textContent = dirty ? 'تغييرات غير محفوظة' : 'كل التغييرات محفوظة';
    }
    function mark() { if (!dirty) { dirty = true; render(); } }
    render();
    form.addEventListener('input', mark);
    form.addEventListener('change', mark);
    // Adding / deleting / reordering formset cards is also an unsaved change.
    form.addEventListener('click', function (e) {
      if (e.target.closest('[data-add],[data-del],[data-up],[data-down],[data-move],.card-add')) mark();
    });
  })();
});

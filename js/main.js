'use strict';
(() => {
  const hamburger = document.querySelector('.hamburger');
  const menu = document.querySelector('.mobile-menu');
  function setMenu(open) {
    if (!hamburger || !menu) return;
    menu.classList.toggle('open', open);
    hamburger.setAttribute('aria-expanded', String(open));
    hamburger.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
  }
  if (hamburger && menu) {
    menu.id = 'mobile-navigation';
    hamburger.setAttribute('aria-controls', menu.id);
    hamburger.addEventListener('click', () => setMenu(!menu.classList.contains('open')));
    menu.querySelectorAll('a').forEach(a => a.addEventListener('click', () => setMenu(false)));
    document.addEventListener('keydown', e => {
      if (e.key === 'Escape' && menu.classList.contains('open')) { setMenu(false); hamburger.focus(); }
    });
    document.addEventListener('click', e => {
      if (!menu.contains(e.target) && !hamburger.contains(e.target)) setMenu(false);
    });
  }
  document.querySelectorAll('.m-toggle').forEach(button => {
    const sub = document.getElementById(button.dataset.target);
    if (!sub) return;
    button.setAttribute('aria-controls', sub.id);
    button.setAttribute('aria-expanded', 'false');
    button.addEventListener('click', () => {
      const open = sub.classList.toggle('open');
      button.setAttribute('aria-expanded', String(open));
    });
  });
  // Never save personal form data to localStorage or claim email delivery.
  document.querySelectorAll('[data-email-form]').forEach(form => {
    const status = form.querySelector('.form-status');
    if (status) { status.setAttribute('role', 'status'); status.setAttribute('aria-live', 'polite'); }
    form.querySelectorAll('input[type="text"], textarea').forEach(field => field.maxLength = 2000);
    form.addEventListener('submit', e => {
      e.preventDefault();
      if (!form.reportValidity()) return;
      const kind = form.dataset.enquiry || 'contact';
      const subject = 'IYONEX ' + kind + ' enquiry';
      const lines = [];
      new FormData(form).forEach((value, name) => {
        const field = form.elements.namedItem(name);
        const label = field && field.labels && field.labels[0] ? field.labels[0].textContent : name;
        lines.push(label.trim() + ': ' + String(value).trim());
      });
      if (kind === 'internship') lines.push('\nPlease attach your PDF resume before sending.');
      const body = lines.join('\n');
      const mailto = 'mailto:ceo@iyonex.com?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
      let preview = form.querySelector('.email-preview');
      if (!preview) {
        preview = document.createElement('div');
        preview.className = 'email-preview';
        const title = document.createElement('h3'); title.textContent = 'Review your email';
        const info = document.createElement('p'); info.textContent = 'To: ceo@iyonex.com. Open your email app and send the draft. If it does not open, copy the text below into a new email.';
        const text = document.createElement('textarea'); text.readOnly = true; text.setAttribute('aria-label', 'Prepared enquiry email');
        const actions = document.createElement('div'); actions.className = 'btn-row';
        const link = document.createElement('a'); link.className = 'btn btn-primary'; link.textContent = 'Open Email App';
        const copy = document.createElement('button'); copy.type = 'button'; copy.className = 'btn'; copy.textContent = 'Copy Email Text';
        copy.addEventListener('click', async () => {
          try {
            await navigator.clipboard.writeText('To: ceo@iyonex.com\nSubject: ' + subject + '\n\n' + text.value);
            if (status) status.textContent = 'Copied. Paste into your email app and send to ceo@iyonex.com.';
          } catch {
            text.focus(); text.select();
            if (status) status.textContent = 'Email text selected. Copy it and paste into your email app.';
          }
        });
        actions.append(link, copy); preview.append(title, info, text, actions); form.append(preview);
      }
      preview.querySelector('textarea').value = body;
      preview.querySelector('a').href = mailto;
      if (status) { status.style.display = 'block'; status.textContent = 'Draft prepared. Nothing has been sent yet. Review it below and send from your email app.'; }
      preview.scrollIntoView({block:'nearest', behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'});
    });
  });
})();

// ── Navbar scroll effect ────────────────────────────────────────────────────
const navbar = document.getElementById('navbar');
window.addEventListener('scroll', () => {
  navbar.classList.toggle('scrolled', window.scrollY > 60);
}, { passive: true });

// ── Mobile nav toggle ──────────────────────────────────────────────────────
const navToggle = document.getElementById('navToggle');
const navLinks  = document.getElementById('navLinks');

if (navToggle && navLinks) {
  navToggle.addEventListener('click', () => {
    const open = navLinks.classList.toggle('open');
    navToggle.setAttribute('aria-expanded', open);
  });

  document.addEventListener('click', (e) => {
    if (!navbar.contains(e.target)) {
      navLinks.classList.remove('open');
      navToggle.setAttribute('aria-expanded', false);
    }
  });
}

// ── Countdown timer ─────────────────────────────────────────────────────────
const weddingDateStr = window.WEDDING_DATE;
if (weddingDateStr) {
  const weddingDate = new Date(weddingDateStr);

  function pad(n) { return String(n).padStart(2, '0'); }

  function updateCountdown() {
    const diff = weddingDate - new Date();
    if (diff <= 0) return;

    const days  = Math.floor(diff / 864e5);
    const hours = Math.floor((diff % 864e5) / 36e5);
    const mins  = Math.floor((diff % 36e5)  / 6e4);
    const secs  = Math.floor((diff % 6e4)   / 1e3);

    const set = (id, val) => { const el = document.getElementById(id); if (el) el.textContent = val; };
    set('cd-days',  pad(days));
    set('cd-hours', pad(hours));
    set('cd-mins',  pad(mins));
    set('cd-secs',  pad(secs));
  }

  updateCountdown();
  setInterval(updateCountdown, 1000);
}

// ── RSVP: show/hide attending fields ────────────────────────────────────────
const attendingRadios  = document.querySelectorAll('input[name="attending"]');
const attendingFields  = document.getElementById('attendingFields');
const dietaryField     = document.getElementById('dietaryField');
const songField        = document.getElementById('songField');

function syncAttendingFields() {
  const checked = document.querySelector('input[name="attending"]:checked');
  const attending = checked && checked.value === 'yes';
  if (attendingFields) attendingFields.style.display = attending ? 'flex' : 'none';
  if (dietaryField)    dietaryField.style.display    = attending ? 'flex' : 'none';
  if (songField)       songField.style.display       = attending ? 'flex' : 'none';
}

attendingRadios.forEach(r => r.addEventListener('change', syncAttendingFields));

// ── Password show/hide toggle ────────────────────────────────────────────────
document.querySelectorAll('.password-toggle').forEach(btn => {
  btn.addEventListener('click', () => {
    const input = document.getElementById(btn.dataset.target);
    const isPassword = input.type === 'password';
    input.type = isPassword ? 'text' : 'password';
    btn.querySelector('.eye-open').style.display  = isPassword ? 'none'  : '';
    btn.querySelector('.eye-closed').style.display = isPassword ? ''     : 'none';
  });
});

// ── Timeline: reveal on scroll ───────────────────────────────────────────────
const timelineEvents = document.querySelectorAll('.timeline-event');
if (timelineEvents.length) {
  const observer = new IntersectionObserver(
    (entries) => entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('visible'); observer.unobserve(e.target); } }),
    { threshold: 0.18 }
  );
  timelineEvents.forEach(el => observer.observe(el));
}

// ── Message wall: AJAX submit ─────────────────────────────────────────────────
const messageForm = document.getElementById('messageForm');
if (messageForm) {
  messageForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const input = document.getElementById('messageInput');
    const text = input.value.trim();
    if (!text) return;

    const btn = messageForm.querySelector('button[type="submit"]');
    btn.disabled = true;

    try {
      const res = await fetch('/mensajes/add', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text }),
      });

      if (res.ok) {
        const data = await res.json();
        const grid = document.getElementById('messagesGrid');
        const empty = grid.querySelector('.messages-empty');
        if (empty) empty.remove();

        const card = document.createElement('div');
        card.className = 'message-card message-card-new';
        card.innerHTML =
          `<p class="message-text">${esc(data.message)}</p>` +
          `<span class="message-author">— ${esc(data.guest_name)}</span>`;
        grid.prepend(card);
        input.value = '';

        requestAnimationFrame(() => requestAnimationFrame(() => card.classList.add('visible')));
      }
    } finally {
      btn.disabled = false;
    }
  });
}

function esc(s) {
  return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

// ── Flash message auto-dismiss ───────────────────────────────────────────────
setTimeout(() => {
  document.querySelectorAll('.flash').forEach(el => {
    el.style.transition = 'opacity 0.6s ease';
    el.style.opacity = '0';
    setTimeout(() => el.remove(), 650);
  });
}, 3500);

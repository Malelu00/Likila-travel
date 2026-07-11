const API_BASE = '/api'; 


const navToggle = document.getElementById('nav-toggle');
const navLinksEl = document.querySelector('.nav-links');

navToggle.addEventListener('click', () => {
  navToggle.classList.toggle('open');
  navLinksEl.classList.toggle('open');
});

// Close menu when a link is clicked
navLinksEl.querySelectorAll('a').forEach(a => {
  a.addEventListener('click', () => {
    navToggle.classList.remove('open');
    navLinksEl.classList.remove('open');
  });
});


/* ══════════════════════════════════════════
   HERO SLIDESHOW DATA
   ══════════════════════════════════════════ */
const SLIDES = [
  {
    img: 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=1600&q=80',
    overlay: 'linear-gradient(to right, rgba(6,85,122,0.88) 0%, rgba(6,85,122,0.3) 55%, transparent 100%)',
    eyebrow: "Lesotho's Premier Tour Operator",
    title: 'Discover the <em>Kingdom<br>in the Sky</em>',
    desc: 'Breathtaking mountain landscapes, rich Basotho culture, and unforgettable adventures — your gateway to authentic Lesotho experiences.',
    btn1: { label: 'Explore Tours', href: '#events' },
    btn2: { label: 'Our Story →', href: '#about' }
  },
  {
    img: 'https://images.unsplash.com/photo-1547471080-7cc2caa01a7e?w=1600&q=80',
    overlay: 'linear-gradient(to right, rgba(6,40,30,0.88) 0%, rgba(6,40,30,0.3) 55%, transparent 100%)',
    eyebrow: 'Scenic Wonders Await',
    title: 'Majestic <em>Dams &<br>Highland Lakes</em>',
    desc: 'Mohale, Katse, and beyond — explore Lesotho\'s dramatic highland water landscapes with our expert local guides.',
    btn1: { label: 'Book a Tour', href: '#contact' },
    btn2: { label: 'View Gallery →', href: '#gallery' }
  },
  {
    img: 'https://images.unsplash.com/photo-1516026672322-bc52d61a55d5?w=1600&q=80',
    overlay: 'linear-gradient(to right, rgba(46,60,20,0.88) 0%, rgba(46,60,20,0.3) 55%, transparent 100%)',
    eyebrow: 'Culture & Community',
    title: 'Authentic <em>Basotho<br>Village Life</em>',
    desc: 'Step into centuries-old traditions — village stays, pony trekking, and cultural immersions that connect you to the real Lesotho.',
    btn1: { label: 'Cultural Tours', href: '#services' },
    btn2: { label: 'Contact Us →', href: '#contact' }
  },
  {
    img: 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1600&q=80',
    overlay: 'linear-gradient(to right, rgba(20,20,60,0.88) 0%, rgba(20,20,60,0.3) 55%, transparent 100%)',
    eyebrow: 'Adventure at Altitude',
    title: '<em>Sani Pass</em> &<br>Mountain Peaks',
    desc: 'Conquer the highest passes in southern Africa. Scenic drives, hiking trails, and snow-capped summits await the bold.',
    btn1: { label: 'Plan My Adventure', href: '#contact' },
    btn2: { label: 'See Events →', href: '#events' }
  }
];

/* ══════════════════════════════════════════
   HERO SLIDESHOW ENGINE
   ══════════════════════════════════════════ */
let currentSlide = 0;
let slideTimer = null;
let progressTimer = null;
const SLIDE_DURATION = 11000;

function buildHero() {
  const slidesEl = document.getElementById('hero-slides');
  const contentEl = document.getElementById('hero-content');
  const dotsEl = document.getElementById('hero-dots');

  SLIDES.forEach((s, i) => {
    // Background slide
    const bg = document.createElement('div');
    bg.className = 'hero-slide' + (i === 0 ? ' active' : '');
    bg.style.backgroundImage = `url('${s.img}')`;
    slidesEl.appendChild(bg);

    // Content panel
    const panel = document.createElement('div');
    panel.className = 'slide-panel' + (i === 0 ? ' active' : '');
    panel.innerHTML = `
      <div class="hero-eyebrow">${s.eyebrow}</div>
      <h1>${s.title}</h1>
      <p>${s.desc}</p>
      <div class="hero-actions">
        <a href="${s.btn1.href}" class="btn-primary">${s.btn1.label}</a>
        <a href="${s.btn2.href}" class="btn-ghost">${s.btn2.label}</a>
      </div>`;
    contentEl.appendChild(panel);

    // Dot
    const dot = document.createElement('button');
    dot.className = 'slide-dot' + (i === 0 ? ' active' : '');
    dot.setAttribute('aria-label', `Slide ${i+1}`);
    dot.addEventListener('click', () => goToSlide(i));
    dotsEl.appendChild(dot);
  });
}

function goToSlide(n) {
  const slides = document.querySelectorAll('.hero-slide');
  const panels = document.querySelectorAll('.slide-panel');
  const dots   = document.querySelectorAll('.slide-dot');
  const overlay = document.getElementById('hero-overlay');

  slides[currentSlide].classList.remove('active');
  panels[currentSlide].classList.remove('active');
  dots[currentSlide].classList.remove('active');

  currentSlide = (n + SLIDES.length) % SLIDES.length;

  slides[currentSlide].classList.add('active');
  panels[currentSlide].classList.add('active');
  dots[currentSlide].classList.add('active');
  overlay.style.background = SLIDES[currentSlide].overlay;

  resetProgress();
}

function nextSlide() { goToSlide(currentSlide + 1); }
function prevSlide() { goToSlide(currentSlide - 1); }

function resetProgress() {
  clearInterval(slideTimer);
  clearInterval(progressTimer);

  const bar = document.getElementById('slide-progress');
  bar.style.transition = 'none';
  bar.style.width = '0%';

  requestAnimationFrame(() => requestAnimationFrame(() => {
    bar.style.transition = `width ${SLIDE_DURATION}ms linear`;
    bar.style.width = '100%';
  }));

  slideTimer = setTimeout(nextSlide, SLIDE_DURATION);
}

function initHero() {
  buildHero();
  document.getElementById('slide-prev').addEventListener('click', () => { prevSlide(); });
  document.getElementById('slide-next').addEventListener('click', () => { nextSlide(); });
  resetProgress();
}

/* ══════════════════════════════════════════
   ICON MAP for services
   ══════════════════════════════════════════ */
const ICONS = {
  mountain: `<svg viewBox="0 0 24 24"><path d="M3 17l9-9 4 4 5-6"/><path d="M21 17H3"/></svg>`,
  culture:  `<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M4.22 4.22l2.12 2.12M17.66 17.66l2.12 2.12M2 12h3M19 12h3M4.22 19.78l2.12-2.12M17.66 6.34l2.12-2.12"/></svg>`,
  horse:    `<svg viewBox="0 0 24 24"><path d="M4 15s1-1 4-1 5 2 8 2 4-1 4-1V3s-1 1-4 1-5-2-8-2-4 1-4 1z"/><line x1="4" y1="22" x2="4" y2="15"/></svg>`,
  transport:`<svg viewBox="0 0 24 24"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>`,
  event:    `<svg viewBox="0 0 24 24"><rect x="2" y="7" width="20" height="14" rx="2" ry="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/></svg>`,
  custom:   `<svg viewBox="0 0 24 24"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07A19.5 19.5 0 0 1 4.57 12a19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 3.48 1h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L7.91 8.96a16 16 0 0 0 6.29 6.29l1.31-1.31a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>`
};

/* ══════════════════════════════════════════
   SKELETON LOADERS
   ══════════════════════════════════════════ */
function renderServiceSkeletons(n = 6) {
  document.getElementById('services-grid').innerHTML = Array.from({length: n}, () => `
    <div class="skel-card">
      <div class="skeleton skel-icon"></div>
      <div class="skeleton skel-line short" style="margin-bottom:10px"></div>
      <div class="skeleton skel-line long"></div>
      <div class="skeleton skel-line long"></div>
      <div class="skeleton skel-line" style="width:75%"></div>
    </div>`).join('');
}

function renderEventSkeletons(n = 3) {
  document.getElementById('events-grid').innerHTML = Array.from({length: n}, () => `
    <div class="skel-card" style="border-radius:20px;overflow:hidden;padding:0">
      <div class="skeleton" style="height:190px;border-radius:0"></div>
      <div style="padding:1.4rem">
        <div class="skeleton skel-line short" style="height:28px;margin-bottom:12px"></div>
        <div class="skeleton skel-line long"></div>
        <div class="skeleton skel-line" style="width:80%"></div>
        <div class="skeleton skel-line short" style="margin-top:20px;height:40px;border-radius:10px"></div>
      </div>
    </div>`).join('');
}

function renderGallerySkeletons() {
  document.getElementById('gallery-container').innerHTML = `
    <div class="gallery-grid-skeleton">
      ${Array.from({length: 5}, () => `<div class="skeleton" style="min-height:240px"></div>`).join('')}
    </div>`;
}

/* ══════════════════════════════════════════
   API FETCH HELPERS
   ══════════════════════════════════════════ */
async function apiFetch(path) {
  const res = await fetch(`${API_BASE}${path}`);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

/* ══════════════════════════════════════════
   RENDER SERVICES
   ══════════════════════════════════════════ */
function renderServices(services) {
  const grid = document.getElementById('services-grid');
  if (!services.length) {
    grid.innerHTML = `<p style="color:var(--text-muted);grid-column:1/-1;text-align:center">No services available right now.</p>`;
    return;
  }
  grid.innerHTML = services.map((s, i) => `
    <div class="service-card fade-up" style="transition-delay:${(i % 3) * 0.1}s">
      <div class="service-icon">${ICONS[s.icon] || ICONS.custom}</div>
      <h3>${s.name}</h3>
      <p>${s.description}</p>
      ${s.price ? `<p style="margin-top:0.75rem;font-size:0.82rem;font-weight:600;color:var(--sky-dark)">From M${s.price}</p>` : ''}
    </div>`).join('');
  grid.querySelectorAll('.fade-up').forEach(el => fadeObserver.observe(el));
}

/* Fallback services shown if API is offline */
const FALLBACK_SERVICES = [
  { name: 'Mountain Tours', description: 'Guided excursions through Lesotho\'s dramatic highland terrain, including Maletsunyane Falls and Sani Pass.', icon: 'mountain' },
  { name: 'Cultural Village Tours', description: 'Immersive stays in traditional Basotho villages — experience authentic food, music, and customs.', icon: 'culture' },
  { name: 'Pony Trekking', description: 'Traverse scenic highland routes on the legendary Basotho pony — the traditional way to explore.', icon: 'horse' },
  { name: 'Transport & Transfers', description: 'Comfortable, reliable transfers across Lesotho and to neighbouring South Africa with WiFi.', icon: 'transport' },
  { name: 'Event Packages', description: 'Festival passes, group bookings, and custom event packages — all inclusive.', icon: 'event' },
  { name: 'Custom Itineraries', description: 'Bespoke travel plans designed around your schedule, interests, and group size.', icon: 'custom' }
];

async function loadServices() {
  renderServiceSkeletons();
  try {
    const data = await apiFetch('/services/');
    const services = data.results || (Array.isArray(data) ? data : []);
    renderServices(services);
  } catch {
    renderServices(FALLBACK_SERVICES);
  }
}

/* ══════════════════════════════════════════
   RENDER EVENTS
   ══════════════════════════════════════════ */
function fmtDate(d) {
  if (!d) return '';
  try {
    const dt = new Date(d + 'T00:00:00');
    return dt.toLocaleDateString('en-GB', { day: 'numeric', month: 'long', year: 'numeric' });
  } catch { return d; }
}

function renderEvents(events) {
  const grid = document.getElementById('events-grid');
  if (!events || !events.length) {
    grid.innerHTML = `
      <div class="events-empty">
        <svg viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
        <p style="font-size:1rem;font-weight:500;margin-bottom:0.5rem">No upcoming events right now</p>
        <p>Check back soon — new adventures are always being planned!</p>
      </div>`;
    return;
  }

  grid.innerHTML = events.map(e => {
    const included = e.included ? e.included.split(',').map(t => `<span class="event-tag">${t.trim()}</span>`).join('') : '';
    const excluded = e.excluded ? e.excluded.split(',').map(t => `<span class="event-tag excluded">${t.trim()}</span>`).join('') : '';
    const rawImg = e.display_image || e.image_url || e.image || null;
    const imgSrc = rawImg ? (rawImg.startsWith('http') ? rawImg : `http://127.0.0.1:8000${rawImg}`) : null;

    return `
    <div class="event-card fade-up">
      <div class="event-card-img" style="${imgSrc ? '' : 'background:linear-gradient(135deg,#0BB5D6 0%,#06557A 100%)'}">
        ${imgSrc ? `<img src="${imgSrc}" alt="${e.name}">` : ''}
        <div class="event-card-img-overlay"></div>
        <div class="event-card-img-text">
          <div class="event-date-badge">${fmtDate(e.date)}</div>
          <h3>${e.name}</h3>
        </div>
      </div>
      <div class="event-card-body">
        <div class="event-price">M${parseFloat(e.price).toLocaleString()} <span>per person</span></div>
        ${e.departure ? `<p style="font-size:0.8rem;color:var(--text-muted);margin-bottom:0.75rem">📍 Departing from ${e.departure}</p>` : ''}
        ${included ? `<div class="event-includes"><h4>Included</h4>${included}</div>` : ''}
        ${excluded ? `<div class="event-includes"><h4>Not included</h4>${excluded}</div>` : ''}
        ${e.deposit ? `<p class="deposit-note">* M${e.deposit} non-refundable deposit to secure your spot.</p>` : ''}
        <a href="#contact" class="event-cta" onclick="prefillService('${e.name}')">Book Your Spot</a>
      </div>
    </div>`;
  }).join('');

  grid.querySelectorAll('.fade-up').forEach(el => fadeObserver.observe(el));
}

async function loadEvents() {
  renderEventSkeletons();
  try {
    const data = await apiFetch('/events/?status=upcoming');
    const events = data.results || (Array.isArray(data) ? data : []);
    renderEvents(events);
  } catch {
    renderEvents([]);
  }
}

/* ══════════════════════════════════════════
   RENDER GALLERY
   ══════════════════════════════════════════ */
function renderGallery(photos) {
  const container = document.getElementById('gallery-container');
  const items = photos.slice(0, 5);

  if (!items.length) {
    container.innerHTML = `<div class="gallery-grid-skeleton">${Array.from({length:5},()=>`<div class="skeleton" style="min-height:240px"></div>`).join('')}</div>`;
    return;
  }

  container.innerHTML = `<div class="gallery-grid">
    ${items.map((p, i) => {
      const src = p.display_url || p.url || '';
      const fullSrc = src.startsWith('http') ? src : `http://127.0.0.1:8000${src}`;
      return `
      <div class="gallery-item" onclick="openLightbox('${fullSrc}','${p.caption} — ${p.year || ''}')">
        <img src="${fullSrc}" alt="${p.caption}" class="gallery-img" loading="${i > 0 ? 'lazy' : 'eager'}">
        <div class="gallery-label">${p.caption}${p.year ? ' — ' + p.year : ''}</div>
      </div>`;
    }).join('')}
  </div>`;
}

async function loadGallery() {
  renderGallerySkeletons();
  try {
    const data = await apiFetch('/gallery/?limit=5');
    const photos = data.results || (Array.isArray(data) ? data : []);
    renderGallery(photos);
  } catch {
    renderGallery([]);
  }
}

/* ══════════════════════════════════════════
   LOAD SETTINGS (stats, contact info)
   ══════════════════════════════════════════ */
async function loadSettings() {
  try {
    const s = await apiFetch('/settings/public/');
    if (s.stat_travellers)  document.getElementById('stat-travellers').textContent  = s.stat_travellers;
    if (s.stat_destinations)document.getElementById('stat-destinations').textContent= s.stat_destinations;
    if (s.stat_years)  { document.getElementById('stat-years').textContent  = s.stat_years;  document.getElementById('about-years').textContent = s.stat_years; }
    if (s.stat_countries)   document.getElementById('stat-countries').textContent   = s.stat_countries;
    if (s.location) {
      document.getElementById('contact-location').textContent = s.location;
      document.getElementById('footer-location').textContent  = s.location + ' · Est. 2015';
    }
    if (s.email)    document.getElementById('contact-email').textContent    = s.email;
    if (s.whatsapp) document.getElementById('contact-whatsapp').textContent = s.whatsapp;
    if (s.stat_travellers)  document.getElementById('about-travellers').textContent  = s.stat_travellers;
    if (s.stat_destinations)document.getElementById('about-destinations').textContent= s.stat_destinations;
    if (s.stat_countries)   document.getElementById('about-countries').textContent   = s.stat_countries;

    // Wire up clickable contact links
    const waNumber = (s.whatsapp || '').replace(/[^0-9]/g, '');
    document.getElementById('link-whatsapp').href  = waNumber ? `https://wa.me/${waNumber}` : '#contact';
    document.getElementById('link-facebook').href  = s.facebook || 'https://facebook.com';
    document.getElementById('link-email').href     = `mailto:${s.email || 'likilatours@gmail.com'}`;
    document.getElementById('link-location').href  = `https://www.google.com/maps/search/${encodeURIComponent(s.location || 'Botha-Buthe, Lesotho')}`;
  } catch { /* keep defaults set at init */ }
}

/* ══════════════════════════════════════════
   CONTACT FORM → API
   ══════════════════════════════════════════ */
function prefillService(name) {
  const sel = document.getElementById('f-service');
  for (let opt of sel.options) {
    if (opt.value === name || opt.text === name) { sel.value = opt.value; break; }
  }
  document.getElementById('contact').scrollIntoView({ behavior: 'smooth' });
}

document.getElementById('form-submit-btn').addEventListener('click', async function() {
  const btn    = this;
  const notice = document.getElementById('form-notice');
  const fname  = document.getElementById('f-fname').value.trim();
  const message= document.getElementById('f-message').value.trim();

  if (!fname || !message) {
    notice.className = 'api-notice error';
    notice.style.display = 'flex';
    notice.innerHTML = `<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg> Please fill in your name and message.`;
    return;
  }

  btn.textContent = 'Sending...'; btn.disabled = true;
  notice.style.display = 'none';

  const payload = {
    first_name: fname,
    last_name:  document.getElementById('f-lname').value.trim(),
    email:      document.getElementById('f-email').value.trim(),
    phone:      document.getElementById('f-phone').value.trim(),
    service:    document.getElementById('f-service').value,
    message
  };

  try {
    const res = await fetch(`${API_BASE}/inquiries/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || 'Failed');
    btn.textContent = 'Message Sent ✓'; btn.style.background = '#2E7D32';
    notice.className = 'api-notice'; notice.style.display = 'flex';
    notice.innerHTML = `<svg viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg> Thanks ${fname}! We'll be in touch soon.`;
    ['f-fname','f-lname','f-email','f-phone','f-message'].forEach(id => document.getElementById(id).value = '');
    setTimeout(() => { btn.textContent = 'Send Message →'; btn.style.background = ''; btn.disabled = false; }, 4000);
  } catch {
    btn.textContent = 'Send Message →'; btn.disabled = false;
    notice.className = 'api-notice error'; notice.style.display = 'flex';
    notice.innerHTML = `<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg> Couldn't send right now. Please WhatsApp us directly.`;
  }
});

/* ══════════════════════════════════════════
   LIGHTBOX
   ══════════════════════════════════════════ */
function openLightbox(src, caption) {
  document.getElementById('lightbox-img').src = src;
  document.getElementById('lightbox-caption').textContent = caption;
  document.getElementById('lightbox').classList.add('open');
  document.body.style.overflow = 'hidden';
}
function closeLightbox() {
  document.getElementById('lightbox').classList.remove('open');
  document.body.style.overflow = '';
}
document.addEventListener('keydown', e => { if (e.key === 'Escape') closeLightbox(); });

/* ══════════════════════════════════════════
   SCROLL ANIMATIONS
   ══════════════════════════════════════════ */
const fadeObserver = new IntersectionObserver(entries => {
  entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('visible'); });
}, { threshold: 0.1 });
document.querySelectorAll('.fade-up').forEach(el => fadeObserver.observe(el));

/* Nav shadow on scroll */
const navbar = document.getElementById('navbar');
window.addEventListener('scroll', () => navbar.classList.toggle('scrolled', window.scrollY > 40));

/* ══════════════════════════════════════════
   INIT
   ══════════════════════════════════════════ */
initHero();

// Set default hrefs immediately — overwritten by loadSettings() once API responds
document.getElementById('link-whatsapp').href = 'https://wa.me/62401920';
document.getElementById('link-facebook').href = 'https://web.facebook.com/profile.php?id=100054594153845';
document.getElementById('link-email').href    = 'mailto:likilatours@gmail.com';
document.getElementById('link-location').href = 'https://www.google.com/maps/search/Botha-Buthe%2C%20Lesotho';

loadSettings();
loadServices();
loadEvents();
loadGallery();

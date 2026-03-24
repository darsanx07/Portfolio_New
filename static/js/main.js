// ── Nav scroll effect ──
const nav = document.getElementById('nav');
window.addEventListener('scroll', () => {
  nav.classList.toggle('scrolled', window.scrollY > 60);
});

// ── Scroll reveal ──
const revealEls = document.querySelectorAll(
  '#about, #skills, #projects, #contact, .project-card, .skill-group, .about-facts, .contact-info'
);
revealEls.forEach(el => el.classList.add('reveal'));

const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry, i) => {
      if (entry.isIntersecting) {
        setTimeout(() => entry.target.classList.add('visible'), i * 80);
        observer.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.1, rootMargin: '0px 0px -60px 0px' }
);
revealEls.forEach(el => observer.observe(el));

// ── Contact form ──
const form       = document.getElementById('contact-form');
const submitBtn  = document.getElementById('submit-btn');
const btnText    = document.getElementById('btn-text');
const btnLoader  = document.getElementById('btn-loader');
const formStatus = document.getElementById('form-status');

form.addEventListener('submit', async (e) => {
  e.preventDefault();

  const name    = document.getElementById('name').value.trim();
  const email   = document.getElementById('email').value.trim();
  const message = document.getElementById('message').value.trim();

  // Client-side validation
  if (!name || !email || !message) {
    showStatus('Please fill in all fields.', 'error');
    return;
  }

  setLoading(true);
  formStatus.textContent = '';
  formStatus.className = 'form-status';

  try {
    const res = await fetch('/api/contact', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, email, message })
    });

    const data = await res.json();

    if (data.success) {
      showStatus(data.message, 'success');
      form.reset();
    } else {
      showStatus(data.error || 'Something went wrong. Please try again.', 'error');
    }
  } catch (err) {
    showStatus('Network error — please check your connection and try again.', 'error');
  } finally {
    setLoading(false);
  }
});

function setLoading(on) {
  submitBtn.disabled = on;
  btnText.textContent = on ? 'Sending...' : 'Send message';
  btnLoader.style.display = on ? 'inline-block' : 'none';
}

function showStatus(msg, type) {
  formStatus.textContent = msg;
  formStatus.className = `form-status ${type}`;
}

// ── Smooth anchor scroll (offset for fixed nav) ──
document.querySelectorAll('a[href^="#"]').forEach(link => {
  link.addEventListener('click', (e) => {
    const target = document.querySelector(link.getAttribute('href'));
    if (!target) return;
    e.preventDefault();
    const offset = nav.offsetHeight + 24;
    window.scrollTo({ top: target.offsetTop - offset, behavior: 'smooth' });
  });
});

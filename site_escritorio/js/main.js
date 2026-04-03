// Gastão da Rosa & Moukarzel — Advogados Associados
// Main JavaScript

(function () {
  'use strict';

  // --- Header scroll effect ---
  const header = document.getElementById('header');

  function handleHeaderScroll() {
    if (window.scrollY > 80) {
      header.classList.add('header--scrolled');
    } else {
      header.classList.remove('header--scrolled');
    }
  }

  window.addEventListener('scroll', handleHeaderScroll, { passive: true });

  // --- Mobile menu ---
  const menuBtn = document.getElementById('menu-btn');
  const nav = document.getElementById('nav');

  menuBtn.addEventListener('click', function () {
    menuBtn.classList.toggle('active');
    nav.classList.toggle('active');
  });

  // Close mobile menu when a link is clicked
  var navLinks = document.querySelectorAll('.header__nav-link');
  navLinks.forEach(function (link) {
    link.addEventListener('click', function () {
      menuBtn.classList.remove('active');
      nav.classList.remove('active');
    });
  });

  // --- Smooth scroll for anchor links ---
  document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
    anchor.addEventListener('click', function (e) {
      var targetId = this.getAttribute('href');
      if (targetId === '#') return;
      var target = document.querySelector(targetId);
      if (target) {
        e.preventDefault();
        var offset = header.offsetHeight + 16;
        var top = target.getBoundingClientRect().top + window.scrollY - offset;
        window.scrollTo({ top: top, behavior: 'smooth' });
      }
    });
  });

  // --- Fade-in on scroll (Intersection Observer) ---
  var fadeElements = document.querySelectorAll(
    '.section__header, .sobre__text, .valor-card, .area-card, .membro-card, .contato__info, .contato__form, .pub-card, .cta-band__container, .reconhecimentos__container'
  );

  fadeElements.forEach(function (el) {
    el.classList.add('fade-in');
  });

  if ('IntersectionObserver' in window) {
    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.15, rootMargin: '0px 0px -40px 0px' }
    );

    fadeElements.forEach(function (el) {
      observer.observe(el);
    });
  } else {
    // Fallback: show all immediately
    fadeElements.forEach(function (el) {
      el.classList.add('visible');
    });
  }

  // --- Contact form handler ---
  var form = document.getElementById('contact-form');
  if (form) {
    var isEN = window.location.pathname.indexOf('/en/') !== -1;

    form.addEventListener('submit', function (e) {
      e.preventDefault();

      var nome     = document.getElementById('nome').value.trim();
      var email    = document.getElementById('email').value.trim();
      var mensagem = document.getElementById('mensagem').value.trim();

      if (!nome || !email || !mensagem) {
        alert(isEN ? 'Please fill in all required fields.' : 'Por favor, preencha todos os campos obrigatórios.');
        return;
      }

      var btn = form.querySelector('button[type="submit"]');
      var originalText = btn.textContent;
      btn.textContent = isEN ? 'Sending...' : 'Enviando...';
      btn.disabled = true;

      var payload = {
        nome:     document.getElementById('nome').value.trim(),
        email:    document.getElementById('email').value.trim(),
        telefone: (document.getElementById('telefone') || {}).value || '',
        assunto:  (document.getElementById('assunto')  || {}).value || '',
        mensagem: document.getElementById('mensagem').value.trim(),
        _subject: 'Contato via Site — Gastão da Rosa & Moukarzel'
      };

      fetch('https://formsubmit.co/ajax/contato@gastaoemoukarzel.adv.br', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
        body: JSON.stringify(payload)
      })
        .then(function (res) { return res.json(); })
        .then(function (json) {
          if (json.success === 'true' || json.success === true) {
            btn.textContent = isEN ? 'Message Sent!' : 'Mensagem Enviada!';
            btn.style.background = '#b8945f';
            form.reset();
            setTimeout(function () {
              btn.textContent = originalText;
              btn.style.background = '';
              btn.disabled = false;
            }, 3000);
          } else {
            alert(isEN ? 'Error sending message. Please try again.' : 'Erro ao enviar. Tente novamente.');
            btn.textContent = originalText;
            btn.disabled = false;
          }
        })
        .catch(function () {
          alert(isEN ? 'Connection error. Please try again.' : 'Erro de conexão. Tente novamente.');
          btn.textContent = originalText;
          btn.disabled = false;
        });
    });
  }

  // --- Active nav link highlight (multi-page) ---
  var currentPage = window.location.pathname.split('/').pop() || 'index.html';
  navLinks.forEach(function (link) {
    var href = link.getAttribute('href');
    if (href === currentPage) {
      link.classList.add('active');
    }
  });
})();

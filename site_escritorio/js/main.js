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

      var data = new FormData(form);

      // mail.php is always at site root
      var phpPath = window.location.pathname.indexOf('/en/') !== -1 ? '../mail.php' : 'mail.php';

      fetch(phpPath, { method: 'POST', body: data })
        .then(function (res) {
          return res.text().then(function (text) {
            try {
              return JSON.parse(text);
            } catch (e) {
              throw new Error('Resposta inválida do servidor: ' + text.substring(0, 200));
            }
          });
        })
        .then(function (json) {
          if (json.success) {
            btn.textContent = isEN ? 'Message Sent!' : 'Mensagem Enviada!';
            btn.style.background = '#b8945f';
            form.reset();
            setTimeout(function () {
              btn.textContent = originalText;
              btn.style.background = '';
              btn.disabled = false;
            }, 3000);
          } else {
            alert(json.message || (isEN ? 'Error sending message.' : 'Erro ao enviar mensagem.'));
            btn.textContent = originalText;
            btn.disabled = false;
          }
        })
        .catch(function (err) {
          alert(err.message || (isEN ? 'Connection error. Please try again.' : 'Erro de conexão. Tente novamente.'));
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

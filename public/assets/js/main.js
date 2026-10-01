/* ==========================================================================
   Premkumar V — Portfolio Scripts
   Premium Micro-animations:
   - Staggered entrance & scroll progress
   - IntersectionObserver scroll reveal
   - Living organic shape & floating portrait
   - Hand-drawn SVG stroke animation
   - Realistic LLM typing simulation
   - Subtle decorative mouse parallax
   - Direct Email & WhatsApp delivery
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
  // 1. Initialize Lucide Icons
  if (window.lucide) {
    window.lucide.createIcons();
  }

  // 2. Scroll Progress Bar
  const progressBar = document.getElementById('scroll-progress');
  window.addEventListener('scroll', () => {
    if (progressBar) {
      const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
      const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
      const scrolled = height > 0 ? (winScroll / height) * 100 : 0;
      progressBar.style.width = scrolled + '%';
    }
  }, { passive: true });

  // 3. Scroll Reveal with IntersectionObserver (trigger once per section)
  const revealElements = document.querySelectorAll('.reveal-on-scroll');
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries, obs) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-revealed');
          obs.unobserve(entry.target);
        }
      });
    }, {
      threshold: 0.12,
      rootMargin: '0px 0px -40px 0px'
    });

    revealElements.forEach(el => observer.observe(el));
  } else {
    revealElements.forEach(el => el.classList.add('is-revealed'));
  }

  // 4. Subtle Decorative Mouse Parallax (1–3px movement ONLY on decorative shapes)
  const parallaxItems = document.querySelectorAll('.mouse-parallax');
  let ticking = false;

  window.addEventListener('mousemove', (e) => {
    if (!ticking) {
      window.requestAnimationFrame(() => {
        const xFactor = (e.clientX / window.innerWidth - 0.5) * 6; // max 3px
        const yFactor = (e.clientY / window.innerHeight - 0.5) * 6; // max 3px
        parallaxItems.forEach(item => {
          const depth = parseFloat(item.getAttribute('data-depth') || '0.5');
          item.style.transform = `translate3d(${xFactor * depth}px, ${yFactor * depth}px, 0)`;
        });
        ticking = false;
      });
      ticking = true;
    }
  }, { passive: true });

  // 5. Realistic LLM Chat Simulation (TamilRootLabs.ai Featured Project)
  const chatAiText = document.getElementById('chat-ai-typing-text');
  const chatAiCursor = document.getElementById('chat-ai-cursor');
  const fullText = "Absolutely. What would you like to explore?";
  let charIndex = 0;
  let isTyping = false;

  function typeAiResponse() {
    if (!chatAiText) return;
    isTyping = true;
    chatAiText.textContent = '';
    charIndex = 0;
    if (chatAiCursor) chatAiCursor.style.display = 'inline-block';

    const typingInterval = setInterval(() => {
      if (charIndex < fullText.length) {
        chatAiText.textContent += fullText.charAt(charIndex);
        charIndex++;
      } else {
        clearInterval(typingInterval);
        isTyping = false;
        // Pause 7 seconds before gently retyping
        setTimeout(() => {
          if (!isTyping) typeAiResponse();
        }, 7000);
      }
    }, 55);
  }

  // Trigger typing simulation when featured section is revealed
  const featuredSection = document.getElementById('featured-ai-project');
  if (featuredSection && 'IntersectionObserver' in window) {
    const chatObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting && !isTyping && charIndex === 0) {
          setTimeout(typeAiResponse, 800);
        }
      });
    }, { threshold: 0.2 });
    chatObserver.observe(featuredSection);
  } else {
    setTimeout(typeAiResponse, 1500);
  }

  // 6. Toast Notification Helper
  const toast = document.getElementById('toast');
  function showToast(message) {
    if (!toast) return;
    const toastText = document.getElementById('toast-text');
    if (toastText) toastText.textContent = message;
    toast.classList.add('show');
    setTimeout(() => {
      toast.classList.remove('show');
    }, 3600);
  }

  // 7. Email Copy Action
  const copyButtons = document.querySelectorAll('.copy-email-btn');
  const emailText = 'vpremkumar0113@gmail.com';

  copyButtons.forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      navigator.clipboard.writeText(emailText).then(() => {
        showToast('Email copied to clipboard: ' + emailText);
      }).catch(() => {
        const textarea = document.createElement('textarea');
        textarea.value = emailText;
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);
        showToast('Email copied: ' + emailText);
      });
    });
  });

  // 8. Phone / WhatsApp Number Copy Action (+91 6385382658)
  const copyPhoneButtons = document.querySelectorAll('.copy-phone-btn');
  const phoneText = '+91 6385382658';

  copyPhoneButtons.forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      navigator.clipboard.writeText(phoneText).then(() => {
        showToast('Phone & WhatsApp number copied: ' + phoneText);
      }).catch(() => {
        showToast('Phone number: ' + phoneText);
      });
    });
  });

  // 9. Mobile Menu Toggle
  const mobileMenuBtn = document.getElementById('mobile-menu-btn');
  const mobileMenu = document.getElementById('mobile-menu');
  const mobileMenuIcon = document.getElementById('mobile-menu-icon');

  if (mobileMenuBtn && mobileMenu) {
    mobileMenuBtn.addEventListener('click', () => {
      const isHidden = mobileMenu.classList.contains('hidden');
      if (isHidden) {
        mobileMenu.classList.remove('hidden');
        if (mobileMenuIcon) mobileMenuIcon.setAttribute('data-lucide', 'x');
      } else {
        mobileMenu.classList.add('hidden');
        if (mobileMenuIcon) mobileMenuIcon.setAttribute('data-lucide', 'menu');
      }
      if (window.lucide) window.lucide.createIcons();
    });

    mobileMenu.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        mobileMenu.classList.add('hidden');
        if (mobileMenuIcon) mobileMenuIcon.setAttribute('data-lucide', 'menu');
        if (window.lucide) window.lucide.createIcons();
      });
    });
  }

  // 10. Skills Filter Tabs
  const filterBtns = document.querySelectorAll('.skill-filter-btn');
  const skillCards = document.querySelectorAll('.skill-item');

  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      filterBtns.forEach(b => {
        b.classList.remove('bg-stone-900', 'text-white', 'border-stone-900');
        b.classList.add('bg-white', 'text-stone-700', 'border-stone-200');
      });
      btn.classList.remove('bg-white', 'text-stone-700', 'border-stone-200');
      btn.classList.add('bg-stone-900', 'text-white', 'border-stone-900');

      const filter = btn.getAttribute('data-filter');
      skillCards.forEach(card => {
        const category = card.getAttribute('data-category');
        if (filter === 'all' || category === filter) {
          card.style.display = 'flex';
        } else {
          card.style.display = 'none';
        }
      });
    });
  });

  // 11. Featured Project Modal
  const openModalBtn = document.getElementById('open-chatbot-modal');
  const closeModalBtns = document.querySelectorAll('.close-modal-btn');
  const modal = document.getElementById('chatbot-modal');

  if (openModalBtn && modal) {
    openModalBtn.addEventListener('click', () => {
      modal.classList.remove('hidden');
      document.body.style.overflow = 'hidden';
      if (window.lucide) window.lucide.createIcons();
    });

    closeModalBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        modal.classList.add('hidden');
        document.body.style.overflow = '';
      });
    });

    modal.addEventListener('click', (e) => {
      if (e.target === modal) {
        modal.classList.add('hidden');
        document.body.style.overflow = '';
      }
    });
  }

  // Contact Card Entrance Observer (Triggers only once when entering viewport)
  const contactCard = document.getElementById('contact-card');
  if (contactCard) {
    if ('IntersectionObserver' in window) {
      const contactCardObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            contactCard.classList.add('card-entered');
            observer.unobserve(entry.target);
          }
        });
      }, {
        threshold: 0.15,
        rootMargin: '0px 0px -40px 0px'
      });
      contactCardObserver.observe(contactCard);
    } else {
      contactCard.classList.add('card-entered');
    }
  }

  // 12. Contact Form & Delivery Dispatch (Email or WhatsApp)
  const contactForm = document.getElementById('contact-form');
  const methodEmailBtn = document.getElementById('method-email-btn');
  const methodWhatsAppBtn = document.getElementById('method-whatsapp-btn');
  const deliveryMethodInput = document.getElementById('selected-delivery-method');
  const submitBtnText = document.getElementById('submit-btn-text');
  const formSuccess = document.getElementById('form-success');
  const formSuccessText = document.getElementById('form-success-text');

  if (methodEmailBtn && methodWhatsAppBtn && deliveryMethodInput) {
    methodEmailBtn.addEventListener('click', () => {
      deliveryMethodInput.value = 'email';
      methodEmailBtn.classList.add('bg-white', 'text-stone-900', 'shadow-sm');
      methodEmailBtn.classList.remove('text-stone-600');
      methodWhatsAppBtn.classList.remove('bg-white', 'text-stone-900', 'shadow-sm');
      methodWhatsAppBtn.classList.add('text-stone-600');
      if (submitBtnText) submitBtnText.textContent = 'Send via Email';
    });

    methodWhatsAppBtn.addEventListener('click', () => {
      deliveryMethodInput.value = 'whatsapp';
      methodWhatsAppBtn.classList.add('bg-white', 'text-stone-900', 'shadow-sm');
      methodWhatsAppBtn.classList.remove('text-stone-600');
      methodEmailBtn.classList.remove('bg-white', 'text-stone-900', 'shadow-sm');
      methodEmailBtn.classList.add('text-stone-600');
      if (submitBtnText) submitBtnText.textContent = 'Send via WhatsApp (+91 6385382658)';
    });
  }

  if (contactForm) {
    contactForm.addEventListener('submit', (e) => {
      e.preventDefault();

      const name = document.getElementById('contact-name')?.value.trim() || 'Visitor';
      const company = document.getElementById('contact-company')?.value.trim() || '';
      const contactInfo = document.getElementById('contact-info')?.value.trim() || '';
      const subject = document.getElementById('contact-subject')?.value || 'Portfolio Inquiry';
      const message = document.getElementById('contact-message')?.value.trim() || '';
      const method = deliveryMethodInput?.value || 'email';

      const submitBtn = document.getElementById('submit-btn');
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.classList.add('arrow-launching');
      }

      if (method === 'whatsapp') {
        const companyText = company ? `\n*Company:* ${company}` : '';
        const waText = `Hi Premkumar,\n\nI saw your AI Developer portfolio.\n\n*Name:* ${name}${companyText}\n*Contact (Email/Mobile):* ${contactInfo}\n*Subject:* ${subject}\n\n*Message:*\n${message}`;
        const waUrl = `https://wa.me/916385382658?text=${encodeURIComponent(waText)}`;

        if (formSuccess && formSuccessText) {
          formSuccessText.textContent = 'Opening WhatsApp to send your message directly to Premkumar (+91 6385382658)...';
          formSuccess.classList.remove('hidden');
        }

        showToast('Opening WhatsApp with your pre-filled message...');
        setTimeout(() => {
          window.open(waUrl, '_blank');
          if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.classList.remove('arrow-launching');
          }
        }, 350);
      } else {
        const companyLine = company ? `Company / Org: ${company}\n` : '';
        const mailBody = `Hi Premkumar,\n\n${message}\n\n------------------------------\nSender Name: ${name}\n${companyLine}Contact Info: ${contactInfo}\nInquiry Type: ${subject}\nSent from your portfolio website.`;
        const mailSubject = `[Portfolio Inquiry] ${subject} - from ${name}`;
        const mailtoUrl = `mailto:vpremkumar0113@gmail.com?subject=${encodeURIComponent(mailSubject)}&body=${encodeURIComponent(mailBody)}`;

        if (formSuccess && formSuccessText) {
          formSuccessText.textContent = 'Opening your email client to send to vpremkumar0113@gmail.com...';
          formSuccess.classList.remove('hidden');
        }

        showToast('Opening your email client to dispatch to vpremkumar0113@gmail.com...');
        setTimeout(() => {
          window.location.href = mailtoUrl;
          if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.classList.remove('arrow-launching');
          }
        }, 350);
      }
    });
  }

  // 13. Active Nav Highlighting on Scroll
  const sections = document.querySelectorAll('section[id]');
  const navLinks = document.querySelectorAll('.nav-link');

  window.addEventListener('scroll', () => {
    let current = '';
    const scrollPosition = window.pageYOffset + 160;

    sections.forEach(section => {
      const sectionTop = section.offsetTop;
      const sectionHeight = section.offsetHeight;
      if (scrollPosition >= sectionTop && scrollPosition < sectionTop + sectionHeight) {
        current = section.getAttribute('id');
      }
    });

    navLinks.forEach(link => {
      link.classList.remove('text-stone-900', 'font-semibold');
      link.classList.add('text-stone-600');
      if (link.getAttribute('href') === `#${current}`) {
        link.classList.add('text-stone-900', 'font-semibold');
        link.classList.remove('text-stone-600');
      }
    });
  }, { passive: true });
});

/**
 * IRONFORGE FITNESS - MAIN JAVASCRIPT
 */

document.addEventListener('DOMContentLoaded', function () {
  // 1. Sticky Navbar on Scroll
  const navbar = document.querySelector('.main-navbar');
  if (navbar) {
    const handleScroll = () => {
      if (window.scrollY > 40) {
        navbar.classList.add('scrolled');
      } else {
        navbar.classList.remove('scrolled');
      }
    };
    window.addEventListener('scroll', handleScroll, { passive: true });
    handleScroll();
  }

  // 2. Set Minimum Date for Booking Pickers (Cannot book past dates)
  const datePickers = document.querySelectorAll('input[type="date"], input[name="preferred_date"]');
  const today = new Date().toISOString().split('T')[0];
  datePickers.forEach(picker => {
    picker.setAttribute('min', today);
    if (!picker.value) {
      picker.value = today;
    }
  });

  // 3. Instagram Reel Video Modal Player
  const reelCards = document.querySelectorAll('.reel-card');
  const reelModalEl = document.getElementById('reelVideoModal');
  
  if (reelModalEl && reelCards.length > 0) {
    const reelVideo = document.getElementById('modalReelVideo');
    const reelTitle = document.getElementById('modalReelTitle');
    const reelCaption = document.getElementById('modalReelCaption');
    const reelIgLink = document.getElementById('modalReelIgLink');
    const bsModal = new bootstrap.Modal(reelModalEl);

    reelCards.forEach(card => {
      card.addEventListener('click', function () {
        const title = this.getAttribute('data-title') || 'Ironforge Reel';
        const caption = this.getAttribute('data-caption') || '';
        const videoUrl = this.getAttribute('data-video') || '';
        const igUrl = this.getAttribute('data-ig-url') || 'https://instagram.com/ironforgefitness';

        if (reelTitle) reelTitle.textContent = title;
        if (reelCaption) reelCaption.textContent = caption;
        if (reelIgLink) reelIgLink.href = igUrl;

        if (reelVideo) {
          if (videoUrl) {
            reelVideo.src = videoUrl;
            reelVideo.style.display = 'block';
            reelVideo.play().catch(() => {});
          } else {
            reelVideo.style.display = 'none';
          }
        }

        bsModal.show();
      });
    });

    reelModalEl.addEventListener('hidden.bs.modal', function () {
      if (reelVideo) {
        reelVideo.pause();
        reelVideo.currentTime = 0;
        reelVideo.src = '';
      }
    });
  }

  // 4. Classes Day Filter Tabs
  const dayFilters = document.querySelectorAll('.class-day-btn');
  const classRows = document.querySelectorAll('.class-schedule-block');

  if (dayFilters.length > 0 && classRows.length > 0) {
    dayFilters.forEach(btn => {
      btn.addEventListener('click', function () {
        dayFilters.forEach(b => b.classList.remove('active', 'btn-primary-glow'));
        dayFilters.forEach(b => b.classList.add('btn-outline-glass'));
        
        this.classList.remove('btn-outline-glass');
        this.classList.add('active', 'btn-primary-glow');

        const targetDay = this.getAttribute('data-day');
        classRows.forEach(row => {
          if (targetDay === 'ALL' || row.getAttribute('data-day') === targetDay) {
            row.style.display = 'block';
          } else {
            row.style.display = 'none';
          }
        });
      });
    });
  }

  // 5. Facilities Category Filter
  const facilityFilters = document.querySelectorAll('.facility-filter-btn');
  const facilityCards = document.querySelectorAll('.facility-item');

  if (facilityFilters.length > 0 && facilityCards.length > 0) {
    facilityFilters.forEach(btn => {
      btn.addEventListener('click', function () {
        facilityFilters.forEach(b => b.classList.remove('active', 'btn-primary-glow'));
        facilityFilters.forEach(b => b.classList.add('btn-outline-glass'));

        this.classList.remove('btn-outline-glass');
        this.classList.add('active', 'btn-primary-glow');

        const category = this.getAttribute('data-category');
        facilityCards.forEach(card => {
          if (category === 'ALL' || card.getAttribute('data-category') === category) {
            card.style.display = 'block';
          } else {
            card.style.display = 'none';
          }
        });
      });
    });
  }

  // 6. Auto-dismiss alerts after 6 seconds
  const autoAlerts = document.querySelectorAll('.alert-dismissible');
  autoAlerts.forEach(alert => {
    setTimeout(() => {
      const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
      if (bsAlert) bsAlert.close();
    }, 6000);
  });
});

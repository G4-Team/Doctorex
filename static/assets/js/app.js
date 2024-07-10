//========= start specialty ==============/

var swiper = new Swiper(".specialty-swiper", {
  slidesPerView: 7,

  spaceBetween: 10,
  navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev",
  },

  breakpoints: {
    100: {
      slidesPerView: 1,
    },
    300: {
      slidesPerView: 2,
    },
    450: {
      slidesPerView: 2,
    },
    576: {
      slidesPerView: 3,
    },
    768: {
      slidesPerView: 4,
    },
    1024: {
      slidesPerView: 5,
    },
    1200: {
      slidesPerView: 6,
    },
    1400: {
      slidesPerView: 6,
    }
  },
});


//========= end specialty ==============/


//========= start doctor ==============/

var swiper = new Swiper(".doctor-swiper", {
  slidesPerView: 7,

  spaceBetween: 20,
  navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev",
  },

  breakpoints: {
    100: {
      slidesPerView: 1,
    },
    576: {
      slidesPerView: 2,
    },
    1024: {
      slidesPerView: 3,
    },
    1400: {
      slidesPerView: 4,
    }
  },
});


//========= end doctor ==============/


document.addEventListener("DOMContentLoaded", function () {

    // Initialize AOS
    AOS.init({
        duration: 700,
        once: true
    });

    // Back to Top Button
    const btn = document.getElementById("backToTop");

    if (btn) {

        window.addEventListener("scroll", function () {
            btn.style.display = window.scrollY > 300 ? "block" : "none";
        });

        btn.addEventListener("click", function () {
            window.scrollTo({
                top: 0,
                behavior: "smooth"
            });
        });

    }

    // Hero Swiper
    if (document.querySelector(".heroSwiper")) {

        new Swiper(".heroSwiper", {

            loop: true,

            effect: "fade",

            speed: 1000,

            autoplay: {
                delay: 5000,
                disableOnInteraction: false
            },

            pagination: {
                el: ".swiper-pagination",
                clickable: true
            },

            navigation: {
                nextEl: ".swiper-button-next",
                prevEl: ".swiper-button-prev"
            }

        });

    }

    // Animated Counters
    document.querySelectorAll(".counter").forEach(counter => {

        const target = parseInt(counter.dataset.target) || 0;

        let current = 0;

        const increment = target / 100;

        const update = () => {

            current += increment;

            if (current >= target) {

                counter.textContent = target.toLocaleString();

            } else {

                counter.textContent = Math.floor(current).toLocaleString();

                requestAnimationFrame(update);

            }

        };

        update();

    });

});
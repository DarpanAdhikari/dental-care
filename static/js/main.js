document.addEventListener('DOMContentLoaded', function() {
    const faBars = document.querySelector('.fa-bars');
    const navbar = document.querySelector('.navbar');
    const header = document.querySelector('header');
    faBars.addEventListener('click', function() {
        faBars.classList.toggle('fa-times');
        navbar.classList.toggle('nav-toggle');
    });
    window.addEventListener('scroll', function() {
        loadScrollAction();
    });
    window.addEventListener('load', function() {
       loadScrollAction();
    });
    function loadScrollAction(){
        faBars.classList.remove('fa-times');
        navbar.classList.remove('nav-toggle');

        if (window.scrollY > 30) {
            header.classList.add('header-active');
        } else {
            header.classList.remove('header-active');
        }
    }
});

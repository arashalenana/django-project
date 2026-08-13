document.addEventListener('DOMContentLoaded', function () {
    const toggle = document.getElementById('navToggle');
    const links = document.getElementById('navLinks');
    if (toggle && links) {
        toggle.addEventListener('click', function () {
            links.classList.toggle('open');
        });
    }
});

document.addEventListener('DOMContentLoaded', function () {
    const toggle = document.getElementById('accountDropdownToggle');
    const menu = document.getElementById('accountDropdownMenu');
    const wrapper = document.getElementById('accountDropdown');

    if (toggle && menu && wrapper) {
        toggle.addEventListener('click', function (event) {
            event.stopPropagation();
            const isOpen = menu.classList.toggle('open');
            toggle.setAttribute('aria-expanded', isOpen);
        });

        document.addEventListener('click', function (event) {
            if (!wrapper.contains(event.target)) {
                menu.classList.remove('open');
                toggle.setAttribute('aria-expanded', 'false');
            }
        });
    }
});
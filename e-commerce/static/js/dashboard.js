document.addEventListener('DOMContentLoaded', function () {
    const toggle = document.getElementById('dashboardSidebarToggle');
    const sidebar = document.getElementById('dashboardSidebar');
    if (toggle && sidebar) {
        toggle.addEventListener('click', function () {
            sidebar.classList.toggle('open');
        });
    }
});
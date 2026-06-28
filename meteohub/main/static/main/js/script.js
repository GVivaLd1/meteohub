const sideBarButton = document.getElementById('toggle-sidebar-btn')

sideBarButton.addEventListener('click', function() {
    document.getElementById('sidebar').classList.toggle('collapsed');
});
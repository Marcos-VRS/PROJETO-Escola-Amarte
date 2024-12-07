document.addEventListener('DOMContentLoaded', function () {
    // Função para carregar conteúdo via AJAX
    function loadContent(url) {
        fetch(url)
            .then(response => response.text())
            .then(html => {
                document.querySelector('.main-content').innerHTML = html;
            })
            .catch(error => {
                console.error('Erro ao carregar o conteúdo:', error);
            });
    }

    // Evento para links do menu
    const links = document.querySelectorAll('.sidebar a[data-url]');
    links.forEach(link => {
        link.addEventListener('click', function (e) {
            e.preventDefault();
            const url = this.getAttribute('data-url');
            loadContent(url);
        });
    });

    // Evento para botão de logout
    const logoutButton = document.getElementById('logout-button');
    if (logoutButton) {
        logoutButton.addEventListener('click', function (e) {
            e.preventDefault();
            window.location.href = this.href;
        });
    }
});
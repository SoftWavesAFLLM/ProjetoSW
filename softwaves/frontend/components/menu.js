function loadMenu() {
    // Recupera dados do usuário
    let usuarioLogado = JSON.parse(localStorage.getItem("usuarioLogado")) || {};
    const nomeUsuario =
        usuarioLogado.nome ||
        usuarioLogado.nome_funcionario ||
        usuarioLogado.nome_usuario ||
        usuarioLogado.user ||
        usuarioLogado.username ||
        "Usuário";

    // HTML do menu
    const menuHtml = `
        <header>
            <nav class="navbar bg-body-tertiary fixed-top">
                <div class="container-fluid d-flex justify-content-start align-items-center gap-3">
                    
                    <!-- BOTÃO MENU (para offcanvas) -->
                    <button class="navbar-toggler" type="button" data-bs-toggle="offcanvas"
                        data-bs-target="#offcanvasNavbar" aria-controls="offcanvasNavbar">
                        <span class="navbar-toggler-icon"></span>
                    </button>

                    <!-- LOGO -->
                    <img src="/imagens/logo.png" alt="logo" id="logo2">

                    <!-- USER + SAIR -->
                    <div class="d-flex align-items-center gap-3 ms-auto">
                        <span id="userName" class="fw-bold">${nomeUsuario}</span>
                        <button id="btnLogout" class="btn btn-danger btn-sm">Sair</button>
                    </div>

                    <!-- MENU LATERAL -->
                    <div class="offcanvas offcanvas-start" tabindex="-1" id="offcanvasNavbar">
                        <div class="offcanvas-header">
                            <h5 class="offcanvas-title">SoftWaves</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="offcanvas"></button>
                        </div>

                        <div class="offcanvas-body">
                            <ul class="navbar-nav justify-content-start flex-grow-1 pe-3">
                                <li><a class="nav-link" href="/view/pages/inicial.html">Home</a></li>
                                <li><a class="nav-link" href="/view/pages/dashboards.html">Dashboards</a></li>
                                <li class="nav-item dropdown">
                                    <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">
                                        Gestões e Gerenciamentos
                                    </a>
                                    <ul class="dropdown-menu">
                                        <li><a class="dropdown-item" href="/view/pages/gestao_maquinas.html">Gerenciamento de Máquinas</a></li>
                                        <li><a class="dropdown-item" href="/view/pages/gestao_usuarios.html">Gerenciamento de Usuários</a></li>
                                        <li><a class="dropdown-item" href="/view/pages/gestao_sensores.html">Gerenciamento de Sensores</a></li>
                                        <li><a class="dropdown-item" href="/view/pages/gestao_manutencao.html">Ordem de Manutenção</a></li>
                                        <li><a class="dropdown-item" href="/view/pages/gestao_pecas.html">Gerenciamento de Peças</a></li>
                                        <li><a class="dropdown-item" href="/view/pages/relatorios_to.html">Relatórios T.O.</a></li>
                                    </ul>
                                </li>
                                <li><a class="nav-link" href="/view/pages/suporte.html">Suporte</a></li>
                            </ul>
                        </div>
                    </div>

                </div>
            </nav>
        </header>
    `;

    // Renderiza o menu
    const menuContainer = document.getElementById('menu-container');
    if (!menuContainer) return;
    menuContainer.innerHTML = menuHtml;

    // Logout
    document.getElementById("btnLogout").addEventListener("click", () => {
        localStorage.removeItem("usuarioLogado");
        window.location.href = "/view/pages/login.html";
    });

    // CSS da logo
    const style = document.createElement("style");
    style.innerHTML = `
        #logo2 {
            width: 40px !important;
            height: auto !important;
        }
    `;
    document.head.appendChild(style);
}

window.addEventListener("DOMContentLoaded", loadMenu);

// js/main.js

// Ponto Chave: Esta função carrega o HTML da página e, se necessário, o módulo JS correspondente.
export async function loadPage(page) {
  const contentDiv = document.getElementById('main-content');

  try {
    const response = await fetch(`/view/pages/${page}`);
    if (!response.ok) throw new Error('Página não encontrada');
    const data = await response.text();
    contentDiv.innerHTML = data;

    const route = page.replace('.html', '');

    // Roteamento para carregar o módulo JS específico da página
    if (route === "gestao_maquinas") {
      const modulo = await import(`/js/gestao_maquina.js`);
      modulo.init();
    } else if (route === "gestao_usuarios") {
      const modulo = await import(`/js/gestao_usuarios.js`);
      modulo.init();
    } else if (route === "gestao_sensores") {
      const modulo = await import(`/js/gestao_sensores.js`);
      modulo.init();
    } else if (route === "gestao_pecas") {
      const modulo = await import(`/js/gestao_pecas.js`);
      modulo.init();
    } else if (route === "gestao_manutencao") {
      const modulo = await import(`/js/gestao_manutencao.js`);
      modulo.init();
    } else if (route === "relatorios_to") {
      const modulo = await import(`/js/relatorios_to.js`);
      modulo.init();
    } else if (route === "relatorios") {
      const modulo = await import(`/js/relatorios.js`);
      modulo.carregarRelatorios?.();
    } else if (route === "dashboards") {
      // Ponto Chave: Chama a função correta 'carregarDashboards' exportada pelo módulo.
      const modulo = await import(`/js/dashboards.js`);
      modulo.carregarDashboards();

    }

  } catch (error) {
    contentDiv.innerHTML = `<h2>Erro ao carregar a página</h2><p>${error.message}</p>`;
    console.error("Erro ao carregar a página:", error);
  }
}

// Ponto Chave: Inicializa a SPA, cuidando dos cliques nos links e do histórico do navegador.
export function initSPA() {
  const menuContainer = document.getElementById('menu-container');

  menuContainer.addEventListener('click', (e) => {
    const target = e.target.closest('a'); // Garante que pegue o link mesmo se clicar num ícone dentro dele
    if (target && target.getAttribute('href') && target.getAttribute('href').endsWith('.html')) {
      e.preventDefault();
      let route = target.getAttribute('href').substring(1);
      if (route === '') route = 'home';

      loadPage(route + '.html');
      history.pushState(null, '', target.getAttribute('href'));
    }
  });

  // Carrega a página inicial baseada na URL atual
  let initialRoute = window.location.pathname.substring(1);
  if (initialRoute === '') initialRoute = 'home';
  loadPage(initialRoute + '.html');

  // Lida com os botões de "voltar" e "avançar" do navegador
  window.addEventListener('popstate', () => {
    let route = window.location.pathname.substring(1);
    console.log(route)
    if (route === '') route = 'home';
    loadPage(route + '.html');
  });
}
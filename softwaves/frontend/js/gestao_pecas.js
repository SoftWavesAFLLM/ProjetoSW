// gestao_pecas.js

// Variável global para armazenar a lista completa de peças, usada pelo filtro.
let todasAsPecas = [];

// --- FUNÇÕES DE MENSAGEM ---

/**
 * Exibe uma mensagem no modal de edição/criação de peças.
 * @param {string} texto - A mensagem a ser exibida.
 * @param {string} [tipo='danger'] - O tipo de alerta (ex: 'success', 'danger', 'warning').
 */
function mostrarMensagemModalPeca(texto, tipo = 'danger') {
  const mensagemDiv = document.getElementById('mensagemModalPeca');
  if (mensagemDiv) {
    mensagemDiv.textContent = texto;
    mensagemDiv.className = `alert alert-${tipo}`;
    mensagemDiv.classList.remove('d-none');
  } else {
    // Fallback caso o elemento de mensagem não exista
    alert(texto);
  }
}

/**
 * Limpa a mensagem no modal de edição/criação de peças.
 */
function limparMensagemModalPeca() {
  const mensagemDiv = document.getElementById('mensagemModalPeca');
  if (mensagemDiv) {
    mensagemDiv.classList.add('d-none');
    mensagemDiv.textContent = '';
  }
}

// --- FUNÇÕES DE RENDERIZAÇÃO E FILTRO ---

/**
 * Desenha as linhas da tabela de peças com base nos dados fornecidos.
 * @param {Array} pecasParaRenderizar - O array de peças a ser exibido na tabela.
 */
function renderizarTabelaPecas(pecasParaRenderizar) {
  const tbody = document.getElementById('tabelaPecas');
  if (!tbody) return;
  tbody.innerHTML = '';

  if (pecasParaRenderizar.length === 0) {
    tbody.innerHTML = '<tr><td colspan="5" class="text-center">Nenhum resultado encontrado.</td></tr>';
    return;
  }

  pecasParaRenderizar.forEach(peca => {
    const [idpeca, nome_pecas, codigo_pecas, quantidade] = peca;
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${idpeca}</td>
      <td>${nome_pecas}</td>
      <td>${codigo_pecas}</td>
      <td>${quantidade}</td>
      <td class="text-center">
        <button class="btn btn-primary btn-sm btn-editar" data-id="${idpeca}">✏️</button>
        <button class="btn btn-danger btn-sm btn-excluir" data-id="${idpeca}">🗑️</button>
      </td>
    `;
    tbody.appendChild(tr);
  });
}

/**
 * Filtra a lista de peças com base na coluna e valor selecionados e chama a renderização.
 */
function aplicarFiltro() {
  const colunaIndex = document.getElementById('colunaFiltroPecas').value;
  const valor = document.getElementById('filtroPecas').value.toLowerCase().trim();

  if (!valor) {
    renderizarTabelaPecas(todasAsPecas);
    return;
  }

  const pecasFiltradas = todasAsPecas.filter(peca => {
    const valorDaColuna = peca[colunaIndex] ? peca[colunaIndex].toString().toLowerCase() : '';
    return valorDaColuna.includes(valor);
  });

  renderizarTabelaPecas(pecasFiltradas);
}

// --- FUNÇÕES DE DADOS (API) ---

/**
 * Busca os dados das peças da API, armazena na variável global e renderiza a tabela.
 */
export async function carregarPecas() {
  const tbody = document.getElementById('tabelaPecas');
  if (!tbody) {
    console.warn('Elemento #tabelaPecas não encontrado.');
    return;
  }

  try {
    const response = await fetch('http://localhost:5000/api/peca');
    if (!response.ok) throw new Error(`Erro HTTP: ${response.status}`);
    const data = await response.json();
    todasAsPecas = data.dados || [];

    if (!Array.isArray(todasAsPecas)) throw new Error('Resposta da API inválida');

    renderizarTabelaPecas(todasAsPecas);
  } catch (error) {
    alert('Erro ao carregar peças: ' + error.message);
  }
}

// --- FUNÇÕES CRUD (INTERAÇÃO COM MODAIS) ---

/**
 * Abre o modal para edição, preenchendo os campos com os dados da peça selecionada.
 * @param {string|number} id - O ID da peça a ser editada.
 */
function abrirModalEdicao(id) {
  const tbody = document.getElementById('tabelaPecas');
  if (!tbody) return;

  const tr = document.querySelector(`#tabelaPecas .btn-editar[data-id="${id}"]`).closest('tr');
  if (!tr) return alert('Linha da peça não encontrada.');

  const cells = tr.querySelectorAll('td');

  document.getElementById('idpeca').value = cells[0].textContent.trim();
  document.getElementById('nomePeca').value = cells[1].textContent.trim();
  document.getElementById('codigoPeca').value = cells[2].textContent.trim();
  document.getElementById('quantidadePeca').value = cells[3].textContent.trim();

  document.getElementById('exampleModalPecaLabel').innerText = "Editar Peça";
  limparMensagemModalPeca();

  const modal = new bootstrap.Modal(document.getElementById('exampleModalPeca'));
  modal.show();
}

/**
 * Prepara e abre o modal de confirmação de exclusão.
 * @param {string|number} id - O ID da peça a ser excluída.
 */
function abrirModalExclusao(id) {
    const modalEl = document.getElementById('modalConfirmarExclusao');
    if (!modalEl) return;

    const corpoModal = modalEl.querySelector('#corpoModalExclusao');
    const mensagemDiv = modalEl.querySelector('#mensagemModalExclusao');
    const footer = modalEl.querySelector('.modal-footer');
    const btnConfirmar = modalEl.querySelector('#btnConfirmarExclusao');
    
    // 1. Reseta a UI para o estado inicial
    corpoModal.classList.remove('d-none');
    footer.classList.remove('d-none');
    mensagemDiv.classList.add('d-none');
    btnConfirmar.disabled = false;

    // 2. Armazena o ID no botão de confirmação para uso posterior
    btnConfirmar.dataset.id = id;
    
    // 3. Abre o modal
    const modal = new bootstrap.Modal(modalEl);
    modal.show();
}

/**
 * Executa a exclusão da peça, com feedback visual dentro do modal.
 * @param {string|number} id - O ID da peça a ser excluída.
 */
async function excluirPeca(id) {
    const modalEl = document.getElementById('modalConfirmarExclusao');
    if (!modalEl) return;

    const modalInstance = bootstrap.Modal.getInstance(modalEl);
    const corpoModal = modalEl.querySelector('#corpoModalExclusao');
    const mensagemDiv = modalEl.querySelector('#mensagemModalExclusao');
    const footer = modalEl.querySelector('.modal-footer');
    const btnConfirmar = modalEl.querySelector('#btnConfirmarExclusao');

    btnConfirmar.disabled = true;

    try {
        const response = await fetch(`http://localhost:5000/api/peca/${id}`, { method: 'DELETE' });
        const data = await response.json().catch(() => ({}));
        
        if (!response.ok || data.status === 'erro') {
            throw new Error(data.mensagem || 'Erro ao excluir peça');
        }

        corpoModal.classList.add('d-none');
        footer.classList.add('d-none');
        mensagemDiv.textContent = 'Peça excluída com sucesso!';
        mensagemDiv.className = 'alert alert-success mt-2';
        
        setTimeout(() => {
            if (modalInstance) modalInstance.hide();
            carregarPecas();
        }, 1500);

    } catch (error) {
        corpoModal.classList.add('d-none');
        footer.classList.add('d-none');
        mensagemDiv.textContent = `Erro: ${error.message}`;
        mensagemDiv.className = 'alert alert-danger mt-2';

        setTimeout(() => {
            if (modalInstance) modalInstance.hide();
        }, 2500);
    }
}

// --- FUNÇÃO DE INICIALIZAÇÃO ---

/**
 * Inicializa todos os event listeners da página.
 */
export function init() {
  const tbody = document.getElementById('tabelaPecas');
  const form = document.getElementById('formPeca');
  const inputFiltro = document.getElementById('filtroPecas');
  const selectColuna = document.getElementById('colunaFiltroPecas');
  const btnLimparFiltro = document.getElementById('limparFiltroPecas');
  const btnConfirmarExclusao = document.getElementById('btnConfirmarExclusao');

  if (!tbody || !form || !inputFiltro) {
    console.warn('Elementos essenciais para a inicialização não foram encontrados.');
    return;
  }

  // --- Event Listeners do Filtro ---
  inputFiltro.addEventListener('input', aplicarFiltro);
  selectColuna.addEventListener('change', aplicarFiltro);
  btnLimparFiltro.addEventListener('click', () => {
    inputFiltro.value = '';
    selectColuna.selectedIndex = 0;
    renderizarTabelaPecas(todasAsPecas);
  });

  // --- Event Listener da Tabela (para botões de Ação) ---
  tbody.addEventListener('click', (e) => {
    const btn = e.target.closest('button');
    if (!btn) return;
    const id = btn.dataset.id;
    if (btn.classList.contains('btn-editar')) {
      abrirModalEdicao(id);
    } else if (btn.classList.contains('btn-excluir')) {
      abrirModalExclusao(id);
    }
  });

  // --- Event Listener do Modal de Exclusão ---
  if (btnConfirmarExclusao) {
    btnConfirmarExclusao.addEventListener('click', () => {
      const id = btnConfirmarExclusao.dataset.id;
      if (id) {
        excluirPeca(id);
      }
    });
  }

  // --- Event Listener do Formulário de Adicionar/Editar ---
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const idpeca = document.getElementById('idpeca').value.trim();
    const dados = {
      nome_pecas: document.getElementById('nomePeca').value.trim(),
      codigo_pecas: document.getElementById('codigoPeca').value.trim(),
      quantidade: document.getElementById('quantidadePeca').value.trim()
    };
    const url = idpeca ? `http://localhost:5000/api/peca/${idpeca}` : 'http://localhost:5000/api/peca';
    const method = idpeca ? 'PUT' : 'POST';
    
    limparMensagemModalPeca();

    try {
      const response = await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(dados)
      });
      const resData = await response.json().catch(() => ({}));
      if (!response.ok || resData.status === 'erro') {
        throw new Error(resData.mensagem || 'Erro desconhecido ao salvar peça');
      }
      const mensagemSucesso = idpeca ? 'Peça atualizada com sucesso!' : 'Peça cadastrada com sucesso!';
      mostrarMensagemModalPeca(mensagemSucesso, 'success');
      
      await carregarPecas();
      
      setTimeout(() => {
        const modalEl = document.getElementById('exampleModalPeca');
        const modal = bootstrap.Modal.getInstance(modalEl);
        if (modal) modal.hide();
        limparMensagemModalPeca();
      }, 1500);

    } catch (error) {
      mostrarMensagemModalPeca('Erro: ' + error.message, 'danger');
    }
  });

  // --- Event Listener do Modal de Adicionar/Editar (para limpar o formulário) ---
  const modalPeca = document.getElementById('exampleModalPeca');
  if (modalPeca) {
    modalPeca.addEventListener('show.bs.modal', (e) => {
      // Limpa o formulário apenas se foi aberto pelo botão "Adicionar Peças"
      const botao = e.relatedTarget;
      if (botao && botao.dataset.bsTarget === `#${modalPeca.id}`) {
        form.reset();
        document.getElementById('idpeca').value = '';
        document.getElementById('exampleModalPecaLabel').innerText = "Adicionar Peça";
        limparMensagemModalPeca();
      }
    });
  }

  // Carga inicial dos dados
  carregarPecas();
}
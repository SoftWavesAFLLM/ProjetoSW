// gestao_manutencao.js (VERSÃO COMPLETA com modal de exclusão personalizado)

const API = 'http://localhost:5000/api/manutencao';

// Variável para armazenar todos os dados para o filtro
let todasAsManutencoes = [];

// --- FUNÇÕES DE MENSAGEM NO MODAL (sem alteração) ---
function mostrarMensagemModalManutencao(texto, tipo = 'danger') {
  const mensagemDiv = document.getElementById('mensagemModalManutencao');
  if (mensagemDiv) {
    mensagemDiv.textContent = texto;
    mensagemDiv.className = `alert alert-${tipo}`;
    mensagemDiv.classList.remove('d-none');
  } else {
    alert(texto);
  }
}

function limparMensagemModalManutencao() {
  const mensagemDiv = document.getElementById('mensagemModalManutencao');
  if (mensagemDiv) {
    mensagemDiv.classList.add('d-none');
    mensagemDiv.textContent = '';
  }
}

// --- FUNÇÃO PARA RENDERIZAR A TABELA (sem alteração) ---
function renderizarTabelaManutencao(manutencoesParaRenderizar) {
  const tbody = document.getElementById('tabelaManutencao');
  tbody.innerHTML = '';

  if (manutencoesParaRenderizar.length === 0) {
    tbody.innerHTML = '<tr><td colspan="7" class="text-center">Nenhum resultado encontrado.</td></tr>';
    return;
  }

  manutencoesParaRenderizar.forEach(m => {
    const row = document.createElement('tr');
    row.innerHTML = `
      <td>${m[0]}</td>
      <td>${m[1]}</td>
      <td>${m[2]}</td>
      <td>${m[3]}</td>
      <td>${m[4]}</td>
      <td>${m[5]}</td>
      <td class="text-nowrap">
        <button class="btn btn-primary btn-sm btn-editar" data-id="${m[0]}">✏️</button>
        <button class="btn btn-danger btn-sm btn-excluir" data-id="${m[0]}">🗑️</button>
      </td>
    `;
    tbody.appendChild(row);
  });
}

// --- FUNÇÃO QUE APLICA O FILTRO (sem alteração) ---
function aplicarFiltro() {
  const colunaIndex = document.getElementById('colunaFiltroManutencao').value;
  const valor = document.getElementById('filtroManutencao').value.toLowerCase().trim();

  if (!valor) {
    renderizarTabelaManutencao(todasAsManutencoes);
    return;
  }

  const manutencoesFiltradas = todasAsManutencoes.filter(m => {
    const valorDaColuna = m[colunaIndex] ? m[colunaIndex].toString().toLowerCase() : '';
    return valorDaColuna.includes(valor);
  });

  renderizarTabelaManutencao(manutencoesFiltradas);
}

// --- FUNÇÃO PARA CARREGAR DADOS DA API (sem alteração) ---
export async function carregarManutencoes() {
  try {
    const response = await fetch(API);
    if (!response.ok) throw new Error('Erro ao buscar manutenções');
    const data = await response.json();
    todasAsManutencoes = data.dados || [];
    renderizarTabelaManutencao(todasAsManutencoes);
  } catch (error) {
    console.error('Erro ao carregar manutenções:', error);
    alert('Erro ao carregar manutenções: ' + error.message);
  }
}

// --- Funções do CRUD (COM ALTERAÇÕES NA EXCLUSÃO) ---

function abrirModalEdicaoFromRow(btn) {
  const tr = btn.closest('tr');
  const cells = tr.querySelectorAll('td');
  document.getElementById('id_manutencao').value = cells[0].textContent.trim();
  document.getElementById('descricao_manutencao').value = cells[1].textContent.trim();
  document.getElementById('tipo_manutencao').value = cells[2].textContent.trim();
  document.getElementById('status_manutencao').value = cells[3].textContent.trim();
  document.getElementById('selectMaquina').value = cells[4].textContent.trim();
  document.getElementById('selectUsuario').value = cells[5].textContent.trim();
  document.getElementById('modalAdicionarManutencaoLabel').textContent = 'Editar Manutenção';
  limparMensagemModalManutencao();
  const modal = new bootstrap.Modal(document.getElementById('modalAdicionarManutencao'));
  modal.show();
}

// ===============================================================
// NOVO: Função para abrir e resetar o modal de confirmação de exclusão.
// ===============================================================
function abrirModalExclusaoManutencao(id) {
    const modalEl = document.getElementById('modalConfirmarExclusaoManutencao');
    if (!modalEl) return;

    const corpoModal = modalEl.querySelector('#corpoModalExclusaoManutencao');
    const mensagemDiv = modalEl.querySelector('#mensagemModalExclusaoManutencao');
    const footer = modalEl.querySelector('.modal-footer');
    const btnConfirmar = modalEl.querySelector('#btnConfirmarExclusaoManutencao');
    
    // Reseta a UI para o estado inicial
    corpoModal.classList.remove('d-none');
    footer.classList.remove('d-none');
    mensagemDiv.classList.add('d-none');
    btnConfirmar.disabled = false;

    // Armazena o ID no botão de confirmação
    btnConfirmar.dataset.id = id;
    
    // Abre o modal
    const modal = new bootstrap.Modal(modalEl);
    modal.show();
}


// ===============================================================
// MODIFICADO: Função de exclusão com feedback visual dentro do modal.
// ===============================================================
async function excluirManutencao(id) {
    const modalEl = document.getElementById('modalConfirmarExclusaoManutencao');
    if (!modalEl) return;

    const modalInstance = bootstrap.Modal.getInstance(modalEl);
    const corpoModal = modalEl.querySelector('#corpoModalExclusaoManutencao');
    const mensagemDiv = modalEl.querySelector('#mensagemModalExclusaoManutencao');
    const footer = modalEl.querySelector('.modal-footer');
    const btnConfirmar = modalEl.querySelector('#btnConfirmarExclusaoManutencao');

    btnConfirmar.disabled = true;

    try {
        const resp = await fetch(`${API}/${id}`, { method: 'DELETE' });
        const data = await resp.json().catch(() => ({}));
        if (!resp.ok || data.status === 'erro') {
            throw new Error(data.mensagem || 'Erro ao excluir manutenção');
        }

        // Feedback de SUCESSO
        corpoModal.classList.add('d-none');
        footer.classList.add('d-none');
        mensagemDiv.textContent = 'Manutenção excluída com sucesso!';
        mensagemDiv.className = 'alert alert-success mt-2';

        setTimeout(async () => {
            if (modalInstance) modalInstance.hide();
            await carregarManutencoes();
        }, 1500);

    } catch (err) {
        // Feedback de ERRO
        corpoModal.classList.add('d-none');
        footer.classList.add('d-none');
        mensagemDiv.textContent = 'Erro: ' + err.message;
        mensagemDiv.className = 'alert alert-danger mt-2';

        setTimeout(() => {
            if (modalInstance) modalInstance.hide();
        }, 2500);
    }
}


async function salvarManutencao(e) {
  e.preventDefault();
  const id = document.getElementById('id_manutencao').value.trim();
  const dados = {
    descricao_problema: document.getElementById('descricao_manutencao').value.trim(),
    tipo_manutencao: document.getElementById('tipo_manutencao').value.trim(),
    status_manutencao: document.getElementById('status_manutencao').value.trim(),
    maquinas_idmaquinas: document.getElementById('selectMaquina').value.trim(),
    usuarios_idusuario: document.getElementById('selectUsuario').value.trim()
  };
  const url = id ? `${API}/${id}` : API;
  const method = id ? 'PUT' : 'POST';
  
  limparMensagemModalManutencao();
  
  try {
    const response = await fetch(url, { method, headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(dados) });
    const data = await response.json().catch(() => ({}));
    if (!response.ok || data.status === 'erro') {
      throw new Error(data.mensagem || 'Erro ao salvar manutenção');
    }
    
    const msgSucesso = id ? 'Manutenção atualizada com sucesso!' : 'Manutenção cadastrada com sucesso!';
    mostrarMensagemModalManutencao(msgSucesso, 'success');
    
    await carregarManutencoes();
    
    setTimeout(() => {
      const modalEl = document.getElementById('modalAdicionarManutencao');
      const modal = bootstrap.Modal.getInstance(modalEl);
      if (modal) modal.hide();
      limparMensagemModalManutencao();
    }, 1500);
    
  } catch (error) {
    mostrarMensagemModalManutencao('Erro: ' + error.message, 'danger');
    console.error('Erro ao salvar manutenção:', error);
  }
}

// --- MODIFICADO: init() agora configura o novo modal de exclusão ---
export function init() {
  const tbody = document.getElementById('tabelaManutencao');
  const form = document.getElementById('formManutencao');
  const btnAdicionar = document.querySelector('[data-bs-target="#modalAdicionarManutencao"]');
  const inputFiltro = document.getElementById('filtroManutencao');
  const selectColuna = document.getElementById('colunaFiltroManutencao');
  const btnLimparFiltro = document.getElementById('limparFiltroManutencao');
  
  // NOVO: Botão de confirmação do modal de exclusão
  const btnConfirmarExclusao = document.getElementById('btnConfirmarExclusaoManutencao');

  if (!tbody || !form || !inputFiltro) {
    console.warn('Elementos da página de manutenção não encontrados.');
    return;
  }

  // Event listeners para o filtro
  inputFiltro.addEventListener('input', aplicarFiltro);
  selectColuna.addEventListener('change', aplicarFiltro);
  btnLimparFiltro.addEventListener('click', () => {
    inputFiltro.value = '';
    selectColuna.selectedIndex = 0;
    renderizarTabelaManutencao(todasAsManutencoes);
  });

  // ===============================================================
  // MODIFICADO: Evento de clique na tabela agora chama o novo modal.
  // ===============================================================
  tbody.addEventListener('click', (e) => {
    const btn = e.target.closest('button');
    if (!btn) return;
    const id = btn.dataset.id;
    if (btn.classList.contains('btn-editar')) {
      abrirModalEdicaoFromRow(btn);
    } else if (btn.classList.contains('btn-excluir')) {
      abrirModalExclusaoManutencao(id); // Alterado aqui!
    }
  });

  // ===============================================================
  // NOVO: Event listener para o botão de confirmação no modal de exclusão.
  // ===============================================================
  if (btnConfirmarExclusao) {
      btnConfirmarExclusao.addEventListener('click', () => {
          const id = btnConfirmarExclusao.dataset.id;
          if (id) {
              excluirManutencao(id);
          }
      });
  }

  // Reseta o modal de adicionar/editar ao abrir
  if (btnAdicionar) {
    btnAdicionar.addEventListener('click', () => {
      form.reset();
      document.getElementById('id_manutencao').value = '';
      document.getElementById('modalAdicionarManutencaoLabel').textContent = 'Adicionar Manutenção';
      limparMensagemModalManutencao();
    });
  }

  form.addEventListener('submit', salvarManutencao);

  carregarManutencoes(); // Carga inicial dos dados
}
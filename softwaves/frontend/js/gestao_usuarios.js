// gestao_usuarios.js

const API = 'http://localhost:5000/api/usuario';

// Variável para armazenar a lista completa de usuários
let todosOsUsuarios = [];

// --- FUNÇÕES DE RENDERIZAÇÃO E FILTRO ---

function renderizarTabelaUsuarios(usuariosParaRenderizar) {
  const tbody = document.getElementById('usersTablesBody');
  if (!tbody) return;
  tbody.innerHTML = '';

  if (usuariosParaRenderizar.length === 0) {
    tbody.innerHTML = '<tr><td colspan="8" class="text-center">Nenhum resultado encontrado.</td></tr>';
    return;
  }

  usuariosParaRenderizar.forEach(user => {
    const row = document.createElement('tr');
    row.innerHTML = `
      <td>${user[0]}</td>
      <td>${user[1]}</td>
      <td>${user[2]}</td>
      <td>${user[3]}</td>
      <td>${user[4]}</td>
      <td>${user[5]}</td>
      <td>•••••••••</td>
      <td class="text-nowrap">
        <button class="btn btn-primary btn-sm btn-editar" data-id="${user[0]}">✏️</button>
        <button class="btn btn-danger btn-sm btn-excluir" data-id="${user[0]}">🗑️</button>
      </td>
    `;
    tbody.appendChild(row);
  });
}

function aplicarFiltro() {
  const colunaIndex = document.getElementById('colunaFiltroUsuarios').value;
  const valor = document.getElementById('filtroUsuarios').value.toLowerCase().trim();

  if (!valor) {
    renderizarTabelaUsuarios(todosOsUsuarios);
    return;
  }

  const usuariosFiltrados = todosOsUsuarios.filter(user => {
    const valorDaColuna = user[colunaIndex] ? user[colunaIndex].toString().toLowerCase() : '';
    return valorDaColuna.includes(valor);
  });

  renderizarTabelaUsuarios(usuariosFiltrados);
}

// --- FUNÇÕES DE DADOS (API) E CRUD ---

export async function carregarUsuarios() {
  try {
    const response = await fetch(API);
    if (!response.ok) throw new Error('Erro ao buscar usuários');
    const data = await response.json();
    todosOsUsuarios = data.dados || [];
    renderizarTabelaUsuarios(todosOsUsuarios);
  } catch (error) {
    console.error('Erro ao carregar usuários:', error);
    alert('Erro ao carregar usuários: ' + error.message);
  }
}

function abrirModalEdicaoFromRow(btn) {
  const tr = btn.closest('tr');
  const cells = tr.querySelectorAll('td');

  document.getElementById('id_usuario').value = cells[0].textContent.trim();
  document.getElementById('nome_funcionario').value = cells[1].textContent.trim();
  document.getElementById('email').value = cells[2].textContent.trim();
  document.getElementById('CPF').value = cells[3].textContent.trim();
  document.getElementById('telefone').value = cells[4].textContent.trim();
  document.getElementById('funcao').value = cells[5].textContent.trim();
  document.getElementById('senha_funcionario').value = '';
  document.getElementById('senha_funcionario').required = false; // Senha não é obrigatória na edição

  document.getElementById('modalUsuarioLabel').textContent = 'Editar Usuário';
  limparMensagemModal();
  const modal = new bootstrap.Modal(document.getElementById('modalUsuario'));
  modal.show();
}

// ===============================================================
// NOVO: Função para abrir e resetar o modal de confirmação de exclusão.
// ===============================================================
function abrirModalExclusaoUsuario(id) {
    const modalEl = document.getElementById('modalConfirmarExclusaoUsuario');
    if (!modalEl) return;

    const corpoModal = modalEl.querySelector('#corpoModalExclusaoUsuario');
    const mensagemDiv = modalEl.querySelector('#mensagemModalExclusaoUsuario');
    const footer = modalEl.querySelector('.modal-footer');
    const btnConfirmar = modalEl.querySelector('#btnConfirmarExclusaoUsuario');
    
    // Reseta a UI para o estado inicial
    corpoModal.classList.remove('d-none');
    footer.classList.remove('d-none');
    mensagemDiv.classList.add('d-none');
    btnConfirmar.disabled = false;

    // Armazena o ID no botão
    btnConfirmar.dataset.id = id;
    
    // Abre o modal
    const modal = new bootstrap.Modal(modalEl);
    modal.show();
}

// ===============================================================
// MODIFICADO: Função de exclusão com feedback visual dentro do modal.
// ===============================================================
async function excluirUsuario(id) {
    const modalEl = document.getElementById('modalConfirmarExclusaoUsuario');
    if (!modalEl) return;

    const modalInstance = bootstrap.Modal.getInstance(modalEl);
    const corpoModal = modalEl.querySelector('#corpoModalExclusaoUsuario');
    const mensagemDiv = modalEl.querySelector('#mensagemModalExclusaoUsuario');
    const footer = modalEl.querySelector('.modal-footer');
    const btnConfirmar = modalEl.querySelector('#btnConfirmarExclusaoUsuario');

    btnConfirmar.disabled = true;

    try {
        const resp = await fetch(`${API}/${id}`, { method: 'DELETE' });
        const data = await resp.json().catch(() => ({}));
        if (!resp.ok || data.status === 'erro') {
            throw new Error(data.mensagem || 'Erro ao excluir usuário');
        }

        // Feedback de SUCESSO
        corpoModal.classList.add('d-none');
        footer.classList.add('d-none');
        mensagemDiv.textContent = 'Usuário excluído com sucesso!';
        mensagemDiv.className = 'alert alert-success mt-2';

        setTimeout(async () => {
            if (modalInstance) modalInstance.hide();
            await carregarUsuarios();
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

async function salvarUsuario(e) {
  e.preventDefault();

  const id = document.getElementById('id_usuario').value.trim();
  const senha_funcionario = document.getElementById('senha_funcionario').value.trim();

  const dados = {
    nome_usuario: document.getElementById('nome_funcionario').value.trim(),
    email: document.getElementById('email').value.trim(),
    cpf_cnpj: document.getElementById('CPF').value.trim(),
    telefone: document.getElementById('telefone').value.trim(),
    cargo: document.getElementById('funcao').value.trim(),
    senha: senha_funcionario,
  };

  const url = id ? `${API}/${id}` : API;
  const method = id ? 'PUT' : 'POST';

  limparMensagemModal();
  try {
    const response = await fetch(url, {
      method,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(dados),
    });
    const data = await response.json().catch(() => ({}));

    if (!response.ok || data.status === 'erro') {
      throw new Error(data.mensagem || 'Erro ao salvar usuário');
    }

    mostrarMensagemModal(id ? 'Usuário atualizado com sucesso!' : 'Usuário cadastrado com sucesso!', 'success');
    
    await carregarUsuarios();

    setTimeout(() => {
      const modal = bootstrap.Modal.getInstance(document.getElementById('modalUsuario'));
      if (modal) modal.hide();
    }, 1500);
  } catch (error) {
    mostrarMensagemModal('Erro: ' + error.message, 'danger');
  }
}

// --- FUNÇÕES DE MENSAGEM DO MODAL ADICIONAR/EDITAR ---
function mostrarMensagemModal(texto, tipo = 'danger') {
  const mensagemDiv = document.getElementById('mensagemAdicionarModal');
  if (mensagemDiv) {
    mensagemDiv.textContent = texto;
    mensagemDiv.className = `alert alert-${tipo}`;
    mensagemDiv.classList.remove('d-none');
  } else {
    alert(texto);
  }
}

function limparMensagemModal() {
  const mensagemDiv = document.getElementById('mensagemAdicionarModal');
  if (mensagemDiv) {
    mensagemDiv.classList.add('d-none');
    mensagemDiv.textContent = '';
  }
}

// --- FUNÇÃO DE INICIALIZAÇÃO ---
export function init() {
  const tbody = document.getElementById('usersTablesBody');
  const form = document.getElementById('formUsuario');
  const btnAbrirModalAdicionar = document.getElementById('btnAbrirModalAdicionar');
  
  const inputFiltro = document.getElementById('filtroUsuarios');
  const selectColuna = document.getElementById('colunaFiltroUsuarios');
  const btnLimparFiltro = document.getElementById('limparFiltroUsuarios');
  
  // NOVO: Botão de confirmação do modal de exclusão
  const btnConfirmarExclusao = document.getElementById('btnConfirmarExclusaoUsuario');

  if (!tbody || !form || !inputFiltro) {
    console.warn('Elementos da página de usuários não encontrados.');
    return;
  }
  
  // Event listeners para o filtro
  inputFiltro.addEventListener('input', aplicarFiltro);
  selectColuna.addEventListener('change', aplicarFiltro);
  btnLimparFiltro.addEventListener('click', () => {
      inputFiltro.value = '';
      selectColuna.selectedIndex = 0;
      renderizarTabelaUsuarios(todosOsUsuarios);
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
      abrirModalExclusaoUsuario(id); // Alterado aqui!
    }
  });

  // ===============================================================
  // NOVO: Event listener para o botão de confirmação no modal de exclusão.
  // ===============================================================
  if (btnConfirmarExclusao) {
      btnConfirmarExclusao.addEventListener('click', () => {
          const id = btnConfirmarExclusao.dataset.id;
          if (id) {
              excluirUsuario(id);
          }
      });
  }

  form.addEventListener('submit', salvarUsuario);

  if (btnAbrirModalAdicionar) {
    btnAbrirModalAdicionar.addEventListener('click', () => {
      form.reset();
      document.getElementById('id_usuario').value = '';
      document.getElementById('modalUsuarioLabel').textContent = 'Adicionar Usuário';
      document.getElementById('senha_funcionario').required = true; // Senha é obrigatória ao adicionar
      limparMensagemModal();
    });
  }

  carregarUsuarios();
}
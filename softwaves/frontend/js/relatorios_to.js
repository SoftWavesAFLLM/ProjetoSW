// relatorios_to.js (VERSÃO COMPLETA E FINAL)

// Variável para armazenar todos os dados já formatados
let todasAsOrdens = [];

// --- FUNÇÕES AUXILIARES DE DATA ---
function formatarDataVisual(dataISO) {
    if (!dataISO) return '';
    const dataObj = new Date(dataISO);
    if (isNaN(dataObj.getTime())) return '';
    
    const dia = String(dataObj.getUTCDate()).padStart(2, '0');
    const mes = String(dataObj.getUTCMonth() + 1).padStart(2, '0');
    const ano = dataObj.getUTCFullYear();
    
    return `${dia}/${mes}/${ano}`;
}

function formatarDataParaInput(dataBR) {
    if (!dataBR || !dataBR.includes('/')) return '';
    const [dia, mes, ano] = dataBR.split('/');
    return `${ano}-${mes.padStart(2, '0')}-${dia.padStart(2, '0')}`;
}

// --- FUNÇÕES DE MENSAGEM NO MODAL ---
function mostrarMensagemModalOrdem(texto, tipo = 'danger') {
    const mensagemDiv = document.getElementById('mensagemModalOrdem');
    if (mensagemDiv) {
        mensagemDiv.textContent = texto;
        mensagemDiv.className = `alert alert-${tipo}`;
        mensagemDiv.classList.remove('d-none');
    } else {
        alert(texto);
    }
}

function limparMensagemModalOrdem() {
    const mensagemDiv = document.getElementById('mensagemModalOrdem');
    if (mensagemDiv) {
        mensagemDiv.classList.add('d-none');
        mensagemDiv.textContent = '';
    }
}

// --- RENDERIZAÇÃO ---
function renderizarTabelaOrdens(ordensParaRenderizar) {
    const tbody = document.getElementById('tabelaOrdens');
    tbody.innerHTML = '';

    if (ordensParaRenderizar.length === 0) {
        tbody.innerHTML = '<tr><td colspan="9" class="text-center">Nenhum resultado encontrado.</td></tr>';
        return;
    }

    ordensParaRenderizar.forEach(ordem => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${ordem.idordens}</td>
            <td>${ordem.descricao_manutencao}</td>
            <td>${ordem.status_ordem}</td>
            <td>${ordem.tipo_manutencao}</td>
            <td>${formatarDataVisual(ordem.data_criacao)}</td>
            <td>${formatarDataVisual(ordem.data_conclusao)}</td>
            <td>${ordem.ordens_manutencao_idordens_manutencao}</td>
            <td>${ordem.usuarios_idusuario}</td>
            <td class="text-center">
                <button class="btn btn-primary btn-sm btn-editar" data-id="${ordem.idordens}">✏️</button>
                <button class="btn btn-danger btn-sm btn-excluir" data-id="${ordem.idordens}">🗑️</button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

// --- LÓGICA DE DADOS E API ---
async function carregarOrdens() {
    const tbody = document.getElementById('tabelaOrdens');
    try {
        const response = await fetch('http://localhost:5000/api/trabalho_ordens');
        if (!response.ok && response.status !== 201) {
            throw new Error(`Erro HTTP: ${response.status} - ${response.statusText}`);
        }
        
        const data = await response.json();
        const colunas = [
            'idordens', 'descricao_manutencao', 'status_ordem', 'tipo_manutencao',
            'data_criacao', 'data_conclusao', 'ordens_manutencao_idordens_manutencao',
            'usuarios_idusuario'
        ];
        const dadosArray = data.dados || [];
        const ordensFormatadas = dadosArray.map(linhaArray => {
            const objetoOrdem = {};
            colunas.forEach((nomeDaColuna, index) => {
                objetoOrdem[nomeDaColuna] = linhaArray[index];
            });
            return objetoOrdem;
        });
        
        todasAsOrdens = ordensFormatadas;
        renderizarTabelaOrdens(todasAsOrdens);
    } catch (error) {
        console.error('ERRO DETALHADO AO CARREGAR ORDENS:', error);
        tbody.innerHTML = `<tr><td colspan="9" class="text-center text-danger">Falha ao carregar dados. Verifique o console (F12). Causa: ${error.message}</td></tr>`;
    }
}

// --- FUNÇÃO DE FILTRO ---
function aplicarFiltro() {
    const coluna = document.getElementById('colunaFiltroOrdens').value;
    let ordensFiltradas = todasAsOrdens;

    if (coluna === 'data_criacao' || coluna === 'data_conclusao') {
        const dataInicioInput = document.getElementById('filtroDataInicio').value;
        const dataFimInput = document.getElementById('filtroDataFim').value;

        if (dataInicioInput || dataFimInput) {
            const timestampInicio = dataInicioInput ? new Date(dataInicioInput + 'T00:00:00Z').getTime() : null;
            const timestampFim = dataFimInput ? new Date(dataFimInput + 'T23:59:59Z').getTime() : null;

            ordensFiltradas = todasAsOrdens.filter(ordem => {
                const dataOrdemStr = ordem[coluna];
                if (!dataOrdemStr) return false;
                const timestampOrdem = new Date(dataOrdemStr).getTime();

                const atendeInicio = !timestampInicio || timestampOrdem >= timestampInicio;
                const atendeFim = !timestampFim || timestampOrdem <= timestampFim;

                return atendeInicio && atendeFim;
            });
        }
    } 
    else {
        const valor = document.getElementById('filtroOrdens').value.toLowerCase().trim();
        if (valor) {
            ordensFiltradas = todasAsOrdens.filter(ordem => {
                const valorDaColuna = ordem[coluna] ? ordem[coluna].toString().toLowerCase() : '';
                return valorDaColuna.includes(valor);
            });
        }
    }
    
    renderizarTabelaOrdens(ordensFiltradas);
}

// --- FUNÇÕES DO CRUD ---
function abrirModalEdicao(btn) {
    const id = btn.dataset.id;
    const ordem = todasAsOrdens.find(o => o.idordens == id);
    if (!ordem) return alert('Dados da ordem não encontrados.');

    document.getElementById('id_ordem').value = ordem.idordens;
    document.getElementById('descricao_manutencao').value = ordem.descricao_manutencao;
    document.getElementById('status_ordem').value = ordem.status_ordem;
    document.getElementById('tipo_manutencao').value = ordem.tipo_manutencao;
    document.getElementById('data_criacao').value = formatarDataParaInput(formatarDataVisual(ordem.data_criacao));
    document.getElementById('data_conclusao').value = formatarDataParaInput(formatarDataVisual(ordem.data_conclusao));
    document.getElementById('selectManutencao').value = ordem.ordens_manutencao_idordens_manutencao;
    document.getElementById('selectUsuario').value = ordem.usuarios_idusuario;

    document.getElementById('modalAdicionarOrdemLabel').textContent = 'Editar Ordem de Trabalho';
    limparMensagemModalOrdem();
    const modal = new bootstrap.Modal(document.getElementById('modalAdicionarOrdem'));
    modal.show();
}

function abrirModalExclusaoOrdem(id) {
    const modalEl = document.getElementById('modalConfirmarExclusaoOrdem');
    if (!modalEl) return;
    const btnConfirmar = modalEl.querySelector('#btnConfirmarExclusaoOrdem');
    btnConfirmar.dataset.id = id;
    const modal = new bootstrap.Modal(modalEl);
    modal.show();
}

async function excluirOrdem(id) {
    try {
        const response = await fetch(`http://localhost:5000/api/trabalho_ordens/${id}`, { method: 'DELETE' });
        const data = await response.json().catch(() => ({}));
        if (!response.ok || data.status === 'erro') {
            throw new Error(data.mensagem || 'Erro ao excluir ordem');
        }
        await carregarOrdens();
    } catch (error) {
        alert('Erro: ' + error.message);
    }
}

// --- FUNÇÃO DE INICIALIZAÇÃO (PONTO DE ENTRADA) ---
export function init() {
    console.log("JavaScript `relatorios_to.js` INICIADO");

    const tbody = document.getElementById('tabelaOrdens');
    const form = document.getElementById('formOrdem');
    const modalOrdem = document.getElementById('modalAdicionarOrdem');
    const selectColuna = document.getElementById('colunaFiltroOrdens');
    const filtroTextoContainer = document.getElementById('filtroTextoContainer');
    const filtroDataContainer = document.getElementById('filtroDataContainer');
    const inputFiltro = document.getElementById('filtroOrdens');
    const filtroDataInicio = document.getElementById('filtroDataInicio');
    const filtroDataFim = document.getElementById('filtroDataFim');
    const btnLimparFiltro = document.getElementById('limparFiltroOrdens');
    const btnConfirmarExclusao = document.getElementById('btnConfirmarExclusaoOrdem');

    // --- LISTENER DE EVENTOS CORRIGIDO ---
    selectColuna.addEventListener('change', () => {
        const valorSelecionado = selectColuna.value;
        if (valorSelecionado === 'data_criacao' || valorSelecionado === 'data_conclusao') {
            filtroTextoContainer.classList.add('d-none');
            filtroDataContainer.classList.remove('d-none');
        } else {
            filtroTextoContainer.classList.remove('d-none');
            filtroDataContainer.classList.add('d-none');
        }
        document.getElementById('filtroOrdens').value = '';
        document.getElementById('filtroDataInicio').value = '';
        document.getElementById('filtroDataFim').value = '';
        aplicarFiltro();
    });

    inputFiltro.addEventListener('input', aplicarFiltro);
    filtroDataInicio.addEventListener('change', aplicarFiltro);
    filtroDataFim.addEventListener('change', aplicarFiltro);
    
    btnLimparFiltro.addEventListener('click', () => {
        selectColuna.selectedIndex = 0;
        selectColuna.dispatchEvent(new Event('change')); // Simula a troca para resetar a UI
    });

    tbody.addEventListener('click', (e) => {
        const btn = e.target.closest('button');
        if (!btn) return;
        const id = btn.dataset.id;
        if (btn.classList.contains('btn-editar')) {
            abrirModalEdicao(btn);
        } else if (btn.classList.contains('btn-excluir')) {
            abrirModalExclusaoOrdem(id);
        }
    });
    
    if (btnConfirmarExclusao) {
        btnConfirmarExclusao.addEventListener('click', () => {
            const modalInstance = bootstrap.Modal.getInstance(document.getElementById('modalConfirmarExclusaoOrdem'));
            const id = btnConfirmarExclusao.dataset.id;
            if (id) {
                excluirOrdem(id).finally(() => { if (modalInstance) modalInstance.hide(); });
            }
        });
    }

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const id_ordem = document.getElementById('id_ordem').value.trim();
        const dados = {
            descricao_manutencao: document.getElementById('descricao_manutencao').value.trim(),
            status_ordem: document.getElementById('status_ordem').value,
            tipo_manutencao: document.getElementById('tipo_manutencao').value,
            data_criacao: document.getElementById('data_criacao').value,
            data_conclusao: document.getElementById('data_conclusao').value || null,
            ordens_manutencao_idordens_manutencao: parseInt(document.getElementById('selectManutencao').value, 10),
            usuarios_idusuario: parseInt(document.getElementById('selectUsuario').value, 10)
        };
        const url = id_ordem ? `http://localhost:5000/api/trabalho_ordens/${id_ordem}` : 'http://localhost:5000/api/trabalho_ordens';
        const method = id_ordem ? 'PUT' : 'POST';
        limparMensagemModalOrdem();
        try {
            const response = await fetch(url, {
                method,
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(dados)
            });
            const resData = await response.json().catch(() => ({}));
            if (!response.ok || resData.status === 'erro') {
                throw new Error(resData.mensagem || 'Erro desconhecido ao salvar ordem');
            }
            mostrarMensagemModalOrdem(id_ordem ? 'Ordem atualizada com sucesso!' : 'Ordem cadastrada com sucesso!', 'success');
            await carregarOrdens();
            setTimeout(() => {
                const modal = bootstrap.Modal.getInstance(modalOrdem);
                if (modal) modal.hide();
            }, 1500);
        } catch (error) {
            mostrarMensagemModalOrdem('Erro: ' + error.message, 'danger');
        }
    });

    modalOrdem.addEventListener('show.bs.modal', (e) => {
        const botao = e.relatedTarget;
        if (botao && !botao.classList.contains('btn-editar')) {
            form.reset();
            document.getElementById('id_ordem').value = '';
            document.getElementById('modalAdicionarOrdemLabel').textContent = 'Adicionar Ordem de Trabalho';
            limparMensagemModalOrdem();
        }
    });

    carregarOrdens();
}
// ========================
//  INICIALIZAÇÃO
// ========================

export function init() {
    loadMenu();
    listarMaquinas();
    configurarFiltro();
    configurarFormulario();

    const btnAbrirModal = document.getElementById('btnAbrirModalAdicionarMaquina');
    if (btnAbrirModal) {
        btnAbrirModal.addEventListener('click', () => {
            document.getElementById('formMaquina').reset();
            document.getElementById('id_maquina').value = '';
            document.getElementById('modalAdicionarMaquinaLabel').textContent = 'Adicionar Máquina';
            limparMensagemModalMaquina();
        });
    }

    const btnConfirmarExclusao = document.getElementById('btnConfirmarExclusaoMaquina');
    if (btnConfirmarExclusao) {
        btnConfirmarExclusao.addEventListener('click', () => {
            const id = btnConfirmarExclusao.dataset.id;
            if (id) excluirMaquina(id);
        });
    }
}

let maquinasCache = [];

// ========================
//  LISTAR MÁQUINAS
// ========================
async function listarMaquinas() {
    const tabela = document.getElementById("tabelaMaquinas");
    tabela.innerHTML = `<tr><td colspan="8" class="text-center">Carregando...</td></tr>`;

    try {
        const response = await fetch("http://127.0.0.1:5000/api/maquina");
        const data = await response.json();

        if (data.status !== "sucesso") {
            tabela.innerHTML = `<tr><td colspan="8" class="text-center text-danger">Erro ao carregar dados.</td></tr>`;
            return;
        }

        maquinasCache = data.maquinas;
        renderizarTabela(data.maquinas);

    } catch (err) {
        console.error(err);
        tabela.innerHTML = `<tr><td colspan="8" class="text-center text-danger">Falha ao conectar com API.</td></tr>`;
    }
}

function renderizarTabela(lista) {
    const tabela = document.getElementById("tabelaMaquinas");
    tabela.innerHTML = "";

    if (!lista || lista.length === 0) {
        tabela.innerHTML = '<tr><td colspan="8" class="text-center">Nenhum resultado encontrado.</td></tr>';
        return;
    }

    lista.forEach(maquina => {
        const tr = document.createElement("tr");

        let imagemHTML = `<span class="text-muted">Sem imagem</span>`;
        if (maquina.imagem) {
            imagemHTML = `<img src="${maquina.imagem}" data-img="${maquina.imagem}" alt="imagem" class="img-thumbnail" style="max-width: 70px; cursor: pointer;" onclick="visualizarImagem(this.dataset.img)">`;
        }

        tr.innerHTML = `
            <td>${maquina.idmaquinas}</td>
            <td>${maquina.nome_maquina}</td>
            <td>${maquina.localizacao}</td>
            <td>${maquina.status_maquina}</td>
            <td>${formatarDataBR(maquina.data_instalacao_maquina)}</td>
            <td>${maquina.fabricante}</td>
            <td>${imagemHTML}</td>
            <td>
                <button class="btn btn-primary btn-sm me-1 btn-editar" data-id="${maquina.idmaquinas}">✏️</button>
                <button class="btn btn-danger btn-sm btn-excluir" data-id="${maquina.idmaquinas}">🗑</button>
            </td>
        `;
        tabela.appendChild(tr);
    });

    // Eventos para editar/excluir
    tabela.querySelectorAll('.btn-editar').forEach(btn => 
        btn.addEventListener('click', () => abrirModalEdicao(btn.dataset.id))
    );

    // 🔥 CORREÇÃO AQUI
    tabela.querySelectorAll('.btn-excluir').forEach(btn => 
        btn.addEventListener('click', abrirModalExclusao)
    );
}


// ========================
//  FORMATAR DATA
// ========================
function formatarDataBR(dataISO) {
    if (!dataISO) return "";
    const partes = dataISO.split("-");
    return `${partes[2]}/${partes[1]}/${partes[0]}`;
}

// ========================
//  VISUALIZAR IMAGEM
// ========================
window.visualizarImagem = function (imgBase64) {
    const modalBody = document.getElementById("modalImagemBody");
    if (!imgBase64 || imgBase64 === "null") {
        modalBody.innerHTML = `<p class="text-center text-muted fs-5">Nenhuma imagem disponível.</p>`;
    } else {
        modalBody.innerHTML = `<img src="${imgBase64}" style="max-width: 100%; max-height: 80vh; border-radius: 6px;" class="img-fluid">`;
    }
    const modal = new bootstrap.Modal(document.getElementById("modalImagem"));
    modal.show();
};

// ========================
//  FORMULÁRIO
// ========================
function configurarFormulario() {
    document.getElementById("formMaquina").addEventListener("submit", salvarMaquina);
}

async function salvarMaquina(event) {
    event.preventDefault();
    limparMensagemModalMaquina();

    const form = document.getElementById("formMaquina");
    const id = document.getElementById("id_maquina").value;

    const fileInput = document.getElementById("imagem");
    let imagemBase64 = null;
    if (fileInput.files && fileInput.files[0]) {
        imagemBase64 = await converterImagemBase64(fileInput.files[0]);
    }

    const dados = {
        nome_maquina: document.getElementById("nome").value,
        localizacao: document.getElementById("localizacao").value,
        status_maquina: document.getElementById("status_maquina").value,
        data_instalacao_maquina: document.getElementById("data_instalacao_maquina").value,
        fabricante: document.getElementById("fabricante").value,
        imagem: imagemBase64
    };

    const url = id ? `http://127.0.0.1:5000/api/maquina/${id}` : "http://127.0.0.1:5000/api/maquina";
    const metodo = id ? "PUT" : "POST";

    try {
        const response = await fetch(url, {
            method: metodo,
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(dados)
        });
        const result = await response.json();

        if (result.status === "sucesso") {
            mostrarMensagemModalMaquina(id ? 'Máquina atualizada com sucesso!' : 'Máquina cadastrada com sucesso!', 'success');
            form.reset();
            listarMaquinas();

            setTimeout(() => {
                const modal = bootstrap.Modal.getInstance(document.getElementById("modalAdicionarMaquina"));
                if (modal) modal.hide();
                limparMensagemModalMaquina();
            }, 1500);
        } else {
            mostrarMensagemModalMaquina('Erro: ' + (result.mensagem || 'Não foi possível salvar a máquina'), 'danger');
        }
    } catch (err) {
        mostrarMensagemModalMaquina('Erro: ' + err.message, 'danger');
    }
}

// ========================
//  CONVERTER IMAGEM PARA BASE64
// ========================
function converterImagemBase64(arquivo) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => resolve(reader.result);
        reader.onerror = err => reject(err);
        reader.readAsDataURL(arquivo);
    });
}

// ========================
//  MENSAGENS DO MODAL
// ========================
function mostrarMensagemModalMaquina(texto, tipo = 'danger') {
    const div = document.getElementById('mensagemAdicionarModalMaquina');
    div.textContent = texto;
    div.className = `alert alert-${tipo}`;
    div.classList.remove('d-none');
}

function limparMensagemModalMaquina() {
    const div = document.getElementById('mensagemAdicionarModalMaquina');
    div.classList.add('d-none');
    div.textContent = '';
}

// ========================
//  EDITAR MÁQUINA
// ========================
function abrirModalEdicao(id) {
    const maquina = maquinasCache.find(m => m.idmaquinas == id);
    if (!maquina) return;

    document.getElementById('id_maquina').value = id;
    document.getElementById('nome').value = maquina.nome_maquina;
    document.getElementById('localizacao').value = maquina.localizacao;
    document.getElementById('status_maquina').value = maquina.status_maquina;
    document.getElementById('data_instalacao_maquina').value = maquina.data_instalacao_maquina;
    document.getElementById('fabricante').value = maquina.fabricante;

    document.getElementById('modalAdicionarMaquinaLabel').textContent = 'Editar Máquina';
    limparMensagemModalMaquina();

    const modal = new bootstrap.Modal(document.getElementById('modalAdicionarMaquina'));
    modal.show();
}

// ========================
//  EXCLUSÃO
// ========================
function abrirModalExclusao(event) {
    const id = event.target.dataset.id;
    const modalEl = document.getElementById('modalConfirmarExclusaoMaquina');
    const btnConfirm = document.getElementById('btnConfirmarExclusaoMaquina');

    btnConfirm.dataset.id = id;
    document.getElementById('corpoModalExclusaoMaquina').classList.remove('d-none');
    document.querySelector('#modalConfirmarExclusaoMaquina .modal-footer').classList.remove('d-none');
    document.getElementById('mensagemModalExclusaoMaquina').classList.add('d-none');

    const modal = new bootstrap.Modal(modalEl);
    modal.show();
}

async function excluirMaquina(id) {
    const modalEl = document.getElementById('modalConfirmarExclusaoMaquina');
    const btnConfirm = document.getElementById('btnConfirmarExclusaoMaquina');
    const corpo = document.getElementById('corpoModalExclusaoMaquina');
    const mensagemDiv = document.getElementById('mensagemModalExclusaoMaquina');
    const footer = modalEl.querySelector('.modal-footer');

    btnConfirm.disabled = true;

    try {
        const response = await fetch(`http://127.0.0.1:5000/api/maquina/${id}`, { method: 'DELETE' });
        const data = await response.json();

        if (data.status !== 'sucesso') throw new Error(data.mensagem || 'Erro ao excluir');

        // Sucesso
        corpo.classList.add('d-none');
        footer.classList.add('d-none');
        mensagemDiv.textContent = 'Máquina excluída com sucesso!';
        mensagemDiv.className = 'alert alert-success mt-2';
        mensagemDiv.classList.remove('d-none');

        setTimeout(() => {
            const modalInstance = bootstrap.Modal.getInstance(modalEl);
            if (modalInstance) modalInstance.hide();
            listarMaquinas();
        }, 1500);

    } catch (err) {
        mensagemDiv.textContent = 'Erro: ' + err.message;
        mensagemDiv.className = 'alert alert-danger mt-2';
        mensagemDiv.classList.remove('d-none');
    } finally {
        btnConfirm.disabled = false;
    }
}

// ========================
//  FILTRO
// ========================
function configurarFiltro() {
    const inputFiltro = document.getElementById('filtroMaquinas');
    const selectColuna = document.getElementById('colunaFiltroMaquinas');
    const btnLimpar = document.getElementById('limparFiltroMaquinas');

    inputFiltro.addEventListener('input', filtrarMaquinas);
    selectColuna.addEventListener('change', filtrarMaquinas);
    btnLimpar.addEventListener('click', () => {
        inputFiltro.value = '';
        filtrarMaquinas();
    });
}

function filtrarMaquinas() {
    const valor = document.getElementById('filtroMaquinas').value.toLowerCase();
    const coluna = document.getElementById('colunaFiltroMaquinas').value;

    const filtrados = maquinasCache.filter(m => {
        let campo = m[coluna] ? m[coluna].toString().toLowerCase() : '';
        return campo.includes(valor);
    });

    renderizarTabela(filtrados);
}

// ========================
//  INICIALIZAÇÃO
// ========================
init();

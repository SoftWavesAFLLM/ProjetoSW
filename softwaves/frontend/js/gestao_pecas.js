// ===========================================
//  CONFIGURAÇÃO BASE
// ===========================================
const API_PECAS = "http://127.0.0.1:5000/api/peca";
let pecasCache = [];

// ===========================================
//  INICIALIZAÇÃO
// ===========================================
window.addEventListener("DOMContentLoaded", () => {
    listarPecas();
    configurarFiltro();
    configurarFormulario();

    document.getElementById("btnAbrirModalAdicionarPecas").addEventListener("click", () => {
        document.getElementById("formPeca").reset();
        document.getElementById("idpecas").value = "";
        document.getElementById("exampleModalPecaLabel").textContent = "Adicionar Peça";
        limparMensagemModalPeca();
    });

    document.getElementById("btnConfirmarExclusao").addEventListener("click", () => {
        const id = document.getElementById("btnConfirmarExclusao").dataset.id;
        excluirPeca(id);
    });
});

// ===========================================
//  LISTAR PEÇAS
// ===========================================
async function listarPecas() {
    const tabela = document.getElementById("tabelaPecas");
    tabela.innerHTML = `<tr><td colspan="6" class="text-center">Carregando...</td></tr>`;

    try {
        const response = await fetch(API_PECAS);
        const data = await response.json();

        if (data.status !== "sucesso") {
            tabela.innerHTML = `<tr><td colspan="6" class="text-center text-danger">Erro ao carregar dados.</td></tr>`;
            return;
        }

        pecasCache = data.pecas;
        renderizarTabela(pecasCache);
        verificarEstoqueBaixo(pecasCache);

    } catch (err) {
        console.error(err);
        tabela.innerHTML = `<tr><td colspan="6" class="text-center text-danger">Falha ao conectar com a API.</td></tr>`;
    }
}

// ===========================================
//  RENDERIZAR TABELA
// ===========================================
function renderizarTabela(lista) {
    const tabela = document.getElementById("tabelaPecas");
    tabela.innerHTML = "";

    if (!lista.length) {
        tabela.innerHTML = `<tr><td colspan="6" class="text-center">Nenhum resultado encontrado.</td></tr>`;
        return;
    }

    lista.forEach(peca => {
        const estoqueBaixo = Number(peca.quantidade) <= 5 ? "table-danger" : "";

        const imgTag = peca.imagem
            ? `<img src="${peca.imagem}" class="img-thumbnail" style="max-width: 70px; cursor:pointer" onclick="visualizarImagem('${peca.imagem}')">`
            : `<span class="text-muted">Sem imagem</span>`;

        tabela.innerHTML += `
            <tr class="${estoqueBaixo}">
                <td>${peca.idpecas}</td>
                <td>${peca.nome_pecas}</td>
                <td>${peca.codigo_pecas}</td>
                <td>${peca.quantidade}</td>
                <td>${imgTag}</td>
                <td class="text-center">
                    <button class="btn btn-primary btn-sm" onclick="abrirModalEdicao(${peca.idpecas})">✏️</button>
                    <button class="btn btn-danger btn-sm" onclick="abrirModalExclusao(${peca.idpecas})">🗑</button>
                </td>
            </tr>
        `;
    });
}

// ===========================================
//  ALERTA DE ESTOQUE BAIXO
// ===========================================
function verificarEstoqueBaixo(lista) {
    const limite = 5;
    const alerta = document.getElementById("alertaEstoqueBaixo");

    const pecasBaixas = lista.filter(p => Number(p.quantidade) <= limite);

    if (pecasBaixas.length > 0) {
        alerta.textContent = `⚠️ Atenção: ${pecasBaixas.length} peça(s) com estoque baixo!`;
        alerta.classList.remove("d-none");
    } else {
        alerta.classList.add("d-none");
    }
}

// ===========================================
//  VISUALIZAR IMAGEM
// ===========================================
window.visualizarImagem = function (img) {
    const modalBody = document.getElementById("modalImagemBody");
    modalBody.innerHTML = `<img src="${img}" style="max-width:100%; max-height:80vh;">`;

    new bootstrap.Modal(document.getElementById("modalImagem")).show();
};

// ===========================================
//  FORMULÁRIO
// ===========================================
function configurarFormulario() {
    document.getElementById("formPeca").addEventListener("submit", salvarPeca);
}

async function salvarPeca(event) {
    event.preventDefault();
    limparMensagemModalPeca();

    const id = document.getElementById("idpecas").value;

    const nome = document.getElementById("nome_pecas").value;
    const codigo = document.getElementById("codigo_pecas").value;
    const quantidade = document.getElementById("quantidade").value;

    const fileInput = document.getElementById("imagem");
    let imagemBase64 = null;

    if (fileInput.files && fileInput.files[0]) {
        imagemBase64 = await converterImagemBase64(fileInput.files[0]);
    }

    const dados = {
        nome_pecas: nome,
        codigo_pecas: codigo,
        quantidade: quantidade,
        imagem: imagemBase64
    };

    const url = id ? `${API_PECAS}/${id}` : API_PECAS;
    const metodo = id ? "PUT" : "POST";

    try {
        const response = await fetch(url, {
            method: metodo,
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(dados)
        });

        const result = await response.json();

        if (result.status === "sucesso") {
            mostrarMensagemModalPeca("Salvo com sucesso!", "success");
            listarPecas();

            setTimeout(() => {
                bootstrap.Modal.getInstance(document.getElementById("exampleModalPeca")).hide();
            }, 1000);
        } else {
            mostrarMensagemModalPeca(result.mensagem || "Erro ao salvar", "danger");
        }

    } catch (err) {
        mostrarMensagemModalPeca("Erro: " + err.message, "danger");
    }
}

// ===========================================
//  CONVERTER IMAGEM PARA BASE64
// ===========================================
function converterImagemBase64(arquivo) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => resolve(reader.result);
        reader.onerror = err => reject(err);
        reader.readAsDataURL(arquivo);
    });
}

// ===========================================
//  MENSAGENS DO MODAL
// ===========================================
function mostrarMensagemModalPeca(texto, tipo = "danger") {
    const div = document.getElementById("mensagemModalPeca");
    div.textContent = texto;
    div.className = `alert alert-${tipo}`;
    div.classList.remove("d-none");
}

function limparMensagemModalPeca() {
    const div = document.getElementById("mensagemModalPeca");
    div.classList.add("d-none");
    div.textContent = "";
}

// ===========================================
//  EDITAR PEÇA
// ===========================================
window.abrirModalEdicao = function (id) {
    const peca = pecasCache.find(p => p.idpecas == id);

    document.getElementById("idpecas").value = peca.idpecas;
    document.getElementById("nome_pecas").value = peca.nome_pecas;
    document.getElementById("codigo_pecas").value = peca.codigo_pecas;
    document.getElementById("quantidade").value = peca.quantidade;

    document.getElementById("exampleModalPecaLabel").textContent = "Editar Peça";
    new bootstrap.Modal(document.getElementById("exampleModalPeca")).show();
};

// ===========================================
//  EXCLUSÃO
// ===========================================
window.abrirModalExclusao = function (id) {
    document.getElementById("btnConfirmarExclusao").dataset.id = id;
    document.getElementById("mensagemModalExclusao").classList.add("d-none");

    new bootstrap.Modal(document.getElementById("modalConfirmarExclusao")).show();
};

async function excluirPeca(id) {
    try {
        const response = await fetch(`${API_PECAS}/${id}`, {
            method: "DELETE"
        });

        const result = await response.json();

        if (result.status === "sucesso") {
            document.getElementById("mensagemModalExclusao").className = "alert alert-success";
            document.getElementById("mensagemModalExclusao").textContent = "Peça excluída!";
            document.getElementById("mensagemModalExclusao").classList.remove("d-none");

            listarPecas();

            setTimeout(() => {
                bootstrap.Modal.getInstance(document.getElementById("modalConfirmarExclusao")).hide();
            }, 1000);

        } else {
            throw new Error(result.mensagem);
        }

    } catch (err) {
        document.getElementById("mensagemModalExclusao").className = "alert alert-danger";
        document.getElementById("mensagemModalExclusao").textContent = "Erro: " + err.message;
        document.getElementById("mensagemModalExclusao").classList.remove("d-none");
    }
}

// ===========================================
//  FILTRO
// ===========================================
function configurarFiltro() {
    const filtro = document.getElementById("filtroPecas");
    const coluna = document.getElementById("colunaFiltroPecas");
    const limpar = document.getElementById("limparFiltroPecas");

    filtro.addEventListener("input", filtrarPecas);
    coluna.addEventListener("change", filtrarPecas);
    limpar.addEventListener("click", () => {
        filtro.value = "";
        filtrarPecas();
    });
}

function filtrarPecas() {
    const valor = document.getElementById("filtroPecas").value.toLowerCase();
    const coluna = document.getElementById("colunaFiltroPecas").value;

    const campo = {
        1: "nome_pecas",
        2: "codigo_pecas",
        3: "quantidade"
    };

    const lista = pecasCache.filter(p =>
        (p[campo[coluna]] || "").toString().toLowerCase().includes(valor)
    );

    renderizarTabela(lista);
    verificarEstoqueBaixo(lista);
}

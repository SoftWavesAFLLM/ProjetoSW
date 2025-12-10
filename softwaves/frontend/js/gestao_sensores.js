// =========================
// VARIÁVEIS GLOBAIS
// =========================
const API = "http://localhost:5000/api/sensor";
const API_GENERIC_SELECT = "http://localhost:5000/api/generic_select"; 
let sensoresCache = [];
let maquinaMap = {}; // Mapa ID -> Nome da Máquina para exibição e cache
let editandoSensorId = null;

// =========================
// INICIALIZAÇÃO
// =========================
document.addEventListener("DOMContentLoaded", () => {
    // 1. Carregar Máquinas (assíncrono)
    carregarMaquinas() 
        .then(() => {
            // 2. Listar Sensores (depende das máquinas)
            listarSensores();
        })
        .catch(error => {
            console.error("Falha na inicialização do sistema:", error);
        });
    
    // 3. Configurar listeners de formulário e filtros
    configurarFormulario();
    configurarFiltro();
    configurarEventosGlobais();
});

function configurarEventosGlobais() {
    const btnExcluir = document.getElementById("btnConfirmarExclusaoSensor");
    if (btnExcluir) {
        btnExcluir.addEventListener("click", confirmarExclusaoSensor);
    }



    // Listener para resetar o estado quando o modal de Adicionar/Editar é fechado
    const modalSensorEl = document.getElementById("exampleModal");
    if (modalSensorEl) {
        modalSensorEl.addEventListener('hidden.bs.modal', function () {
            document.getElementById("formSensor").reset();
            document.getElementById("exampleModalLabel").textContent = "Adicionar Sensor";
            limparMensagemSensor();
            editandoSensorId = null;
        });
    }
}

// =========================
// CARREGAR MÁQUINAS
// =========================
async function carregarMaquinas() {
    const select = document.getElementById("selectMaquina");
    
    try {
        const payload = {
            table: "maquinas",
            columns: "idmaquinas, nome_maquina",
            database: "softwavesafllm"
        };

        const response = await fetch(API_GENERIC_SELECT, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        const data = await response.json();
        maquinaMap = {}; // Reseta o mapa
        select.innerHTML = '<option value="">Selecione a máquina</option>';

        if (data.length === 0) {
            select.innerHTML = '<option value="">Nenhuma máquina encontrada</option>';
            return;
        }

        data.forEach(maquina => {
            maquinaMap[maquina.idmaquinas] = maquina.nome_maquina; 

            const option = document.createElement("option");
            option.value = maquina.idmaquinas;
            option.textContent = maquina.nome_maquina;
            select.appendChild(option);
        });
    } catch (error) {
        console.error("Erro ao carregar máquinas:", error);
        select.innerHTML = '<option value="">Erro ao carregar</option>';
        throw new Error("Erro de API ao carregar máquinas.");
    }
}

// =========================
// LISTAR E ATUALIZAR TABELA
// =========================
async function listarSensores() {
    try {
        const resposta = await fetch(API);
        const json = await resposta.json();

        if (json.status !== "sucesso" || !json.dados) {
            console.error("Erro ao listar sensores:", json);
            sensoresCache = [];
        } else {
            // Popula o cache com o nome da máquina para facilitar o filtro e a exibição
            sensoresCache = json.dados.map(sensor => ({
                ...sensor,
                nome_maquina: maquinaMap[sensor.maquinas_idmaquinas] || "N/A" 
            }));
        }
        
        atualizarTabelaSensores(sensoresCache);

    } catch (error) {
        console.error("Erro de rede ao listar sensores:", error);
        atualizarTabelaSensores([]);
    }
}

function atualizarTabelaSensores(dados) {
    const tabela = document.getElementById("tabelaSensores");
    tabela.innerHTML = "";

    if (!dados || dados.length === 0) {
        tabela.innerHTML = '<tr><td colspan="7" class="text-center">Nenhum resultado encontrado.</td></tr>';
        return;
    }

    dados.forEach(sensor => {
        const base64Img = sensor.imagem
            ? `data:image/jpeg;base64,${sensor.imagem}`
            : "https://via.placeholder.com/80x80?text=Sem+Imagem";

        const nomeMaquina = sensor.nome_maquina || "N/A"; 

        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${sensor.idsensores}</td>
            <td>${sensor.tipo_sensor}</td>
            <td>${sensor.descricao_sensor}</td>
            <td>${sensor.data_instalacao_sensor}</td>
            <td>${nomeMaquina}</td> 
            <td>
                <img src="${base64Img}" 
                    class="img-thumbnail"
                    style="width:80px; height:80px; cursor:pointer;"
                    onclick="abrirModalImagem('${base64Img}')">
            </td>
            <td>
                <button class="btn btn-sm btn-primary me-1" onclick="editarSensor(${sensor.idsensores})">✏️</button>
                <button class="btn btn-sm btn-danger" onclick="abrirModalExcluirSensor(${sensor.idsensores})">🗑️</button>
            </td>
        `;
        tabela.appendChild(tr);
    });
}

// =========================
// CRUD: SALVAR/EDITAR
// =========================
function configurarFormulario() {
    const form = document.getElementById("formSensor");
    if (!form) return;

    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        salvarSensor();
    });
}

async function salvarSensor() {
    limparMensagemSensor();

    const tipo = document.getElementById("tipo_sensor").value;
    const descricao = document.getElementById("descricao_sensor").value;
    const data_instalacao = document.getElementById("data_instalacao_sensor").value;
    const maquina_id = document.getElementById("selectMaquina").value;
    const inputImagem = document.getElementById("imagem");

    let base64Imagem = null;
    if (inputImagem && inputImagem.files.length > 0) {
        // Converte a imagem APENAS se um novo arquivo for selecionado
        base64Imagem = await converterImagemParaBase64(inputImagem.files[0]);
    }
    // Se estiver editando e não houver nova imagem, base64Imagem será null, 
    // e o backend deverá ignorar o campo ou manter o valor existente.

    const dados = {
        tipo_sensor: tipo,
        descricao_sensor: descricao,
        data_instalacao_sensor: data_instalacao,
        maquinas_idmaquinas: maquina_id,
        imagem: base64Imagem
    };

    const metodo = editandoSensorId ? "PUT" : "POST";
    const url = editandoSensorId ? `${API}/${editandoSensorId}` : API;

    try {
        const resposta = await fetch(url, {
            method: metodo,
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(dados)
        });
        const json = await resposta.json();

        if (json.status === "sucesso") {
            mostrarMensagemSensor(editandoSensorId ? "Sensor atualizado com sucesso!" : "Sensor cadastrado com sucesso!", "success");
            
            // Fecha o modal e reseta (listener 'hidden.bs.modal' faz o reset)
            const modal = bootstrap.Modal.getInstance(document.getElementById("exampleModal")); 
            if (modal) modal.hide(); 
            
            listarSensores(); // Recarrega a tabela

        } else {
            mostrarMensagemSensor("Erro ao salvar: " + (json.mensagem || "Erro desconhecido."), "danger");
        }
    } catch (error) {
        mostrarMensagemSensor("Erro ao salvar: " + error.message, "danger");
    }
}

window.editarSensor = function(id) {
    const sensor = sensoresCache.find(s => s.idsensores === id);
    if (!sensor) return;

    editandoSensorId = id;
    
    // 1. Preenche o formulário
    document.getElementById("tipo_sensor").value = sensor.tipo_sensor;
    document.getElementById("descricao_sensor").value = sensor.descricao_sensor;
    document.getElementById("data_instalacao_sensor").value = sensor.data_instalacao_sensor;
    document.getElementById("selectMaquina").value = sensor.maquinas_idmaquinas;
    
    // 2. Limpa o campo de arquivo para que o usuário não envie a imagem antiga sem querer
    document.getElementById("imagem").value = ""; 
    
    // 3. Atualiza o título do modal
    document.getElementById("exampleModalLabel").textContent = `Editar Sensor (ID: ${id})`;

    // 4. Abre o modal
    const modal = new bootstrap.Modal(document.getElementById("exampleModal"));
    modal.show();
}

// =========================
// CRUD: EXCLUIR (Revisada)
// =========================
window.abrirModalExcluirSensor = function(id) {
    const modalEl = document.getElementById("modalConfirmarExclusaoSensor");
    const modal = new bootstrap.Modal(modalEl);

    const btnConfirmar = document.getElementById("btnConfirmarExclusaoSensor");
    btnConfirmar.dataset.id = id;  // AQUI ESTÁ A CORREÇÃO

    const mensagemModal = document.getElementById("mensagemModalExclusaoSensor");
    mensagemModal.classList.add("d-none");
    mensagemModal.textContent = "";

    modal.show();
};


// =======================================================
// CONFIRMAR EXCLUSÃO (VERSÃO DE DEBUG MAIS DETALHADA)
// =======================================================
async function confirmarExclusaoSensor() {
    const id = this.dataset.id;
    const API_URL = `${API}/${id}`; // Exemplo: http://localhost:5000/api/sensor/123
    const mensagemModal = document.getElementById("mensagemModalExclusaoSensor");
    const btn = this;
    const modalInstance = bootstrap.Modal.getInstance(document.getElementById("modalConfirmarExclusaoSensor"));

    // Prepara a UI para o processamento
    btn.disabled = true;
    mensagemModal.classList.add("d-none");
    console.log(`[DELETE] Tentando excluir ID: ${id} na URL: ${API_URL}`);

    try {
        const resposta = await fetch(API_URL, { method: "DELETE" });

        // PASSO 1: Captura o Status HTTP
        console.log(`[DELETE] Status HTTP Recebido: ${resposta.status} ${resposta.statusText}`);

        // 🚨 BLOCO 1: TRATAMENTO DE FALHA DE STATUS HTTP (4xx ou 5xx)
        if (!resposta.ok) {
            let erroMensagem = `ERRO: Status HTTP ${resposta.status}.`;
            try {
                // Tenta ler o JSON de erro do backend para obter mais detalhes
                const jsonErro = await resposta.json();
                console.error("[DELETE] JSON de Erro do Servidor:", jsonErro);
                erroMensagem += ` Detalhe: ${jsonErro.mensagem || JSON.stringify(jsonErro)}`;
            } catch {
                // Se falhar a leitura do JSON, significa que não há corpo
                erroMensagem += " O servidor não retornou JSON de erro.";
            }
            throw new Error(erroMensagem);
        }
        
        // PASSO 2: Trata o sucesso (Status 2xx)
        let json = {};
        
        // Verifica se o servidor retornou 204 No Content (muito comum para DELETE sem corpo)
        if (resposta.status === 204) {
            console.log("[DELETE] Exclusão bem-sucedida (Status 204 No Content).");
            // Se for 204, pulamos a leitura do JSON, consideramos sucesso.
        } else {
            // Se for 200 OK ou 201 Created (espera-se um JSON)
            json = await resposta.json();
            console.log("[DELETE] JSON de Sucesso Recebido:", json);
        }

        // 🚨 BLOCO 2: VERIFICAÇÃO DE SUCESSO (Baseado no JSON ou no 204)
        if (json.status === "sucesso" || resposta.status === 204) {
            // SUCESSO!
            mensagemModal.textContent = "Sensor excluído com sucesso!";
            mensagemModal.className = "alert alert-success mt-2";
            mensagemModal.classList.remove("d-none");

            setTimeout(() => {
                listarSensores(); // Recarrega a tabela
                modalInstance.hide();
                btn.disabled = false;
            }, 1000);
            
        } else {
            // FALHA INTERNA (Servidor retornou 200, mas o JSON disse que falhou)
            throw new Error(json.mensagem || "Exclusão falhou (checagem interna do JSON).");
        }
        
    } catch (error) {
        // TRATAMENTO DE ERRO FINAL
        mensagemModal.textContent = "Falha na exclusão: " + error.message;
        mensagemModal.className = "alert alert-danger mt-2";
        mensagemModal.classList.remove("d-none");
        btn.disabled = false;
        console.error("ERRO FINAL:", error);
    }
}

// =========================
// FILTRO DINÂMICO
// =========================
function configurarFiltro() {
    const inputFiltro = document.getElementById("filtroSensores");
    const selectColuna = document.getElementById("colunaFiltroSensores");
    const btnLimpar = document.getElementById("limparFiltroSensores");
    const filtroTextoContainer = document.getElementById("filtroTextoContainer");
    const filtroDataContainer = document.getElementById("filtroDataContainer");
    const filtroDataInicio = document.getElementById("filtroDataInicio");
    const filtroDataFim = document.getElementById("filtroDataFim");

    if (!inputFiltro || !selectColuna || !btnLimpar) return;

    // Função para alternar a visibilidade dos campos de filtro (Texto vs Data)
    function alternarCamposFiltro() {
        const coluna = selectColuna.value;
        if (coluna === "data_instalacao_sensor") {
            filtroTextoContainer.classList.add("d-none");
            filtroDataContainer.classList.remove("d-none");
        } else {
            filtroTextoContainer.classList.remove("d-none");
            filtroDataContainer.classList.add("d-none");
        }
        aplicarFiltro();
    }

    // Função única para aplicar o filtro
    function aplicarFiltro() {
        const coluna = selectColuna.value;
        let filtrados = sensoresCache;

        if (coluna === "data_instalacao_sensor") {
            // Lógica de filtro por Data (Range)
            const inicio = filtroDataInicio.value;
            const fim = filtroDataFim.value;

            filtrados = sensoresCache.filter(sensor => {
                const dataSensor = sensor.data_instalacao_sensor; 
                let passaInicio = true;
                let passaFim = true;

                if (inicio) passaInicio = dataSensor >= inicio;
                if (fim) passaFim = dataSensor <= fim;
                
                return passaInicio && passaFim;
            });
            
        } else {
            // Lógica de filtro por Texto
            const valor = inputFiltro.value.toLowerCase().trim();
            
            filtrados = sensoresCache.filter(sensor => {
                let valorSensor;
                
                // Utiliza o campo correto para pesquisa
                if (coluna === "nome_maquina") {
                    valorSensor = String(sensor.nome_maquina || "").toLowerCase();
                } else {
                    valorSensor = String(sensor[coluna] || "").toLowerCase();
                }

                return valorSensor.includes(valor);
            });
        }
        
        atualizarTabelaSensores(filtrados);
    }

    // Eventos
    selectColuna.addEventListener("change", alternarCamposFiltro);
    inputFiltro.addEventListener("input", aplicarFiltro);
    filtroDataInicio.addEventListener("change", aplicarFiltro);
    filtroDataFim.addEventListener("change", aplicarFiltro);

    // Evento Limpar Filtro
    btnLimpar.addEventListener("click", () => {
        inputFiltro.value = "";
        filtroDataInicio.value = "";
        filtroDataFim.value = "";
        selectColuna.value = "tipo_sensor"; 
        alternarCamposFiltro(); 
        atualizarTabelaSensores(sensoresCache);
    });
}

// =========================
// FUNÇÕES AUXILIARES
// =========================
function converterImagemParaBase64(arquivo) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => {
            // Remove o prefixo "data:image/jpeg;base64," para enviar apenas o Base64 puro para a API
            const base64Data = reader.result.split(',')[1];
            resolve(base64Data);
        };
        reader.onerror = err => reject(err);
        reader.readAsDataURL(arquivo);
    });
}

window.abrirModalImagem = function(src) {
    const img = document.getElementById("imagemModal");
    if (!img) return;

    img.src = src;
    const modal = new bootstrap.Modal(document.getElementById("modalImagem"));
    modal.show();
};

function mostrarMensagemSensor(texto, tipo = "success") {
    const div = document.getElementById("mensagemFormularioSensor");
    if (!div) return;

    div.textContent = texto;
    div.className = `alert alert-${tipo} mt-2`;
    div.classList.remove("d-none");

    setTimeout(() => div.classList.add("d-none"), 3000);
}

function limparMensagemSensor() {
    const div = document.getElementById("mensagemFormularioSensor");
    if (div) {
        div.classList.add("d-none");
        div.textContent = "";
    }
}
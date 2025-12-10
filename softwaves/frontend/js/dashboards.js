// dashboards.js

let chartTemp, chartUmid, chartMov;

/**
 * Cria um gráfico de linha ou barra.
 */
function criarGrafico(ctx, label, cor, tipo = 'line') {
  return new Chart(ctx, {
    type: tipo,
    data: {
      labels: [],
      datasets: [{
        label,
        data: [],
        borderColor: cor,
        backgroundColor: tipo === 'bar' ? cor : 'transparent',
        borderWidth: 2,
        fill: false,
        tension: 0.2
      }]
    },
    options: {
      responsive: true,
      plugins: { legend: { labels: { color: 'black' } } },
      scales: {
        x: { ticks: { color: 'black' }, grid: { color: 'rgba(0,0,0,0.1)' } },
        y: { ticks: { color: 'black' }, grid: { color: 'rgba(0,0,0,0.1)' } }
      }
    }
  });
}

/**
 * Atualiza um gráfico com os dados do sensor.
 */
function atualizarGrafico(chart, dados, tipoSensor = 'valor') {
  chart.data.labels = dados.map(d => new Date(d.timestamp).toLocaleTimeString('pt-BR'));
  chart.data.datasets[0].data = dados.map(d => tipoSensor === 'valor' ? parseFloat(d.valor) : d.valor ? 1 : 0);
  chart.update();
}

/**
 * Pega o último valor de um sensor baseado no timestamp.
 */
function ultimoValor(dados, tipo) {
  const filtrados = dados.filter(d => d.tipo === tipo);
  if (filtrados.length === 0) return null;
  return filtrados.reduce((max, item) =>
    new Date(item.timestamp) > new Date(max.timestamp) ? item : max
  );
}

/**
 * Atualiza cards e gráficos com os dados do backend.
 */
export async function atualizarSensores() {
  try {
    const response = await fetch('http://localhost:5000/api/sensores');
    const dados = await response.json();

    // Pega últimos valores para os cards
    const tempUltimo = ultimoValor(dados, 'temperatura');
    const umidUltimo = ultimoValor(dados, 'umidade');
    const movUltimo = ultimoValor(dados, 'movimento');

    // Atualiza cards
    document.getElementById('temp').textContent = tempUltimo?.valor !== undefined ? `${tempUltimo.valor} °C` : '-- °C';
    document.getElementById('umid').textContent = umidUltimo?.valor !== undefined ? `${umidUltimo.valor} %` : '-- %';
    document.getElementById('movimento').textContent = movUltimo?.valor ? 'Detectado' : 'Nenhum';


    // Atualiza gráficos com todos os dados
    const tempDados = dados.filter(d => d.tipo === 'temperatura');
    const umidDados = dados.filter(d => d.tipo === 'umidade');
    const movDados = dados.filter(d => d.tipo === 'movimento');

    atualizarGrafico(chartTemp, tempDados);
    atualizarGrafico(chartUmid, umidDados);
    atualizarGrafico(chartMov, movDados, 'movimento');

  } catch (erro) {
    console.error('Erro ao carregar sensores:', erro);
  }
}

/**
 * Inicializa dashboards e gráficos.
 */
export function carregarDashboards() {
  chartTemp = criarGrafico(document.getElementById('graficoTemp'), 'Temperatura (°C)', 'red');
  chartUmid = criarGrafico(document.getElementById('graficoUmid'), 'Umidade (%)', 'blue');
  chartMov = criarGrafico(document.getElementById('graficoMov'), 'Movimento', 'green', 'bar');

  // Atualiza imediatamente e depois a cada 2 segundos
  atualizarSensores();
  setInterval(atualizarSensores, 2000);
}

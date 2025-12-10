// login.js (versão combinada)
const loginForm = document.getElementById('loginForm');

if (!loginForm) {
  // nada a fazer
  console.warn("loginForm não encontrado");
} else if (document.getElementById('senha')) {
  // --- TELA DE LOGIN ---
  loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const email = document.getElementById('email').value.trim();
    const senha = document.getElementById('senha').value.trim();
    const mensagem = document.getElementById('mensagem');

    try {
      const res = await fetch("http://localhost:5000/api/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, senha })
      });
      const data = await res.json();
      if (res.ok && data.success) {
        localStorage.setItem("usuarioLogado", JSON.stringify(data.usuario));
        localStorage.setItem('cargoLogado', JSON.stringify(data.cargo));
        if (mensagem) { mensagem.textContent = data.message || "Login ok"; mensagem.style.color = "green"; }
        setTimeout(()=> window.location.href = "inicial.html", 800);
      } else {
        if (mensagem) { mensagem.textContent = data.error || "E-mail ou senha inválidos."; mensagem.style.color = "white"; }
      }
    } catch (err) {
      console.error(err);
      if (mensagem) { mensagem.textContent = "Erro ao conectar com o servidor."; mensagem.style.color = "white"; }
    }
  });
} else {
  // --- TELA DE RECUPERAÇÃO (somente e-mail) ---
  loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const email = document.getElementById('email').value.trim();
    if (!email) { alert("Digite um e-mail válido."); return; }

    try {
      const res = await fetch("http://localhost:5000/api/auth/recuperar-senha", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email })
      });
      const data = await res.json();
      if (res.ok) {
        alert("Se o e-mail existir, enviamos instruções para redefinir sua senha.");
      } else {
        alert(data.message || "Erro ao processar pedido.");
      }
    } catch (err) {
      console.error(err);
      alert("Erro ao conectar com o servidor.");
    }
  });
}

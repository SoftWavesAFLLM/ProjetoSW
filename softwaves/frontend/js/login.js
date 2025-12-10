document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const email = document.getElementById('email').value.trim();
    const senha = document.getElementById('senha').value.trim();

    try {
        const response = await fetch("http://localhost:5000/api/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, senha })
        });

        const data = await response.json();
        console.log("Front:", data);

        const mensagem = document.getElementById('mensagem');

        if (response.ok && data.success) {

    // Salva o USUÁRIO COMPLETO
    localStorage.setItem("usuarioLogado", JSON.stringify(data.usuario));
    localStorage.setItem('cargoLogado', JSON.stringify(data.cargo))

    mensagem.textContent = data.message || "Login realizado com sucesso!";
    mensagem.style.color = "green";

    setTimeout(() => {
        window.location.href = "inicial.html";
    }, 1000);
}

         else {
            mensagem.textContent = data.error || "E-mail ou senha inválidos.";
            mensagem.style.color = "white";
        }
    } catch (error) {
        console.error("Erro ao logar:", error);
        const mensagem = document.getElementById('mensagem');
        mensagem.textContent = "Erro ao conectar com o servidor.";
        mensagem.style.color = "white";
    }
});

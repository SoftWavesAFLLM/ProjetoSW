const express = require('express');
const path = require('path');
const app = express();
const PORT = 3000;

// Servir arquivos estáticos (js, css, imagens etc)
app.use('/js', express.static(path.join(__dirname, 'js')));
app.use('/css', express.static(path.join(__dirname, 'css')));
app.use('/view', express.static(path.join(__dirname, 'view')));
app.use('/components', express.static(path.join(__dirname, 'components')));
app.use('/node_modules', express.static(path.join(__dirname, 'node_modules')));
app.use('/imagens', express.static(path.join(__dirname, 'imagens')));


// Rota SPA - serve index.html só se não for arquivo com extensão
app.get(/^\/(?!js|css|view|components|node_modules|imagens)([^.]*)$/, (req, res) => {
  res.sendFile(path.join(__dirname, 'view', 'index.html'));
});
/*app.get(/^\/[^.]*$/, (req, res) => {
  res.sendFile(path.join(__dirname, 'view', 'index.html'));
}); */
// Rota SPA


app.listen(PORT, () => {
  console.log(`Servidor rodando em http://localhost:${PORT}`);
});

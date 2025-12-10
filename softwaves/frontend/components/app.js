import { loadMenu } from './menu.js';
import { initSPA } from './main.js';

document.addEventListener('DOMContentLoaded', () => {
  loadMenu();
  initSPA();  // já carrega home.html no initSPA automaticamente
});

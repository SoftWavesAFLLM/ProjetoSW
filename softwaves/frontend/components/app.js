import { loadMenu } from './menu.js';
import { initSPA } from './main.js';

document.addEventListener('DOMContentLoaded', () => {
  
  initSPA();  // já carrega home.html no initSPA automaticamente
  loadMenu();
});

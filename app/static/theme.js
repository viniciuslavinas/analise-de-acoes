const themes = {
  sage: {ink:'#16231e', paper:'#f6f4ed', line:'#d9ddd2', lime:'#ccfa65', green:'#167150', red:'#b34b43'},
  ocean: {ink:'#102635', paper:'#f2f7f8', line:'#cfdee2', lime:'#7ce6d0', green:'#19788c', red:'#b3474f'},
  plum: {ink:'#2b1c32', paper:'#f8f3f6', line:'#e1d7de', lime:'#e7b7f5', green:'#79538b', red:'#b34662'},
  sun: {ink:'#302718', paper:'#fbf7ed', line:'#e4dac4', lime:'#f7da70', green:'#9b6823', red:'#b24b35'}
};
function applyTheme(name) { const theme = themes[name] || themes.sage; Object.entries(theme).forEach(([key, value]) => document.documentElement.style.setProperty(`--${key}`, value)); localStorage.setItem('site-theme', name); }
applyTheme(localStorage.getItem('site-theme') || 'sage');
const themeDialog = document.querySelector('#theme-dialog');
document.querySelector('#open-theme').onclick = () => themeDialog.showModal();
document.querySelector('#close-theme').onclick = () => themeDialog.close();
document.querySelectorAll('[data-theme]').forEach(button => button.onclick = () => { applyTheme(button.dataset.theme); themeDialog.close(); });

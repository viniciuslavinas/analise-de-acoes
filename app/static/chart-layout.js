const comparison = document.querySelector('#chart');
if (comparison) {
  const values = [['Preço atual', Number(comparison.dataset.price)], ['DCF', Number(comparison.dataset.dcf)], ['DDM', Number(comparison.dataset.ddm)], ['Múltiplos', Number(comparison.dataset.multiple)]];
  const maximum = Math.max(...values.map(([, value]) => value), 1);
  comparison.innerHTML = values.map(([name, value]) => `<div class="comparison-row"><label>${name}</label><div class="comparison-track"><i style="width:${Math.max(value / maximum * 100, 2)}%"></i></div><strong>R$ ${value.toFixed(2)}</strong></div>`).join('');
}

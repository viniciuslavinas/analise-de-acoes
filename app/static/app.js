const chart = document.querySelector('#chart');
if (chart) {
  const values = [['Preço', +chart.dataset.price], ['DCF', +chart.dataset.dcf], ['DDM', +chart.dataset.ddm], ['Múltiplos', +chart.dataset.multiple]];
  const max = Math.max(...values.map(([, value]) => value), 1);
  values.forEach(([name, value]) => { const bar = document.createElement('div'); bar.className = 'bar'; bar.style.height = `${Math.max(value / max * 170, 5)}px`; bar.innerHTML = `<span>R$ ${value.toFixed(2)}</span><label>${name}</label>`; chart.append(bar); });
  const form = document.querySelector('#simulator'), result = document.querySelector('#simulation-result');
  const refreshOutputs = () => form.querySelectorAll('input[type=range]').forEach(input => document.querySelector(`#${input.name.replace('revenue_growth','growth').replace('ebit_margin','margin')}-out`).textContent = `${input.value}%`);
  refreshOutputs(); form.addEventListener('input', refreshOutputs);
  form.addEventListener('submit', async event => { event.preventDefault(); const raw = Object.fromEntries(new FormData(form)); const payload = Object.fromEntries(Object.entries(raw).map(([k,v]) => [k, +v / (k === 'payout_growth' ? 1 : 100)])); result.textContent = 'Calculando…'; const response = await fetch(`/api/acoes/${window.TICKER}/simular`, {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(payload)}); const data = await response.json(); result.textContent = response.ok ? `DCF simulado: R$ ${data.dcf.per_share.toFixed(2)} · Margem de segurança: ${(data.safety_margin*100).toFixed(1)}%` : data.detail; });
}

const dialog = document.querySelector('#add-dialog');
if (dialog) {
  document.querySelector('#open-add').onclick = () => dialog.showModal();
  document.querySelector('#close-add').onclick = () => dialog.close();
  document.querySelector('#add-company').addEventListener('submit', async event => {
    event.preventDefault();
    const form = event.currentTarget, error = document.querySelector('#add-error');
    const percentage = new Set(['ebit_margin', 'tax_rate', 'revenue_growth', 'terminal_growth', 'wacc', 'cost_of_equity']);
    const payload = Object.fromEntries([...new FormData(form)].map(([key, value]) => [key, percentage.has(key) ? Number(value) / 100 : (key === 'ticker' || key === 'name' || key === 'sector' ? value : Number(value))]));
    error.textContent = 'Salvando…';
    const response = await fetch('/api/acoes', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(payload)});
    const data = await response.json();
    if (response.ok) window.location.href = `/acoes/${data.ticker}`;
    else error.textContent = data.detail || 'Não foi possível cadastrar a ação.';
  });
}

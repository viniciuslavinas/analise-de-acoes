const addForm = document.querySelector('#add-company');
if (addForm) {
  addForm.insertAdjacentHTML('afterbegin', `
    <section class="ticker-import">
      <h3>Buscar automaticamente</h3>
      <p>Informe somente o ticker da B3. Vamos buscar cotação e os dados financeiros disponíveis.</p>
      <div><input id="ticker-only" placeholder="Ex.: PETR4" maxlength="8"><button type="button" id="import-ticker">Buscar e adicionar</button></div>
      <p id="import-status" class="error"></p>
    </section>`);
  document.querySelector('#import-ticker').onclick = async () => {
    const ticker = document.querySelector('#ticker-only').value.trim().toUpperCase();
    const status = document.querySelector('#import-status');
    if (!ticker) { status.textContent = 'Digite o ticker da ação, por exemplo: PETR4.'; return; }
    status.textContent = 'Buscando dados financeiros…';
    const response = await fetch(`/api/acoes/importar/${encodeURIComponent(ticker)}`, {method: 'POST'});
    const data = await response.json();
    if (response.ok) window.location.href = `/acoes/${data.ticker}`;
    else status.textContent = data.detail || 'Não foi possível buscar esta ação.';
  };
}

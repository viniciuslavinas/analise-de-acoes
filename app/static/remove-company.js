const removeButton = document.querySelector('.remove-button');
if (removeButton) removeButton.onclick = async () => {
  const ticker = removeButton.dataset.ticker;
  if (!confirm(`Remover ${ticker} do radar? Esta ação poderá ser adicionada novamente depois.`)) return;
  removeButton.textContent = 'Removendo…';
  const response = await fetch(`/api/acoes/${ticker}`, {method: 'DELETE'});
  if (response.ok) window.location.href = '/';
  else { alert('Não foi possível remover a ação.'); removeButton.textContent = 'Remover ação'; }
};

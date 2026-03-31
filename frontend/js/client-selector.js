/**
 * Componente de selecao de clientes na sidebar.
 */
const ClientSelector = {
  clients: [],
  filteredClients: [],
  selectedClientId: null,
  currentFilter: 'all',

  async init() {
    this.clients = await API.listClients();
    this.filteredClients = [...this.clients];
    this.render();
    this.setupEvents();
  },

  setupEvents() {
    const searchInput = document.getElementById('clientSearch');
    if (searchInput) {
      searchInput.addEventListener('input', () => this.applyFilters());
    }
  },

  setFilter(filter) {
    this.currentFilter = filter;
    document.querySelectorAll('.filter-chip').forEach(chip => {
      chip.classList.toggle('active', chip.dataset.filter === filter);
    });
    this.applyFilters();
  },

  applyFilters() {
    const search = (document.getElementById('clientSearch')?.value || '').toLowerCase();

    this.filteredClients = this.clients.filter(c => {
      const matchFilter = this.currentFilter === 'all' || c.status === this.currentFilter;
      const matchSearch = !search ||
        c.nome.toLowerCase().includes(search) ||
        (c.sintese || '').toLowerCase().includes(search);
      return matchFilter && matchSearch;
    });

    this.renderList();
  },

  getInitials(name) {
    return name.split(/\s+/)
      .filter(w => w.length > 2 || w === w.toUpperCase())
      .slice(0, 2)
      .map(w => w[0].toUpperCase())
      .join('');
  },

  async selectClient(clientId) {
    this.selectedClientId = clientId;
    const client = this.clients.find(c => c.id === clientId);

    // Atualizar visual
    document.querySelectorAll('.client-item').forEach(item => {
      item.classList.toggle('selected', parseInt(item.dataset.id) === clientId);
    });

    // Atualizar header
    const badge = document.getElementById('activeClientBadge');
    if (badge && client) {
      badge.querySelector('.client-badge-name').textContent = client.nome;
      badge.querySelector('.client-status-dot').className =
        `client-status-dot ${client.status === 'Ativa' ? 'ativa' : 'encerrada'}`;
      badge.querySelector('.client-badge-count').textContent = `${client.peticoes} peticoes`;
      badge.classList.add('visible');
    }

    // Criar conversa se necessario
    await Chat.onClientSelected(client);

    // Fechar sidebar no mobile
    document.querySelector('.sidebar')?.classList.remove('open');
    document.querySelector('.sidebar-overlay')?.classList.remove('open');
  },

  render() {
    this.renderList();
  },

  renderList() {
    const container = document.getElementById('clientList');
    if (!container) return;

    if (!this.filteredClients.length) {
      container.innerHTML = '<div style="text-align:center;padding:20px;color:var(--texto-leve);font-size:0.86rem">Nenhum cliente encontrado</div>';
      return;
    }

    container.innerHTML = this.filteredClients.map(c => `
      <div class="client-item ${c.id === this.selectedClientId ? 'selected' : ''}"
           data-id="${c.id}"
           onclick="ClientSelector.selectClient(${c.id})">
        <div class="client-avatar">${this.getInitials(c.nome)}</div>
        <div class="client-info">
          <div class="client-name">${c.nome}</div>
          <div class="client-meta">
            <span class="client-status-dot ${c.status === 'Ativa' ? 'ativa' : 'encerrada'}"></span>
            <span>${c.status}</span>
            <span class="client-pet-badge">${c.peticoes}</span>
          </div>
        </div>
      </div>
    `).join('');
  },

  async loadConversations() {
    const container = document.getElementById('convList');
    if (!container) return;

    const params = {};
    if (this.selectedClientId) {
      params.client_id = this.selectedClientId;
    }
    params.limit = 20;

    const convs = await API.listConversations(params);

    if (!convs.length) {
      container.innerHTML = '<div style="padding:8px 16px;font-size:0.82rem;color:var(--texto-leve)">Sem conversas recentes</div>';
      return;
    }

    container.innerHTML = convs.map(c => `
      <div class="conv-item" onclick="Chat.loadConversation(${c.id})">
        <span class="conv-icon">\uD83D\uDCAC</span>
        <span class="conv-title">${c.title || 'Nova conversa'}</span>
      </div>
    `).join('');
  },
};

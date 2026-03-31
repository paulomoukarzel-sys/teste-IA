/**
 * Helpers para chamadas HTTP ao backend.
 */
const API = {
  base: '',

  async get(path) {
    const res = await fetch(`${this.base}${path}`);
    return res.json();
  },

  async post(path, data) {
    const res = await fetch(`${this.base}${path}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    return res.json();
  },

  async put(path, data) {
    const res = await fetch(`${this.base}${path}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    return res.json();
  },

  async del(path) {
    const res = await fetch(`${this.base}${path}`, { method: 'DELETE' });
    return res.json();
  },

  // Clientes
  async listClients(params = {}) {
    const qs = new URLSearchParams(params).toString();
    return this.get(`/api/clients${qs ? '?' + qs : ''}`);
  },

  async getClient(id) {
    return this.get(`/api/clients/${id}`);
  },

  async syncClients() {
    return this.get('/api/clients/sync');
  },

  // Conversas
  async listConversations(params = {}) {
    const qs = new URLSearchParams(params).toString();
    return this.get(`/api/conversations${qs ? '?' + qs : ''}`);
  },

  async createConversation(data) {
    return this.post('/api/conversations', data);
  },

  async getConversation(id) {
    return this.get(`/api/conversations/${id}`);
  },

  async deleteConversation(id) {
    return this.del(`/api/conversations/${id}`);
  },

  // Documentos
  async generateDocument(data) {
    return this.post('/api/documents/generate', data);
  },

  async getDocumentPreview(id) {
    return this.get(`/api/documents/${id}/preview`);
  },

  getDocumentDownloadUrl(id) {
    return `${this.base}/api/documents/${id}/download`;
  },

  // Dashboard
  async getDashboardStats() {
    return this.get('/api/dashboard/stats');
  },

  async getTopClients(limit = 15) {
    return this.get(`/api/dashboard/top-clients?limit=${limit}`);
  },

  async getPetitionTypes() {
    return this.get('/api/dashboard/petition-types');
  },
};

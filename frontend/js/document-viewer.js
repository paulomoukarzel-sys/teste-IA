/**
 * Painel de preview de documentos (slide-in).
 */
const DocumentViewer = {
  open(content, title) {
    const panel = document.getElementById('docPanel');
    const overlay = document.getElementById('docPanelOverlay');
    const body = document.getElementById('docPanelBody');
    const headerTitle = document.getElementById('docPanelTitle');

    if (headerTitle) headerTitle.textContent = title || 'Documento';
    if (body) body.textContent = content || '';

    panel?.classList.add('open');
    overlay?.classList.add('open');
  },

  close() {
    document.getElementById('docPanel')?.classList.remove('open');
    document.getElementById('docPanelOverlay')?.classList.remove('open');
  },

  async openById(docId) {
    const data = await API.getDocumentPreview(docId);
    if (data && data.content_text) {
      this.open(data.content_text, data.titulo);
    }
  },

  copyContent() {
    const body = document.getElementById('docPanelBody');
    if (body) {
      navigator.clipboard.writeText(body.textContent);
    }
  },

  async downloadById(docId) {
    window.open(API.getDocumentDownloadUrl(docId), '_blank');
  },
};

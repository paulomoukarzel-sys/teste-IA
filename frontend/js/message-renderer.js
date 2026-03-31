/**
 * Renderizador dos 6 tipos de mensagem no chat.
 */
const MessageRenderer = {
  /**
   * Renderiza uma mensagem com base no tipo.
   * @returns {HTMLElement}
   */
  render(msg) {
    switch (msg.message_type || msg.type) {
      case 'document_preview':
        return this.renderDocumentPreview(msg);
      case 'form_input':
        return this.renderForm(msg);
      case 'checklist':
        return this.renderChecklist(msg);
      case 'status':
        return this.renderStatus(msg);
      case 'document_link':
        return this.renderDocumentLink(msg);
      default:
        return this.renderText(msg);
    }
  },

  /** 1. TextMessage */
  renderText(msg) {
    const div = document.createElement('div');
    div.className = `message ${msg.role}`;

    const bubble = document.createElement('div');
    bubble.className = 'message-bubble';
    bubble.innerHTML = this.parseMarkdown(msg.content || '');

    div.appendChild(bubble);
    return div;
  },

  /** 2. DocumentPreviewMessage */
  renderDocumentPreview(msg) {
    const meta = msg.metadata_json || msg.metadata || {};
    const card = document.createElement('div');
    card.className = 'doc-preview-card';

    card.innerHTML = `
      <div class="doc-preview-header">
        <span>${meta.titulo || 'Documento'}</span>
        <span style="font-size:0.78rem;opacity:0.8">${meta.status || 'rascunho'}</span>
      </div>
      <div class="doc-preview-body">${this.escapeHtml(msg.content || '')}</div>
      <div class="doc-preview-actions">
        <button class="doc-action-btn" onclick="DocumentViewer.open('${this.escapeAttr(msg.content || '')}', '${this.escapeAttr(meta.titulo || '')}')">Ver Completo</button>
        <button class="doc-action-btn primary" onclick="Chat.generateDocx(${meta.doc_id || 0})">Gerar .docx</button>
        <button class="doc-action-btn" onclick="navigator.clipboard.writeText(${JSON.stringify(msg.content || '')})">Copiar</button>
      </div>
    `;

    return card;
  },

  /** 3. FormMessage */
  renderForm(msg) {
    const meta = msg.metadata_json || msg.metadata || {};
    const card = document.createElement('div');
    card.className = 'form-card';

    const tipoPecaOptions = [
      'Habeas Corpus', 'Contestacao', 'Alegacoes Finais', 'Apelacao Criminal',
      'Embargos de Declaracao', 'Peticao Inicial', 'Replica', 'Agravo de Instrumento',
      'Agravo Interno', 'Mandado de Seguranca', 'Tutela de Urgencia',
      'Contrarrazoes', 'Impugnacao ao Cumprimento de Sentenca', 'AREsp', 'REsp',
    ].map(t => `<option value="${t}" ${meta.tipo === t ? 'selected' : ''}>${t}</option>`).join('');

    card.innerHTML = `
      <div class="form-header">Elaborar Peca Juridica</div>
      <div class="form-body">
        <div class="form-field">
          <label class="form-label">Tipo da Peca</label>
          <select class="form-select" id="formTipoPeca">${tipoPecaOptions}</select>
        </div>
        <div class="form-field">
          <label class="form-label">Tribunal / Juizo</label>
          <input class="form-input" id="formTribunal" placeholder="Ex: Vara Criminal da Comarca de Florianopolis" value="${meta.tribunal || ''}">
        </div>
        <div class="form-field">
          <label class="form-label">Numero do Processo</label>
          <input class="form-input" id="formProcesso" placeholder="Ex: 0000123-45.2024.8.24.0023" value="${meta.processo || ''}">
        </div>
        <div class="form-field">
          <label class="form-label">Fatos Relevantes</label>
          <textarea class="form-textarea" id="formFatos" placeholder="Descreva os fatos principais do caso...">${meta.fatos || ''}</textarea>
        </div>
        <div class="form-field">
          <label class="form-label">Fundamentos Juridicos</label>
          <textarea class="form-textarea" id="formFundamentos" placeholder="Artigos, teses, jurisprudencia aplicavel...">${meta.fundamentos || ''}</textarea>
        </div>
        <div class="form-field">
          <label class="form-label">Provas / Referencias dos Autos</label>
          <input class="form-input" id="formProvas" placeholder="Ex: evento 45, OUT3, fl. 12" value="${meta.provas || ''}">
        </div>
        <div class="form-field">
          <label class="form-label">Pedidos Especificos</label>
          <textarea class="form-textarea" id="formPedidos" placeholder="O que deve ser requerido ao juizo...">${meta.pedidos || ''}</textarea>
        </div>
        <button class="form-submit-btn" onclick="Chat.submitForm()">Elaborar Peticao</button>
      </div>
    `;

    return card;
  },

  /** 4. ChecklistMessage */
  renderChecklist(msg) {
    const meta = msg.metadata_json || msg.metadata || {};
    const sections = meta.sections || [];
    const card = document.createElement('div');
    card.className = 'checklist-card';

    let totalPass = 0, totalItems = 0;
    sections.forEach(s => {
      s.items.forEach(item => {
        totalItems++;
        if (item.pass) totalPass++;
      });
    });

    const summaryClass = totalPass === totalItems ? 'pass' : 'partial';

    let sectionsHtml = sections.map(section => {
      const sectionPass = section.items.filter(i => i.pass).length;
      const itemsHtml = section.items.map(item => `
        <div class="checklist-item">
          <span class="check-icon ${item.pass ? 'pass' : 'fail'}">${item.pass ? '\u2713' : '\u2717'}</span>
          <span>${this.escapeHtml(item.label)}</span>
        </div>
        ${item.note ? `<div class="check-note">${this.escapeHtml(item.note)}</div>` : ''}
      `).join('');

      return `
        <div class="checklist-section">
          <div class="checklist-section-title" onclick="this.nextElementSibling.style.display = this.nextElementSibling.style.display === 'none' ? 'block' : 'none'">
            <span>${this.escapeHtml(section.title)} (${sectionPass}/${section.items.length})</span>
            <span class="arrow">\u25BC</span>
          </div>
          <div class="checklist-items">${itemsHtml}</div>
        </div>
      `;
    }).join('');

    card.innerHTML = `
      <div class="checklist-header">
        <span>Checklist de Revisao</span>
        <span class="checklist-summary ${summaryClass}">${totalPass}/${totalItems} aprovados</span>
      </div>
      ${sectionsHtml}
    `;

    return card;
  },

  /** 5. StatusMessage */
  renderStatus(msg) {
    const meta = msg.metadata_json || msg.metadata || {};
    const div = document.createElement('div');
    div.className = 'status-message';

    let icon = '\u23F3'; // hourglass
    if (meta.status === 'complete') icon = '\u2705';
    if (meta.status === 'error') icon = '\u274C';

    let progressHtml = '';
    if (meta.progress !== undefined) {
      progressHtml = `
        <div class="progress-bar-container">
          <div class="progress-bar-fill" style="width:${meta.progress}%"></div>
        </div>
      `;
    }

    div.innerHTML = `
      <span class="status-icon">${icon}</span>
      <span class="status-text">${this.escapeHtml(msg.content || '')}</span>
      ${progressHtml}
    `;

    return div;
  },

  /** 6. DocumentLinkMessage */
  renderDocumentLink(msg) {
    const meta = msg.metadata_json || msg.metadata || {};
    const card = document.createElement('div');
    card.className = 'doc-link-card';

    card.innerHTML = `
      <div class="doc-link-icon">\uD83D\uDCC4</div>
      <div class="doc-link-info">
        <div class="doc-link-name">${this.escapeHtml(meta.file_name || 'documento.docx')}</div>
        <div class="doc-link-path">${this.escapeHtml(meta.file_path || '')}</div>
      </div>
      <button class="doc-download-btn" onclick="window.open('${API.getDocumentDownloadUrl(meta.doc_id || 0)}', '_blank')">Download</button>
    `;

    return card;
  },

  /** Markdown simples para HTML */
  parseMarkdown(text) {
    if (!text) return '';
    let html = this.escapeHtml(text);

    // Code blocks
    html = html.replace(/```(\w*)\n([\s\S]*?)```/g, '<pre><code>$2</code></pre>');
    // Inline code
    html = html.replace(/`([^`]+)`/g, '<code>$1</code>');
    // Bold+italic
    html = html.replace(/\*\*\*(.+?)\*\*\*/g, '<strong><em>$1</em></strong>');
    // Bold
    html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
    // Italic
    html = html.replace(/\*(.+?)\*/g, '<em>$1</em>');
    // Headers
    html = html.replace(/^### (.+)$/gm, '<h3>$1</h3>');
    html = html.replace(/^## (.+)$/gm, '<h2>$1</h2>');
    html = html.replace(/^# (.+)$/gm, '<h1>$1</h1>');
    // Line breaks -> paragraphs
    html = html.replace(/\n\n/g, '</p><p>');
    html = html.replace(/\n/g, '<br>');
    html = `<p>${html}</p>`;

    return html;
  },

  escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  },

  escapeAttr(text) {
    return text.replace(/'/g, "\\'").replace(/\n/g, '\\n');
  },
};

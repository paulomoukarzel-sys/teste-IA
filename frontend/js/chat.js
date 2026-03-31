/**
 * Logica principal do chat: WebSocket, renderizacao, workflow.
 */
const Chat = {
  ws: null,
  conversationId: null,
  currentClient: null,
  isStreaming: false,
  streamBuffer: '',
  currentStreamBubble: null,
  lastDocContent: '',

  async init() {
    this.setupInputEvents();
    this.setupScrollDetection();
    this.setupThemeToggle();
    this.setupSidebarToggle();
    this.showWelcome();
    await ClientSelector.init();
    await ClientSelector.loadConversations();
  },

  // ==================== EVENTS ====================

  setupInputEvents() {
    const input = document.getElementById('chatInput');
    const sendBtn = document.getElementById('sendBtn');

    if (input) {
      input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
          e.preventDefault();
          this.sendMessage();
        }
      });

      // Auto-resize
      input.addEventListener('input', () => {
        input.style.height = 'auto';
        input.style.height = Math.min(input.scrollHeight, 200) + 'px';
      });
    }

    if (sendBtn) {
      sendBtn.addEventListener('click', () => this.sendMessage());
    }
  },

  setupScrollDetection() {
    const container = document.getElementById('messagesContainer');
    const scrollBtn = document.getElementById('scrollBottomBtn');

    if (container && scrollBtn) {
      container.addEventListener('scroll', () => {
        const atBottom = container.scrollHeight - container.scrollTop - container.clientHeight < 100;
        scrollBtn.classList.toggle('visible', !atBottom);
      });

      scrollBtn.addEventListener('click', () => {
        container.scrollTo({ top: container.scrollHeight, behavior: 'smooth' });
      });
    }
  },

  setupThemeToggle() {
    const btn = document.getElementById('themeToggle');
    if (btn) {
      // Load saved theme
      const saved = localStorage.getItem('theme') || 'light';
      if (saved === 'dark') {
        document.documentElement.setAttribute('data-theme', 'dark');
        btn.textContent = '\u2600\uFE0F';
      }

      btn.addEventListener('click', () => {
        const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
        if (isDark) {
          document.documentElement.removeAttribute('data-theme');
          btn.textContent = '\uD83C\uDF19';
          localStorage.setItem('theme', 'light');
        } else {
          document.documentElement.setAttribute('data-theme', 'dark');
          btn.textContent = '\u2600\uFE0F';
          localStorage.setItem('theme', 'dark');
        }
      });
    }
  },

  setupSidebarToggle() {
    const hamburger = document.getElementById('hamburgerBtn');
    const sidebar = document.querySelector('.sidebar');
    const overlay = document.querySelector('.sidebar-overlay');

    if (hamburger) {
      hamburger.addEventListener('click', () => {
        sidebar?.classList.toggle('open');
        overlay?.classList.toggle('open');
      });
    }

    if (overlay) {
      overlay.addEventListener('click', () => {
        sidebar?.classList.remove('open');
        overlay?.classList.remove('open');
      });
    }
  },

  // ==================== CLIENT / CONVERSATION ====================

  async onClientSelected(client) {
    this.currentClient = client;
    this.clearMessages();

    // Criar nova conversa
    const conv = await API.createConversation({
      client_id: client.id,
      title: `Conversa com ${client.nome}`,
    });

    this.conversationId = conv.id;
    this.connectWebSocket(conv.id);

    // Adicionar mensagem de sistema
    this.addSystemMessage(
      `Conversa com **${client.nome}**. ` +
      `Cliente ${client.status.toLowerCase()}, ${client.peticoes} peticoes (${client.tipos} tipos). ` +
      `Selecione um comando rapido ou digite sua solicitacao.`
    );

    // Esconder welcome, mostrar chat
    this.hideWelcome();

    // Atualizar conversas recentes
    await ClientSelector.loadConversations();
  },

  async loadConversation(convId) {
    this.clearMessages();
    this.conversationId = convId;

    const conv = await API.getConversation(convId);

    if (conv.client_id) {
      const client = ClientSelector.clients.find(c => c.id === conv.client_id);
      if (client) {
        this.currentClient = client;
        ClientSelector.selectedClientId = client.id;
        ClientSelector.renderList();

        // Atualizar header
        const badge = document.getElementById('activeClientBadge');
        if (badge) {
          badge.querySelector('.client-badge-name').textContent = client.nome;
          badge.querySelector('.client-status-dot').className =
            `client-status-dot ${client.status === 'Ativa' ? 'ativa' : 'encerrada'}`;
          badge.querySelector('.client-badge-count').textContent = `${client.peticoes} peticoes`;
          badge.classList.add('visible');
        }
      }
    }

    // Renderizar mensagens existentes
    if (conv.messages) {
      conv.messages.forEach(msg => {
        const el = MessageRenderer.render(msg);
        document.getElementById('messagesContainer')?.appendChild(el);
      });
    }

    this.connectWebSocket(convId);
    this.hideWelcome();
    this.scrollToBottom();
  },

  async newConversation() {
    if (this.currentClient) {
      await this.onClientSelected(this.currentClient);
    } else {
      this.clearMessages();
      this.showWelcome();
      this.conversationId = null;
      if (this.ws) {
        this.ws.close();
        this.ws = null;
      }
    }
  },

  // ==================== WEBSOCKET ====================

  connectWebSocket(convId) {
    if (this.ws) {
      this.ws.close();
    }

    const protocol = location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${location.host}/ws/chat/${convId}`;

    this.ws = new WebSocket(wsUrl);

    this.ws.onopen = () => {
      console.log('WebSocket conectado');
    };

    this.ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      this.handleWsMessage(data);
    };

    this.ws.onclose = () => {
      console.log('WebSocket desconectado');
    };

    this.ws.onerror = (err) => {
      console.error('WebSocket erro:', err);
    };
  },

  handleWsMessage(data) {
    switch (data.type) {
      case 'user_message_saved':
        break;

      case 'stream_start':
        this.isStreaming = true;
        this.streamBuffer = '';
        this.showTyping(false);

        // Criar bubble para streaming
        const msgDiv = document.createElement('div');
        msgDiv.className = 'message assistant';
        const bubble = document.createElement('div');
        bubble.className = 'message-bubble';
        bubble.innerHTML = '<p></p>';
        msgDiv.appendChild(bubble);
        document.getElementById('messagesContainer')?.appendChild(msgDiv);
        this.currentStreamBubble = bubble;
        this.scrollToBottom();
        break;

      case 'stream_token':
        this.streamBuffer += data.content;
        if (this.currentStreamBubble) {
          this.currentStreamBubble.innerHTML = MessageRenderer.parseMarkdown(this.streamBuffer);
          this.scrollToBottom();
        }
        break;

      case 'stream_end':
        this.isStreaming = false;
        this.lastDocContent = data.full_content || this.streamBuffer;
        this.currentStreamBubble = null;
        this.streamBuffer = '';

        // Habilitar botoes
        document.getElementById('sendBtn').disabled = false;
        document.getElementById('chatInput').disabled = false;
        this.scrollToBottom();
        break;

      case 'error':
        this.isStreaming = false;
        this.showTyping(false);
        this.addSystemMessage(`Erro: ${data.content}`);
        document.getElementById('sendBtn').disabled = false;
        document.getElementById('chatInput').disabled = false;
        break;
    }
  },

  // ==================== SEND MESSAGE ====================

  async sendMessage(text) {
    const input = document.getElementById('chatInput');
    const content = text || input?.value?.trim();

    if (!content || this.isStreaming) return;

    // Verificar se precisa criar conversa primeiro
    if (!this.conversationId) {
      if (!this.currentClient) {
        this.addSystemMessage('Selecione um cliente na sidebar antes de enviar mensagens.');
        return;
      }
      await this.onClientSelected(this.currentClient);
    }

    // Limpar input
    if (input) {
      input.value = '';
      input.style.height = 'auto';
    }

    // Verificar comandos rapidos
    if (content.startsWith('/')) {
      this.handleCommand(content);
      return;
    }

    // Adicionar mensagem do usuario na tela
    const userMsg = MessageRenderer.render({
      role: 'user',
      message_type: 'text',
      content: content,
    });
    document.getElementById('messagesContainer')?.appendChild(userMsg);
    this.scrollToBottom();

    // Mostrar typing
    this.showTyping(true);

    // Desabilitar input durante streaming
    document.getElementById('sendBtn').disabled = true;
    document.getElementById('chatInput').disabled = true;

    // Enviar via WebSocket
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify({
        content: content,
        message_type: 'text',
      }));
    }
  },

  // ==================== COMANDOS RAPIDOS ====================

  handleCommand(cmd) {
    const command = cmd.toLowerCase().trim();

    const commandMap = {
      '/inicial': 'Peticao Inicial',
      '/contestacao': 'Contestacao',
      '/hc': 'Habeas Corpus',
      '/embargos': 'Embargos de Declaracao',
      '/alegacoes': 'Alegacoes Finais',
      '/apelacao': 'Apelacao Criminal',
      '/agravo': 'Agravo de Instrumento',
      '/agravo-interno': 'Agravo Interno',
      '/resp': 'REsp',
      '/aresp': 'AREsp',
      '/contrarrazoes': 'Contrarrazoes',
      '/tutela': 'Tutela de Urgencia',
      '/mandado': 'Mandado de Seguranca',
      '/impugnacao': 'Impugnacao ao Cumprimento de Sentenca',
      '/replica': 'Replica',
    };

    if (command === '/revisar') {
      this.sendMessage('Gostaria de revisar uma peca juridica existente. Por favor, analise o texto que vou fornecer, identificando problemas Criticos (vermelho), Importantes (amarelo) e Sugestoes (azul), conforme o checklist de revisao.');
      return;
    }

    if (command === '/docx') {
      if (this.lastDocContent) {
        this.generateDocxFromLast();
      } else {
        this.addSystemMessage('Nenhuma peca redigida nesta conversa ainda. Redija uma peca primeiro.');
      }
      return;
    }

    const tipoPeca = commandMap[command];
    if (tipoPeca) {
      // Mostrar formulario inline
      const formMsg = MessageRenderer.renderForm({
        role: 'assistant',
        message_type: 'form_input',
        content: '',
        metadata_json: { tipo: tipoPeca },
      });
      document.getElementById('messagesContainer')?.appendChild(formMsg);
      this.scrollToBottom();
      return;
    }

    // Comando nao reconhecido - enviar como texto
    this.sendMessage(cmd.substring(1));
  },

  // ==================== FORMULARIO ====================

  submitForm() {
    const tipo = document.getElementById('formTipoPeca')?.value || '';
    const tribunal = document.getElementById('formTribunal')?.value || '';
    const processo = document.getElementById('formProcesso')?.value || '';
    const fatos = document.getElementById('formFatos')?.value || '';
    const fundamentos = document.getElementById('formFundamentos')?.value || '';
    const provas = document.getElementById('formProvas')?.value || '';
    const pedidos = document.getElementById('formPedidos')?.value || '';

    const clientNome = this.currentClient?.nome || 'Cliente';

    const prompt = `Elabore uma ${tipo} para o cliente ${clientNome}.

Tribunal/Juizo: ${tribunal || 'Nao especificado'}
Numero do Processo: ${processo || 'Nao especificado'}

FATOS:
${fatos || 'Nao informado'}

FUNDAMENTOS JURIDICOS:
${fundamentos || 'Nao informado'}

PROVAS / REFERENCIAS DOS AUTOS:
${provas || 'Nao informado'}

PEDIDOS:
${pedidos || 'Nao informado'}

Siga rigorosamente o workflow de 5 passos da skill: consulte o perfil de estilo, redija a peca completa com enderecamento, qualificacao, secoes em numeracao romana, fundamentacao juridica com citacao de artigos e jurisprudencia, e pedidos em alineas. Aplique o checklist de revisao ao final.`;

    this.sendMessage(prompt);
  },

  // ==================== DOCX GENERATION ====================

  async generateDocxFromLast() {
    if (!this.lastDocContent || !this.currentClient) return;

    // Status message
    this.addStatusMessage('Gerando .docx...', { progress: 30 });

    const result = await API.generateDocument({
      client_id: this.currentClient.id,
      conversation_id: this.conversationId,
      titulo: this.detectTipoPeca(this.lastDocContent),
      conteudo: this.lastDocContent,
      cliente_nome: this.currentClient.nome,
    });

    if (result.status === 'completed') {
      // Atualizar status
      this.addStatusMessage('Documento gerado com sucesso!', { status: 'complete', progress: 100 });

      // Document link
      const linkEl = MessageRenderer.renderDocumentLink({
        content: '',
        metadata_json: {
          file_name: result.file_name,
          file_path: result.file_path,
          doc_id: result.id,
        },
      });
      document.getElementById('messagesContainer')?.appendChild(linkEl);
      this.scrollToBottom();
    } else {
      this.addStatusMessage(`Erro ao gerar .docx: ${result.error || 'erro desconhecido'}`, { status: 'error' });
    }
  },

  async generateDocx(docId) {
    if (this.lastDocContent) {
      await this.generateDocxFromLast();
    }
  },

  detectTipoPeca(content) {
    const upper = content.substring(0, 500).toUpperCase();
    const tipos = [
      'HABEAS CORPUS', 'CONTESTACAO', 'ALEGACOES FINAIS', 'APELACAO',
      'EMBARGOS DE DECLARACAO', 'PETICAO INICIAL', 'REPLICA', 'AGRAVO',
      'MANDADO DE SEGURANCA', 'TUTELA DE URGENCIA', 'CONTRARRAZOES',
      'IMPUGNACAO', 'RESP', 'ARESP',
    ];
    for (const tipo of tipos) {
      if (upper.includes(tipo)) return tipo;
    }
    return 'PETICAO';
  },

  // ==================== UI HELPERS ====================

  clearMessages() {
    const container = document.getElementById('messagesContainer');
    if (container) container.innerHTML = '';
  },

  showWelcome() {
    document.getElementById('welcomeScreen').style.display = 'flex';
    document.getElementById('messagesContainer').style.display = 'none';
    document.querySelector('.commands-bar').style.display = 'none';
    document.querySelector('.input-bar').style.display = 'none';
  },

  hideWelcome() {
    document.getElementById('welcomeScreen').style.display = 'none';
    document.getElementById('messagesContainer').style.display = 'block';
    document.querySelector('.commands-bar').style.display = 'flex';
    document.querySelector('.input-bar').style.display = 'flex';
  },

  addSystemMessage(content) {
    const msg = MessageRenderer.render({
      role: 'assistant',
      message_type: 'text',
      content: content,
    });
    document.getElementById('messagesContainer')?.appendChild(msg);
    this.scrollToBottom();
  },

  addStatusMessage(text, meta = {}) {
    const el = MessageRenderer.renderStatus({
      content: text,
      metadata_json: meta,
    });
    document.getElementById('messagesContainer')?.appendChild(el);
    this.scrollToBottom();
  },

  showTyping(show) {
    const indicator = document.getElementById('typingIndicator');
    if (indicator) {
      indicator.classList.toggle('visible', show);
    }
  },

  scrollToBottom() {
    const container = document.getElementById('messagesContainer');
    if (container) {
      requestAnimationFrame(() => {
        container.scrollTop = container.scrollHeight;
      });
    }
  },

  // ==================== WELCOME CARD ACTIONS ====================

  welcomeAction(action) {
    switch (action) {
      case 'elaborar':
        if (!this.currentClient) {
          this.addSystemMessage('Selecione um cliente na sidebar primeiro.');
          return;
        }
        this.handleCommand('/inicial');
        break;
      case 'revisar':
        if (!this.currentClient) {
          this.addSystemMessage('Selecione um cliente na sidebar primeiro.');
          return;
        }
        this.handleCommand('/revisar');
        break;
      case 'docx':
        this.addSystemMessage('Selecione um cliente, redija uma peca, e clique em "Gerar .docx".');
        break;
    }
  },
};

// ==================== INIT ====================
document.addEventListener('DOMContentLoaded', () => {
  Chat.init();
});

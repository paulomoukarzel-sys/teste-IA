"""
Wizard de configuração do leitor de e-mail
Gastão da Rosa & Moukarzel — Advogados Associados

Execute: python configurar_email.py
"""
import json
import os
import sys
import imaplib

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "email_config.json")

SERVIDORES = {
    "1": {"nome": "Gmail",           "imap_server": "imap.gmail.com",          "imap_port": 993},
    "2": {"nome": "Outlook/Office365","imap_server": "outlook.office365.com",  "imap_port": 993},
    "3": {"nome": "Yahoo Mail",       "imap_server": "imap.mail.yahoo.com",    "imap_port": 993},
    "4": {"nome": "Outro (manual)",   "imap_server": "",                        "imap_port": 993},
}

def linha(char="─", n=60):
    print(char * n)

def cabecalho():
    print("\n")
    linha("═")
    print("  Configuração do Leitor de E-mail")
    print("  Gastão da Rosa & Moukarzel — Controle de Prazos")
    linha("═")
    print()

def testar_conexao(cfg):
    print(f"\n  Testando conexão com {cfg['imap_server']}:{cfg['imap_port']}...")
    try:
        mail = imaplib.IMAP4_SSL(cfg["imap_server"], cfg["imap_port"])
        mail.login(cfg["email"], cfg["senha"])
        mail.select("INBOX")
        mail.logout()
        print("  ✓ Conexão bem-sucedida!\n")
        return True
    except imaplib.IMAP4.error as e:
        print(f"  ✗ Falha de autenticação: {e}")
        return False
    except Exception as e:
        print(f"  ✗ Erro de conexão: {e}")
        return False

def wizard():
    cabecalho()

    # Provedor
    print("  Qual é o seu provedor de e-mail?\n")
    for k, v in SERVIDORES.items():
        print(f"  [{k}] {v['nome']}")
    print()
    escolha = input("  Opção: ").strip()
    if escolha not in SERVIDORES:
        print("  Opção inválida. Encerrando.")
        sys.exit(1)

    srv = SERVIDORES[escolha]
    print(f"\n  Provedor: {srv['nome']}")
    linha()

    if escolha == "4":
        srv["imap_server"] = input("  Servidor IMAP: ").strip()
        srv["imap_port"]   = int(input("  Porta (padrão 993): ").strip() or "993")

    # Credenciais
    email_addr = input("\n  Endereço de e-mail: ").strip()

    if srv["nome"] == "Gmail":
        print("""
  ⚠  Para o Gmail, você precisa de uma SENHA DE APP (não a senha normal).

  Como gerar:
  1. Acesse: myaccount.google.com/security
  2. Ative a verificação em duas etapas (se ainda não tiver)
  3. Vá em "Senhas de app" → selecione "Correio" → "Computador Windows"
  4. Copie a senha de 16 caracteres gerada

  → Caso contrário, o Gmail bloqueará o acesso.
""")
    elif "Outlook" in srv["nome"]:
        print("""
  ⚠  Para o Outlook com 2FA, use uma Senha de App:
  1. Acesse: account.microsoft.com/security
  2. Vá em "Opções de segurança avançadas" → "Senhas de aplicativos"
  3. Crie uma nova senha de app
""")

    import getpass
    senha = getpass.getpass("  Senha (ou Senha de App): ")

    # Intervalo
    print()
    intervalo = input("  Verificar e-mails a cada quantos minutos? [30]: ").strip()
    intervalo = int(intervalo) if intervalo.isdigit() else 30

    apenas_nao_lidos = input("  Processar apenas e-mails não lidos? [S/n]: ").strip().lower()
    apenas_nao_lidos = apenas_nao_lidos != "n"

    cfg = {
        "email":            email_addr,
        "senha":            senha,
        "imap_server":      srv["imap_server"],
        "imap_port":        srv["imap_port"],
        "intervalo_minutos": intervalo,
        "apenas_nao_lidos": apenas_nao_lidos,
    }

    # Testa conexão
    if not testar_conexao(cfg):
        print("  Verifique as credenciais e tente novamente.\n")
        sys.exit(1)

    # Salva
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)

    linha()
    print(f"  ✓ Configuração salva em: {CONFIG_FILE}")
    print()
    print("  Para sincronizar agora:          python leitor_email.py")
    print("  Para rodar em segundo plano:     python leitor_email.py daemon")
    linha()
    print()

if __name__ == "__main__":
    wizard()

"""Carrega SKILL.md e perfil-estilo.md como system prompt para a Claude API."""

from pathlib import Path
from backend.config import SKILL_DIR

_cached_system_prompt: str | None = None


def load_system_prompt() -> str:
    """Le e concatena SKILL.md + perfil-estilo.md como system prompt."""
    global _cached_system_prompt
    if _cached_system_prompt is not None:
        return _cached_system_prompt

    parts = []

    skill_path = SKILL_DIR / "SKILL.md"
    if skill_path.exists():
        parts.append(f"# SKILL DE REDACAO JURIDICA\n\n{skill_path.read_text(encoding='utf-8')}")

    perfil_path = SKILL_DIR / "references" / "perfil-estilo.md"
    if perfil_path.exists():
        parts.append(f"# PERFIL DE ESTILO DO DR. PAULO MOUKARZEL\n\n{perfil_path.read_text(encoding='utf-8')}")

    parts.append(
        "\n\n# INSTRUCOES ADICIONAIS\n"
        "- Voce e o assistente juridico do Dr. Paulo Ekke Moukarzel Junior.\n"
        "- SEMPRE redija no estilo descrito acima.\n"
        "- SEMPRE aplique a checklist de revisao antes de entregar qualquer peca.\n"
        "- Responda SEMPRE em portugues brasileiro.\n"
        "- Use registro formal, expressoes latinas quando apropriado.\n"
        "- NUNCA inclua 'tempestividade' em nenhuma peca.\n"
        "- Ao redigir pecas, use numeracao romana para secoes (I, II, III...).\n"
        "- Cite jurisprudencia no formato completo: tribunal, tipo, numero, turma, relator, data.\n"
    )

    _cached_system_prompt = "\n\n---\n\n".join(parts)
    return _cached_system_prompt


def get_client_context(client_nome: str, client_status: str,
                       client_peticoes: int, client_sintese: str) -> str:
    """Gera contexto do cliente para injetar no prompt."""
    return (
        f"\n\n# CONTEXTO DO CLIENTE ATUAL\n"
        f"- Nome: {client_nome}\n"
        f"- Status: {client_status}\n"
        f"- Peticoes anteriores: {client_peticoes}\n"
        f"- Sintese: {client_sintese}\n"
    )

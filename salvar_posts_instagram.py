"""
Salva cada post do Instagram (1080x1080px) como PNG.
Usa Playwright para renderizar o HTML com fontes e animações reais.

Uso: python salvar_posts_instagram.py
"""

import asyncio
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

HTML_FILE  = Path(__file__).parent / "instagram_gastao_moukarzel.html"
OUTPUT_DIR = Path(__file__).parent / "instagram_posts"

NOMES = [
    "01_apresentacao",
    "02_socio_bruno",
    "03_socio_paulo",
    "04_area_direito_penal",
    "05_area_direito_civel",
    "06_area_direito_empresarial",
    "07_area_improbidade_administrativa",
    "08_area_direito_imobiliario",
    "09_area_familia_e_sucessoes",
    "10_horario_de_atendimento",
    "11_contato",
]


async def main():
    from playwright.async_api import async_playwright

    OUTPUT_DIR.mkdir(exist_ok=True)
    url = HTML_FILE.as_uri()   # file:///C:/Users/...

    print(f"\n▶ Abrindo: {HTML_FILE.name}")
    print(f"▶ Salvando em: {OUTPUT_DIR}\n")

    async with async_playwright() as pw:
        browser = await pw.chromium.launch()
        page = await browser.new_page(viewport={"width": 1080, "height": 1080})

        # Carrega a página original para que fontes e CSS fiquem disponíveis
        await page.goto(url, wait_until="domcontentloaded")

        # Aguarda Google Fonts carregar
        print("  ⏳ Carregando fontes Google...")
        await page.wait_for_timeout(3000)

        # Estilos extras: isolar o post no centro da tela
        await page.add_style_tag(content="""
            body {
                margin: 0 !important;
                padding: 0 !important;
                background: #000 !important;
                overflow: hidden !important;
            }
            /* Garante que o elemento .post não escale */
            .post {
                transform: none !important;
            }
        """)

        for i, nome in enumerate(NOMES):
            output_path = OUTPUT_DIR / f"{nome}.png"

            # Substitui o conteúdo do body pelo HTML do post
            await page.evaluate(f"""() => {{
                document.body.innerHTML = POSTS[{i}]();
            }}""")

            # Pequena pausa para animação shimmer renderizar em bom estado
            await page.wait_for_timeout(400)

            # Captura exatamente o elemento .post (1080×1080)
            post_el = page.locator(".post")
            await post_el.screenshot(path=str(output_path))

            print(f"  ✓ {nome}.png")

        await browser.close()

    print(f"\n✅ {len(NOMES)} posts salvos em:\n   {OUTPUT_DIR}\n")


if __name__ == "__main__":
    # Verifica se playwright está instalado
    try:
        import playwright  # noqa: F401
    except ImportError:
        print("❌ Playwright não encontrado. Execute:\n   pip install playwright\n   playwright install chromium")
        sys.exit(1)

    asyncio.run(main())

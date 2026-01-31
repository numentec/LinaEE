from dataclasses import dataclass
from playwright.sync_api import sync_playwright

@dataclass
class PdfOptions:
    landscape: bool = False

def render_url_to_pdf(url: str, options) -> bytes:
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                # Opcional: reduce variabilidad de render
                "--font-render-hinting=medium",
            ],
        )

        context = browser.new_context(
            # Opcional: si tu print depende de locale/formatos
            locale="es-PA",
        )
        page = context.new_page()

        # Logs útiles
        page.on("console", lambda msg: print(f"[PDF console] {msg.type}: {msg.text}"))
        page.on("pageerror", lambda exc: print(f"[PDF pageerror] {exc}"))
        page.on("requestfailed", lambda req: print(
            f"[PDF requestfailed] {req.method} {req.url} -> {req.failure}"
        ))

        # ✅ Aplicar estilos de impresión
        page.emulate_media(media="print")

        # Viewport: solo afecta layout de pantalla; tu template usa mm, así que da igual,
        # pero lo dejamos fijo para consistencia.
        page.set_viewport_size({"width": 1280, "height": 720})

        # Carga base
        page.goto(url, wait_until="domcontentloaded", timeout=120000)

        # Espera a que Nuxt + datos + paginado estén listos
        page.wait_for_function("window.__PDF_READY__ === true", timeout=120000)

        # ✅ Espera determinista: todas las imágenes del documento completas
        # (img.complete == true incluye éxito o error; si quieres detectar error,
        # hacemos un chequeo extra abajo)
        page.wait_for_function(
            """
            () => {
              const imgs = Array.from(document.images || []);
              return imgs.every(img => img.complete);
            }
            """,
            timeout=120000,
        )

        # ✅ 2 frames para estabilizar layout (evita “cortes raros” por reflow tardío)
        page.evaluate(
            "() => new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)))"
        )

        # (Opcional pero útil) Log de imágenes rotas (naturalWidth = 0 suele indicar fallo)
        broken = page.evaluate(
            """
            () => Array.from(document.images || [])
              .filter(img => img.complete && img.naturalWidth === 0)
              .map(img => img.currentSrc || img.src)
            """
        )
        if broken:
            print(f"[PDF warn] Broken images: {len(broken)}")
            for u in broken[:25]:
                print(f"  - {u}")
            if len(broken) > 25:
                print("  - ... (more)")

        # ✅ PDF: márgenes 0 (los márgenes van en CSS del template)
        pdf_bytes = page.pdf(
            format="Letter",
            landscape=bool(getattr(options, "landscape", False)),
            print_background=True,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
            prefer_css_page_size=True,  # ✅ respeta @page si está presente
        )

        context.close()
        browser.close()
        return pdf_bytes


# def render_url_to_pdf(url: str, options: PdfOptions) -> bytes:
#     with sync_playwright() as p:
#         browser = p.chromium.launch(
#             headless=True,
#             args=["--no-sandbox", "--disable-dev-shm-usage"],
#         )

#         context = browser.new_context()
#         page = context.new_page()

#         # Logs útiles (si algo falla, te dirá por qué)
#         page.on("console", lambda msg: print(f"[PDF console] {msg.type}: {msg.text}"))
#         page.on("pageerror", lambda exc: print(f"[PDF pageerror] {exc}"))
#         page.on("requestfailed", lambda req: print(f"[PDF requestfailed] {req.url}"))

#         # 1) No uses networkidle para SPAs
#         # page.emulate_media(media="print")
#         page.set_viewport_size({"width": 1280, "height": 720})
#         page.goto(url, wait_until="domcontentloaded", timeout=120000)

#         # 2) Espera a que Nuxt monte + datos listos
#         # Esto lo pondremos en el frontend: window.__PDF_READY__ = true
#         page.wait_for_function("window.__PDF_READY__ === true", timeout=120000)

#         pdf_bytes = page.pdf(
#             format="Letter",
#             landscape=options.landscape,
#             print_background=True,
#             margin={"top": "10mm", "right": "10mm", "bottom": "10mm", "left": "10mm"},
#         )

#         context.close()
#         browser.close()
#         return pdf_bytes
    
# def render_url_to_pdf(url: str, options: PdfOptions) -> bytes:
#     with sync_playwright() as p:
#         browser = p.chromium.launch(
#             headless=True,
#             args=["--no-sandbox", "--disable-dev-shm-usage"],
#         )

#         context = browser.new_context()
#         page = context.new_page()

#         # Logs útiles (si algo falla, te dirá por qué)
#         page.on("console", lambda msg: print(f"[PDF console] {msg.type}: {msg.text}"))
#         page.on("pageerror", lambda exc: print(f"[PDF pageerror] {exc}"))
#         page.on("requestfailed", lambda req: print(f"[PDF requestfailed] {req.url}"))

#         # 1) No uses networkidle para SPAs
#         # page.emulate_media(media="print")
#         # page.set_viewport_size({"width": 1280, "height": 720})
#         page.goto(url, wait_until="load", timeout=60000)

#         page.pdf(
#             format="Letter",
#             print_background=True,
#             margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
#         )

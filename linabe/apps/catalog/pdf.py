from dataclasses import dataclass
from playwright.sync_api import sync_playwright


@dataclass
class PdfOptions:
    landscape: bool = False


def render_url_to_pdf(url: str, options: PdfOptions) -> bytes:
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage"],
        )
        page = browser.new_page()

        # Carga y espera a que esté lista la app
        page.goto(url, wait_until="networkidle", timeout=60000)

        pdf_bytes = page.pdf(
            format="Letter",
            landscape=options.landscape,
            print_background=True,
            margin={"top": "10mm", "right": "10mm", "bottom": "10mm", "left": "10mm"},
        )

        browser.close()
        return pdf_bytes

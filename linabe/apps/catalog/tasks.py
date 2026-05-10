# tasks.py
from celery import shared_task
from urllib.parse import urlencode, urljoin
from django.conf import settings
from django.utils import timezone
from .models import PdfJob
from .pdf import catalog_pdf_cache_path, render_url_to_pdf, PdfOptions


def _is_cancelled(job_id: str) -> bool:
    try:
        job = PdfJob.objects.get(id=job_id)
    except PdfJob.DoesNotExist:
        return True

    if job.status == "cancelled" or job.cancel_requested:
        if job.status != "cancelled":
            job.status = "cancelled"
            job.cancelled_at = timezone.now()
            job.save(update_fields=["status", "cancelled_at", "updated_at"])
        return True

    return False


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=2)
def generate_catalog_pdf(self, job_id: str):
    job = PdfJob.objects.select_related("catalog").get(id=job_id)
    catalog = job.catalog

    if _is_cancelled(job_id):
        return

    job.status = "running"
    job.save(update_fields=["status", "updated_at"])

    if _is_cancelled(job_id):
        return

    # Cache hit
    out_path = catalog_pdf_cache_path(catalog)
    if out_path.exists():
        if _is_cancelled(job_id):
            return
        job.status = "success"
        job.file_path = str(out_path)
        job.save(update_fields=["status", "file_path", "updated_at"])
        return

    base = settings.FRONTEND_BASE_URL.rstrip("/") + "/"

    path = f"portal/shared-catalog/{catalog.share_token}/print"
    query = urlencode({"pdf": "1"})
    url = urljoin(base, path) + "?" + query

    # url = f"{base}portal/shared-catalog/{catalog.share_token}/print?pdf=1"

    landscape = (catalog.orientation == "landscape")
    pdf_bytes = render_url_to_pdf(url, PdfOptions(landscape=landscape))

    if _is_cancelled(job_id):
        return

    out_path.write_bytes(pdf_bytes)

    if _is_cancelled(job_id):
        return

    job.status = "success"
    job.file_path = str(out_path)
    job.save(update_fields=["status", "file_path", "updated_at"])

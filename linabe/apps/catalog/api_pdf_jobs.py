# linabe/catalog/api_pdf_jobs.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import FileResponse, Http404

from .models import PdfJob


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def pdf_job_status(request, job_id: str):
    job = PdfJob.objects.get(id=job_id, owner=request.user)
    data = {"job_id": str(job.id), "status": job.status}
    if job.status == "success":
        data["download_url"] = f"/catalog/api/pdf-jobs/{job.id}/download/"
    if job.status == "failed":
        data["error"] = job.error
    return Response(data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def pdf_job_download(request, job_id: str):
    job = PdfJob.objects.get(id=job_id, owner=request.user)
    if job.status != "success" or not job.file_path:
        raise Http404("PDF not ready")

    return FileResponse(
        open(job.file_path, "rb"),
        content_type="application/pdf",
        as_attachment=True,
        filename=f"catalogo-{job.catalog_id}.pdf",
    )

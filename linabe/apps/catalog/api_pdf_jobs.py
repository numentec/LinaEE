# linabe/catalog/api_pdf_jobs.py
from celery.result import AsyncResult
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import FileResponse, Http404

from .models import PdfJob


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def pdf_job_status(request, job_id: str):
    try:
        job = PdfJob.objects.get(id=job_id, owner=request.user)
    except PdfJob.DoesNotExist:
        return Response({"detail": "PDF job no encontrado."}, status=404)

    data = {
        "job_id": str(job.id),
        "status": job.status,
        "can_cancel": job.status in ("queued", "running"),
    }
    if job.status == "success":
        data["download_url"] = f"/catalog/api/pdf-jobs/{job.id}/download/"
    if job.status == "failed":
        data["error"] = job.error
    if job.status == "cancelled":
        data["cancelled_at"] = job.cancelled_at
    return Response(data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def pdf_job_download(request, job_id: str):
    try:
        job = PdfJob.objects.get(id=job_id, owner=request.user)
    except PdfJob.DoesNotExist:
        raise Http404("PDF job not found")

    if job.status != "success" or not job.file_path:
        raise Http404("PDF not ready")

    return FileResponse(
        open(job.file_path, "rb"),
        content_type="application/pdf",
        as_attachment=True,
        filename=f"catalogo-{job.catalog_id}.pdf",
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def pdf_job_cancel(request, job_id: str):
    try:
        job = PdfJob.objects.get(id=job_id, owner=request.user)
    except PdfJob.DoesNotExist:
        return Response({"detail": "PDF job no encontrado."}, status=404)

    if job.status in ("success", "failed", "cancelled"):
        return Response(
            {
                "job_id": str(job.id),
                "status": job.status,
                "detail": "El job ya finalizo.",
            },
            status=status.HTTP_200_OK,
        )

    update_fields = ["cancel_requested", "updated_at"]
    job.cancel_requested = True

    if job.status == "queued":
        job.status = "cancelled"
        job.cancelled_at = timezone.now()
        update_fields.extend(["status", "cancelled_at"])

    job.save(update_fields=update_fields)

    if job.celery_task_id:
        AsyncResult(job.celery_task_id).revoke(terminate=False)

    return Response(
        {
            "job_id": str(job.id),
            "status": job.status,
            "cancel_requested": True,
            "cancelled_at": job.cancelled_at,
            "detail": "Cancelacion solicitada.",
        },
        status=status.HTTP_200_OK,
    )

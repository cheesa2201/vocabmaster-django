import os
import random
from datetime import timedelta

from celery import shared_task
from django.utils import timezone


@shared_task
def clean_old_data():
    """
    Chạy ngày 1 mỗi tháng lúc 2h sáng (xem celery_beat_schedule.py).
    - Xóa 30-40% từ vựng ít được ôn nhất (mastery thấp + last_review lâu nhất)
    - Xóa file upload đã hết hạn + file vật lý khỏi disk
    """
    from .models import FileUpload, Word

    threshold = timezone.now() - timedelta(days=30)

    # ── Xóa từ vựng cũ ───────────────────────────────────────────────────────
    old_words_qs = Word.objects.filter(last_review__lt=threshold)
    total_old = old_words_qs.count()

    if total_old > 0:
        delete_count = int(total_old * random.uniform(0.3, 0.4))

        # BUG FIX: .delete() không hoạt động trên sliced queryset → dùng id__in
        # Ưu tiên xóa từ mastery thấp nhất + last_review lâu nhất trước
        ids_to_delete = list(
            old_words_qs
            .order_by('mastery', 'last_review')   # mastery=0 + cũ nhất trước
            .values_list('id', flat=True)[:delete_count]
        )
        deleted_words, _ = Word.objects.filter(id__in=ids_to_delete).delete()
        print(f"[clean_old_data] Đã xóa {deleted_words} từ vựng cũ.")

    # ── Xóa file upload hết hạn ───────────────────────────────────────────────
    expired_files = FileUpload.objects.filter(expires_at__lt=timezone.now())
    file_count = expired_files.count()

    for file_obj in expired_files:
        # Xóa file vật lý trên disk trước
        try:
            if file_obj.file and os.path.isfile(file_obj.file.path):
                os.remove(file_obj.file.path)
        except Exception as e:
            print(f"[clean_old_data] Không xóa được file {file_obj.file.name}: {e}")

    expired_files.delete()
    print(f"[clean_old_data] Đã xóa {file_count} file hết hạn.")

    return {
        'words_deleted': deleted_words if total_old > 0 else 0,
        'files_deleted': file_count,
    }
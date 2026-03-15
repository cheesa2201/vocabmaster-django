# Patch 2 chỗ trong views.py hiện tại:
#
# 1. dashboard view — thêm mastery_counts cho Chart.js
# 2. quiz_question view — đổi template name sang quiz_question.html (1 file thay vì 2)
#
# Chỉ copy 2 function này vào views.py, giữ nguyên phần còn lại.

from datetime import timezone

from django.db.models import Count

from core.models import LANGUAGE_CHOICES, FileUpload, Word

@login_required
def dashboard(request):
    total = Word.objects.filter(user=request.user).count()
    stats = {
        code: {
            'label': label,
            'total': Word.objects.filter(user=request.user, lang=code).count(),
            'mastered': Word.objects.filter(user=request.user, lang=code, mastery=2).count(),
        }
        for code, label in LANGUAGE_CHOICES
    }
    recent_files = FileUpload.objects.filter(
        user=request.user,
        expires_at__gt=timezone.now()
    ).order_by('-uploaded_at')[:3]

    # Mastery counts cho Chart.js
    mastery_qs = (
        Word.objects.filter(user=request.user)
        .values('mastery')
        .annotate(cnt=Count('id'))
    )
    mastery_counts = {0: 0, 1: 0, 2: 0}
    for row in mastery_qs:
        mastery_counts[row['mastery']] = row['cnt']

    return render(request, 'dashboard.html', {
        'total': total,
        'stats': stats,
        'max_words': MAX_WORDS_PER_USER,
        'recent_files': recent_files,
        'mastery_counts': mastery_counts,
    })


@login_required
def quiz_question(request, session_id, q_index):
    try:
        session = QuizSession.objects.get(id=session_id, user=request.user)
    except QuizSession.DoesNotExist:
        messages.error(request, "Không tìm thấy phiên quiz.")
        return redirect('quiz_home')

    word_ids = request.session.get(f'quiz_{session.id}_words', [])
    if not word_ids:
        messages.error(request, "Phiên quiz hết hạn. Hãy bắt đầu lại.")
        return redirect('quiz_home')

    if q_index >= len(word_ids):
        return redirect('quiz_result', session_id=session.id)

    word = Word.objects.get(id=word_ids[q_index])

    if request.method == 'POST':
        user_answer = request.POST.get('answer', '').strip()
        is_correct = _check_answer(session.quiz_type, user_answer, word)

        QuizAnswer.objects.create(
            session=session, word=word,
            user_answer=user_answer, is_correct=is_correct,
        )
        if is_correct:
            session.correct_count += 1
            session.save(update_fields=['correct_count'])

        _update_mastery_quiz(word, is_correct)

        request.session[f'quiz_{session.id}_last'] = {
            'is_correct': is_correct,
            'correct_answer': word.meaning,
            'user_answer': user_answer,
            'word': word.word,
            'reading': word.reading,
        }
        return redirect('quiz_question', session_id=session.id, q_index=q_index + 1)

    last_result = request.session.pop(f'quiz_{session.id}_last', None)
    context = {
        'session': session,
        'word': word,
        'q_index': q_index,
        'q_number': q_index + 1,
        'total': len(word_ids),
        'progress_percent': round(q_index / len(word_ids) * 100),
        'last_result': last_result,
    }
    if session.quiz_type == 'multiple':
        context['choices'] = _get_choices(word, request.user, word_ids)

    # Dùng 1 template duy nhất quiz_question.html (có if/else bên trong)
    return render(request, 'quiz_question.html', context)
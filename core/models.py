from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

LANGUAGE_CHOICES = [
    ('en', 'English'),
    ('zh', 'Chinese'),
    ('jp', 'Japanese'),
]

MAX_WORDS_PER_USER = 10_000


# ── Word ──────────────────────────────────────────────────────────────────────

class Word(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='words')
    lang = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='en')
    word = models.CharField(max_length=200)
    reading = models.CharField(max_length=200, blank=True)
    meaning = models.TextField()
    word_type = models.CharField(max_length=20, blank=True)
    example = models.TextField(blank=True)
    mastery = models.PositiveSmallIntegerField(default=0, choices=[
        (0, 'Chưa nhớ'), (1, 'Đang học'), (2, 'Thành thạo')
    ])
    last_review = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'word', 'lang']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.word} ({self.lang}) - {self.user.username}"


# ── FileUpload ────────────────────────────────────────────────────────────────

class FileUpload(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='uploads/%Y/%m/%d/')
    title = models.CharField(max_length=200, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    notes_json = models.JSONField(default=list, blank=True)

    def __str__(self):
        return f"{self.title or self.file.name} - {self.user.username}"

    def save(self, *args, **kwargs):
        if not self.expires_at:
            # BUG FIX: uploaded_at chưa có khi save() lần đầu → dùng timezone.now()
            self.expires_at = timezone.now() + timezone.timedelta(days=30)
        super().save(*args, **kwargs)

    @property
    def is_expired(self):
        return self.expires_at and self.expires_at < timezone.now()

    @property
    def days_remaining(self):
        if not self.expires_at:
            return None
        delta = self.expires_at - timezone.now()
        return max(0, delta.days)


# ── Quiz ──────────────────────────────────────────────────────────────────────

QUIZ_TYPE_CHOICES = [
    ('fill', 'Fill in the blank'),
    ('multiple', 'Multiple choice'),
]


class QuizSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_sessions')
    quiz_type = models.CharField(max_length=10, choices=QUIZ_TYPE_CHOICES)
    lang = models.CharField(max_length=2, blank=True)
    total_questions = models.PositiveSmallIntegerField(default=0)
    correct_count = models.PositiveSmallIntegerField(default=0)
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-started_at']

    @property
    def score_percent(self):
        if self.total_questions == 0:
            return 0
        return round(self.correct_count / self.total_questions * 100)

    @property
    def duration_seconds(self):
        if not self.finished_at:
            return None
        return int((self.finished_at - self.started_at).total_seconds())

    def __str__(self):
        return f"{self.user.username} | {self.get_quiz_type_display()} | {self.score_percent}%"


class QuizAnswer(models.Model):
    session = models.ForeignKey(QuizSession, on_delete=models.CASCADE, related_name='answers')
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    user_answer = models.TextField(blank=True)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{'✓' if self.is_correct else '✗'} {self.word.word}"
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Flashcard(models.Model):
    """Model representing a flashcard"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='flashcards')
    front = models.TextField(help_text='Question or prompt')
    back = models.TextField(help_text='Answer or explanation')
    topic = models.CharField(max_length=100, help_text='Subject or category')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Study tracking fields
    times_reviewed = models.IntegerField(default=0)
    times_correct = models.IntegerField(default=0)
    last_reviewed = models.DateTimeField(null=True, blank=True)
    is_known = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'topic']),
            models.Index(fields=['user', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.topic}: {self.front[:50]}"
    
    def mark_reviewed(self, is_correct=True):
        """Mark card as reviewed and update statistics"""
        self.times_reviewed += 1
        if is_correct:
            self.times_correct += 1
        self.last_reviewed = timezone.now()
        self.save()
    
    def get_success_rate(self):
        """Calculate success rate as percentage"""
        if self.times_reviewed == 0:
            return 0
        return int((self.times_correct / self.times_reviewed) * 100)


class StudySession(models.Model):
    """Model to track study sessions"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='study_sessions')
    started_at = models.DateTimeField(default=timezone.now)
    ended_at = models.DateTimeField(null=True, blank=True)
    cards_studied = models.IntegerField(default=0)
    cards_known = models.IntegerField(default=0)
    topic = models.CharField(max_length=100, blank=True)
    
    class Meta:
        ordering = ['-started_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.started_at.strftime('%Y-%m-%d %H:%M')}"
    
    def duration_minutes(self):
        """Calculate session duration in minutes"""
        if self.ended_at:
            duration = self.ended_at - self.started_at
            return int(duration.total_seconds() / 60)
        return 0

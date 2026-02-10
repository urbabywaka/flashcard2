from django import forms
from .models import Flashcard


class FlashcardForm(forms.ModelForm):
    """Form for creating and editing flashcards"""
    
    class Meta:
        model = Flashcard
        fields = ['front', 'back', 'topic']
        widgets = {
            'front': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter the question or prompt...'
            }),
            'back': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter the answer or explanation...'
            }),
            'topic': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Mathematics, History, Biology'
            }),
        }
        labels = {
            'front': 'Question (Front)',
            'back': 'Answer (Back)',
            'topic': 'Topic/Subject',
        }


class FlashcardSearchForm(forms.Form):
    """Form for searching and filtering flashcards"""
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search flashcards...'
        })
    )
    topic = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Filter by topic...'
        })
    )
    
    SORT_CHOICES = [
        ('-created_at', 'Newest First'),
        ('created_at', 'Oldest First'),
        ('topic', 'Topic A-Z'),
        ('-topic', 'Topic Z-A'),
    ]
    
    sort = forms.ChoiceField(
        choices=SORT_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.utils import timezone
from django.http import JsonResponse, HttpResponse
import json
import csv
import random

from .models import Flashcard, StudySession
from .forms import FlashcardForm, FlashcardSearchForm


@login_required
def dashboard(request):
    """Main dashboard view"""
    user_cards = Flashcard.objects.filter(user=request.user)
    
    # Statistics
    total_cards = user_cards.count()
    topics = user_cards.values('topic').annotate(count=Count('topic')).order_by('-count')
    known_cards = user_cards.filter(is_known=True).count()
    review_cards = total_cards - known_cards
    
    # Recent sessions
    recent_sessions = StudySession.objects.filter(user=request.user)[:5]
    
    context = {
        'total_cards': total_cards,
        'known_cards': known_cards,
        'review_cards': review_cards,
        'topics': topics[:5],  # Top 5 topics
        'recent_sessions': recent_sessions,
    }
    return render(request, 'flashcards/dashboard.html', context)


@login_required
def flashcard_list(request):
    """List all flashcards with search and filter"""
    flashcards = Flashcard.objects.filter(user=request.user)
    form = FlashcardSearchForm(request.GET)
    
    if form.is_valid():
        search = form.cleaned_data.get('search')
        topic = form.cleaned_data.get('topic')
        sort = form.cleaned_data.get('sort')
        
        if search:
            flashcards = flashcards.filter(
                Q(front__icontains=search) | 
                Q(back__icontains=search) |
                Q(topic__icontains=search)
            )
        
        if topic:
            flashcards = flashcards.filter(topic__icontains=topic)
        
        if sort:
            flashcards = flashcards.order_by(sort)
    
    # Get unique topics for filter
    topics = Flashcard.objects.filter(user=request.user).values_list('topic', flat=True).distinct()
    
    context = {
        'flashcards': flashcards,
        'form': form,
        'topics': topics,
    }
    return render(request, 'flashcards/flashcard_list.html', context)


@login_required
def flashcard_create(request):
    """Create a new flashcard"""
    if request.method == 'POST':
        form = FlashcardForm(request.POST)
        if form.is_valid():
            flashcard = form.save(commit=False)
            flashcard.user = request.user
            flashcard.save()
            messages.success(request, 'Flashcard created successfully!')
            return redirect('flashcards:flashcard_list')
    else:
        form = FlashcardForm()
    
    return render(request, 'flashcards/flashcard_form.html', {'form': form, 'action': 'Create'})


@login_required
def flashcard_edit(request, pk):
    """Edit an existing flashcard"""
    flashcard = get_object_or_404(Flashcard, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = FlashcardForm(request.POST, instance=flashcard)
        if form.is_valid():
            form.save()
            messages.success(request, 'Flashcard updated successfully!')
            return redirect('flashcards:flashcard_list')
    else:
        form = FlashcardForm(instance=flashcard)
    
    return render(request, 'flashcards/flashcard_form.html', {
        'form': form, 
        'action': 'Edit',
        'flashcard': flashcard
    })


@login_required
def flashcard_delete(request, pk):
    """Delete a flashcard"""
    flashcard = get_object_or_404(Flashcard, pk=pk, user=request.user)
    
    if request.method == 'POST':
        flashcard.delete()
        messages.success(request, 'Flashcard deleted successfully!')
        return redirect('flashcards:flashcard_list')
    
    return render(request, 'flashcards/flashcard_confirm_delete.html', {'flashcard': flashcard})


@login_required
def flashcard_detail(request, pk):
    """View a single flashcard"""
    flashcard = get_object_or_404(Flashcard, pk=pk, user=request.user)
    return render(request, 'flashcards/flashcard_detail.html', {'flashcard': flashcard})


@login_required
def study_mode(request):
    """Study mode - review flashcards"""
    # Get filter parameters
    topic = request.GET.get('topic', '')
    only_review = request.GET.get('only_review', '')
    
    # Filter flashcards
    flashcards = Flashcard.objects.filter(user=request.user)
    
    if topic:
        flashcards = flashcards.filter(topic=topic)
    
    if only_review:
        flashcards = flashcards.filter(is_known=False)
    
    # Convert to list and shuffle
    flashcard_list = list(flashcards)
    random.shuffle(flashcard_list)
    
    # Create or get current study session
    session = None
    if flashcard_list:
        session = StudySession.objects.create(
            user=request.user,
            topic=topic if topic else 'All Topics'
        )
        request.session['study_session_id'] = session.id
    
    # Get unique topics
    topics = Flashcard.objects.filter(user=request.user).values_list('topic', flat=True).distinct()
    
    context = {
        'flashcards': flashcard_list,
        'total_cards': len(flashcard_list),
        'topics': topics,
        'selected_topic': topic,
        'only_review': only_review,
        'session': session,
    }
    return render(request, 'flashcards/study_mode.html', context)


@login_required
def mark_flashcard(request, pk):
    """Mark flashcard as known or review"""
    if request.method == 'POST':
        try:
            flashcard = get_object_or_404(Flashcard, pk=pk, user=request.user)
            action = request.POST.get('action')
            
            if action == 'known':
                flashcard.is_known = True
                flashcard.mark_reviewed(is_correct=True)
                
                # Update session
                session_id = request.session.get('study_session_id')
                if session_id:
                    try:
                        session = StudySession.objects.get(id=session_id)
                        session.cards_studied += 1
                        session.cards_known += 1
                        session.save()
                    except StudySession.DoesNotExist:
                        pass
                
                return JsonResponse({
                    'status': 'success',
                    'message': 'Card marked as known!',
                    'is_known': True
                })
            
            elif action == 'review':
                flashcard.is_known = False
                flashcard.mark_reviewed(is_correct=False)
                
                # Update session
                session_id = request.session.get('study_session_id')
                if session_id:
                    try:
                        session = StudySession.objects.get(id=session_id)
                        session.cards_studied += 1
                        session.save()
                    except StudySession.DoesNotExist:
                        pass
                
                return JsonResponse({
                    'status': 'success',
                    'message': 'Card marked for review!',
                    'is_known': False
                })
            else:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Invalid action'
                })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            })
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


@login_required
def end_study_session(request):
    """End the current study session"""
    session_id = request.session.get('study_session_id')
    if session_id:
        try:
            session = StudySession.objects.get(id=session_id)
            session.ended_at = timezone.now()
            session.save()
            del request.session['study_session_id']
        except StudySession.DoesNotExist:
            pass
    
    return redirect('flashcards:dashboard')


@login_required
def export_flashcards(request):
    """Export flashcards to CSV"""
    flashcards = Flashcard.objects.filter(user=request.user)
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="flashcards.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Topic', 'Question (Front)', 'Answer (Back)', 'Created Date', 'Times Reviewed', 'Success Rate'])
    
    for card in flashcards:
        writer.writerow([
            card.topic,
            card.front,
            card.back,
            card.created_at.strftime('%Y-%m-%d'),
            card.times_reviewed,
            f"{card.get_success_rate()}%"
        ])
    
    return response


@login_required
def import_flashcards(request):
    """Import flashcards from CSV"""
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        
        try:
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)
            
            count = 0
            for row in reader:
                Flashcard.objects.create(
                    user=request.user,
                    topic=row.get('Topic', 'Imported'),
                    front=row.get('Question (Front)', row.get('Front', '')),
                    back=row.get('Answer (Back)', row.get('Back', ''))
                )
                count += 1
            
            messages.success(request, f'Successfully imported {count} flashcards!')
        except Exception as e:
            messages.error(request, f'Error importing flashcards: {str(e)}')
        
        return redirect('flashcards:flashcard_list')
    
    return render(request, 'flashcards/import_flashcards.html')


@login_required
def statistics(request):
    """View detailed statistics"""
    flashcards = Flashcard.objects.filter(user=request.user)
    
    # Overall stats
    total_cards = flashcards.count()
    known_cards = flashcards.filter(is_known=True).count()
    total_reviews = sum(card.times_reviewed for card in flashcards)
    
    # Topic breakdown
    topics = flashcards.values('topic').annotate(
        total=Count('id'),
        known=Count('id', filter=Q(is_known=True))
    ).order_by('-total')
    
    # Recent activity
    recent_sessions = StudySession.objects.filter(user=request.user).order_by('-started_at')[:10]
    
    context = {
        'total_cards': total_cards,
        'known_cards': known_cards,
        'review_cards': total_cards - known_cards,
        'total_reviews': total_reviews,
        'topics': topics,
        'recent_sessions': recent_sessions,
    }
    return render(request, 'flashcards/statistics.html', context)

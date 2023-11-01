from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from .forms import RegistrationForm, LoginForm
from django_email_verification import send_email
from django.contrib.auth import logout, login, authenticate
from .models import Comments, Posts
from django.db.models import Count
from django.contrib import messages


def create_user(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            send_email(user)
            messages.success(request, 'Please confirm your email by clicking on the link in the console')
            return redirect('login')
    else:
        form = RegistrationForm()

    return render(request, 'registration_form.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')

def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                return render(request, 'login.html', {'form': form, 'error': 'Invalid email or password'})
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def dashboard_view(request):
    questions = Posts.objects.prefetch_related('comments').annotate(total_likes=Count('likes')).order_by('-added')
    return render(request, "dashboard.html", {'questions':questions})

def add_question(request):
    if request.method == 'POST' and request.user.is_authenticated:
        title = request.POST.get("title")
        question = request.POST.get("question")
        if title and question:
            post = Posts()
            post.title = title
            post.description = question
            post.posted_by = request.user
            post.save()
        return JsonResponse({'message': 'Question has been added'}, status=200)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=400)
    
def add_like(request, question_id):
    if request.method == 'POST' and request.user.is_authenticated:
        question = get_object_or_404(Posts, id=question_id)
        if question.likes.filter(id=request.user.id).exists():
            question.likes.remove(request.user)
            liked = True
        else:
            question.likes.add(request.user)
            liked = True
        total_likes = question.likes.count()
        return JsonResponse({'liked': liked, 'total_likes': total_likes})
    else:
        return JsonResponse({"error": "Error"}, status=400)
    
def add_comment(request):
    if request.method == 'POST':
        question_id = request.POST.get('post_id')
        comment_text = request.POST.get('comment')
        try:
            question = Posts.objects.get(id=question_id)
            comment = Comments.objects.create(
                question_id = question, user_id = request.user, comment = comment_text
            )
            return JsonResponse({'success': True, 'comment_id': comment.id})
        except Posts.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Post does not exist'})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request'})
    
def add_comment_like(request, comment_id):
    if request.method == 'POST' and request.user.is_authenticated:
        comment = get_object_or_404(Comments, id=comment_id)
        if comment.likes.filter(id=request.user.id).exists():
            comment.likes.remove(request.user)
            liked = True
        else:
            comment.likes.add(request.user)
            liked = True
        total_likes = comment.likes.count()
        return JsonResponse({'liked': liked, 'total_likes': total_likes})
    else:
        return JsonResponse({"error": "Error"}, status=400)












from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Question, Answer


def question_list(request):
    questions = Question.objects.all()
    return render(request, 'qa/question_list.html', {'questions': questions})


def question_detail(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        content = request.POST.get('content', '').strip()
        if content:
            Answer.objects.create(
                question=question,
                content=content,
                author=request.user
            )
        return redirect('question_detail', pk=pk)
    return render(request, 'qa/question_detail.html', {'question': question})


@login_required
def ask_question(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()
        if title and content:
            question = Question.objects.create(
                title=title,
                content=content,
                author=request.user
            )
            return redirect('question_list')
    return render(request, 'qa/ask_question.html')

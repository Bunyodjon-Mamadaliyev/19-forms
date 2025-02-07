from django.shortcuts import render, redirect, get_object_or_404
from django.forms import modelformset_factory
from .models import Test, Question, Answer
from .forms import TestForm, QuestionForm, AnswerForm


def test_list(request):
    tests = Test.objects.all()
    ctx = {'tests': tests}
    return render(request, 'questions/test-list.html', ctx)


def create_test(request):
    QuestionFormSet = modelformset_factory(Question, form=QuestionForm, extra=1)

    if request.method == 'POST':
        form = TestForm(request.POST)
        formset = QuestionFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            test = form.save()
            questions = formset.save(commit=False)
            for question in questions:
                question.test = test
                question.save()
            return redirect('questions:list')

    else:
        form = TestForm()
        formset = QuestionFormSet(queryset=Question.objects.none())

    return render(request, 'questions/test-formset.html', {
        'form': form,
        'question_formset': formset,
    })


def delete(request, pk):
    test = get_object_or_404(Test, pk=pk)
    test.delete()
    return redirect('questions:list')

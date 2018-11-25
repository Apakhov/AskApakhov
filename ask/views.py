from django.shortcuts import render, redirect
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import Http404
from ask.models import Profile, Question, Tag, Answer, Like
from ask.forms import QuestionForm
 

def pag(items, items_on_page, page_am, request, num):
    paginator = Paginator(items, items_on_page)
    try:
        page_num = paginator.validate_number(num)
    except (ValueError, TypeError, EmptyPage):
        page_num = 1

    if page_num > page_am / 2 :
        beg_idx = page_num - page_am / 2
    else:
        beg_idx = 1
    
    if page_num + page_am / 2 < paginator.num_pages:
        end_idx = page_num + page_am / 2
        if end_idx < page_am:
            end_idx = page_am + 1
    else:
        end_idx = paginator.num_pages + 1 
    paginator.indexes = range(int(beg_idx), int(end_idx))
    page = paginator.get_page(page_num)
    return paginator, page
    


def index(request, page_num=-1):
    if page_num == -1:
        page_num = 1
        indexed = False
    else:
        indexed = True
    questions = Question.objects.order_by_date(100)
    paginator, page = pag(questions, 10, 10,request, page_num)
    return render(request, 'ask/index.html', {'questions' : page, 'paginator': paginator, 'indexed':indexed})

def hot(request, page_num=-1):
    if page_num == -1:
        page_num = 1
        indexed = False
    else:
        indexed = True
    
    
    questions = Question.objects.order_by_hot()
    paginator, page = pag(questions, 10, 10,request, page_num)
    return render(request, 'ask/hot.html', {'questions' : page, 'paginator': paginator, 'indexed':indexed})    

def ask(request):
    return render(request, 'ask/question_form.html', {'form': QuestionForm()})

def signup(request):
    return render(request, 'registration/signup.html')

def question(request, question_num):
    q = Question.objects.get(id=question_num)
    return render(request, 'ask/question.html', {'question':q})

def settings(request):
    return render(request, 'ask/settings.html')

def tagged(request, tag='bender', page_num=-1):
    if page_num == -1:
        page_num = 1
        indexed = False
    else:
        indexed = True
    questions = Question.objects.filter_by_tag(tag)
    paginator, page = pag(questions, 10, 10,request, page_num)
    return render(request, 'ask/tagged.html', {'tag':tag,'questions' : page, 'paginator': paginator, 'indexed':indexed})

def page404(request):
    raise Http404("Page does not exist")
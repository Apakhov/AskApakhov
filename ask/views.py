from django.shortcuts import render, redirect
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import Http404, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from ask.models import Profile, Question, Tag, Answer, Like
from ask.forms import QuestionForm, ProfileForm
 

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
    if request.method == 'POST':
        print("POST")
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/login')
        
        form=QuestionForm(request.POST)
        if form.is_valid():
            autor = Profile.objects.get_by_natural_key(request.user.username)
            title = form.cleaned_data['title']
            text = form.cleaned_data['text']
            q = Question.objects.create(autor=autor, title=title, text=text)
            for tag in form.cleaned_data['tags']:
                q.tags.add(Tag.objects.get_or_create(title=tag)[0])
            q.save()
            return HttpResponseRedirect('/question/'+str(q.id))
    else:
        form=QuestionForm()    
    return render(request, 'ask/question_form.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        
        if request.user.is_authenticated:
            return HttpResponseRedirect('/')
        
        form=ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            print('VALID')
            form.save()
            #messages.info(request, "Thanks for registering. You are now logged in.")
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password'],
                                    )
            login(request, new_user)
            return HttpResponseRedirect('/login')
    else:
        form=ProfileForm() 
    return render(request, 'registration/signup.html', {'form': form})

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
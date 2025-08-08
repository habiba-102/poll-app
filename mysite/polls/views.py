from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.db.models import F
from .models import Choice, Question, Vote
from django.views import generic
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
# Create your views here.

class IndexView(generic.ListView):#for ListView, the automatically generated context variable is question_list
    template_name = 'index.html'
    context_object_name = 'latest_questions'

#Django injects that data into the template using the context name

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]
    #__lte means “less than or equal to” (this is a Django query lookup).

class DetailView(generic.DetailView):
    model = Question
    template_name = 'detail.html' 

    #If you don’t specify context_object_name, Django will automatically use the model’s lowercase name:
    #context_object_name = 'question'  # this is what Django uses by default   

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte = timezone.now())
    
class ResultsView(generic.DetailView):
    model = Question
    template_name = 'results.html'

@login_required
def vote(request, question_id):
    question = get_object_or_404(Question, pk = question_id)

    if Vote.objects.filter(user = request.user, question = question).exists():
        return render(request, 'detail.html', {'question': question, 'error_message': 'You already voted.'})
    
    try:
        selected_choice = question.choice_set.get(pk = request.POST["choice"])
        #request.POST["choice"] -> Looks for the value of the input with name="choice" (in your HTML form).

    except (KeyError, Choice.DoesNotExist):
        return render(request, 'detail.html',{"question":question,
                                              "error_message": "You didn't select a choice"})
    else:
        selected_choice.votes = F("votes")+1
        selected_choice.save()

    Vote.objects.create(user=request.user, question=question, choice = selected_choice)
    return redirect(reverse("results", args = (question_id,)))
#args needs to be a tuble or list
#reverse(...) This function converts the view name 
# and arguments into a real URL string.
#So reverse("polls:results", args=(5,)) → "/polls/5/results/"

def signup_view(request):

    if request.method=='POST':
        form= UserCreationForm(request.POST)
        if form.is_valid():
            login(request,form.save()) #log the user in after signing up
            return redirect('index')
        
    else:
        form = UserCreationForm()

    return render(request, 'registration/signup.html', {'form':form})


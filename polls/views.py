# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from polls.models import Poll, Choice
from django.core.urlresolvers import reverse
from django.views import generic

class IndexView(generic.ListView):
    context_object_name= 'plist'
    template_name='polls/index.html'
    def get_queryset(self):
        return Poll.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    template_name='polls/detail.html'
    model=Poll

class ResultsView(generic.DetailView):
    model=Poll
    template_name='polls/result.html'

def vote(request, poll_id):
    p= get_object_or_404(Poll, pk=poll_id)
    try:
        selected_choice= p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html',{
            'poll':p,
            'error_message':"You didnt select a choice . ",
            })
    else:
        selected_choice.votes+=1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))

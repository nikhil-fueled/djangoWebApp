# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from polls.models import Poll, Choice
from django.core.urlresolvers import reverse

def index(request):
    poll_list = Poll.objects.order_by('-pub_date')[:5]
    context= {'plist':poll_list}
    print context['plist']
    return render(request, 'polls/index.html', context)

def detail(request, poll_id):
    poll= get_object_or_404(Poll, pk=poll_id)
    print poll.question
    return render(request, 'polls/detail.html', {'poll':poll})

def results(request, poll_id):
    return HttpResponse("You're looking at the results of poll %s." % poll_id)

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

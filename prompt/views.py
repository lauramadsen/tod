from django.contrib.auth.decorators import login_required
from django.views.generic.create_update import delete_object
from django.views.generic.list_detail import object_list
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.core.mail import send_mail

from tod.settings import DEBUG, SITE_ROOT, SERVER_EMAIL
from tod.common.decorators import http_response
from tod.prompt.models import Prompt
from tod.prompt.forms import PromptForm
from tod.comment.forms import CommentForm

@login_required
def limited_object_list(*args, **kwargs):
    """Lists prompt object

    TODO - (defer) test that view provides prompt object list
    """
    return object_list(*args, **kwargs)

@login_required
def limited_delete_object(*args, **kwargs):
    """Deletes prompt object
    """
    request = args[0]
    prompt_id = kwargs['object_id']
    prompt = Prompt.objects.get(id = prompt_id)
    if request.user != prompt.owner:
        return HttpResponseRedirect('/prompt/')
    return delete_object(*args, **kwargs)

@login_required
@http_response
def index(request):
    """Index of prompt objects

    TODO - (defer) test that this lists prompt objects
    TODO - (defer) decide between object list and index to display prompts
    """
    prompts = Prompt.objects.exclude(private=True) | Prompt.objects.filter(owner=request.user)
    template = "prompt/index.html"
    return locals()

@login_required
@http_response
def detail(request):
    """Creates a prompt object using form input

    TODO - (defer) move post functionality into Prompt Form
    TODO - (defer) separate form processing into function
    """
    template = "prompt/prompt_detail.html"
    tag_file = file(SITE_ROOT + '/prompt/tags.txt')
    tags = [tag.strip() for tag in tag_file]
    if request.method == 'POST':
        values = request.POST.copy()
        form = PromptForm(values, owner=request.user)
        if form.is_valid():
            current_prompt=form.save()
            for tag in tags:
                if values.get(tag,None):
                    current_prompt.tags.create(tag=tag)
            message =  "%s\n%s\n%s\n%d" % (current_prompt.name, current_prompt.truth, current_prompt.dare, current_prompt.difficulty)
            # try to send mail. If it fails print out an error
            if not DEBUG:
                try:
                    send_mail('Private Prompt Created', message, "prompts@freetruthordare.com", [SERVER_EMAIL], fail_silently=False)
                except:
                    print "Error: could not send mail to admins"

            return HttpResponseRedirect("/prompt/")
        else:
            errors=form.errors
    else:
        form = PromptForm()
    return locals()

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import simplejson
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.template import RequestContext

from tod.comment.forms import CommentForm

def http_response(view):
    """ return a render_to_response adding global context variables
    """
    def _handle_response(request, *args, **kwargs):
        result = view(request, *args, **kwargs)
        # if this is a redirect, just pass it through
        if isinstance(result, HttpResponseRedirect):
            return result
        context = result
        try:
            template = context.pop('template')
        except KeyError:
            raise KeyError("You forgot to specify a template in the context returned by your view")
        return render_to_response(template, context, context_instance=RequestContext(request))
    return _handle_response

from tod.game.models import Game
def active_game(view):
    """ redirect back to the complete page if a game is no longer active
    """
    def _handle_response(request, *args, **kwargs):
        game_id = kwargs.get("game_id")
        game = Game.objects.get(id=game_id)
        if game.status == "completed":
            url = game.get_absolute_url()
            return HttpResponseRedirect(url)
        result = view(request, *args, **kwargs)
        # if this is a redirect, just pass it through
        if isinstance(result, HttpResponseRedirect):
            return result
        context = result
        try:
            template = context.pop('template')
        except KeyError:
            raise KeyError("You forgot to specify a template in the context returned by your view")
        return render_to_response(template, context, context_instance=RequestContext(request))
    return _handle_response

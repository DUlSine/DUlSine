from django import template
from DUlSine.models.DPS import Dimensionnement

from DUlSine.models.dulsine_commons import DIPLOME_CI, DIPLOME_PSC1

register = template.Library()

@register.simple_tag
def badge(dim_id, function_id):
    function_id = int(function_id)
    if function_id < DIPLOME_CI or function_id > DIPLOME_PSC1:
        raise template.TemplateSyntaxError("'badge'(%s) tag second argument should be in [0, 3]" %(function_id))

    # Grab the corresponding Dimensionnement
    dim = Dimensionnement.objects.get(id = dim_id)

    # Compute the answer
    current = dim.nombreIS(function_id)
    required = dim.nombreISMax(function_id)

    # Filter out the badge if the function is not needed
    if(required == 0 or required == 0):
        return u'';

    # Select the right badge
    if(current == 0):
        badge = 'important'
    elif(current < required):
        badge = 'warning'
    else:
        badge = 'success'

    # If the PSC1 is missing that's not an issue
    if(function_id == DIPLOME_PSC1 and current < required):
        badge = 'info'

    return u"<span class=\"badge badge-%s\" dim-id=\"%d\" function-id=\"%s\">%d/%d</span>" %(badge, dim_id, function_id, current, required)

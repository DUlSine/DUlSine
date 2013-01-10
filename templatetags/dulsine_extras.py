from django import template
from DUlSine.models.DPS import Dimensionnement

register = template.Library()

@register.simple_tag
def badge(dim_id, function):
    if not function in ['CI', 'PSE2', 'PSE1', 'PSC1']:
        raise template.TemplateSyntaxError("'badge' tag second argument should be CI, PSE2, PSE1 or PSC1")

    # Grab the corresponding Dimensionnement
    dim = Dimensionnement.objects.get(id = dim_id)

    # Compute the answer
    current = dim.nombreIS(function)
    required = dim.nombreISMax(function)

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
    if(function == 'PSC1' and current < required):
        badge = 'info'

    return u"<span class=\"badge badge-%s\">%d/%d</span>" %(badge, current, required)

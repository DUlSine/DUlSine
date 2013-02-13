from django import template
from DUlSine.models.DPS import Dimensionnement
from DUlSine.models.team import Inscription, Wish

from DUlSine.models.dulsine_commons import NOT_AVAILABLE, DIPLOME_CI, DIPLOME_PSC1, DIPLOME_SECOURS, WISH_ND

register = template.Library()


@register.simple_tag
def badge(dim_id, function_id):
    function_id = int(function_id)
    if function_id < DIPLOME_CI or function_id > DIPLOME_PSC1:
        raise template.TemplateSyntaxError("'badge'(%s) tag second argument should be in [1, 4]" %(function_id))

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

    return u"<span class=\"badge badge-%s\" dim-id=\"%d\">%d/%d</span>" %(badge, dim_id, current, required)



@register.simple_tag
def label(dim_id, user_id):
    # Test if the user is registered in a team
    try:
        subscription = Inscription.objects.get(team__dimensionnement = dim_id, benevole = user_id)
    except Inscription.DoesNotExist:
        # Get the wish if any (should be unique)
        try:
            wish = Wish.objects.get(dimensionnement = dim_id, benevole = user_id)
        except Wish.DoesNotExist:
            class_name = 'default'
            message = '--?--'
        else:
            if wish.wish == WISH_ND:
                class_name = 'inverse'
                message = u"N.D."
            else:
                class_name = 'warning'
                message = u"%s" %(wish.get_wish_display())

    else:
        class_name = 'success'
        message = u"%s" %(subscription.get_fonction_display())

    return "<span class=\"label clickable label-%s\" dim-id=\"%s\" function-id=\"1\">%s</span>" %(class_name, dim_id, message)

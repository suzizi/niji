from django import template
from django.utils.html import escape
from django.contrib.auth.models import User
from urllib.parse import urlencode
from django.core.urlresolvers import reverse
import hashlib

register = template.Library()


@register.simple_tag
def gravatar_url(user, size=48):
    if isinstance(user, User):
        email = user.email
    else:
        email = user

    default = ""

    avatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(
        email.lower().encode('utf-8')
    ).hexdigest() + "?"
    avatar_url += urlencode({'d': default, 's': str(size)})

    return escape(avatar_url)


@register.simple_tag
def change_page(request, page=1):
    rm = request.resolver_match
    kwargs = rm.kwargs.copy()
    if page == 1:
        kwargs.pop('page', None)
    else:
        kwargs.update({'page': page})
    return reverse(
        '%s:%s' % (rm.namespace, rm.url_name),
        args=rm.args,
        kwargs=kwargs,
    )


@register.inclusion_tag('niji/includes/pagination.html', takes_context=True)
def get_pagination(context, first_last_amount=2, before_after_amount=4):
    page_obj = context['page_obj']
    paginator = context['paginator']
    is_paginated = context['is_paginated']
    page_numbers = []

    # Pages before current page
    if page_obj.number > first_last_amount + before_after_amount:
        for i in range(1, first_last_amount + 1):
            page_numbers.append(i)

        if first_last_amount + before_after_amount + 1 != paginator.num_pages:
            page_numbers.append(None)

        for i in range(page_obj.number - before_after_amount, page_obj.number):
            page_numbers.append(i)

    else:
        for i in range(1, page_obj.number):
            page_numbers.append(i)

    # Current page and pages after current page
    if page_obj.number + first_last_amount + before_after_amount < paginator.num_pages:
        for i in range(page_obj.number, page_obj.number + before_after_amount + 1):
            page_numbers.append(i)

        page_numbers.append(None)

        for i in range(paginator.num_pages - first_last_amount + 1, paginator.num_pages + 1):
            page_numbers.append(i)

    else:
        for i in range(page_obj.number, paginator.num_pages + 1):
            page_numbers.append(i)

    return {
        'paginator': paginator,
        'page_obj': page_obj,
        'page_numbers': page_numbers,
        'is_paginated': is_paginated,
        'request': context['request'],
    }

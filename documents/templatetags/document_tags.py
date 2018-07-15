from django import template
from django.utils.encoding import iri_to_uri
from el_pagination import (settings, utils)


register = template.Library()


@register.filter
def has_children(value):
	if value.get_children().exists():
		return True
	else:
		return False


@register.inclusion_tag('documents/show_more_info.html', takes_context=True)
def show_more_info(context, label=None, loading=settings.LOADING, class_name=None):
    data = utils.get_data_from_context(context)
    page = data['page']
    if page.has_next():
        request = context['request']
        page_number = page.next_page_number()
        querystring_key = data['querystring_key']
        querystring = utils.get_querystring_for_page(
            request, page_number, querystring_key,
            default_number=data['default_number'])
        return {
            'label': label,
            'loading': loading,
            'class_name': class_name,
            'path': iri_to_uri(data['override_path'] or request.path),
            'querystring': querystring,
            'querystring_key': querystring_key,
            'request': request,
        }
    return {}

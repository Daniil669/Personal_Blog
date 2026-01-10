from django.contrib.auth import get_user_model
from django import template
from django.utils.html import format_html


register = template.Library()
user_model = get_user_model()

@register.filter
def author_details(author, current_user):
    if not isinstance(author, user_model):
        return ""
    
    if author == current_user:
        return format_html("<strong>{}</strong>", "me")

    if author.first_name and author.last_name:
        name = f"{author.first_name} {author.last_name}"
    else:
        name = f"{author.username}"
    

    if author.email:
        return format_html(
            '<a href="mailto:{}">{}</a>',
            author.email,
            name
        )

    return format_html(name)
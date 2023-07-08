from django.contrib.auth.models import User
from django.utils.html import format_html, format_html_join
from django.template import Library

from blog.models import Post

register = Library()

@register.filter
def author_details(author, current_user):
    if not isinstance(author, User):
        # return empty string as safe default
        return ""

    if author == current_user:
        return format_html("<strong>me</strong>")

    if author.first_name and author.last_name:
        name = f"{author.first_name} {author.last_name}"
    else:
        name = f"{author.username}"

    if author.email:
        prefix = format_html('<a href="mailto:{}">', author.email)
        suffix = format_html("</a>")
    else:
        prefix = ""
        suffix = ""

    return format_html('{}{}{}', prefix, name, suffix)

@register.simple_tag(takes_context=True)
def author_details_tag(context):
  request = context["request"]
  current_user = request.user
  post = context["post"]
  author = post.author

  return author_details(author, current_user)

@register.simple_tag
def row(extra_classes=""):
  return format_html('<div class="row {}">', extra_classes)

@register.simple_tag
def endrow():
  return format_html('</div>')
  
@register.simple_tag
def col(extra_classes='', **kwargs):
  kw = format_html_join(' ', '{}="{}"', kwargs.items())
  return format_html('<div class="col {}" {}>', extra_classes, kw)

@register.simple_tag
def endcol():
  return format_html('</div>')

@register.inclusion_tag("blog/post-list.html")
def recent_posts(excluded_post):
  posts = Post.objects.exclude(pk=excluded_post.pk)[:5]
  return {"title": "Recent Posts", "posts": posts}

from django import template
from django.utils.safestring import mark_safe
import markdown as md

register = template.Library()

@register.filter(name='markdown')
def markdown_format(text):
    """Convert markdown text to HTML"""
    if not text:
        return ''
    
    # Enable extensions for better formatting
    # footnotes: supports [^1] style footnotes with automatic superscript
    # nl2br: converts single newlines to <br> tags (preserves line breaks)
    # extra: includes tables, definitions, fenced code blocks, etc.
    # sane_lists: better list handling
    # smarty: smart quotes and dashes
    return mark_safe(md.markdown(
        text, 
        extensions=[
            'footnotes',
            'nl2br',
            'extra',
            'sane_lists',
            'smarty'  # Converts -- to –, --- to —, "quotes" to "quotes"
        ],
        extension_configs={
            'footnotes': {
                'BACKLINK_TEXT': '',  # Remove the back arrow
            }
        }
    ))

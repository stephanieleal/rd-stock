from django import template
from ..utils import CompanyUtils
import json

register = template.Library()

@register.inclusion_tag('siteApp/wikipedia.html')
def wikipedia(company):
    return {
        "wikipedia": json.loads(company.wikipedia)
}

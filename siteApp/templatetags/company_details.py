from django import template
from ..utils import CompanyUtils

register = template.Library()

@register.inclusion_tag('siteApp/company_details.html')
def company_small_details(company):
    previous = company.getActualStock().value
    return {
        "name": company.name,
        "actual_stock": company.stock,
        "stock_change": CompanyUtils.getPercentIncrement(company.stock, previous),
        "id": company.id,
        "logo": company.logo
}

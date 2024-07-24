from django import template

register = template.Library()

@register.filter
def getProductTotal(obj):
    amount = (obj.product.price)*(obj.quantity)
    return amount

@register.filter
def getPayable(items):
    total=0
    for item in items :
        total= total+((item.product.price)*(item.quantity))
    return total

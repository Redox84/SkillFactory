from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter()
def censor(value):  # Естественно если делать реальный проект слов будет в разы больше.
    words_to_censor = ['6лядь', '6лять', 'cock', 'cunt',  'fuck', 'xyй',
                       'гавнюк', 'долбоёб', 'лошок', 'пидарас', 'шлюха']

    if not isinstance(value, str):  # Проверка, чтобы фильтр цензурирования применялся только к переменным строкового
        # типа.
        raise ValueError("Значение должно быть строкой")

    for word in words_to_censor:
        value = value.replace(word, '*' * len(word))

    return mark_safe(value)
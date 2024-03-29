from django.db.models import Sum
from django.http import HttpResponse
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas

from recipes.models import IngredientRecipe


def generate_pdf_shopping_list(user):
    shopping_list = IngredientRecipe.objects.filter(
        recipe__cart__user=user).values(
            'ingredient__name',
            'ingredient__measurement_unit'
    ).annotate(amount=Sum('amount'))
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = (
        'attachment; filename="shopping_list.pdf"'
    )
    pdfmetrics.registerFont(
        TTFont('DejaVuSerif', 'DejaVuSerif.ttf', 'UTF-8')
    )
    page = Canvas(filename=response)
    page.setFont('DejaVuSerif', 24)
    page.drawString(210, 800, 'Список покупок')
    page.setFont('DejaVuSerif', 16)
    height = 760
    is_page_done = False
    for idx, ingr in enumerate(shopping_list, start=1):
        is_page_done = False
        page.drawString(60, height, text=(
            f'{idx}. {ingr["ingredient__name"]} - {ingr["amount"]} '
            f'{ingr["ingredient__measurement_unit"]}'
        ))
        height -= 30
        if height <= 40:
            page.showPage()
            height = 800
            page.setFont('DejaVuSerif', 16)
            is_page_done = True
    if not is_page_done:
        page.showPage()
    page.save()
    return response

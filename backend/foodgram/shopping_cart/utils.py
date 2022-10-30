import io
import os

from django.http import FileResponse

from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, SimpleDocTemplate, Table, TableStyle

from foodgram import settings


def shopping_cart_pdf(user):
    reciepts = user.is_favorited.select_related('is_favorited').all()
    reciepts_str = ''
    components = {}
    for reciept in reciepts:
        reciepts_str += f'&bull {reciept.is_favorited}<br/>'
        for componet in reciept.is_favorited.components.all():
            if components.get(componet.ingredient):
                components[componet.ingredient] = [
                    components[componet.ingredient][0] + componet.quantity,
                    componet.ingredient.measurement_unit]
            else:
                components[componet.ingredient] = [
                    componet.quantity,
                    componet.ingredient.measurement_unit]
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer)
    pdfmetrics.registerFont(TTFont('Times', os.path.join(
                                settings.STATIC_ROOT,
                                'fonts', 'Calibri Regular.ttf'), 'UTF-8'))
    style = getSampleStyleSheet()
    title = ParagraphStyle('title', fontName="Times",
                           parent=style['Heading1'],
                           alignment=1,
                           spaceAfter=14)
    title_reciepts = Paragraph(text='СПИСОК РЕЦЕПТОВ В ИЗБРАННОМ', style=title)
    list = ParagraphStyle('list', fontName="Times",
                          spaceAfter=14,
                          leading=24,
                          fontSize=14,
                          parent=style['Bullet'],)
    list_reciepts = Paragraph(text=reciepts_str, style=list)
    title_ingredients = Paragraph(text='СПИСОК ИНГРИДЕНТОВ К ПОКУПКЕ',
                                  style=title)
    story = []
    table_style = TableStyle(
        [
            ('FONT', (0,0), (-1,-1), 'Times'),
            ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black,),
            ('BOX', (0,0), (-1,-1), 0.25, colors.black),
        ]
    )
    components_table = [['Наименование ингредиента',
                         'Количество', 'Единица измерений']]
    for name, quantity in components.items():
        components_table.append([name, quantity[0], quantity[1]])
    final_table = Table(components_table, style=table_style)
    story.append(title_reciepts)
    story.append(list_reciepts)
    story.append(title_ingredients)
    story.append(final_table)
    doc.build(story)
    buffer.seek(0)
    buffer.getvalue()
    return FileResponse(buffer, as_attachment=True,
                        filename='List_of_ingredients.pdf')

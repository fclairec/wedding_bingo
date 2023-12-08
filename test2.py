from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table
from reportlab.platypus.tables import TableStyle

inner_table_1 = Table([["Some foo text"]],)
inner_table_2 = Table([["Some bar text"]],)
outer_table = Table([[inner_table_1], [inner_table_2]])

inner_table_1_style = TableStyle([("BOX", (0, 0), (-1, -1), 1, colors.red),])
inner_table_1.setStyle(inner_table_1_style)

inner_table_2_style = TableStyle([("FONTSIZE", (0, 0), (-1, -1), 24),("BOX", (0, 0), (-1, -1), 1, colors.red),])
inner_table_2.setStyle(inner_table_2_style)

outer_table_style = TableStyle([("BOX", (0, 0), (-1, -1), 1, colors.blue),])
outer_table.setStyle(outer_table_style)

elements = []
elements.append(outer_table)

fileName = "test.pdf"
pdf = SimpleDocTemplate(fileName)

pdf.build(elements)
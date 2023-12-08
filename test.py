import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Table, TableStyle, Paragraph, SimpleDocTemplate, Image
from reportlab.lib import colors
from random import sample, choice
import io
from PyPDF2 import PdfReader, PdfWriter

def generate_bingo_matrix(quests):
    # Select 25 random quests
    selected_quests = sample(quests, min(25, len(quests)))

    # Add empty quests if there are fewer than 25
    selected_quests.extend([''] * (25 - len(selected_quests)))

    # Split the quests into a 5x5 matrix
    matrix = [selected_quests[i:i+5] for i in range(0, len(selected_quests), 5)]

    return matrix

def generate_bingo_pdf(matrix, output_path):
    # Calculate the cell size dynamically based on the A4 page dimensions and desired vertical offset
    vertical_offset = 2.5 * inch
    cell_size = (A4[0] - 2 * inch) / 5
    table_height = 5 * cell_size
    available_height = A4[1] - vertical_offset
    if table_height > available_height:
        cell_size = available_height / 5

    # Set up the Paragraph styles for text wrapping
    styles = getSampleStyleSheet()

    # Use a predefined font for the instructions
    instructions_style = styles["BodyText"]
    instructions_style.alignment = 1

    # Define a pastel color palette
    pastel_colors = [
        colors.HexColor("#FEC8D8"),  # Pastel Pink
        colors.HexColor("#FEE2C3"),  # Pastel Orange
        colors.HexColor("#FEF3C7"),  # Pastel Yellow
        colors.HexColor("#D9F1D9"),  # Pastel Green
        colors.HexColor("#D4EEF9"),  # Pastel Blue
    ]

    # Create the data and table style for the bingo matrix
    data = [[Paragraph(cell, instructions_style) for cell in row] for row in matrix]
    table_style = TableStyle([
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('INNERGRID', (0, 0), (-1, -1), 1, colors.black),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
    ])

    # Create the table with proper cell dimensions and apply the table style
    table = Table(data, colWidths=[cell_size] * 5, rowHeights=[cell_size] * 5, spaceBefore=10 * inch, repeatCols=1)
    table.setStyle(table_style)

    # Set random pastel color for each cell in the bingo matrix
    for i in range(5):
        for j in range(5):
            cell_color = choice(pastel_colors)
            table.setStyle(TableStyle([
                ('BACKGROUND', (i, j), (i, j), cell_color),
            ]))

    # Create a PDF with the bingo matrix


    elements = []

    inner_table_1  = Table([[" "]],)
    inner_table_3 = Table([[" "]], )
    inner_table_2 = table

    """inner_table_1_style = TableStyle([("BOX", (0, 0), (-1, -1), 1, colors.red), ])
    inner_table_1.setStyle(inner_table_1_style)"""


    outer_table = Table([[inner_table_1], [inner_table_3], [inner_table_2]])

    """outer_table_style = TableStyle([("BOX", (0, 0), (-1, -1), 1, colors.blue), ])
    outer_table.setStyle(outer_table_style)"""



    elements.append(outer_table)

    pdf_buffer = io.BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=A4)



    doc.build(elements)
    pdf_buffer.seek(0)


    return pdf_buffer

def merge_all_pdfs_in_folder(folder_path, output_path):
    import os
    from PyPDF2 import PdfMerger

    # Get all PDF files in the folder
    pdf_files = [file for file in os.listdir(folder_path) if file.endswith(".pdf")]

    # Merge all the PDF files
    merger = PdfMerger()
    for pdf_file in pdf_files:
        pdf_path = os.path.join(folder_path, pdf_file)
        merger.append(pdf_path)

    # Save the merged PDF to the output path
    with open(output_path, "wb") as output_file:
        merger.write(output_file)

    merger.close()



def generate():
    # Read quests from Excel file
    quests_data = pd.read_excel("quests.xlsx")  # Replace with the path to your Excel file
    quests_per_sprache = [quests_data.iloc[:, 0].tolist(), quests_data.iloc[:, 1].tolist()]

    sprachen = ["de", "fr"]
    nb_per_sprache = [70, 30]
    #nb_per_sprache = [1, 1]
    background_per_sprache = ["quest_background_de.pdf", "quest_background_fr.pdf"]



    for i, sp in enumerate(sprachen):
        nb_bingo_de = nb_per_sprache[i]
        quests = quests_per_sprache[i]
        # Replace with the path to your background PDF


        for j in range(nb_bingo_de):
            output_path = f"output/bingo_{j}_{sp}.pdf"
            bingo_matrix = generate_bingo_matrix(quests)

            # Load the existing background PDF

            # Generate the bingo PDF
            bingo_pdf = generate_bingo_pdf(bingo_matrix, output_path)

            # Merge the bingo PDF with the background PDF
            merged_pdf = PdfWriter()
            bingo_page = PdfReader(bingo_pdf).pages[0]

            background_pdf = PdfReader(background_per_sprache[i])
            background_page = background_pdf.pages[0]

            background_page.merge_page(bingo_page)
            merged_pdf.add_page(background_page)

            # Save the merged PDF to the output path
            with open(output_path, "wb") as output_file:
                merged_pdf.write(output_file)

            bingo_pdf.close()
            bingo_pdf = None
            merged_pdf.close()
            merged_pdf = None
            del bingo_matrix, bingo_pdf, merged_pdf, background_page, output_path, bingo_page




    merge_all_pdfs_in_folder("output", "output/bingo_all.pdf")


if __name__ == "__main__":
    generate()
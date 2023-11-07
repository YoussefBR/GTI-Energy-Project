import nltk
import PyPDF2

pdf = open("2020 RECS_Methodology Report.pdf", 'rb')
pdfreader=PyPDF2.PdfReader(pdf)

numPages = len(pdfreader.pages)
text = []
for pageNum in range(numPages):
    page = pdfreader.pages[pageNum]
    text.append(page.extract_text())

with open("converted_pdf.txt", 'w') as f:
    f.writelines(text)

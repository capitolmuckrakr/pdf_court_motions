#Create pdf motions for each case file we want
#adapted from https://gist.github.com/kzim44/5023021
import os
import StringIO
import unicodecsv
home_dir = os.environ['HOME']
data_dir = home_dir + '/data/court_motions/'
from PyPDF2 import PdfFileWriter, PdfFileReader, PdfFileMerger
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
# Read the signature page so we can add it later as a second page
page2_pdf = data_dir + 'motion_template_page2.pdf'
page2 = PdfFileReader(file(page2_pdf,'rb'))
victims_data = data_dir + 'victims_first_filter.csv'
with open(victims_data, 'rU') as f:
    reader = unicodecsv.reader(f)
    for row in reader:
        case, name = row[0].split("\t") #Excel resaved victims data as one column with a tab delimiter between values. Annoying.
        outputfile = data_dir + case + '.pdf' 
        packet = StringIO.StringIO()
        # create a new PDF with Reportlab
        can = canvas.Canvas(packet, pagesize=letter)
        #can.setLineWidth(.3)
        #can.setFont('Helvetica', 12)
        can.drawString(70, 650, "State of Nevada")
        can.drawString(380, 625, case)
        can.drawString(70, 550, name)
        can.save()
        #move to the beginning of the StringIO buffer
        packet.seek(0)
        new_pdf = PdfFileReader(packet)
        # read your existing PDF
        page1_pdf_template = data_dir + 'motion_template_test1.pdf'
        existing_pdf = PdfFileReader(file(page1_pdf_template, "rb"))
        output = PdfFileWriter()
        # Fill in the form on the existing page with the name and case number
        page = existing_pdf.getPage(0)
        page.mergePage(new_pdf.getPage(0))
        output.addPage(page)
        # write "output" to a real file
        outputStream = file(outputfile, "wb")
        output.write(outputStream)
        outputStream.close()
        # Add the signature page, #adapted from https://www.boxcontrol.net/merge-pdf-files-with-under-10-lines-in-python.html
        merger = PdfFileMerger()
        page1 = PdfFileReader(file(outputfile,'rb'))
        merger.append(page1)
        merger.append(page2)
        merger.write(outputfile)
#Create motions for each case Brian is interested in
import StringIO
import unicodecsv
from PyPDF2 import PdfFileWriter, PdfFileReader, PdfFileMerger
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
# Read the signature page so we can add it later as a second page
page2 = PdfFileReader(file('motion_template_page2.pdf','rb'))
with open('victims_first_filter.csv', 'rU') as f:
    reader = unicodecsv.reader(f)
    for row in reader:
        case, name = row[0].split("\t")
        outputfile = case + '.pdf' 
        packet = StringIO.StringIO()
        # create a new PDF with Reportlab
        can = canvas.Canvas(packet, pagesize=letter)
        can.drawString(70, 650, "State of Nevada")
        can.drawString(380, 625, case)
        can.drawString(70, 550, name)
        can.save()
        #move to the beginning of the StringIO buffer
        packet.seek(0)
        new_pdf = PdfFileReader(packet)
        # read your existing PDF
        existing_pdf = PdfFileReader(file("motion_template_test1.pdf", "rb"))
        output = PdfFileWriter()
        # Fill in the form on the existing page with the name and case number
        page = existing_pdf.getPage(0)
        page.mergePage(new_pdf.getPage(0))
        output.addPage(page)
        # write "output" to a real file
        outputStream = file(outputfile, "wb")
        output.write(outputStream)
        outputStream.close()
        # Add the signature page
        merger = PdfFileMerger()
        page1 = PdfFileReader(file(outputfile,'rb'))
        merger.append(page1)
        merger.append(page2)
        merger.write(outputfile)
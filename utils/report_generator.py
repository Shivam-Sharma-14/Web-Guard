from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter


def generate_pdf_report(alerts,output,target):

    doc=SimpleDocTemplate(output,pagesize=letter)
    styles=getSampleStyleSheet()
    elements=[]

    elements.append(Paragraph("Web Vulnerability Report",styles["Title"]))
    elements.append(Spacer(1,12))
    elements.append(Paragraph("Target: "+target,styles["Normal"]))
    elements.append(Spacer(1,12))


    for a in alerts:

        elements.append(Paragraph(f"<b>Severity:</b> {a['severity']} (Score {a['score']})",styles["Normal"]))
        elements.append(Paragraph(str(a),styles["Normal"]))
        elements.append(Spacer(1,14))


    doc.build(elements)
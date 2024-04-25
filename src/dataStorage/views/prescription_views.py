from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.template.loader import get_template
from dataStorage.models import Prescription
from main.settings import MEDIA_ROOT as media_root
from main.settings import STATICFILES_DIRS as staticfile_dirs
import qrcode, io, base64, os

# def render_to_pdf(template_src, context_dict={}):
#     template = get_template(template_src)
#     html  = template.render(context_dict)
#     result = io.BytesIO()
#     pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
#     if not pdf.err:
#         return HttpResponse(result.getvalue(), content_type='application/pdf')
#     return None

# def render_to_pdf(template_src, context_dict={}):
#     css = [os.path.join(f"{staticfile_dirs[0]}", "css\\bootstrap.css")]
#     options = {
#         'page-size': 'Letter',
#         'margin-top': '0.75in',
#         'margin-right': '0.75in',
#         'margin-bottom': '0.75in',
#         'margin-left': '0.75in',
#         'encoding': "UTF-8",
#         'custom-header': [
#             ('Accept-Encoding', 'gzip')
#         ],
#         'cookie': [
#             ('cookie-empty-value', '""'),
#             ('cookie-name1', 'cookie-value1'),
#             ('cookie-name2', 'cookie-value2'),
#         ],
#         'no-outline': None
#     }
#     template = get_template(template_src)
#     html = template.render(context_dict)
#     return pdfkit.from_file(html, options=options, css=css)

def process_prescription(prescription_id, request=None, mode="html"):
    prescriptionObj = Prescription.objects.get(id = prescription_id)
    qr_code_json = {
        "id": prescriptionObj.id,
        "hash": prescriptionObj.prescription_hash,
        "patient_name": prescriptionObj.patient.user.username,
        "doctor_name": prescriptionObj.doctor.user.username,
        "timestamp": prescriptionObj.createTimestamp.strftime("%d-%B-%Y %I:%M %p"),
    }
    qrCode = qrcode.make(qr_code_json)
    qrCode = qrCode.resize((162, 162))
    qrCodeBytes = io.BytesIO()
    qrCode.save(qrCodeBytes, format='JPEG')
    qrCodeBytes = qrCodeBytes.getvalue()
    qrCode = base64.b64encode(qrCodeBytes).decode('utf-8')

    context = {
        "hospital_name": "Hospital Name",
        "address": "Hospital Address",
        "phone": "Hospital Phone",
        "email": "Hospital Email",
        "patient_name": prescriptionObj.patient.user.username,
        "patient_id": prescriptionObj.patient.id,
        "patient_dob": prescriptionObj.patient.date_of_birth,
        "patient_age": prescriptionObj.patient.age,
        "doctor_name": prescriptionObj.doctor.user.username,
        "department": "-",
        "createTimestamp": prescriptionObj.createTimestamp,
        "medicines": prescriptionObj.prescription_json.get("medicines"),
        "qrCode": qrCode,
    }

    if mode == "html":
        response = render(request, "prescription.html", context)
        return response
    # elif mode == "view":
    #     pdf_response = render_to_pdf("prescription.html", context_dict=context)
    #     filename = f"{prescriptionObj.prescription_hash}.pdf"
    #     content = "attachment; filename='%s'" %(filename)
    #     pdf_response['Content-Disposition'] = content
    #     return HttpResponse(pdf_response, content_type='application/pdf')
    # else:
    #     pdf_response = render_to_pdf("prescription.html", context_dict=context)
    #     response = HttpResponse(pdf_response, content_type='application/pdf')
    #     filename = f"{prescriptionObj.prescription_hash[:8]}.pdf"
    #     content = "attachment; filename='%s'" %(filename)
    #     response['Content-Disposition'] = content
    #     return response

@login_required
def prescription_operation(request):

    if request.method == "GET" and not request.is_ajax():
        prescription_id = request.GET.get("prescription_id")
        return process_prescription(prescription_id, request=request, mode="html")
        # return process_prescription(prescription_id, request=request, mode="view")
        # return process_prescription(prescription_id, request=request, mode="download")
    
    # elif request.method == "POST" and request.is_ajax():
    #     prescription_id = request.POST.get("prescription_id")
    #     mode = request.POST.get("mode")
    #     # return process_prescription(prescription_id, request=request, mode="view")
    #     return process_prescription(prescription_id, request=request, mode=mode)

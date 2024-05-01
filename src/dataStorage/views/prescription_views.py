from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.http.request import QueryDict
from django.template.loader import get_template
from dataStorage.models import Prescription, Doctor, Patient
from main.settings import MEDIA_ROOT as media_root
from main.settings import STATICFILES_DIRS as staticfile_dirs
import qrcode, io, base64, os, json
from datetime import datetime
import hashlib


def hash_dict_content(dictionary):
    json_string = json.dumps(dictionary, sort_keys=True)
    hash_object = hashlib.sha256(json_string.encode())
    return hash_object.hexdigest()

from django.http import HttpResponse
# from django_wkhtmltopdf.views import PDFTemplateView

# class GeneratePDFView(PDFTemplateView):
#     template_name = "prescription.html"
#     filename = 'report.pdf'
#     context_data = {'data': 'Your data to be displayed'}

#     def get_context(self, request):
#         context = super().get_context(request)
#         css_path = [os.path.join(f"{staticfile_dirs[0]}", "css\\bootstrap.css")]
#         context['css_filename'] = css_path
#         return context

# from django.shortcuts import render
# from django.http import HttpResponse
# from django.template.loader import render_to_string
# from weasyprint import HTML, CSS

# def generate_pdf(template_src, css_path, context):
#     html_template = render_to_string(template_src, context)
#     css_file = CSS(css_path)
#     pdf_file = HTML(string=html_template).render(stylesheets=[css_file])
#     response = HttpResponse(pdf_file, content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="document.pdf"'
#     return response

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
        if not request.user.is_staff:
            prescription_idList = Prescription.objects.filter(
                patient__user = request.user
            ).values_list("id", flat=True)
            if int(prescription_id) not in prescription_idList:
                return HttpResponse("<h1>404</h1>")
        return process_prescription(prescription_id, request=request, mode="html")
        # return process_prescription(prescription_id, request=request, mode="view")
        # return process_prescription(prescription_id, request=request, mode="download")
    
    # elif request.method == "POST" and request.is_ajax():
    #     prescription_id = request.POST.get("prescription_id")
    #     mode = request.POST.get("mode")
    #     # return process_prescription(prescription_id, request=request, mode="view")
    #     return process_prescription(prescription_id, request=request, mode=mode)

    elif request.method == "POST" and request.is_ajax() and request.user.is_staff:
        patient_id = request.POST.get("patient_id")
        prescription = request.POST.get("prescription")

        doctorObj = Doctor.objects.get(user_id=request.user.id)
        patientObj = Patient.objects.get(id=int(patient_id))
        prescription_dict = {}
        prescription_dict["medicines"] = json.loads(prescription)
        prescription_dict["doctor_name"] = doctorObj.user.username
        prescription_dict["patient_name"] = patientObj.user.username
        prescription_dict["date_time"] = datetime.now().strftime("%d-%b-%Y %I:%M %p")
        
        prescriptionObj = Prescription.objects.create(
            prescription_hash=hash_dict_content(prescription_dict),
            prescription_json=prescription_dict,
            doctor=doctorObj,
            patient=patientObj,
        )
        return JsonResponse(
            {
                "message": f"Added Prescription of {patient_id} by {request.user.username}",
                "prescription_id": prescriptionObj.id,
            },
            status=200,
        )
    
    elif request.method == "DELETE" and request.is_ajax() and request.user.is_staff:
        prescription_id = QueryDict(request.body).get("prescription_id")
        prescriptionObj = Prescription.objects.get(id=prescription_id)
        prescriptionObj.is_active = False
        prescriptionObj.save()
        return JsonResponse(
            {
                "message": f"Prescription Deleted {prescription_id} by {request.user.username}",
            },
            status=200,
        )

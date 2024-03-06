# views.py

from django.shortcuts import render, HttpResponse
import requests


def smsler_view(request):
    api_url = "http://panel.1sms.com.tr:8080/api/credit/v1"
    username = "test"
    password = "test"

    # Sending GET request to the API endpoint
    response = requests.get(api_url, params={"username": username, "password": password})

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        response_data = response.text.split()  # Split the response into separate words
        return_code = response_data[0]  # First word is the return code
        if return_code == "00":  # Check for successful return code
            balance = response_data[1]  # Second word is the balance
            # Render the balance template with the balance
            return render(request, "app_base/smsfolder/sms_view_main.html", {"balance": balance})
        elif return_code == "93":
            return render(request, "app_base/smsfolder/sms_view_main.html", {"error": "Missing GET parameters"})
        elif return_code == "87":
            return render(request, "app_base/smsfolder/sms_view_main.html", {"error": "Wrong username or password"})
        else:
            return render(request, "app_base/smsfolder/sms_view_main.html", {"error": "Unknown error"})
    else:
        # If the request was unsuccessful, render an error template
        return render(request, "app_base/smsfolder/sms_view_main.html", {"error": "Failed to retrieve balance"})


# views.py

from django.shortcuts import render
import requests

# Assuming these values are constant or managed elsewhere
username = "test"
password = "test"
validity = "2880"  # Example value


# def send_sms(request):
#     if request.method == "POST":
#         api_url = "http://panel.1sms.com.tr:8080/api/smspost/v1"
#         header = request.POST.get("header")
#         message = request.POST.get("message")
#         phone_numbers = request.POST.getlist("phone_numbers")

#         # Constructing XML payload
#         xml_payload = f"""
#             <sms>
#                 <username>{username}</username>
#                 <password>{password}</password>
#                 <header>{header}</header>
#                 <validity>{validity}</validity>

#                 <message>
#                     <gsm>
#                         {''.join([f'<no>{phone}</no>' for phone in phone_numbers])}
#                     </gsm>
#                     <msg><![CDATA[{message}]]></msg>
#                 </message>
#             </sms>
#         """

#         # Sending POST request with XML payload
#         response = requests.post(api_url, data=xml_payload)

#         # # Check if the request was successful (status code 200)
#         # if response.status_code == 200:
#         #     # Assuming the API returns a success message upon successful sending
#         #     return render(request, "app_base/smsfolder/sms_send_success.html")
#         # else:
#         #     # If the request was unsuccessful, render an error template
#         #     return render(request, "app_base/smsfolder/sms_send_error.html", {"error": "Failed to send SMS"})
#         if response.status_code == 200:
#             return HttpResponse(response.content, content_type=response.headers["Content-Type"])
#         else:
#             return HttpResponse(f"Failed to send SMS. Status code: {response.status_code}", status=response.status_code)
#     else:
#         # Handle GET request if needed
#         return render(request, "app_base/smsfolder/sms_send_form.html")


import requests
import pandas as pd
from django.http import HttpResponse
from django.shortcuts import render
from ..forms import UploadFileForm


def send_sms(request):
    if request.method == "POST":
        api_url = "http://panel.1sms.com.tr:8080/api/smspost/v1"
        header = request.POST.get("header")
        message = request.POST.get("message")

        # Check if phone numbers are provided through manual entry
        if "phone_numbers" in request.POST:
            phone_numbers = request.POST.getlist("phone_numbers")
        else:
            # If phone numbers are provided through an Excel file upload
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                excel_data = pd.read_excel(request.FILES["file"])
                phone_numbers = list(excel_data["phonenumber"])

        # Constructing XML payload
        xml_payload = f"""
            <sms>
                <username>{username}</username>
                <password>{password}</password>
                <header>{header}</header>
                <validity>{validity}</validity>
                
                <message>
                    <gsm>
                        {''.join([f'<no>{phone}</no>' for phone in phone_numbers])}
                    </gsm>
                    <msg><![CDATA[{message}]]></msg>
                </message>
            </sms>
        """

        # Sending POST request with XML payload
        response = requests.post(api_url, data=xml_payload)

        if response.status_code == 200:
            return HttpResponse(response.content, content_type=response.headers["Content-Type"])
        else:
            return HttpResponse(f"Failed to send SMS. Status code: {response.status_code}", status=response.status_code)
    else:
        form = UploadFileForm()
        return render(request, "app_base/smsfolder/sms_send_form.html", {"form": form})

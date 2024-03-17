# views.py

from django.shortcuts import render, HttpResponse
import requests
from django.contrib.auth.decorators import login_required, user_passes_test

from django.conf import settings


def is_staff(user):
    return user.is_staff


validity = "2880"  # Example value


@login_required
@user_passes_test(is_staff)
def smsler_view(request):
    api_url = "http://panel.1sms.com.tr:8080/api/credit/v1"
    print(settings.USERNAMESMS)

    # Sending GET request to the API endpoint
    response = requests.get(api_url, params={"username": settings.USERNAMESMS, "password": settings.PASSWORDSMS})

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        response_data = response.text.split()  # Split the response into separate words
        return_code = response_data[0]  # First word is the return code
        if return_code == "00":  # Check for successful return code
            balance = response_data[1]  # Second word is the balance
            request.session["balance"] = balance
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


import requests
import pandas as pd
from django.http import HttpResponse
from django.shortcuts import render
from ..forms import UploadFileForm


from django.template import loader
from django.http import HttpResponse


@login_required
@user_passes_test(is_staff)
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
                <username>{settings.USERNAMESMS}</username>
                <password>{settings.PASSWORDSMS}</password>
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

        # Determine if the SMS was sent successfully
        success = False
        if response.status_code == 200:
            # Assuming response.content contains the status code information
            success = response.content.startswith(b"00")

        # Render the template with appropriate context
        template = loader.get_template("app_base/smsfolder/smsanswer.html")
        api_url = "http://panel.1sms.com.tr:8080/api/credit/v1"

        # Sending GET request to the API endpoint
        response2 = requests.get(api_url, params={"username": settings.USERNAMESMS, "password": settings.PASSWORDSMS})

        # Check if the request was successful (status code 200)
        if response2.status_code == 200:
            response_data = response2.text.split()  # Split the response into separate words
            return_code = response_data[0]  # First word is the return code
            if return_code == "00":  # Check for successful return code
                balance2 = response_data[1]  # Second word is the balance
        # Retrieve the stored balance from session
        balance = request.session.get("balance", 0.0)
        balances = [balance, balance2]
        context = {"success": success, "balances": balances, "status_code": response.status_code, "response_content": response.content.decode("utf-8")}

        return HttpResponse(template.render(context, request))
    else:
        form = UploadFileForm()
        return render(request, "app_base/smsfolder/sms_send_form.html", {"form": form})

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import razorpay
from twilio.rest import Client
import json

from productdata.models import PRODUCTADD
from userdata.models import USERDATA

# Razorpay client
client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


def home(request):
    """Homepage with product listing"""
    try:
        data = PRODUCTADD.objects.all()
        return render(request, 'main.html', {'products': data})
    except Exception as e:
        print("HOME ERROR:", e)
        return render(request, "error.html")


def order(request):
    """Order page → collect user info + create Razorpay order"""
    try:
        if request.method == "POST":
            name = request.POST.get("name")
            if name:
                phone = request.POST.get("phone")
                address = request.POST.get("address")
                state = request.POST.get("state")
                country = request.POST.get("country")
                pincode = request.POST.get("pincode")
                amount = request.POST.get("amount")
                city = request.POST.get("city")
                idsss = request.POST.get('idn')

                if not amount:
                    amount = 500  # default ₹5
                else:
                    amount = float(amount)

                # convert to paise
                amount_paise = int(amount * 100)

                # Create Razorpay order
                order = client.order.create({
                    "amount": amount_paise,
                    "currency": "INR",
                    "payment_capture": 1
                })

                # Pass to template
                context = {
                    "order": order,
                    "key_id": settings.RAZORPAY_KEY_ID,
                    "name": name,
                    "phone": phone,
                    "address": address,
                    "state": state,
                    "country": country,
                    "pincode": pincode,
                    "amount": amount,
                    "city": city,
                    "idss": idsss
                }
                return render(request, "payment.html", context)

        # Fallback: show product order page
        data = request.POST.get('product_id')
        product = get_object_or_404(PRODUCTADD, idsss=data)
        return render(request, "order.html", {"product": product})

    except Exception as e:
        print("ORDER ERROR:", e)
        return render(request, "error.html")


@csrf_exempt
def ordercon(request):
    """Verify payment & save order in DB"""
    try:
        if request.method == "POST":
            data = json.loads(request.body)

            # Verify signature
            client.utility.verify_payment_signature({
                "razorpay_order_id": data["razorpay_order_id"],
                "razorpay_payment_id": data["razorpay_payment_id"],
                "razorpay_signature": data["razorpay_signature"]
            })

            # Save order to DB
            userdata = USERDATA.objects.create(
                name=data["name"],
                phone=data["phone"],
                address=data["address"],
                state=data["state"],
                city=data["city"],
                idno=data["idsss"],
                country=data["country"],
                pincode=data["pincode"],
                amount=float(data["amount"])
            )
            

            return JsonResponse({"status": "success", "order_id": userdata.id})

        return JsonResponse({"status": "invalid"})

    except Exception as e:
        print("PAYMENT ERROR:", e)
        return JsonResponse({"status": "failed"})


def successorder(request, order_id):
    """Show order details after success"""
    try:
        userdata = get_object_or_404(USERDATA, id=order_id)
        return render(request, "success.html", {"order": userdata})
    except Exception as e:
        print("SUCCESSORDER ERROR:", e)
        return render(request, "error.html")


def layout(request):
    try:
        if request.method == 'GET':
            name = request.GET.get('productname')
            data = get_object_or_404(PRODUCTADD, idsss=name)
            return render(request, 'layout.html', {"product": data})
    except Exception as e:
        print("LAYOUT ERROR:", e)
        return render(request, "error.html")


def ordersucesss(request):
        try:
    
            account_sid = "ACbd6b0a20cd540e7693104aa2007b24a0"
            auth_token = "797ac8d384886e530224814580160c3c"

            client = Client(account_sid, auth_token)

            
            message = client.messages.create(
                    body="📦 order ",
                    from_="whatsapp:+14155238886",  # sandbox
                    to="whatsapp:+918235737774"     # must join sandbox
                )

            return render(request, 'ordersucess.html')
        except Exception as e:
            print("TWILIO ERROR:", e)
            return render(request, "error.html", {"error": str(e)})

        
            
            

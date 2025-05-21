from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.utils.timezone import now
from user.models import Cart, CartItem, Product, Sale, Bill, Payment, PayMethod
from django.contrib.auth import get_user_model
import pdfkit

User = get_user_model()


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return JsonResponse({
        'status': 'success',
        'message': f"{product.pro_name} ajouté au panier.",
        'cart_count': cart.get_total_quantity()
    })


@login_required
def cart_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.cart_items.all()
    total = cart.get_total()
    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'user/cart.html', context)


@login_required
def confirm_payment(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = cart.cart_items.all()

    # Si le panier est vide, on redirige
    if not cart_items.exists():
        return redirect('cart_view')

    # Récupère la méthode de paiement
    payment_method = request.POST.get('payment_method', 'Simulé')

    # Créer une nouvelle vente
    sale = Sale.objects.create(user=request.user)

    # Créer les factures pour chaque article du panier
    for cart_item in cart_items:
        Bill.objects.create(
            qty=cart_item.quantity,
            product=cart_item.product,
            sale=sale,
            sale_price=cart_item.get_total_price()
        )

    # Récupérer ou créer la méthode de paiement
    pay_method, _ = PayMethod.objects.get_or_create(pay_name=payment_method)

    # Enregistrer le paiement
    payment = Payment.objects.create(
        amount=cart.get_total(),
        paymethod=pay_method,
        sale=sale
    )

    # Vider le panier
    cart_items.delete()

    # Rediriger vers la page de succès avec l'id du paiement
    return redirect('payment_success', payment_id=payment.id)


@login_required
def payment_success(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    sale = payment.sale
    bills = Bill.objects.filter(sale=sale)

    context = {
        'payment': payment,
        'sale': sale,
        'bills': bills,
        'total': payment.amount,
    }
    return render(request, 'user/payment_success.html', context)


@login_required
def download_invoice(request, invoice_id):
    payment = get_object_or_404(Payment, id=invoice_id)
    sale = payment.sale
    bills = Bill.objects.filter(sale=sale)

    if not bills.exists():
        return HttpResponse("Aucune facture disponible", status=404)

    html_content = render_to_string('user/invoice.html', {
        'payment': payment,
        'sale': sale,
        'bills': bills,
        'now': now()
    })

    try:
        pdf = pdfkit.from_string(html_content, False)
    except OSError:
        config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")
        pdf = pdfkit.from_string(html_content, False, configuration=config)

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="facture_{invoice_id}.pdf"'
    return response

from django.shortcuts import redirect

@login_required
def update_cart(request, cart_item_id, action):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)

    if action == 'increase':
        cart_item.quantity += 1
    elif action == 'decrease' and cart_item.quantity > 1:
        cart_item.quantity -= 1
    cart_item.save()

    return redirect('cart_view')

from django.shortcuts import get_object_or_404, redirect
from user.models import CartItem

@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('cart_view')
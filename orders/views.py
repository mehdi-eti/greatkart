import datetime
import random
from django.shortcuts import redirect, reverse

from carts.models import CartItem
from .forms import OrderForm
from .models import Order


def place_order(request, total=0, quantity=0):
    grand_total = 0
    tax = 0

    current_user = request.user
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()

    if cart_count <= 0:
        return redirect(reverse('store'))

    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity

    tax = (2 * total) / 100
    grand_total = total + tax

    order_form = OrderForm(request.POST or None)

    print(order_form.data)
    print(order_form.errors)

    if request.method == "POST":
        if order_form.is_valid():
            data: Order = Order()
            data.user = current_user
            data.first_name = order_form.cleaned_data['first_name']
            data.last_name = order_form.cleaned_data['last_name']
            data.phone = order_form.cleaned_data['phone']
            data.email = order_form.cleaned_data['email']
            data.address_line_1 = order_form.cleaned_data['address_line_1']
            data.address_line_2 = order_form.cleaned_data['address_line_2']
            data.country = order_form.cleaned_data['country']
            data.state = order_form.cleaned_data['state']
            data.city = order_form.cleaned_data['city']
            data.order_note = order_form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR', None)

            yr = int(datetime.date.today().strftime("%Y"))
            mt = int(datetime.date.today().strftime("%m"))
            dt = int(datetime.date.today().strftime("%d"))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime("%Y%m%d")
            order_number = current_date + str(data.user.id) + str(tax) + str(grand_total)
            order_number = f'{current_date}-{data.user.id}-{tax}-{grand_total}-{random.randint(1, 100000000)}'
            data.order_number = order_number
            data.save()

            return redirect(reverse('check-out'))

    return redirect('check-out')

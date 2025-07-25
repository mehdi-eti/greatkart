from django.shortcuts import get_object_or_404, redirect, render
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

from carts.models import Cart, CartItem
from store.models import Products, Veriation


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    current_user = request.user
    product: Products = Products.objects.get(id=product_id)
    product_variation = []
    ex_var_list = []
    items_id = []

    if request.method == "POST":
        for item in request.POST:
            key = item
            value = request.POST[key]

            try:
                variation = Veriation.objects.get(product=product,
                                                  veriation_category__iexact=key,
                                                  variation_value__iexact=value)
                product_variation.append(variation)
            except Exception as e:
                pass

    if current_user.is_authenticated:
        is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user)
        if is_cart_item_exists.exists():
            cart_item = CartItem.objects.filter(product=product, user=current_user)

            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                items_id.append(item.id)

            if product_variation in ex_var_list:
                index = ex_var_list.index(product_variation)
                item_id = items_id[index]
                item = cart_item.get(product=product, id=item_id)
                item.quantity += 1
                item.save()
            else:
                item = cart_item.create(product=product, user=current_user, quantity=1)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
        else:
            cart_item = CartItem.objects.create(product=product, quantity=1, user=current_user)
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
    else:
        try:
            cart: Cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart: Cart = Cart.objects.create(cart_id=_cart_id(request))
            cart.save()

        is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart)
        if is_cart_item_exists.exists():
            cart_item = CartItem.objects.filter(product=product, cart=cart)

            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                items_id.append(item.id)

            if product_variation in ex_var_list:
                index = ex_var_list.index(product_variation)
                item_id = items_id[index]
                item = cart_item.get(product=product, id=item_id)
                item.quantity += 1
                item.save()
            else:
                item = cart_item.create(product=product, cart=cart, quantity=1)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
        else:
            cart_item = CartItem.objects.create(product=product, quantity=1, cart=cart)
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
    return redirect('cart')


def remove_cart(request, product_id, cart_item_id):
    product = get_object_or_404(Products, id=product_id)

    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart: Cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('/cart')


def remove_cart_items(request, product_id, cart_item_id):
    product = get_object_or_404(Products, id=product_id)

    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)

    cart_item.delete()
    return redirect('/cart')


def cart(request, total=0, quantity=0, cart_items=None):
    tax = 0
    grand_total = 0
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        for cart_item in cart_items:
            total += (cart_item.product.price) * cart_item.quantity
            quantity += cart_item.quantity
        tax = (2 * total) / 100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass

    context = {
        "total": total,
        "quantity": quantity,
        "cart_items": cart_items,
        "tax": tax,
        "grand_total": grand_total
    }

    return render(request, 'App/cart.html', context)


@login_required(login_url='login')
def check_out(request, total=0, quantity=0, cart_items=None):
    tax = 0
    grand_total = 0
    try:
        cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price) * cart_item.quantity
            quantity += cart_item.quantity
        tax = (2 * total) / 100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass

    context = {
        "total": total,
        "quantity": quantity,
        "cart_items": cart_items,
        "tax": tax,
        "grand_total": grand_total
    }
    return render(request, 'store/check-out.html', context)

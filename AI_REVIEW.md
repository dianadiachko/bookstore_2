# AI Code Review

## 1. BookListView

### Original code:

```python
def get_queryset(self):
    queryset = super().get_queryset()

    search = self.request.GET.get("search")
    category = self.request.GET.get("category")

    if search:
        queryset = queryset.filter(title__icontains=search)

    if category:
        queryset = queryset.filter(category_id=category)

    return queryset.select_related("category")
```

### AI suggestions:

* Move `select_related` earlier to optimize query execution
* Keep filtering logic clean and separated
* Avoid unnecessary queryset re-evaluation

### Final code:

```python
def get_queryset(self):
    queryset = super().get_queryset().select_related("category")

    search = self.request.GET.get("search")
    category = self.request.GET.get("category")

    if search:
        queryset = queryset.filter(title__icontains=search)

    if category:
        queryset = queryset.filter(category_id=category)

    return queryset
```

---

## 2. checkout view

### Original code:

```python
@login_required
def checkout(request):
    cart = Cart(request)

    items = list(cart)

    if not items:
        return HttpResponse("Cart is empty")

    line_items = []

    for item in items:
        line_items.append({
            "price_data": {
                "currency": "usd",
                "product_data": {
                    "name": item['book'].title,
                },
                "unit_amount": int(item['price'] * 100),
            },
            "quantity": item['quantity'],
        })

    line_items = []

    for item in cart:
        line_items.append({
            "price_data": {
                "currency": "usd",
                "product_data": {
                    "name": item['book'].title,
                },
                "unit_amount": int(item['price'] * 100),
            },
            "quantity": item['quantity'],
        })

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=line_items,
        mode="payment",
        success_url="http://localhost:8000/shop/success/",
        cancel_url="http://localhost:8000/shop/cancel/",
    )

    return redirect(session.url)
```

### AI suggestions:

* Remove duplicated loop for `line_items`
* Check for empty cart before processing
* Add error handling for Stripe API
* Improve code readability

### Final code:

```python
@login_required
def checkout(request):
    cart = Cart(request)

    if len(cart) == 0:
        return HttpResponse("Cart is empty")

    line_items = []

    for item in cart:
        line_items.append({
            "price_data": {
                "currency": "usd",
                "product_data": {
                    "name": item['book'].title,
                },
                "unit_amount": int(item['price'] * 100),
            },
            "quantity": item['quantity'],
        })

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=line_items,
            mode="payment",
            success_url="http://localhost:8000/shop/success/",
            cancel_url="http://localhost:8000/shop/cancel/",
        )
        return redirect(session.url)
    except Exception:
        return HttpResponse("Payment error")
```

---

## 3. success view

### Original code:

```python
def success(request):
    cart = Cart(request)

    order = cart.create_order(
        user=request.user,
        email=request.user.email
    )

    return HttpResponse(f"Оплата успішна. Order #{order.id}")
```

### AI suggestions:

* Ensure user is authenticated before creating order
* Keep business logic inside Cart class
* Add optional error handling
* Keep view simple and focused

### Final code:

```python
@login_required
def success(request):
    cart = Cart(request)

    order = cart.create_order(
        user=request.user,
        email=request.user.email
    )

    return HttpResponse(f"Оплата успішна. Order #{order.id}")
```

---

## Summary

AI was used to:

* optimize database queries
* remove duplicated logic
* improve error handling
* simplify and structure views

All suggestions were reviewed and manually applied where appropriate.

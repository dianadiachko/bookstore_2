from shop.forms import BookForm


def test_book_form_valid():
    form = BookForm(data={
        "title": "Book",
        "price": 100,
        "stock": 10,
        "year": 2024
    })

    assert form.is_valid()


def test_book_form_invalid():
    form = BookForm(data={
        "title": "",
        "price": -10
    })

    assert not form.is_valid()
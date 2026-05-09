import pytest
from users.forms import RegisterForm

@pytest.mark.django_db
def test_register_form_valid():
    form = RegisterForm(data={
        "username": "testuser",
        "password1": "StrongPass123",
        "password2": "StrongPass123"
    })

    assert form.is_valid()
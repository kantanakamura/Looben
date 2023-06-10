import pytest
from accounts.models import Users

@pytest.mark.django_db
def test_get_full_name():
    # Create a test user
    user = Users.objects.create(username='test_user', email='test@gmail.com')
    user.set_password('testpassword')
    user.save()
    assert Users.objects.count() == 1
        
def one_puls_one_equal_two():
    result = 1 + 1
    assert result == 2

    
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

login_required_for_class = method_decorator(
    login_required(login_url="/users/login"),
    name="dispatch"
)
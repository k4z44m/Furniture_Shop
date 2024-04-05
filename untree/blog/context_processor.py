from .forms import SubscriptionForm


def add_my_form(request):
    return {
        'sub_form': SubscriptionForm()
    }

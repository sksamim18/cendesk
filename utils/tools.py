from django.http import HttpResponseRedirect


def login_required(func):

    def wrapper(request, *args, **kwargs):
        user = request.user
        if user.is_anonymous:
            return HttpResponseRedirect('/user/login/')
        elif not user.active:
            return HttpResponseRedirect('/user/confirm_otp/')
        elif not user.document_submitted:
            return HttpResponseRedirect('/user/upload_docs/')
        else:
            return func(request, *args, **kwargs)
    return wrapper


service_document_mapping = {
    1: ['Pan Card', 'Aadhar Card', 'NOC']
}

RAZORPAY_KEY_ID = 'rzp_live_r2DrsHbnTVFqwp'
RAZORPAY_KEY_SECRET = 'p63h3InhYAFbwLTdSDk9vH83'

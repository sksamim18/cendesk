from django.shortcuts import render
from taxmust.forms import AddContactForm, AddServiceForm, DocumentUploadFileForm
from django.http import HttpResponseRedirect
from taxmust.models import Service, Order, Contact, Document, Note
from django.core.files.storage import FileSystemStorage
from utils.tools import login_required, login_required_admin
from utils import tools
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404


def index(request):
    return render(request, 'taxmust/index.html')


def dashboard(request):
    return render(request, 'taxmust/dashboard.html')


@login_required
def add_contact(request):
    form = AddContactForm()
    if request.method == 'POST':
        form = AddContactForm(request.POST)
        if form.is_valid():
            contact_instance = form.save()
            contact_instance.client = request.user
            contact_instance.save()
            contact_instance_id = contact_instance.id
            url = '/add-service/{}/'.format(contact_instance_id)
            return HttpResponseRedirect(url)
    return render(request, 'taxmust/add_contact.html', {'form': form})


@login_required
def select_service(request, customer_id):
    form = AddServiceForm()
    if request.method == 'POST':
        selected_service = request.POST.get('service_name')
        url = '/update-documents/{}/{}/'.format(
            customer_id, selected_service)
        return HttpResponseRedirect(url)
    return render(request, 'taxmust/select_service.html', {'form': form,
                  'customer_id': customer_id})


# @login_required
# def update_documents(request, customer_id, service_id):
#     form = tools.document_form_mapping.get(service_id)
#     model = tools.document_model_mapping.get(service_id)
#     document_upload_instance = model()

#     context = {}
#     context['form'] = form
#     context['customer_id'] = customer_id
#     context['service_id'] = service_id

#     if request.method == 'POST':
#         for field, image in request.FILES.items():
#             url = upload_single_file(image, field, request)
#             setattr(document_upload_instance, field, url)
#         document_upload_instance.save()
#         order_instance = Order()
#         order_instance.service_id = service_id
#         order_instance.customer = Contact.objects.get(id=customer_id)
#         order_instance.content_object = document_upload_instance
#         order_instance.payment_status = False
#         order_instance.save()
#         url = '/taxmust/payment/{}/'.format(order_instance)
#         return HttpResponseRedirect(url)
#     else:
#         context['form'] = form()
#     return render(request, 'taxmust/document_upload.html', context)


def upload_single_file(file):
    import uuid
    file_ext = file.name.split('.')[-1]
    file_name = file.name.split('.')[-2]
    cleaned_file_name = file_name + ''.join(
        str(uuid.uuid4()).split('-')) + '.' + file_ext
    fs = FileSystemStorage()
    filename = fs.save(cleaned_file_name, file)
    uploaded_file_url = fs.url(filename)
    uploaded_file_url = uploaded_file_url.replace('/media/', '')
    return uploaded_file_url


@login_required
def update_documents(request, customer_id, service_id):
    context = {}
    context['form'] = DocumentUploadFileForm()

    order_instance = Order.objects.filter(
        service_id=service_id,
        customer_id=customer_id
    )
    if order_instance:
        order_instance = order_instance.first()
    else:
        order_instance = Order.objects.create(
            service_id=service_id,
            customer_id=customer_id
        )
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        file = request.FILES.get('file')
        file_url = upload_single_file(file)
        document_instance = Document(
            order=order_instance,
            title=title,
            description=description,
            file=file_url
        )
        document_instance.save()

    uploaded_document_instances = Document.objects.filter(
        order_id=order_instance)

    context['show_checkout'] = len(tools.service_document_mapping.get(
        service_id)) <= uploaded_document_instances.count()
    context['uploaded_documents'] = uploaded_document_instances
    context['required_fields'] = tools.service_document_mapping.get(
        service_id)
    context['customer_id'] = customer_id
    context['service_id'] = service_id

    context['client_name'] = request.user.name
    context['email'] = request.user.email
    context['service'] = order_instance.service.name
    context['phone_number'] = request.user.username
    context['amount'] = str(order_instance.service.amount * 100)
    context['api_key'] = tools.RAZORPAY_KEY_ID

    return render(request, 'taxmust/document_upload.html', context)


@login_required
def view_orders(request):
    context = {}
    context['orders'] = Order.objects.filter(customer__client=request.user)
    return render(request, 'taxmust/view_orders.html', context)


@login_required
def order_details(request, id):
    context = {}
    try:
        context['order'] = Order.objects.get(id=id)
        context['documents'] = context['order'].document_set.all()
    except:
        pass
    return render(request, 'taxmust/order_details.html', context)


@login_required
def checkout(request, order_id):
    context = {}
    order_instance = Order.objects.get(id=order_id)
    context['client_name'] = request.user.name
    context['email'] = request.user.email
    context['service'] = order_instance.service.name
    context['phone_number'] = request.user.username
    context['amount'] = str(order_instance.service.amount * 100)
    context['api_key'] = tools.RAZORPAY_KEY_ID
    context['order'] = order_instance
    return render(request, 'taxmust/checkout.html', context)


@login_required
def payment_success_url(request, order_id):
    try:
        order_instance = Order.objects.get(id=order_id)
        order_instance.payment_status = True
        order_instance.payment_ID = request.POST.get('razorpay_payment_id')
        order_instance.save()
    except Exception:
        pass
    return render(request, 'taxmust/payment_success.html')


@login_required_admin
def administration(request):
    context = {}
    return render(request, 'taxmust/administration.html', context)


@login_required_admin
def view_all_orders(request):
    context = {}
    orders = Order.objects.all().order_by('-id')
    paginator = Paginator(orders, 25)
    page_number = request.GET.get('page')
    context['recent_orders'] = paginator.get_page(page_number)
    return render(request, 'taxmust/recent_orders.html', context)


@login_required_admin
def admin_orders(request, id):
    context = {}
    order = get_object_or_404(Order, id=id)
    context['order'] = order
    context['documents'] = order.documents
    context['note'] = Note.objects.filter(order_id=order.id).first()
    print(context['note'])
    return render(request, 'taxmust/admin_order_details.html', context)


@login_required_admin
def update_status(request, id):
    order = get_object_or_404(Order, id=id)
    status = request.POST.get('status')
    status = {
        'APPLIED': 1,
        'ACCEPTED': 2,
        'IN PROGRESS': 3,
        'COMPLETED': 4
    }[status]
    order.status = status
    order.save()
    return HttpResponseRedirect('/order-details/{}/'.format(order.id))


@login_required_admin
def add_note(request, id):
    order = get_object_or_404(Order, id=id)
    note = request.POST.get('text')
    note_instance = Note(order_id=order.id, text=note)
    note_instance.save()
    return HttpResponseRedirect('/order-details/{}/'.format(order.id))

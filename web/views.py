import json

from django.contrib.auth import authenticate, login, logout
from django.core import serializers
from django.contrib import messages

from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.db.models import Q

from datetime import datetime

from .forms import UserForm, TestDriveForm, CompareForm, PostCarForm, TestDriveForm2, OrderForm
from .models import Car, TestDrive, Order


# Create your views here.
def index(request):
    return render(request, 'web/index.html')


def login_user(request):
    if request.user.is_authenticated:
        return redirect('web:cars')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('web:cars')
            else:
                return render(request, 'web/login.html', {'error_message': 'Your account has not been activated!'})
        else:
            return render(request, 'web/login.html', {'error_message': 'Invalid login'})
    return render(request, 'web/login.html')


def logout_user(request):
    logout(request)
    return redirect('web:index')


def register(request):
    if request.user.is_authenticated:
        return redirect('web:cars')
    uform = UserForm(request.POST or None)
    if uform.is_valid():
        user = uform.save(commit=False)
        username = uform.cleaned_data['username']
        password = uform.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('web:dashboard')

    context = {
        "uform": uform,
    }

    return render(request, 'web/register.html', context)


def cars_page(request, pg=1):

    # Each page has 9 requests. That is fixed.
    start = (pg-1) * 9
    end = start + 9

    car_list = Car.objects.all()[start:end]
    context = {
        'cars': car_list
    }

    return render(request, 'web/cars.html', context)


def car_search(request):
    if request.method == 'GET':
        if request.GET.get('search'):
            search = request.GET.get('search')
        else:
            search = ''
        if request.GET.get('start'):
            start = int(request.GET.get('start'))
        else:
            start = 0
        if request.GET.get('end'):
            end = int(request.GET.get('end'))
        else:
            end = 9

        objs = Car.objects.filter(
            Q(brand__icontains=search) | Q(name__icontains=search)
        )[start:end]
        data = serializers.serialize('json', objs)
        return HttpResponse(data)


def cars(request):
    if request.method == 'GET':
        if request.GET.get('start'):
            start = int(request.GET.get('start'))
        else:
            start = 0
        if request.GET.get('end'):
            end = int(request.GET.get('end'))
        else:
            end = 9
        if request.GET.get('make'):
            make = request.GET.get('make')
            if make == 'all':
                make = ''
        else:
            make = ''
        if request.GET.get('cost_min'):
            cost_min = int(float(request.GET.get('cost_min')))
        else:
            cost_min = 0
        if request.GET.get('cost_max'):
            cost_max = int(float(request.GET.get('cost_max')))
        else:
            cost_max = 999999999
        if request.GET.get('fuel'):
            fuel = request.GET.getlist('fuel')
        else:
            fuel = ['petrol', 'diesel']

        if request.GET.get('location'):
            location = request.GET.get('location')
            if location == 'all':
                location = ''
        else:
            location = ''

        if len(fuel) > 1:
            objs = Car.objects.filter(
                Q(car_make__icontains=make) &
                Q(location__icontains=location) &
                Q(price__gte=cost_min) &
                Q(price__lte=cost_max) &
                (Q(fuel__icontains=fuel[0]) | Q(fuel__icontains=fuel[1]))
            )[start:end]

        else:
            objs = Car.objects.filter(
                car_make__icontains=make,
                location__icontains=location,
                price__gte=cost_min,
                price__lte=cost_max,
                fuel__icontains=fuel[0]
            )[start:end]

    else:
        objs = Car.objects.all()[:9]
    # order = Order.objects.filter(is_delivered__in=[True])
    # carIds = []
    # for orderObj in json.loads(serializers.serialize('json', order)):
    #     carIds.append(orderObj['fields']['car'])
    data = serializers.serialize('json', objs)
    return HttpResponse(data)


def car_details(request, cid):
    if not request.user.is_authenticated:
        return redirect('web:login')
    car = Car.objects.get(pk=cid)
    form = TestDriveForm(initial={'car': car})
    context = {
        'car': car,
        'form': form
    }
    return render(request, 'web/car_details.html', context)


def order_car(request, cid):
    if not request.user.is_authenticated:
        return redirect('web:login')
    user = request.user
    car = Car.objects.get(pk=cid)

    if request.method == 'POST':
        try:
            address = request.POST['address']
            insurance = request.POST['insurance']
            licenseNumber = request.POST['license']
            new = Order(
                user=user,
                car=car,
                amount=car.price,
                address=address,
                license=licenseNumber,
                insurance=insurance
            ).save()
            return HttpResponse("Your order has been placed!")
        except Exception as e:
            return HttpResponse("Uh Oh! Something's wrong! Report to the developer with the following error" +
                                e.__str__())
    return HttpResponseForbidden()


def testdrive(request, cid):
    if not request.user.is_authenticated:
        return redirect('web:login')
    user = request.user
    car = Car.objects.get(pk=cid)

    if request.method == 'POST':
        try:
            date = request.POST['date']
            new_date = datetime.strptime(date, '%d/%m/%Y').strftime('%Y-%m-%d')
            licenseNumber = request.POST['license']
            test = TestDrive(
                user=user,
                car=car,
                time=new_date,
                license=licenseNumber
            ).save()

            HttpResponse("Your testdrive has been booked!")
        except Exception as e:
            return HttpResponse("Uh Oh! Something's wrong! Report to the developer with the following error" +
                                e.__str__())
    return HttpResponseForbidden()


def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('web:login')

    user = request.user
    test = TestDrive.objects.filter(user=user)
    orders = Order.objects.filter(user=user)

    context = {
        'tests': test,
        'orders': orders
    }

    return render(request, 'web/dashboard.html', context)


def post_car(request):
    if not request.user.is_authenticated:
        return redirect('web:login')

    form = PostCarForm(request.POST or None)
    context = {
        'form': form
    }
    if request.method == 'POST':
        form = PostCarForm(request.POST, request.FILES)
        print(form.__dict__)
        print(form.is_valid())
        print(form.errors)
        if form.is_valid():
            print("s")
            user = form.save()
            user.save()
            car_list = Car.objects.all()[1:9]
            context = {
                'cars': car_list
            }
            return render(request, 'web/cars.html', context)
    return render(request, 'web/post_car.html', context)


# def create_test_drive(request):
#     if request.method == 'POST':
#         form = TestDriveForm2(request.POST)
#         if form.is_valid():
#             # Save the new test drive
#             test_drive = form.save(commit=False)
#             test_drive.approved = form.cleaned_data['approved']
#             test_drive.save()
#     else:
#         form = TestDriveForm2()
#
#     return render(request, 'web/create_test_drive.html', {'form': form})


def create_test_drive(request):
    try:
        latest_test_drive = TestDrive.objects.filter(approved__in=[False]).latest('id')
    except:
        car_list = Car.objects.all()[1:9]
        context = {
            'cars': car_list
        }
        return render(request, 'web/cars.html', context)
    form_data = {
        'user': latest_test_drive.user,
        'car': latest_test_drive.car,
        'time': latest_test_drive.time,
        'license': latest_test_drive.license,
        'approved': False  # Set the default value of the approved field to False
    }
    if request.method == 'POST':
        form = TestDriveForm2(request.POST, initial=form_data, instance=latest_test_drive)
        if form.is_valid():
            # Save the new test drive
            test_drive = form.save(commit=False)
            test_drive.approved = form.cleaned_data['approved']
            test_drive.save()
            messages.success(request, 'Test drive approved.')
            car_list = Car.objects.all()[1:9]
            context = {
                'cars': car_list
            }
            return render(request, 'web/cars.html', context)
    else:
        form = TestDriveForm2(initial=form_data)

    return render(request, 'web/create_test_drive.html', {'form': form})


def order_approve(request):
    try:
        latest_order = Order.objects.filter(is_delivered__in=[False]).latest('id')
        print(latest_order.__dict__)
    except:
        messages.warning(request, 'No unapproved orders found.')
        car_list = Car.objects.all()[1:9]
        context = {
            'cars': car_list
        }
        return render(request, 'web/cars.html', context)
    form_data = {
        'user': latest_order.user_id,
        'car': latest_order.car,
        'time': latest_order.order_time,
        'amount': latest_order.amount,
        'address': latest_order.address,
        'insurance': latest_order.insurance,
        'approved_by': latest_order.approved_by,
        'license': latest_order.license,
        'approved': False  # Set the default value of the approved field to False
    }
    if request.method == 'POST':
        form = OrderForm(request.POST, initial=form_data, instance=latest_order)
        if form.is_valid():
            # Save the new test drive
            test_drive = form.save(commit=False)
            test_drive.is_delivered = form.cleaned_data['is_delivered']
            test_drive.approved_by = form.cleaned_data['approved_by']
            test_drive.save()
            messages.success(request, 'Order approved.')
            car_list = Car.objects.all()[1:9]
            context = {
                'cars': car_list
            }
            return render(request, 'web/cars.html', context)
    else:
        form = OrderForm(initial=form_data)

    return render(request, 'web/order_approve.html', {'form': form})


def compare(request):

    form = CompareForm(request.POST or None)
    if request.method == 'POST':
        car1 = int(request.POST['car1'])
        car2 = int(request.POST['car2'])

        car1 = Car.objects.get(pk=car1)
        car2 = Car.objects.get(pk=car2)

        data = {
            'car1_id': car1.id,
            'car1_name': car1.brand + " " + car1.name,
            'car1_pic': car1.picture.url,
            'car1_price': car1.price,
            'car1_seats': car1.seats,
            'car1_tank_capacity': car1.tank_capacity,
            'car1_transmission': car1.transmission,
            'car1_gears': car1.gears,
            'car1_engine_displacement': car1.engine_displacement,
            'car1_power': car1.power,
            'car1_dimensions': car1.dimensions,
            'car2_id': car2.id,
            'car2_name': car2.brand + " " + car2.name,
            'car2_pic': car2.picture.url,
            'car2_price': car2.price,
            'car2_seats': car2.seats,
            'car2_tank_capacity': car2.tank_capacity,
            'car2_transmission': car2.transmission,
            'car2_gears': car2.gears,
            'car2_engine_displacement': car2.engine_displacement,
            'car2_power': car2.power,
            'car2_dimensions': car2.dimensions,
        }

        html = '''
        <table class="table table-bordered" id="cmpTable">
            <tbody>
            <tr>
                <td>
                </td>
                <td>
                    <a href="car/{car1_id}">{car1_name}</a>
                </td>
                <td>
                    <a href="car/{car2_id}">{car2_name}</a>
                </td>
            </tr>
            <tr>
                <td>
                </td>
                <td>
                    <img class="img-fluid" src="{car1_pic}" alt="">
                </td>
                <td>
                    <img class="img-fluid" src="{car2_pic}" alt="">
                </td>
            </tr>
            <tr>
                <td>
                    Price (in &#36;)
                </td>
                <td>
                    {car1_price}
                </td>
                <td>
                    {car2_price}
                </td>
            </tr>
            <tr>
                <td>
                    Seating capacity
                </td>
                <td>
                    {car1_seats}
                </td>
                <td>
                    {car2_seats}
                </td>
            </tr>
            <tr>
                <td>
                    Fuel Tank Capacity (litres)
                </td>
                <td>
                    {car1_tank_capacity}
                </td>
                <td>
                    {car2_tank_capacity}
                </td>
            </tr>
            <tr>
                <td>
                    Transmission type
                </td>
                <td>
                    {car1_transmission}
                </td>
                <td>
                    {car2_transmission}
                </td>
            </tr>
            <tr>
                <td>
                    Gears
                </td>
                <td>
                    {car1_gears}
                </td>
                <td>
                    {car2_gears}
                </td>
            </tr>
            <tr>
                <td>
                    Engine displacement (cc)
                </td>
                <td>
                    {car1_engine_displacement}
                </td>
                <td>
                    {car2_engine_displacement}
                </td>
            </tr>
            <tr>
                <td>
                    Maximum power (PS)
                </td>
                <td>
                    {car1_power}
                </td>
                <td>
                    {car2_power}
                </td>
            </tr>
            <tr>
                <td>
                    Dimensions (mm)
                </td>
                <td>
                    {car1_dimensions}
                </td>
                <td>
                    {car2_dimensions}
                </td>
            </tr>
            <tr>
                <td>
                </td>
                <td>
                <form action="/car/{car1_id}">
                    <input type="submit" class="btn btn-primary" value="Order now" />
                </form>
                </td>
                <td>
                    
                <form action="/car/{car2_id}">
                    <input type="submit" class="btn btn-primary" value="Order now" />
                </form>
                </td>
            </tr>
            </tbody>
        </table>
        '''.format(**data)

        return HttpResponse(html)

    context = {
        'form': form
    }

    return render(request, 'web/compare.html', context)

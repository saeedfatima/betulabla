from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Borehole, Orphan
from .forms import BoreholeForm, OrphanForm, RoleLoginForm
from .decorators import coordinator_required, group_required

# Home Page
def home(request):
    return render(request, 'core/home.html')

# Orphans Listing
def orphans(request):
    qs = Orphan.objects.all()
    return render(request, 'core/orphans.html', {
        'orphans_count': qs.count(),
        'orphans': qs,
    })

# Boreholes Listing & Detail
def boreholes(request):
    qs = Borehole.objects.all()
    lg = request.GET.get('local_government', '')
    bid = request.GET.get('borehole_id', '')
    if lg:
        qs = qs.filter(local_government__name__icontains=lg)
    if bid:
        qs = qs.filter(borehole_id=bid)
    return render(request, 'core/boreholes.html', {
        'boreholes_count': qs.count(),
        'boreholes': qs,
        'local_government_filter': lg,
        'borehole_id_filter': bid,
    })
# coordinator borehole
def coordinator_boreholes(request):
    qs = Borehole.objects.all()
    lg = request.GET.get('local_government', '')
    bid = request.GET.get('borehole_id', '')
    if lg:
        qs = qs.filter(local_government__name__icontains=lg)
    if bid:
        qs = qs.filter(borehole_id=bid)
    return render(request, 'core/coordinator_boreholes.html', {
        'boreholes_count': qs.count(),
        'boreholes': qs,
        'local_government_filter': lg,
        'borehole_id_filter': bid,
    })


def borehole_detail(request, pk):
    bh = get_object_or_404(Borehole, pk=pk)
    return render(request, 'core/borehole_detail.html', {'borehole': bh})

# Borehole CRUD (all require login)
@login_required
def borehole_crud(request):
    return render(request, 'dashboard/borehole_crud.html')

@login_required
def add_orphan(request):
    if request.method == 'POST':
        form = OrphanForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('orphans')
    else:
        form = BoreholeForm
    return render(request, 'dashboard/add_orphan.html', {'form':form})

@login_required
def add_borehole(request):
    if request.method == 'POST':
        form = BoreholeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('boreholes')
    else:
        form = BoreholeForm()
    return render(request, 'dashboard/add_borehole.html', {'form': form})

@login_required
def update_borehole(request, pk):
    bh = get_object_or_404(Borehole, pk=pk)
    if request.method == 'POST':
        form = BoreholeForm(request.POST, request.FILES, instance=bh)
        if form.is_valid():
            form.save()
            return redirect('borehole_detail', pk=pk)
    else:
        form = BoreholeForm(instance=bh)
    return render(request, 'dashboard/update_borehole.html', {'form': form, 'borehole': bh})

@login_required
def delete_borehole(request, pk):
    bh = get_object_or_404(Borehole, pk=pk)
    if request.method == 'POST':
        bh.delete()
        return redirect('boreholes')
    return render(request, 'dashboard/delete_borehole.html', {'borehole': bh})

# Coordinator Login
def coordinator_login(request):
    form = RoleLoginForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user and user.is_active and user.is_staff:
                login(request, user)
                return redirect('coordinator_dashboard')
            messages.error(request, 'Invalid credentials or not a coordinator.')
        else:
            messages.error(request, 'Please correct the errors below.')
    return render(request, 'core/coordinator_login.html', {
        'form': form,
        'role': 'Coordinator',
        'post_url': 'coordinator_login',
    })

# Head Login
def head_login(request):
    form = RoleLoginForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user and user.is_active and user.is_staff:
                login(request, user)
                return redirect('head_dashboard')
            messages.error(request, 'Invalid credentials or not a head.')
        else:
            messages.error(request, 'Please correct the errors below.')
    return render(request, 'core/head_login.html', {
        'form': form,
        'role': 'Head',
        'post_url': 'head_login',
    })

# Coordinator Dashboard (staff only)
@login_required
@coordinator_required
def coordinator_dashboard(request):
    qs = Borehole.objects.all()
    return render(request, 'dashboard/coordinator_dashboard.html', {'boreholes': qs})

# Head Dashboard (group “Head” only)
@login_required
@group_required('Head')
def head_dashboard(request):
    return render(request, 'core/head/dashboard.html', {
        'orphans_count': Orphan.objects.count(),
        'boreholes_count': Borehole.objects.count(),
    })

# Logout
def user_logout(request):
    logout(request)
    return redirect('login')

# Static Pages
def feeding_projects(request):
    return render(request, 'core/feeding_projects.html')

def orphans_crud(request):
    return render(request, 'core/orphans_crud.html')

def coordinator_borehole_detail(request, pk):
     borehole = get_object_or_404(Borehole, pk=pk)
     return render(request, 'core/cooordinator_borehole_detail.html', {'borehole': borehole})


def about(request):
    return render(request, 'core/about.html')

def contact(request):
    return render(request, 'core/contact.html')

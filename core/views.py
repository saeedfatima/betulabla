from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Borehole, Orphan, Report, LocalGovernment, StaffProfile
from .forms import (
    BoreholeForm, UserUpdateForm, StaffProfileUpdateForm,
    OrphanForm, ReportForm
)

# Home Page
def home(request):
   
    return render(request, 'core/main/home.html'

  )

# About & Contact Pages
def about(request):
    return render(request, 'core/main/about.html')

def services(request):
    
    return render(request, 'core/main/services.html')

def contact(request):
    return render(request, 'core/main/contact.html')

# Orphan Views
def orphans(request):
    qs = Orphan.objects.all()
    return render(request, 'core/orphans/orphans.html', {
        'orphans_count': qs.count(),
        'orphans': qs,
    })

def orphans_detail(request, pk):
    orphan = get_object_or_404(Orphan, pk=pk)
    return render(request, 'core/orphans/orphans_detail.html', {'orphan': orphan})

@login_required
def add_orphan(request):
    if request.method == 'POST':
        form = OrphanForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('orphans')
    else:
        form = OrphanForm()
    return render(request, 'core/orphans/add_orphan.html', {'form': form})

@login_required
def update_orphan(request, pk):
    orphan = get_object_or_404(Orphan, pk=pk)
    if request.method == 'POST':
        form = OrphanForm(request.POST, request.FILES, instance=orphan)
        if form.is_valid():
            form.save()
            return redirect('orphans_detail', pk=pk)
    else:
        form = OrphanForm(instance=orphan)
    return render(request, 'core/orphans/add_orphan.html', {'form': form, 'obj': orphan})

@login_required
def delete_orphan(request, pk):
    orphan = get_object_or_404(Orphan, pk=pk)
    if request.method == 'POST':
        orphan.delete()
        return redirect('orphans')
    return render(request, 'core/orphans/delete_orphan.html', {'obj': orphan})

@login_required
def orphans_crud(request):
    
    return render(request, 'core/orphans/orphans_crud.html')

# Borehole Views
def boreholes(request):
    query = request.GET.get('q', '')
    boreholes = Borehole.objects.filter(
        Q(local_government__name__icontains=query) |
        Q(location__icontains=query) |
        Q(borehole_id__icontains=query)
    )
    local_governments = LocalGovernment.objects.all()
    return render(request, 'core/boreholes/boreholes.html', {
        'boreholes_count': boreholes.count(),
        'boreholes': boreholes,
        'local_governments': local_governments,
        'query': query,
    })

def borehole_detail(request, pk):
    bh = get_object_or_404(Borehole, pk=pk)
    return render(request, 'core/boreholes/borehole_detail.html', {'borehole': bh})



@login_required(login_url="login")
def add_borehole(request):
    if request.method == 'POST':
        form = BoreholeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Borehole added successfully!")
            return redirect('boreholes')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = BoreholeForm()
    return render(request, 'core/boreholes/add_borehole.html', {'form': form})


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
    return render(request, 'core/boreholes/add_borehole.html', {'form': form, 'borehole': bh})

@login_required
def delete_borehole(request, pk):
    bh = get_object_or_404(Borehole, pk=pk)
    if request.method == 'POST':
        bh.delete()
        return redirect('boreholes')
    return render(request, 'core/boreholes/delete.html', {'obj': bh})

@login_required
def borehole_crud(request):
    return render(request, 'core/boreholes/borehole_crud.html')

# Login & Register
def loginUser(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'core/login_register/login_register_form.html', {'page': page})

def RegisterUser(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('coordinator_dashboard')
        else:
            messages.error(request, 'An error occurred during registration!')
    return render(request, 'core/login_register/login_register_form.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')

# Profile Views
@login_required
def userprofile(request):
    user = StaffProfile.objects.all()
    return render(request, 'dashboard/profile.html', {'user':request.user})

@login_required
def editUserProfile(request):
    user = request.user
    profile, _ = StaffProfile.objects.get_or_create(user=user)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=user)
        p_form = StaffProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('editUserProfile')
    else:
        u_form = UserUpdateForm(instance=user)
        p_form = StaffProfileUpdateForm(instance=profile)
    return render(request, 'dashboard/edit-profile.html', {
        'u_form': u_form,
        'p_form': p_form
    })

# Feeding Projects
def feeding_projects(request):
    projects = Report.objects.order_by('-created_at')
    return render(request, 'core/main/feeding_projects.html', {'projects': projects})

@login_required
def add_feeding_project(request):
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('feeding_projects')
    else:
        form = ReportForm()
    return render(request, 'core/feeding_projects/add_feeding_project.html', {'form': form})

@login_required
def update_feeding_project(request, pk):
    project = get_object_or_404(Report, pk=pk)
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('feeding_project_detail', pk=pk)
    else:
        form = ReportForm(instance=project)
    return render(request, 'core/feeding_projects/add_feeding_project.html', {'form': form, 'project': project})

@login_required
def delete_feeding_project(request, pk):
    project = get_object_or_404(Report, pk=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('feeding_projects')
    return render(request, 'core/feeding_projects/delete.html', {'obj': project})

def feeding_project_detail(request, pk):
    project = get_object_or_404(Report, pk=pk)
    return render(request, 'core/feeding_projects/feeding_project_detail.html', {'project': project})

@login_required
def feeding_projects_crud(request):
    return render(request, 'core/feeding_projects/feeding_crud.html')

# Dashboards
@login_required(login_url="login")
def dashboard(request):
    borehole = Borehole.objects.all()
    orphan = Orphan.objects.all()
    return render(request, 'dashboard/dashboard.html', {
        'borehole': borehole,
        'boreholes_count':borehole.count,
        'orphans_count':orphan.count,
        'orphan': orphan
    })


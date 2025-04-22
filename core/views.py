from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Borehole, Orphan, Report
from .forms import BoreholeForm, OrphanForm, RoleLoginForm,ReportForm
from .decorators import coordinator_required, group_required
from django.contrib.auth.decorators import login_required
# Home Page
def home(request):
    return render(request, 'core/main/home.html')

# Orphans views
# orphans listing
def orphans(request):
    qs = Orphan.objects.all()
    return render(request, 'core/orphans/orphans.html', {
        'orphans_count': qs.count(),
        'orphans': qs,
    })
# detail of individual orphan
def orphans_detail(request, pk):
    orphan = get_object_or_404(Orphan, id=pk)
    return render(request, 'core/orphans/orphans_detail.html', {'orphan':orphan})

#ADD ORPHANN
@login_required
def add_orphan(request):
    if request.method == 'POST':
        form = OrphanForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('orphans')
    else:
        form = OrphanForm
        return render(request, 'core/orphans/add_orphan.html', {'form':form})

# orphans crud orpations view
@login_required
def orphans_crud(request):
    return render(request, 'core/orphans/orphans_crud.html')

# updating an existing orphan by an authenticated user
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
        return render(request, 'core/orphans/update_orphan.html', {'form':form, 'orphan':orphan})

# delete orphan
@login_required
def delete_orphan(request, pk):
    orphan = get_object_or_404(Orphan, id=pk)
    if request.method == 'POST':
        orphan.delete()
        return redirect('orphans')
    return render(request, 'core/orphans/delete_orphan.html', {'orphan':orphan} )

# boreholes views and crud operations
# Boreholes Listing & Detail
def boreholes(request):
    qs = Borehole.objects.all()
    lg = request.GET.get('local_government', '')
    bid = request.GET.get('borehole_id', '')
    if lg:
        qs = qs.filter(local_government__name__icontains=lg)
    if bid:
        qs = qs.filter(borehole_id=bid)
    return render(request, 'core/boreholes/boreholes.html', {
        'boreholes_count': qs.count(),
        'boreholes': qs,
        'local_government_filter': lg,
        'borehole_id_filter': bid,
    })
#detail of individual borehole
def borehole_detail(request, pk):
    bh = get_object_or_404(Borehole, pk=pk)
    return render(request, 'core/boreholes/borehole_detail.html', {'borehole': bh})
    
#add new borehole bu authenticated user
@login_required
def add_borehole(request):
    if request.method == 'POST':
        form = BoreholeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('boreholes')
    else:
        form = BoreholeForm()
    return render(request, 'core/boreholes/add_borehole.html', {'form': form})
# updating an exisiting borehole by authenticated user
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
    return render(request, 'dashboard/boreholes/update_borehole.html', {'form': form, 'borehole': bh})
# deleting an exisitng borehole by an authenticated user
@login_required
def delete_borehole(request, pk):
    bh = get_object_or_404(Borehole, pk=pk)
    if request.method == 'POST':
        bh.delete()
        return redirect('boreholes')
    return render(request, 'dashboard/boreholes/delete_borehole.html', {'borehole': bh})

        
        
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
                return redirect('coordinator_dashboard')  # Corrected name here
            messages.error(request, 'Invalid credentials or not a coordinator.')
        else:
            messages.error(request, 'Please correct the errors below.')
    return render(request, 'dashboard/coordinator_login.html', {
        'form': form,
        'role': 'coordinator',
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
    return render(request, 'core/login/head_login.html', {
        'form': form,
        'role': 'Head',
        'post_url': 'head_login',
    })

# Coordinator Dashboard (staff only)
@login_required
@coordinator_required
def coordinator_dashboard(request):
    qs = Borehole.objects.all()
    return render(request, 'dashboard/coordinator_Dashboard.html', {'boreholes': qs})



# Borehole CRUD (all require login)
@login_required
def borehole_crud(request):
    return render(request, 'core/boreholes/borehole_crud.html')


# Logout
def user_logout(request):
    logout(request)
    return redirect('coordinator_login')

# feeding projects
def feeding_projects(request):
    projects = Report.objects.order_by('-created_at')
    return render(request, 'core/main/feeding_projects.html', {'projects':projects})



def add_feeding_project(request):
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('feeding_projects')
    else:
        form = ReportForm()
    return render(request, 'core/feeding_projects/add_feeding_project.html', {'form': form})

def update_feeding_project(request, pk):
    project = get_object_or_404(Report, pk=pk)
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('feeding_project_detail', pk=pk)
    else:
        form = ReportForm(instance=project)
    return render(request, 'core/feeding_project/update_feeding_project.html', {'form': form, 'project': project})

def delete_feeding_project(request, pk):
    project = get_object_or_404(Report, pk=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('feeding_projects')
    return render(request, 'core/feeding_project/delete_feeding_project.html', {'project': project})

def feeding_projects_crud(request):
    return render(request, 'core/feeding_projects/feeding_crud.html')

def feeding_project_detail(request, pk):
    project = get_object_or_404(Report, pk=pk)
    return render(request, 'core/feeding_projects/feeding_project_detail.html', {'project':project})


def coordinator_borehole_detail(request, pk):
     borehole = get_object_or_404(Borehole, pk=pk)
     return render(request, 'core/dashboard/coordinator/cooordinator_borehole_detail.html', {'borehole': borehole})


def about(request):
    return render(request, 'core/main/about.html')

def contact(request):
    return render(request, 'core/main/contact.html')

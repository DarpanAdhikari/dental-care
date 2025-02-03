from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm,AdminPasswordChangeForm,AuthenticationForm
from django.contrib.auth import logout, update_session_auth_hash,authenticate,login as auth_login
from django.contrib import messages
from .form import CustomUserChangeForm
from django.contrib.auth.models import Permission, User
from django.contrib.admin.models import LogEntry
from django.contrib.admin.models import ADDITION, CHANGE, DELETION
from django.utils.timezone import now
from accounts.utils.logging_utils import log_action
from django.core.exceptions import PermissionDenied

def redirectUser(user, next=None):
    if not user.is_staff and not user.is_superuser:
        return redirect(next if next else "pat_dashboard")
    elif user.is_staff and not user.is_superuser:
        return redirect(next if next else "doctors_index")
    return redirect(next if next else "admin_index")

def Dashboard(request):
    return redirectUser(request.user)

def login(request):
    if request.user.is_authenticated:
        return redirect('pat_dashboard' if not request.user.is_staff and not request.user.is_superuser else 'admin_index')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['pass1']
        getUser = User.objects.filter(email=username).first()
        original_input = username 
        if getUser:
            username = getUser.username  
        checkuser = authenticate(username=username, password=password)
        if checkuser:
            auth_login(request, checkuser)
            messages.success(request, "Logged In Successfully!!")
            next_url = request.GET.get('next')
            return redirectUser(checkuser, next_url) 
        else:
            messages.error(request, "Bad Credentials!!")
            return render(request, 'accounts/login.html', {
                'username': original_input
            })
    
    return render(request, 'accounts/login.html')

@login_required
@permission_required('auth', raise_exception=True)
def manage_accounts(request):
    users = User.objects.all()
    log_entries = LogEntry.objects.all().select_related('content_type', 'user').order_by('-action_time')[:10]
    return render(request,'users.html',{'users':users,'log':log_entries})

@login_required
@permission_required('auth', raise_exception=True)
def edit_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            obj = form.save()
            log_action(request.user, CHANGE, obj)
            return redirect('manage-accounts')
        else:
            messages.error(request,"please fix given error to fix problem")
    else:
        form = CustomUserChangeForm(instance=user)
    return render(request, 'edit-user.html', {'form': form, 'username': user.username,'user_id':user_id})

@login_required
@permission_required('auth', raise_exception=True)
def delete_user(request,user_id):
    user = get_object_or_404(User, pk=user_id)
    
    if request.method == 'POST':
        user.delete()
        log_action(request.user, DELETION, user)
        messages.success(request, 'User and all related data were successfully deleted!')
        return redirect('manage-accounts')
    related_permissions = Permission.objects.filter(user=user)
    related_data = {
        'user': user,
        'permissions': related_permissions,
    }
    
    return render(request, 'user-delete-confirm.html', related_data)

@login_required
@permission_required('auth', raise_exception=True)
def change_password(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = AdminPasswordChangeForm(user=user, data=request.POST)
        if form.is_valid():
            form.save()
            if request.user == user:
                update_session_auth_hash(request, user)
            messages.success(request, 'Password was successfully updated!')
            return redirect('edit-user', user_id=user_id)
    else:
        form = AdminPasswordChangeForm(user=user)
    
    return render(request, 'change-user-password.html', {'form': form})

@login_required
def user_change_password(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.user != user and not request.user.is_superuser:
        raise PermissionDenied
    if request.method == 'POST':
        form = PasswordChangeForm(user=user, data=request.POST)
        if form.is_valid():
            form.save()
            if request.user == user:
                update_session_auth_hash(request, user) 
            messages.success(request, 'Password was successfully updated!')
            return redirect('edit-user', user_id=user_id)
    else:
        form = PasswordChangeForm(user=user)
    
    return render(request, 'change-user-password.html', {'form': form})

def user_profile(request,user_id):
    user = get_object_or_404(User,username=user_id)
    return render(request,'user-profile.html',{'user':user})

def logout_view(request):
    if request.method == 'POST':
       logout(request)
    return redirect('home')
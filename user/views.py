from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from user.forms import UserForm
from .models import User
from django.db.models import Q
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
     return render(request, 'admin/dashboard.html')

@login_required
def my_profile(request):
     return render(request, 'user/profile.html')
@login_required
def member_list_view(request):
    query = request.GET.get('q')
    if query:
        users = User.objects.filter(
            Q(email__icontains=query) |
            Q(name__icontains=query) |
            Q(roll__icontains=query) |
            Q(department__icontains=query) |
            Q(membership_number__icontains=query)
        )
    else:
        users = User.objects.all()

    context = {
        'users': users,
        'search_query': query
    }
    context = {
        'users': users
    }
    return render(request, 'user/member_list.html', context)
@login_required
def update_user_status(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        # Update the is_active status
        user.is_active = request.POST.get('is_active') == 'on'
        user.save()
        # Redirect back to the user list or any other appropriate page
        return redirect('user_list')

@login_required
def create_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        name = request.POST.get('name')
        roll = request.POST.get('roll')
        department = request.POST.get('department')
        session = request.POST.get('session')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        membership_number = request.POST.get('membership_number')
        user_type = request.POST.get('user_type')
        image = request.FILES.get('image')

        # Check if the required fields are provided
        if email and user_type:
            user = User(
                email=email,
                name=name,
                roll=roll,
                department=department,
                session=session,
                phone_number=phone_number,
                address=address,
                membership_number=membership_number,
                user_type=user_type,
                image=image,
            )
            user.save()
            messages.success(request, 'User created successfully.')
            return redirect('user_list')  
        else:
            messages.error(request, 'Please fill in all required fields.')

    return render(request, 'user/user_registration.html')

@login_required
def delete_user_view(request, user_id):
    user = User.objects.get(id=user_id)
    if user:
        if request.method == 'POST':
            user.delete()
            messages.success(request, 'User deleted successfully.')
            return redirect('user_list') 
    else:
        messages.success(request, 'User not deleted.')
        return redirect('user_list')
    
def update_user_view(request, user_id):
    user = User.objects.filter(id=user_id).first()  # Get user by ID
    if not user:
        messages.error(request, 'User not found.')
        return redirect('user_list')

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)  # Handle file upload
        if form.is_valid():
            form.save()
            messages.success(request, 'User updated successfully.')
            return redirect('user_list')
    else:
        form = UserForm(instance=user)

    context = {
        'form': form,
        'user': user
    }
    return render(request, 'user/update_user.html', context)
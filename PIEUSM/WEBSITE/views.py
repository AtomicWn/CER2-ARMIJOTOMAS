from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Propuesta
from django.conf import settings
from .forms import PropuestaForm, PropuestaEditForm

# Create your views here.

def main_view(request):
    if request.method == "POST":
        propuesta_form = PropuestaForm()
        if 'username' in request.POST:  
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('main_view')
            else:
                messages.error(request, "There Was An Error Logging In, Try Again...")
                return redirect('main_view')
        elif 'nombre' in request.POST:  
            propuesta_form = PropuestaForm(request.POST)
            if propuesta_form.is_valid():
                propuesta = propuesta_form.save(commit=False)
                propuesta.estudiante = request.user.username  
                propuesta.save()
                messages.success(request, "Propuesta creada exitosamente")
                return redirect('main_view')
            else:
                messages.error(request, "Error al crear la propuesta")
        elif 'assign_profesor' in request.POST:  # Handling professor assignment
            propuesta_id = request.POST['assign_profesor']
            propuesta = get_object_or_404(Propuesta, pk=propuesta_id)
            if request.user.groups.filter(name='Profesor').exists() and propuesta.profesor == '':
                propuesta.profesor = request.user.username
                propuesta.save()
                messages.success(request, "Te has asignado como profesor a la propuesta exitosamente")
            else:
                messages.error(request, "No puedes asignarte a esta propuesta")
            return redirect('main_view')
    
    else:
        propuesta_form = PropuestaForm()
    
    tema_filter = request.GET.get('tema', 'Todos los Temas')
    profesor_filter = request.GET.get('profesor', 'Todos los Proyectos')
    
    is_estudiante = request.user.groups.filter(name='Estudiante').exists()
    is_profesor = request.user.groups.filter(name='Profesor').exists()
    is_authenticated = request.user.is_authenticated
    
    if not(is_authenticated) and tema_filter == 'Todos los Temas':
        proyectos = Propuesta.objects.exclude(profesor = '')
    elif not(is_authenticated) and tema_filter != 'Todos los Temas':
        proyectos = Propuesta.objects.exclude(profesor = '').filter(tema=tema_filter)
    elif is_estudiante:
        proyectos = Propuesta.objects.all()
    
    if is_profesor and profesor_filter == 'Todos los Proyectos':
        proyectos = Propuesta.objects.all()
    elif is_profesor and profesor_filter != 'Todos los Proyectos':
        proyectos = Propuesta.objects.filter(profesor = '')
    elif is_estudiante:
        proyectos = Propuesta.objects.all()

    temas = settings.TIPO_TEMAS
    
    
    context = {
        'proyectos': proyectos,
        'temas': temas,
        'selected_tema': tema_filter,
        'propuesta_form': propuesta_form,
        'is_estudiante': is_estudiante,
        'is_profesor': is_profesor,
        'is_authenticated': is_authenticated
    }
    return render(request, 'main.html', context)

def edit_propuesta_view(request, pk):
    propuesta = get_object_or_404(Propuesta, pk=pk, estudiante=request.user.username)
    if request.method == "POST":
        form = PropuestaEditForm(request.POST, instance=propuesta)
        if form.is_valid():
            form.save()
            messages.success(request, "Propuesta actualizada exitosamente")
            return redirect('main_view')
        else:
            messages.error(request, "Error al actualizar la propuesta")
    else:
        form = PropuestaEditForm(instance=propuesta)

    return render(request, 'edit_propuesta.html', {'form': form})

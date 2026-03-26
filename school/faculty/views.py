from django.shortcuts import render
from django.http import Http404
from django.template import TemplateDoesNotExist

def index(request):
    return render(request, 'Home/index.html')

def inbox(request):
    return render(request, 'inbox.html')

def profile(request):
    return render(request, 'profile.html')

def dynamic_template(request, template_name):
    # This allows rendering any HTML template requested directly, useful for migration
    try:
        # Try finding it exactly as requested (e.g., if placed in templates/)
        return render(request, template_name)
    except TemplateDoesNotExist:
        try:
            # Check Home subdirectory where many templates seem to go
            return render(request, f'Home/{template_name}')
        except TemplateDoesNotExist:
            try:
                # Check students subdirectory
                return render(request, f'students/{template_name}')
            except TemplateDoesNotExist:
                raise Http404(f"Template {template_name} does not exist. Please make sure the file is in your templates folder.")
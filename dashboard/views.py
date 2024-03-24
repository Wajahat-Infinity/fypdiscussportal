from django.shortcuts import render
from . models import Notes

def home(request):
    return render(request,'dashboard/home.html')
def notes(request):
    notes=Notes.objects.filter(user=request.user)
    context={
        'notes': notes
    }
    return render(request,'dashboard/notes.html',context)

# Create your views here.

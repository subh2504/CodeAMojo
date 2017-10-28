
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm

from django.core.files.storage import FileSystemStorage


# Imaginary function to handle an uploaded file.
#from somewhere import handle_uploaded_file

def upload_file(request):
    if request.method == 'POST' and request.FILES['file']:
        myfile = request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'extractor/upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'extractor/upload.html')


def handle_uploaded_file(f):
    with open('name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
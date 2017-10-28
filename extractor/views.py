
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm
from .tool import extract
from django.core.files.storage import FileSystemStorage


# Imaginary function to handle an uploaded file.
#from somewhere import handle_uploaded_file

def upload_file(request):
    x={}
    if request.method == 'POST' and request.FILES['file']:
        myfile = request.FILES['file']
        f=save_image(myfile)

        if(f["error"]=="N"):
            ext=extract.extract()
            x=ext.extract_pandata_individual(f["uploaded_file_url"],1)
            print("GVGGG")
            print(x)
            x["uploaded_file_url"]=f["uploaded_file_url"]
            return render(request, 'extractor/success.html', dict(x))
        else:
            x=f
            return render(request, 'extractor/index.html', x)
    return render(request, 'extractor/index.html',x)



def success(request):
    x = {}
    if request.method == 'POST':
        x = request.POST.get['x']
        print(x)
    return render(request, 'extractor/success.html')

def save_image(f):
    try:
        fs = FileSystemStorage()
        filename = fs.save(f.name, f)
        uploaded_file_url = fs.url(filename)
        return {"uploaded_file_url":uploaded_file_url,"error":"N"}
    except:
        return {"uploaded_file_url": None, "error": "Y"}

def handle_uploaded_file(f):
    with open('name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)



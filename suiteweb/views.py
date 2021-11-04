from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.core.cache import cache

from suiteweb.forms import UploadForms, FileFieldForm
from .models import ExampleModel
from .analyser import DeepAnalyser


from deepface import DeepFace
from deepface.commons import functions

def options(request):
    return render(request, "suiteweb/options.html")
    
 
def index(request):
    context = {}
    context['form'] =UploadForms()
    return render(request, "suiteweb/index.html",context)

def process_view(request):
     
    if request.method == "POST":
        form = UploadForms(request.POST, request.FILES)
        if form.is_valid():
            
            (model_choice,metric_choice,detector_choice, img) = get_form_clean_data(form)
            
            saved_model = save(img)
           
            path = settings.MEDIA_ROOT +'/'+ saved_model.model_pic.name

            img_info = DeepAnalyser().analyse(path,
                                              model_choice,
                                              metric_choice,
                                              detector_choice)
           
        else:
            print(form.errors)
        return render(request, 'suiteweb/result.html',{'img': saved_model.model_pic.url, "img_info": img_info})
    return HttpResponse("failure")
    
         

def train_view(request):
    if request.method == "POST":
        
        form = FileFieldForm(request.POST, request.FILES)
        
        if form.is_valid():
            
            (model_choice,metric_choice,detector_choice,_) = get_form_clean_data(form)
            
            model = DeepFace.build_model(model_choice)
            target_size = DeepAnalyser().get_img_size(model_choise=model_choice)
            
            for img in form.files.getlist('images'):
                
                saved_model = save(img)
                path        = settings.MEDIA_ROOT +'/'+ saved_model.model_pic.name
                
                source      = functions.preprocess_face(path, target_size=target_size, detector_backend = detector_choice)
                emb         = model.predict(source)[0].tolist()
                
                cache.set(img.name, emb)
                
    else:
        form = FileFieldForm()
    return render(request, 'suiteweb/train.html',{'form':form})
        
 
def save(img) -> object:
    m = ExampleModel()
    m.model_pic = img
    m.save()
    return m
        
def get_form_clean_data(form):
    model_choice    = form.cleaned_data.get("model_choices")
    metric_choice   = form.cleaned_data.get("metric_choices")
    detector_choice = form.cleaned_data.get("detector_choices")
    img             = form.cleaned_data.get("img")
    return (model_choice,metric_choice,detector_choice, img)
    
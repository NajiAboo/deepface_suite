from django import forms


MODEL_SIZE = {
"VGG-Face": (224,224),
"Facenet": (160,160),
"Facenet512":(160,160),
"OpenFace":(96,96),
"DeepFace":( 152, 152),
"DeepID":(55, 47),
"ArcFace":(112, 112),
"Dlib":(160,160),
}

# Create your views here.
MODEL_CHOICES = (
("VGG-Face","VGG-Face"),
("Facenet","Facenet"),
("Facenet512","Facenet512"),
("OpenFace","OpenFace"),
("DeepFace","DeepFace"),
("DeepID","DeepID"),
("ArcFace","ArcFace"),
)

METRIC_CHOICES =[
    ("cosine","cosine"),
    ("euclidean","euclidean"),
    ("euclidean_l2","euclidean_l2" ),
]

DETECTOR_CHOICES = [
    ('opencv','opencv'),
    ('ssd', 'ssd'),
   ( 'mtcnn', 'mtcnn'),
    ('retinaface','retinaface' )    
]

class UploadForms(forms.Form):
    model_choices       = forms.ChoiceField(choices=MODEL_CHOICES)
    metric_choices      = forms.ChoiceField(choices=METRIC_CHOICES )
    detector_choices    = forms.ChoiceField(choices=DETECTOR_CHOICES )
    img                 = forms.ImageField()
    

class FileFieldForm(forms.Form):
    images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    model_choices       = forms.ChoiceField(choices=MODEL_CHOICES)
    metric_choices      = forms.ChoiceField(choices=METRIC_CHOICES )
    detector_choices    = forms.ChoiceField(choices=DETECTOR_CHOICES )

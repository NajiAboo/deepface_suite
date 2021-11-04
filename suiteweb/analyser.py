from operator import le
from deepface import DeepFace
from deepface.commons import functions, distance
import numpy as np
from django.core.cache import cache

from suiteweb.forms import MODEL_SIZE

class DeepAnalyser():
    
    def analyse(self,img_path,model_choice,metric_choice,detector_choice):
        
        result = DeepFace.analyze(img_path, detector_backend=detector_choice)
        
        name   = self.recogonize(img_path,model_choice,metric_choice,detector_choice)
        
        result_json = {
            "dominant_emotion" : result["dominant_emotion"],
            "age"              : result["age"],
            "gender"           : result["gender"],
            "dominant_race"    : result["dominant_race"],
            "name"             : name
        }
        
        return result_json
    
    def recogonize(self, path,model_choice,metric_choice,detector_choice):
        
        model       = DeepFace.build_model(model_choice)
        target_size = self.get_img_size(model_choice)
        source      = functions.preprocess_face(path, target_size=target_size, detector_backend=detector_choice)
        emb         = model.predict(source)[0].tolist()
        name        = "Unknown_0"
        calc_dist   = 100
        
        for key in cache.keys('*'):
            emb1 = cache.get(key)
            source_emb = np.array(emb1).astype('float')
            dist = distance.findEuclideanDistance(emb, source_emb)
            if dist <=10 and calc_dist > dist:
                calc_dist = dist
                name = key
                
        name = self.parse_name(name)
        return name
    
    def get_img_size(self,model_choise):
        input_size = (160,160)
        input_size = MODEL_SIZE[model_choise]
        return input_size
    
    def parse_name(self, name):
        first_name = name.split('_')[0]
        return first_name
            
            
            
        
        
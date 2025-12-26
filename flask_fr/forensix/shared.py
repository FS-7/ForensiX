from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

class ImageAI:
    def __init__(self, img_ai = "Salesforce/blip-image-captioning-large"):
        self.__img_ai = img_ai
        self.__processor = None
        self.__model = None
        self.__load_model()
    
    def __load_model(self):        
        self.__processor = BlipProcessor.from_pretrained(self.__img_ai)
        self.__model = BlipForConditionalGeneration.from_pretrained(self.__img_ai).to("cuda")
    
    def run(self, raw_image):
        inputs = self.__processor(raw_image, return_tensors="pt").to("cuda")
        out = self.__model.generate(**inputs)
        return self.__processor.decode(out[0], skip_special_tokens=True)

    def isLoaded(self):
        return False if self.model == None else True
    
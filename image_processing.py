from keras.applications.resnet50 import ResNet50
from keras.preprocessing import image
from keras.applications.resnet50 import preprocess_input, decode_predictions
import numpy as np
import os
from glob import glob
from app.models import ImageToText 
from app import db

model = ResNet50(weights='imagenet')

os.chdir("images")
for img_path in glob("*.jpg"):
    img = image.load_img(img_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    preds = model.predict(x)    
    image_to_text = ImageToText(img_path,[label[1] for label in decode_predictions(preds, top=10)[0]])
    db.session.add(image_to_text)
    db.session.commit()
    

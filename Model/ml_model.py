import random
import pickle

from sentence_transformers import SentenceTransformer
from sklearn.multioutput import MultiOutputClassifier
from sklearn.tree import DecisionTreeClassifier
import pandas as pd
import warnings
from Other.config import config
warnings.filterwarnings("ignore")

class MLModel:
    def __init__(self):
        self.embedding_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2', device='mps')
        with open('Data/Models/hair_type_classifier.pkl', 'rb') as f:
            self.hair_model = pickle.load(f)

        with open('Data/Models/skin_type_classifier.pkl', 'rb') as f:
            self.skin_model = pickle.load(f)

        with open('Data/Models/porosity_classifier.pkl', 'rb') as f:
            self.por_model = pickle.load(f)

        with open('Data/Models/hair_type_label_encoder.pkl', 'rb') as f:
            self.hair_classes= pickle.load(f).classes_

        with open('Data/Models/skin_type_label_encoder.pkl', 'rb') as f:
            self.skin_classes = pickle.load(f).classes_

        with open('Data/Models/porosity_label_encoder.pkl', 'rb') as f:
            self.por_classes = pickle.load(f).classes_

            
    
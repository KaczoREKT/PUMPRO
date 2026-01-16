import random

from Other.utils import resource_path
from sklearn.feature_extraction.text import CountVectorizer
from .data import Data
from .ml_model import MLModel
from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputClassifier
from sklearn.tree import DecisionTreeClassifier
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

class Model:
    def __init__(self):
        self.ml_model = MLModel()


    

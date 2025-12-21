import pandas as pd
import joblib
import os
import sys
#配置路径
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
sys.path.append(root_dir)
from utils import config


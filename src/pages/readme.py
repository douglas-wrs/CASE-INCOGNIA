import streamlit as st
import pandas as pd
from pathlib import Path
import os.path

def show():

    my_path = Path(__file__).parent.parent.parent
    path = os.path.join(my_path, "README.md")

    
    readme_md = open(path, 'r').readlines()
    
    st.markdown('\n'.join(readme_md))
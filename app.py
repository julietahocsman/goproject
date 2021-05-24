import streamlit as st
from goproject.preprocesador import get_data, preprocess_data, preproc

preproc('raw_data/dataBackup.json')

'''
    # GoProject: Descubrí la demanda en estacionamientos en la Ciudad de Buenos Aires
    '''

st.markdown('''
    Welcome to Goproject!
    ''')


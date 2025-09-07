import streamlit as st
import random

disease_options = ['Depression', 
                   'Epilepsy', 
                   'Obsessive-Compulsive Disorder (OCD)', 
                   'Parkinson\'s Disease', 
                   'Tremor', 
                   'Chronic Pain']

disease_dict = {
    'Depression': 'Depression',
    'Epilepsy': 'Epilepsy',
    'Obsessive-Compulsive Disorder (OCD)': 'OCD',
    'Parkinson\'s Disease': 'PD',
    'Tremor': 'Tremor',
    'Chronic Pain': 'Pain'
}

if 'disease' not in st.session_state:
    st.session_state['disease'] = random.choice(disease_options)

select_page = st.sidebar.radio("Contents", ["Introduction", "Brain Disease information", "Choose Neurotechnology"])

if select_page == "Introduction":

    st.title("Welcome to NeuroGame!")

    st.markdown("""
    ### Learning Objectives:""")
    
    st.markdown("- Learn about brain diseases, their symptoms, demographics, and any neuroscientific basis behing the disease.")
    st.markdown("- Learn about different neurotechnologies available for the treatment of a disease")
    st.markdown("- Assess various features of a neurotechnology towards making an informed decision on the best possible neurotechnological treatment of a disease")
    
    
    
    st.markdown('''
        <style>
        [data-testid="stMarkdownContainer"] ul{
            padding-left:40px;
        }
        </style>
        ''', unsafe_allow_html=True)

elif select_page == "Brain Disease information":

    disease_assigned = st.session_state['disease']

    st.title(f"You have been assigned the disease: **{disease_assigned}**")
    st.image(f'images_dis/{disease_dict[disease_assigned]}_1.png', width=1600)
    st.image(f'images_dis/{disease_dict[disease_assigned]}_2.png', width=1600)

    if st.button("Choose another disease"):
        st.session_state['disease'] = random.choice(disease_options)
        st.rerun()

else:
    st.title(f"Choose a Neurotechnology that you think is best suited for treatment of {st.session_state['disease']}")

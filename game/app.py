import streamlit as st
import random
import os

base_dir = os.path.dirname(__file__)
pdf_dis_dir = os.path.join(base_dir, "dis_pdfs")
pdf_tech_dir = os.path.join(base_dir, "tech_pdfs")

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

technology_dict = {
    'Deep Brain Stimulation (DBS)': 'DBS',
    'Focused Ultrasound (FUS)': 'FUS',
    'Spinal Cord Stimulation (SCS)': 'SCS',
    'Transcranial Magnetic Stimulation (TMS)': 'TMS',
    'Vagus Nerve Stimulation (VNS)': 'VNS',
    'Magnetic Seizure Therapy (MST)': 'MST',
    'Transcranial Direct Current Stimulation (tDCS)': 'TDCS',
    'Transcutaneous Electrical Nerve Stimulation (TENS)': 'TENS'
}

if 'disease' not in st.session_state:
    st.session_state['disease'] = random.choice(disease_options)

if 'disease_index' not in st.session_state:
    st.session_state['disease_index'] = 0  # start with first image

if 'tech_index' not in st.session_state:
    st.session_state['tech_index'] = 0  # start with first image

if 'selected_tech_list' not in st.session_state:
    st.session_state['selected_tech_list'] = []

if 'player_considerations' not in st.session_state:
    st.session_state['player_considerations'] = ""

def handle_tech_change():
    '''
    Reset the image index when the technology selection changes.
    '''
    st.session_state['tech_index'] = 0

def update_selected_tech_list():
    st.session_state.selected_tech_list = st.session_state.select_tech

def update_player_considerations():
    st.session_state.player_considerations = st.session_state.considerations

select_page = st.sidebar.radio("Contents",
                               ["Introduction",
                                "Brain Disease information", 
                                "Choose Neurotechnology", 
                                "Survey"])

if select_page == "Introduction":

    st.title("Welcome to NeuroGame!")

    st.markdown("""
    ### Learning Objectives:""")
    
    st.markdown("- Learn about brain diseases, their symptoms, demographics, and any neuroscientific basis behind the disease.")
    st.markdown("- Learn about different neurotechnologies available for the treatment of a disease.")
    st.markdown("- Assess various features of a neurotechnology towards making an informed decision on the best possible neurotechnological treatment for a disease.")
    st.markdown("- Share your thoughts and considerations with others behind your choice of neurotechnology for treatment of a disease")
    st.markdown('''
        <style>
        [data-testid="stMarkdownContainer"] ul{
            padding-left:40px;
        }
        </style>
        ''', unsafe_allow_html=True)

    st.markdown(""" ### Gameplay Instructions: """)
    st.markdown("""
                1. You will be randomly assigned a brain disease from a list of 6 diseases.
                2. You can view information about the assigned disease including symptoms, demographics, and neuroscientific basis behind the disease.
                3. You can then choose a neurotechnology that you think is best suited for treatment of the assigned disease from a list of 8 neurotechnologies.
                4. You can view details about each neurotechnology including features, advantages, and disadvantages.
                5. You can select one or more neurotechnologies that you think is best suited for treatment of the assigned disease.
                6. You can then share your thoughts and considerations behind your choice of neurotechnology for treatment of the assigned disease.
                7. Finally, you can proceed to a survey to share your perspectives on neurotechnologies in a clinical context.
                """)

elif select_page == "Brain Disease information":

    disease_assigned = st.session_state['disease']

    st.title(f"You have been assigned the disease: **{disease_assigned}**")

    pdf_files = [
        os.path.join(pdf_dis_dir, f"{disease_dict[disease_assigned]}_1.pdf"),
        os.path.join(pdf_dis_dir, f"{disease_dict[disease_assigned]}_2.pdf")
    ]
    
    max_index = len(pdf_files) - 1
    min_index = 0

    col1, col2 = st.columns([1.6, 1])
    with col1:
        if st.session_state['disease_index'] > min_index:
            if st.button("Front"):
                st.session_state['disease_index'] -= 1
                st.rerun()

    with col2:
        if st.session_state['disease_index'] < max_index:
            if st.button("Back"):
                st.session_state['disease_index'] += 1
                st.rerun()
        

    current_disease_index = st.session_state.disease_index
    st.pdf(pdf_files[current_disease_index], height=600)
    
    if st.button("Choose another disease"):
        st.session_state['disease'] = random.choice(disease_options)
        st.session_state['disease_index'] = 0
        current_disease_index = st.session_state.disease_index
        st.rerun()

elif select_page == "Choose Neurotechnology":

    st.title(f"Choose a Neurotechnology that you think is best suited for treatment of {st.session_state['disease']}")

    col_left, col_right = st.columns([1, 3])

    with col_left:
        view_technology = st.radio("View Neurotechnology details by selecting from the dropdown",
                                ['Deep Brain Stimulation (DBS)',
                                    'Focused Ultrasound (FUS)',
                                    'Spinal Cord Stimulation (SCS)',
                                    'Transcranial Magnetic Stimulation (TMS)',
                                    'Vagus Nerve Stimulation (VNS)',
                                    'Magnetic Seizure Therapy (MST)',
                                    'Transcranial Direct Current Stimulation (tDCS)',
                                    'Transcutaneous Electrical Nerve Stimulation (TENS)'],
                                    on_change=handle_tech_change)

    with col_right:
        if view_technology:

            pdf_files = [
                os.path.join(pdf_tech_dir, f"{technology_dict[view_technology]}_1.pdf"),
                os.path.join(pdf_tech_dir, f"{technology_dict[view_technology]}_2.pdf")
            ]

            max_index = len(pdf_files) - 1
            min_index = 0

            col1, col2 = st.columns([6, 1])
            with col1:
                if st.session_state.tech_index > min_index:
                    if st.button("Front"):
                        st.session_state['tech_index'] -= 1
                        st.rerun()

            with col2:
                if st.session_state.tech_index < max_index:
                    if st.button("Back"):
                        st.session_state['tech_index'] += 1
                        st.rerun()
                

            current_tech_index = st.session_state['tech_index']
            st.pdf(pdf_files[current_tech_index], height=600)
    
    st.header(f"Select the Neurotechnology you think is best suited for treatment of {st.session_state['disease']} (you can select multiple)")
    
    st.multiselect('options',['Deep Brain Stimulation (DBS)',
                    'Focused Ultrasound (FUS)',
                    'Spinal Cord Stimulation (SCS)',
                    'Transcranial Magnetic Stimulation (TMS)',
                    'Vagus Nerve Stimulation (VNS)',
                    'Magnetic Seizure Therapy (MST)',
                    'Transcranial Direct Current Stimulation (tDCS)',
                    'Transcutaneous Electrical Nerve Stimulation (TENS)'],
                    default=st.session_state.selected_tech_list,
                    key='select_tech',
                    on_change=update_selected_tech_list,
                    label_visibility="hidden")
    
    if len(st.session_state['selected_tech_list']) >= 1:

        st.markdown("### Please note any considerations/thoughts behind your choice(s) for sharing with the other participants")
        user_thoughts = st.text_area("",
                                     height=200,
                                     value=st.session_state.player_considerations,
                                     key='considerations',
                                     on_change=update_player_considerations)
    
else:
    # link to survey app
    st.markdown("## Proceed to the Survey to share your feedback about the game and any reflections on what you learnt")
    st.markdown("Click the link below to proceed to the survey:")
    st.markdown("[Survey Link](https://forms.office.com/r/cjZ3H3k9Xf)")
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set page configuration for a professional look
st.set_page_config(
    page_title="Mental Health in Tech EDA",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply seaborn theme matching the notebook
sns.set_theme(style="whitegrid")

@st.cache_data
def load_and_clean_data(file):
    """Loads and cleans the dataset based on the EDA notebook."""
    df = pd.read_csv(file)
    
    # 1. Remove duplicates
    df = df.drop_duplicates()
    
    # 2. Handle Missing Values
    if 'comments' in df.columns:
        df = df.drop(columns=['comments'])
    if 'state' in df.columns:
        df['state'] = df['state'].fillna('Unknown')
    if 'work_interfere' in df.columns:
        df['work_interfere'] = df['work_interfere'].fillna('Not sure')
    if 'self_employed' in df.columns:
        df['self_employed'] = df['self_employed'].fillna('No')
        
    # 3. Clean the 'Gender' column
    if 'Gender' in df.columns:
        df['Gender'] = df['Gender'].str.lower().str.strip()
        male_terms = ['male', 'm', 'make', 'man']
        female_terms = ['female', 'f', 'woman']
        
        def clean_gender(x):
            if x in male_terms:
                return 'Male'
            elif x in female_terms:
                return 'Female'
            else:
                return 'Other'
                
        df['Gender'] = df['Gender'].apply(clean_gender)
        df = df[df["Gender"] != "Other"]
        
    # 4. Filter impossible Age values
    if 'Age' in df.columns:
        df = df[(df['Age'] >= 18) & (df['Age'] <= 100)]
        
    return df

# --- Sidebar Navigation & Data Upload ---
st.sidebar.title("Navigation")
st.sidebar.markdown("Upload your data and navigate through the analysis.")

# File uploader (looks for local clean_mental_health_data.csv first for convenience)
uploaded_file = st.sidebar.file_uploader("Upload 'clean_mental_health_data.csv'", type=["csv"])
local_file = "clean_mental_health_data.csv"

if uploaded_file is not None:
    df = load_and_clean_data(uploaded_file)
elif os.path.exists(local_file):
    df = load_and_clean_data(local_file)
else:
    st.warning("⚠️ Please upload the 'clean_mental_health_data.csv' file in the sidebar to proceed.")
    st.stop()

# Navigation options
page = st.sidebar.radio("Select a section:", [
    "1. Overview & Raw Data", 
    "2. Demographics", 
    "3. Workplace Factors", 
    "4. Health Stigma Analysis"
])

st.sidebar.markdown("---")
st.sidebar.info("Data source: OSMI Mental Health in Tech Survey")

# --- App Content ---
st.title("Mental Health in the Workplace: Tech Industry")
st.markdown("This dashboard explores the intersection of mental health and the workplace within the tech industry, quantifying how mental health issues are perceived, treated, and supported in professional environments.")

if page == "1. Overview & Raw Data":
    st.header("1. Dataset Overview")
    st.markdown("After applying the standard cleaning procedures (removing duplicates, handling missing values, and standardizing text inputs), here is the resulting structured dataset.")
    
    st.write(f"**Cleaned Dataset Shape:** {df.shape[0]} rows and {df.shape[1]} columns.")
    st.dataframe(df.head(15), use_container_width=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Summary Statistics (Numerical)")
        st.dataframe(df.describe())
    with col2:
        st.subheader("Missing Values")
        st.dataframe(df.isnull().sum().rename("Missing Count"))

elif page == "2. Demographics":
    st.header("2. Demographics & Treatment Status")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Distribution of Age")
        fig1, ax1 = plt.subplots(figsize=(8, 5))
        sns.histplot(df['Age'], bins=30, kde=True, color='skyblue', ax=ax1)
        ax1.set_title('Distribution of Age', fontsize=12)
        ax1.set_xlabel('Age')
        ax1.set_ylabel('Frequency')
        st.pyplot(fig1)

    with col2:
        st.subheader("Treatment Seeking Overall")
        fig2, ax2 = plt.subplots(figsize=(8, 5))
        sns.countplot(data=df, x='treatment', hue='treatment', legend=False, ax=ax2, palette="muted")
        ax2.set_title('Count of Individuals Seeking Treatment', fontsize=12)
        ax2.set_xlabel('Sought Treatment?')
        ax2.set_ylabel('Count')
        st.pyplot(fig2)
        
    st.markdown("---")
    
    col3, col4 = st.columns(2)
    with col3:
        st.subheader("Age by Treatment Status")
        fig3, ax3 = plt.subplots(figsize=(8, 5))
        sns.boxplot(data=df, x='treatment', y='Age', hue='treatment', palette='Set3', legend=False, ax=ax3)
        ax3.set_title('Age Distribution by Treatment Status', fontsize=12)
        ax3.set_xlabel('Sought Treatment?')
        st.pyplot(fig3)
        
    with col4:
        st.subheader("Treatment by Gender")
        fig4, ax4 = plt.subplots(figsize=(8, 5))
        sns.countplot(data=df, x='Gender', hue='treatment', palette="Set2", ax=ax4)
        ax4.set_title('Treatment Seeking Behavior by Gender', fontsize=12)
        ax4.legend(title='Sought Treatment')
        st.pyplot(fig4)

elif page == "3. Workplace Factors":
    st.header("3. How Workplace Factors Influence Treatment")
    st.markdown("We look at how employer-provided benefits and anonymity affect an employee's decision to seek mental health treatment.")
    
    # Heatmap first
    st.subheader("Feature Correlation Heatmap")
    df_corr = df.copy()
    df_corr['treatment_num'] = df_corr['treatment'].map({'Yes': 1, 'No': 0})
    df_corr['family_history_num'] = df_corr['family_history'].map({'Yes': 1, 'No': 0})
    df_corr['remote_work_num'] = df_corr['remote_work'].map({'Yes': 1, 'No': 0})
    
    fig_corr, ax_corr = plt.subplots(figsize=(8, 4))
    corr = df_corr[['Age', 'treatment_num', 'family_history_num', 'remote_work_num']].corr()
    sns.heatmap(corr, annot=True, cmap='Reds', fmt=".2f", linewidths=0.5, ax=ax_corr)
    st.pyplot(fig_corr)
    
    st.markdown("---")
    
    order = ['Yes', "Don't know", 'No']
    y_limit = (0, 450)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig1, ax1 = plt.subplots(figsize=(8, 5))
        sns.countplot(data=df, x='benefits', hue='treatment', palette='Set2', order=order, ax=ax1)
        ax1.set_title('Impact of Mental Health Benefits on Seeking Treatment')
        ax1.set_xlabel('Does your employer provide mental health benefits?')
        ax1.set_ylabel('Count')
        ax1.set_ylim(y_limit)
        ax1.legend(title='Sought Treatment', loc='upper right')
        st.pyplot(fig1)
        
    with col2:
        fig2, ax2 = plt.subplots(figsize=(8, 5))
        sns.countplot(data=df, x='anonymity', hue='treatment', palette='Set1', order=order, ax=ax2)
        ax2.set_title('Impact of Anonymity on Seeking Treatment')
        ax2.set_xlabel('Is anonymity protected?')
        ax2.set_ylabel('Count')
        ax2.set_ylim(y_limit)
        ax2.legend(title='Sought Treatment', loc='upper right')
        st.pyplot(fig2)
        
    st.success("**Insight:** Employees who know their company provides mental health benefits, guarantees anonymity, and offers easy medical leave are significantly more likely to seek treatment. Interestingly, a large portion of employees answer 'Not sure' to these questions, and this group tends to have lower treatment rates. This highlights that communicating benefits is just as important as having them.")

elif page == "4. Health Stigma Analysis":
    st.header("4. Mental vs. Physical Health Stigma")
    st.markdown("Does discussing mental health at work carry greater perceived negative consequences than discussing physical health?")
    
    order = ['Yes', 'No', 'Maybe']
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Mental Health Consequences
    sns.countplot(data=df, x='mental_health_consequence', hue='mental_health_consequence', palette='Reds', order=order, legend=False, ax=axes[0])
    axes[0].set_title('Perceived Negative Consequence: Mental Health')
    axes[0].set_xlabel('Would discussing it have negative consequences?')
    axes[0].set_ylabel('Count')
    axes[0].set_ylim(0, 900)
    
    # Physical Health Consequences
    sns.countplot(data=df, x='phys_health_consequence', hue='phys_health_consequence', palette='Blues', order=order, legend=False, ax=axes[1])
    axes[1].set_title('Perceived Negative Consequence: Physical Health')
    axes[1].set_xlabel('Would discussing it have negative consequences?')
    axes[1].set_ylabel('Count')
    axes[1].set_ylim(0, 900)
    
    plt.tight_layout()
    st.pyplot(fig)
    
    st.error("**Insight:** Yes, absolutely. This is usually the most striking finding in this dataset. When comparing mental health consequences to physical health consequences, the vast majority of respondents feel that discussing physical health has 'No' negative consequences. However, when asked about mental health, the responses heavily shift toward 'Maybe' and 'Yes.'")

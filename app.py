import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# --- Page Configuration ---
st.set_page_config(
    page_title="Tech Mental Health Dashboard",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Data Loading & Cleaning ---
@st.cache_data
def load_and_clean_data(file):
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
            if x in male_terms: return 'Male'
            elif x in female_terms: return 'Female'
            else: return 'Other'
                
        df['Gender'] = df['Gender'].apply(clean_gender)
        df = df[df["Gender"] != "Other"]
        
    # 4. Filter impossible Age values
    if 'Age' in df.columns:
        df = df[(df['Age'] >= 18) & (df['Age'] <= 100)]
        
    return df

# --- Sidebar: File Upload & Filters ---
st.sidebar.title("🧠 Settings & Filters")

uploaded_file = st.sidebar.file_uploader("Upload 'clean_mental_health_data.csv'", type=["csv"])
local_file = "clean_mental_health_data.csv"

if uploaded_file is not None:
    df = load_and_clean_data(uploaded_file)
elif os.path.exists(local_file):
    df = load_and_clean_data(local_file)
else:
    st.warning("⚠️ Please upload your 'clean_mental_health_data.csv' dataset in the sidebar to begin.")
    st.stop()

st.sidebar.markdown("---")
st.sidebar.subheader("Filter Data")

# Dynamic Filters
selected_gender = st.sidebar.multiselect("Gender", options=df['Gender'].unique(), default=df['Gender'].unique())
selected_tech = st.sidebar.multiselect("Is a Tech Company?", options=df['tech_company'].unique(), default=df['tech_company'].unique())
selected_remote = st.sidebar.multiselect("Remote Work?", options=df['remote_work'].unique(), default=df['remote_work'].unique())

# Apply Filters
filtered_df = df[
    (df['Gender'].isin(selected_gender)) & 
    (df['tech_company'].isin(selected_tech)) & 
    (df['remote_work'].isin(selected_remote))
]

# --- Main Dashboard Header ---
st.title("Mental Health in the Tech Workplace")
st.markdown("Explore how mental health is perceived, supported, and stigmatized in the tech industry.")

# --- KPI Metrics Row ---
col1, col2, col3, col4 = st.columns(4)
total_respondents = len(filtered_df)
pct_treatment = (filtered_df['treatment'] == 'Yes').mean() * 100 if total_respondents > 0 else 0
avg_age = filtered_df['Age'].mean() if total_respondents > 0 else 0

col1.metric("Total Respondents", f"{total_respondents:,}")
col2.metric("Sought Treatment", f"{pct_treatment:.1f}%")
col3.metric("Average Age", f"{avg_age:.1f} yrs")
col4.metric("Companies represented", filtered_df['no_employees'].nunique(), "Size categories")

st.markdown("---")

# --- Interactive Tabs ---
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Demographics", 
    "🏢 Workplace Factors", 
    "⚖️ Mental vs Physical Stigma", 
    "📁 Raw Data"
])

# Define consistent color mapping for Treatment
treatment_colors = {"Yes": "#EF553B", "No": "#636EFA"}

with tab1:
    st.header("Demographics Overview")
    
    col_a, col_b = st.columns([2, 1])
    
    with col_a:
        # Interactive Histogram with marginal boxplot
        fig_age = px.histogram(
            filtered_df, x="Age", color="treatment", 
            marginal="box", # Adds a boxplot above the histogram
            nbins=30, 
            color_discrete_map=treatment_colors,
            title="Age Distribution by Treatment Status",
            opacity=0.8
        )
        st.plotly_chart(fig_age, use_container_width=True)

    with col_b:
        # Interactive Donut Chart
        gender_counts = filtered_df['Gender'].value_counts().reset_index()
        gender_counts.columns = ['Gender', 'Count']
        fig_gender = px.pie(
            gender_counts, names='Gender', values='Count', 
            hole=0.4, title="Gender Breakdown",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_gender.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_gender, use_container_width=True)

with tab2:
    st.header("How Workplace Factors Influence Treatment")
    
    # Pre-calculate numeric mapping for correlation
    corr_df = filtered_df.copy()
    corr_df['treatment_num'] = corr_df['treatment'].map({'Yes': 1, 'No': 0})
    corr_df['family_history_num'] = corr_df['family_history'].map({'Yes': 1, 'No': 0})
    corr_df['remote_work_num'] = corr_df['remote_work'].map({'Yes': 1, 'No': 0})
    corr_matrix = corr_df[['Age', 'treatment_num', 'family_history_num', 'remote_work_num']].corr()

    col_c, col_d = st.columns([1, 2])
    
    with col_c:
        # Interactive Heatmap
        fig_corr = px.imshow(
            corr_matrix, 
            text_auto=".2f", 
            color_continuous_scale="RdBu_r",
            title="Feature Correlation"
        )
        st.plotly_chart(fig_corr, use_container_width=True)

    with col_d:
        # Grouped bar chart for benefits
        cat_orders = {"benefits": ["Yes", "Don't know", "No"], "anonymity": ["Yes", "Don't know", "No"]}
        
        fig_benefits = px.histogram(
            filtered_df, x="benefits", color="treatment", 
            barmode="group", category_orders=cat_orders,
            color_discrete_map=treatment_colors,
            title="Impact of Mental Health Benefits on Seeking Treatment",
            labels={"benefits": "Does employer provide mental health benefits?"}
        )
        st.plotly_chart(fig_benefits, use_container_width=True)

    # Anonymity impact
    fig_anon = px.histogram(
        filtered_df, x="anonymity", color="treatment", 
        barmode="group", category_orders=cat_orders,
        color_discrete_map=treatment_colors,
        title="Impact of Anonymity Protection on Seeking Treatment",
        labels={"anonymity": "Is anonymity protected?"}
    )
    st.plotly_chart(fig_anon, use_container_width=True)
    
    st.info("💡 **Insight:** Employees who know their company provides benefits and protects anonymity are significantly more likely to seek treatment. Note the large 'Don't know' groups—communicating benefits is just as important as having them.")

with tab3:
    st.header("Comparing Mental vs. Physical Health Stigma")
    st.markdown("Would discussing these health issues with an employer have negative consequences?")
    
    col_e, col_f = st.columns(2)
    stigma_order = {"mental_health_consequence": ["Yes", "Maybe", "No"], "phys_health_consequence": ["Yes", "Maybe", "No"]}
    stigma_colors = {"Yes": "#EF553B", "Maybe": "#FFA15A", "No": "#00CC96"}

    with col_e:
        fig_mental = px.histogram(
            filtered_df, x="mental_health_consequence", color="mental_health_consequence",
            category_orders=stigma_order, color_discrete_map=stigma_colors,
            title="Mental Health Consequences",
            labels={"mental_health_consequence": "Negative Consequences?"}
        )
        fig_mental.update_layout(showlegend=False)
        st.plotly_chart(fig_mental, use_container_width=True)

    with col_f:
        fig_phys = px.histogram(
            filtered_df, x="phys_health_consequence", color="phys_health_consequence",
            category_orders=stigma_order, color_discrete_map=stigma_colors,
            title="Physical Health Consequences",
            labels={"phys_health_consequence": "Negative Consequences?"}
        )
        fig_phys.update_layout(showlegend=False)
        st.plotly_chart(fig_phys, use_container_width=True)
        
    st.info("🚨 **Insight:** There is a stark contrast here. Most respondents feel that discussing *physical* health carries 'No' negative consequence. However, when it comes to *mental* health, the sentiment shifts heavily toward 'Maybe' or 'Yes', indicating a lingering workplace stigma.")

with tab4:
    st.header("Filtered Dataset View")
    st.markdown("View and download the data based on your current sidebar filter selections.")
    st.dataframe(filtered_df, use_container_width=True)
    
    # Download button for the filtered data
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered Data as CSV",
        data=csv,
        file_name='filtered_mental_health_clean_mental_health_data.csv',
        mime='text/csv',
    )

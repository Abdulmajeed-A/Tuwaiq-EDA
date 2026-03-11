---

# 🧠 Mental Health in the Tech Workplace: Exploratory Data Analysis (EDA)

![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat&logo=python)
![Pandas](https://img.shields.io/badge/Pandas-Data_Manipulation-150458?style=flat&logo=pandas)
![Seaborn](https://img.shields.io/badge/Seaborn-Data_Visualization-4E9A06?style=flat)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?style=flat&logo=jupyter)

## 📌 Project Overview
This project explores the intersection of mental health and the workplace within the technology industry. Using the **OSMI (Open Sourcing Mental Illness) Mental Health in Tech Survey**, this Exploratory Data Analysis (EDA) aims to quantify how mental health issues are perceived, treated, and supported in professional environments. 

The analysis investigates factors that influence employees to seek treatment and highlights the disparity in workplace stigma between mental and physical health.

## 📊 Dataset Information
* **Source:** [Kaggle - OSMI Mental Health in Tech Survey](https://www.kaggle.com/datasets/osmi/mental-health-in-tech-survey)
* **Description:** The dataset contains survey responses regarding mental health status, workplace benefits, and employer attitudes.
* **Size:** 1,259 rows and 27 columns (before cleaning).

### Key Features Analyzed:
* `Age` & `Gender` (Demographics)
* `treatment` (Has the respondent sought treatment?)
* `benefits`, `anonymity`, `leave` (Workplace support structures)
* `mental_health_consequence` vs. `phys_health_consequence` (Perceived stigma)

## 🧹 Data Cleaning & Preprocessing
To ensure accurate analysis, the raw data underwent rigorous cleaning:
1. **Duplicate Removal:** Dropped duplicate survey entries.
2. **Missing Value Handling:**
   * Dropped the `comments` column due to excessive missing data.
   * Filled missing `state` values with `'Unknown'`.
   * Filled missing `work_interfere` values with `'Not sure'`.
   * Filled missing `self_employed` values with the mode (`'No'`).
3. **Gender Standardization:** Cleaned messy, free-text gender inputs by mapping them to standardized `'Male'` and `'Female'` categories.
4. **Age Filtering:** Removed outliers by restricting the dataset to realistic working ages (18 to 100 years old).
5. **Export:** Saved the processed dataset as `clean_data.csv` for analysis.

## 📈 Exploratory Data Analysis & Visualizations
The project features several visualizations to uncover patterns in the data:
* **Univariate Analysis:** Age distribution histograms and treatment-seeking count plots.
* **Bivariate Analysis:** Boxplots mapping Age against Treatment Status, and bar charts showing Treatment by Gender.
* **Multivariate Analysis:** Correlation heatmaps (converting categorical variables like family history and remote work into numeric values) to find relationships between variables.

## 💡 Key Findings & Insights

Based on the research questions posed in the analysis, we discovered the following:

**1. How do workplace factors influence whether employees seek mental health treatment?**
> **Insight:** Employees who are *aware* that their company provides mental health benefits, guarantees anonymity, and offers easy medical leave are significantly more likely to seek treatment. A large portion of employees answered "Not sure" to these questions, and this group showed lower treatment rates. **Conclusion:** Having benefits is not enough; employers must actively communicate them to their workforce.

**2. Does discussing mental health at work carry greater perceived negative consequences than discussing physical health?**
> **Insight:** Absolutely. The data reveals a striking disparity. When asked about physical health, the vast majority of respondents feel there are **"No"** negative consequences to discussing it with an employer. However, when asked the same question about mental health, responses shift heavily toward **"Maybe"** and **"Yes,"** indicating a strong lingering stigma around mental health in the tech industry.

## 📊 Streamlit dashboard 
**Link** https://tuwaiq-eda-rj6qde9d9uu6xrjsxmzfbv.streamlit.app/

## 🚀 How to Run the Project Locally

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/yourusername/mental-health-tech-eda.git](https://github.com/yourusername/mental-health-tech-eda.git)
   cd mental-health-tech-eda

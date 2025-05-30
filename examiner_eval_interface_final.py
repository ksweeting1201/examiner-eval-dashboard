import pandas as pd
import streamlit as st

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("final_roles_all_missing_filled.csv")

df = load_data()

# Convert Rating to numeric
df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')

st.title("Examiner Evaluation Lookup")

# Sidebar filters
with st.sidebar:
    st.header("🔍 Filter Options")
    examiner_name = st.text_input("Search Examiner Name")
    examiner_list = sorted(df['Examiner'].dropna().unique().tolist())
    selected_examiner = st.selectbox("Or Select from Examiner List", ["None"] + examiner_list)
    selected_role = st.selectbox("Filter by Examiner Role", ["All"] + sorted(df['Examiner Role'].dropna().unique().tolist()))
    selected_rating = st.selectbox("Filter by Rating", ["All"] + sorted(df['Rating'].dropna().unique().tolist()))
    selected_source = st.selectbox("Filter by Source File", ["All"] + sorted(df['Source_File'].dropna().unique().tolist()))

# Apply filters
filtered_df = pd.DataFrame()

if examiner_name:
    filtered_df = df[df['Examiner'].str.contains(examiner_name, case=False, na=False)]
elif selected_examiner != "None":
    filtered_df = df[df['Examiner'] == selected_examiner]

if not filtered_df.empty:
    if selected_role != "All":
        filtered_df = filtered_df[filtered_df['Examiner Role'] == selected_role]

    if selected_rating != "All":
        filtered_df = filtered_df[filtered_df['Rating'] == selected_rating]

    if selected_source != "All":
        filtered_df = filtered_df[filtered_df['Source_File'] == selected_source]

st.subheader("📋 Filtered Evaluations")
if not filtered_df.empty:
    st.dataframe(filtered_df)
else:
    st.info("No examiner selected or matching results.")

# Summary stats
st.subheader("📊 Summary Statistics")
eval_counts = df['Examiner'].value_counts().reset_index()
eval_counts.columns = ['Examiner', 'Evaluation Count']
st.write("Top 10 Examiners by Evaluation Count:")
st.dataframe(eval_counts.head(10))

ratings_summary = df.groupby('Examiner').agg(
    Count=('Rating', 'count'),
    Avg_Rating=('Rating', 'mean')
).query('Count >= 3')

st.write("🔝 Top Rated Examiners (min 3 evals):")
st.dataframe(ratings_summary.sort_values('Avg_Rating', ascending=False).head(10))

st.write("🔻 Lowest Rated Examiners (min 3 evals):")
st.dataframe(ratings_summary.sort_values('Avg_Rating', ascending=True).head(10))

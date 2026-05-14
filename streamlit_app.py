# Counting the Uncounted: GBV Visibility Index in Kenya
# Streamlit App

# Import libraries used
import streamlit as st
import json
from matplotlib import pyplot as plt
from matplotlib import patches as mpatches


st.set_page_config(
    page_title="Counting the Uncounted",
    page_icon=":)",
    layout="wide"
)

# Cache the data loading to run once
@st.cache_data
def load_data():
    with open("Outputs/visibility_scores.json", "r") as f:
        return json.load(f)
    
visibility_data = load_data()

# Header
st.title("Counting the ~~Uncounted~~")
st.subheader("A GBV Visibility Index Across Kenya's 44 Counties")

# Brief overview of the project
st.markdown("""
> **Every year in Kenya, thousands of women are assaulted, 
> tell no one in athority and are never counted, and yet,
> we make policy decisions based on the women we did count.**

According to the Kenya Demographic and Health Survey, 15.8% 
of women aged 15–49 experienced physical violence in the last 
12 months, and 13.0% had ever experienced sexual violence at 
county level.
(Kenya National Bureau of Statistics [KNBS], 2023).

This project compares two government data sources to calculate a 
**GBV Visibility Score** for 44 counties in Kenya:

- **KDHS 2022** (KNBS, 2023) — what women reported *experiencing*, 
  county level
- **NCRC 2021 Crime Yearbook** (NCRC, 2022) — what communities 
  reported *to authorities*, county level- **KDHS 2022** (KNBS, 2023)  

A high Visibility Score means the system sees very little of what 
is actually happening. The higher the score, the more blind 
official systems are in that county.                    
            """)

st.divider()

# Key metrics
# Sort data from highest to lowest
sorted_data = sorted(visibility_data, key=lambda x: x["visibility_score"], reverse=True)

# Get the most and least values
most = sorted_data[0]
least = sorted_data[-1]

# Calculate average score
avg_score = round(sum(r["visibility_score"] for r in visibility_data) / len(visibility_data), 2
        )

# Count rows where score is >= 2.0
high_count = sum(1 for r in visibility_data if r["visibility_score"] >= 2.0)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Most Invisible County",
        value=most["county"],
        delta=f"Visibility Score: {most['visibility_score']}",
        delta_color="inverse"
    )

with col2:
    st.metric(
        label="Average Visibility Score",
        value=f"{avg_score}",
        delta="across 44 counties",
        delta_color="off"
    )

with col3:
    st.metric(
        label="High Invisibility Counties",
        value=f"{high_count} counties",
        delta="Visibility Score >= 2.0",
        delta_color="inverse"
    )

with col4:
    st.metric(
        label="Counties Analysed",
        value=len(visibility_data),
        delta="of 47 total",
        delta_color="off"
    )

st.divider()

# BAR CHART

st.subheader("GBV Visibility Score by County: Ranked Highest to Lowest")
st.caption(
    "Visibility Score = KDHS Physical Violence % / NCRC Reported GBV % | "
    "Higher score = system is more blind in that county (KNBS, 2023; NCRC, 2022)"
)

#Looping
counties = [r["county"] for r in visibility_data]
scores = [r["visibility_score"] for r in visibility_data]

colors = []
for s in scores:
    if s >= 2.0:
        colors.append("#E63F22")
    elif s >= 1.0:
        colors.append("#E67E22")
    else:
        colors.append("#B2E622")

# Build the chart
fig, ax = plt.subplots(figsize=(12, 14))

bars = ax.barh(
    counties, 
    scores, 
    color=colors, 
    edgecolor="white", 
    height=0.7)

# Add reference lines for high underreporting, moderate underreporting.

ax.axvline(x=1.0, color="black", linewidth=1.2, linestyle="--", alpha=0.5)
ax.text(
    1.02, 0.5, 
    "Score = 1.0",
    transform=ax.get_xaxis_transform(),
    fontsize=8, 
    alpha=0.6)

# Add value labels on bars
for bar, score in zip(bars, scores):
    ax.text(
        bar.get_width() + 0.05, # end of bar
        bar.get_y() + bar.get_height() / 2, # center vertically
        f"{score}", # this value only
        va="center",
        ha="left",
        fontsize=8,
        color="#2C3E50"
    )

# Add titles & labels

ax.set_xlabel("Visibility Score (KDHS Physical Violence % / NCRC Reported GBV %)",
              fontsize=10, labelpad=10)
ax.set_title(
    "Counting the Uncounted:\nGBV Visibility Index Across Kenya's 44 counties (2021-2022)",
    fontsize=13, fontweight="bold", pad=20
)

ax.invert_yaxis()
ax.set_xlim(0, max(scores) + 1)
ax.spines["top"].set_visible(False)
ax.spines["right"]. set_visible(False)

red_patch = mpatches.Patch(color="#E63F22", label="High undereporting (score >= 2.0x)")
orange_patch = mpatches.Patch(color="#E67E22", label="Moderate underreporting (score 1.0-2.0x)")
yellow_patch = mpatches.Patch(color="#B2E622", label="Anomaly: more reported than surveyed (score < 1.0)")
ax.legend(handles=[red_patch, orange_patch, yellow_patch],
          loc="lower right", fontsize=9)

plt.tight_layout()
st.pyplot(fig)

st.divider()

"""This is an interactive way for people to view 
and read the project findings from the visibility index"""

st.subheader("Explore the Data")

#Search box
search = st.text_input("Search for a county:", "")

# Filter
min_score = st.slider(
    "Show counties with Visibility Score above:",
    min_value=0.0,
    max_value=8.0,
    value=0.0,
    step=0.5
)

# Apply filters
filtered = [
    r for r in visibility_data
    if r["visibility_score"] >= min_score
    and (search.lower() in r["county"].lower() if search else True)
]

st.markdown(f"Showing **{len(filtered)} counties**")

# Table header
st.markdown(
    "| Rank | County | KDHS Physical Violence % | "
    "NCRC Reported GBV % | Visibilty Score |"
)

st.markdown("|---|---|---|---|---|")

for i, row in enumerate(filtered, start=1):
    st.markdown(
        f"| {i} | **{row['county']}** | "
        f"{row['kdhs_physical_pct']}% | "
        f"{row['police_gbv_pct']}% | "
        f"**{row['visibility_score']}x** | "
    )

st.divider()

st.subheader("County Spotlight")
st.caption("Select any county to see its full GBV Visibilty profile")

selected_county = st.selectbox(
    "Select a county:",
    options=[r["county"] for r in visibility_data]
)

county_row = next(
    r for r in visibility_data if r["county"] == selected_county
)

c1, c2, c3 = st.columns(3)
with c1:
    st.metric(
        "KDHS Physical Violence %",
        f"{county_row['kdhs_physical_pct']}%",
        help="% of women aged 15-49 who experienced physical violence "
        "in the last 12 months (KNBS, 2023)"

    )

with c2:
    st.metric(
        "NCRC Reported GBV %",
        f"{county_row['police_gbv_pct']}%",
        help="Community perception of GBV crime prevalence (NCRC, 2022)"
    )

with c3:
    st.metric(
        "Visibility Score",
        f"{county_row['visibility_score']}x",
        help="How many times larger the lived reality is compared " \
        "to what official systems captured"
    )

st.divider()

with st.expander("Methodolgy & Data Sources"):
    st.markdown("""
                **Visibility Score Formula**
                Visibility Score = KDHS Physical Violence % / NCRC Reported GBV %


                **Data Sources**
                Kenya National Bureau of Statistics (KNBS). (2023). *Kenya Demographic and 
                Health Survey 2022: County crosstab* [Data set]. African Development Data Hub. 
                https://ckan.africadatahub.org/dataset/kenya-demographic-and-health-survey-2022

                National Crime Research Centre. (2022). *2021 annual crime yearbook*. 
                Government of Kenya. 
                https://www.crimeresearch.go.ke/wp-content/uploads/2022/07/2021-ANNUAL-CRIME-YEAR-BOOK.pdf

                World Bank. (2024). *Gender data portal: Kenya* [Data set]. World Bank Group. 
                https://genderdata.worldbank.org/en/economies/kenya


                **Tools Used**
                Python . requests . openpyxl . matplotlib . Streamlit
                """)


with st.expander("Who Needs This?"):
    st.markdown("""
                **NGOs** deciding where to open safe houses
                **County Governments** that need to have more 
                police gender desks in specific areas
                **Donors and funders** that want to move beyond
                news coverage as a proxy for need
                """)
    

with st.expander("References (APA 7th Edition)"):
    st.markdown("""
    Kenya National Bureau of Statistics (KNBS). (2023). *Kenya Demographic 
    and Health Survey 2022: County crosstab* [Data set]. African Development 
    Data Hub. https://ckan.africadatahub.org/dataset/kenya-demographic-and-health-survey-2022

    National Crime Research Centre. (2022). *2021 annual crime yearbook*. 
    Government of Kenya. https://www.crimeresearch.go.ke/wp-content/uploads/2022/07/2021-ANNUAL-CRIME-YEAR-BOOK.pdf
             World Bank. (2024). *Gender data portal: Kenya* [Data set]. 
    World Bank Group. https://genderdata.worldbank.org/en/economies/kenya              
                
                
                """)
    
st.markdown("---")
st.caption(
    "Kenya National Bureau of Statistics (KNBS), 2023 . "
    "National Crime Research Centre (NCRC), 2022 . "
    "World Bank Gender Data Portal, 2024 | "
    "Python Capstone Project | Zindua School | May 2026"
)


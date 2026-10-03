# -*- coding: utf-8 -*-
"""
Created on Sat Oct  3 23:24:16 2026

@author: jjanh
"""

import streamlit as st
import re
from datetime import datetime

# =========================================================
# HIFAZAT KP
# AI Community Resilience & Emergency Action Platform
# =========================================================

st.set_page_config(
    page_title="Hifazat KP",
    page_icon="🛡️",
    layout="wide"
)

# -------------------------
# Styling
# -------------------------
st.markdown("""
<style>
.main-title {
    font-size: 42px;
    font-weight: 800;
    margin-bottom: 0;
}

.subtitle {
    font-size: 20px;
    color: #666;
    margin-top: 0;
}

.card {
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #ddd;
    margin-bottom: 15px;
    background: #fafafa;
}

.high {
    padding: 15px;
    border-radius: 10px;
    background: #ffe5e5;
    border-left: 6px solid #d00000;
}

.medium {
    padding: 15px;
    border-radius: 10px;
    background: #fff4d6;
    border-left: 6px solid #e0a000;
}

.low {
    padding: 15px;
    border-radius: 10px;
    background: #e5f7e5;
    border-left: 6px solid #168a16;
}

.big-number {
    font-size: 32px;
    font-weight: 700;
}

.footer {
    text-align: center;
    color: #777;
    padding: 30px;
}
</style>
""", unsafe_allow_html=True)


# =========================================================
# SESSION STORAGE
# =========================================================

if "reports" not in st.session_state:
    st.session_state.reports = []


# =========================================================
# PRIVACY
# =========================================================

def sanitize_text(text):
    """
    Demo privacy layer.
    Removes common phone numbers and email addresses.
    """

    # Email
    text = re.sub(
        r'[\w\.-]+@[\w\.-]+\.\w+',
        '[EMAIL REMOVED]',
        text
    )

    # Pakistani phone numbers
    text = re.sub(
        r'(\+92|0092|0)?3\d{2}[- ]?\d{7}',
        '[PHONE REMOVED]',
        text
    )

    return text


# =========================================================
# AI CLASSIFICATION
# =========================================================

def classify_report(text):

    text_lower = text.lower()

    categories = {
        "Flood / Flash Flood": [
            "flood", "water rising", "water level",
            "river", "stream", "rain", "flooding",
            "سیلاب", "پانی", "بارش", "دریا", "نالہ"
        ],

        "Landslide": [
            "landslide", "land slide", "mountain collapse",
            "mudslide", "مٹی", "پہاڑ", "لینڈ سلائیڈ"
        ],

        "Fire": [
            "fire", "burning", "smoke",
            "آگ", "دھواں", "جل رہا"
        ],

        "Road / Infrastructure": [
            "road", "bridge", "blocked",
            "broken bridge", "damage",
            "سڑک", "پل", "راستہ", "بند"
        ],

        "Water Shortage": [
            "water shortage", "no water",
            "drinking water", "پینے کا پانی",
            "پانی نہیں"
        ],

        "Health Emergency": [
            "injury", "hospital", "disease",
            "sick", "medical", "زخمی",
            "ہسپتال", "بیماری"
        ]
    }

    scores = {}

    for category, keywords in categories.items():

        score = 0

        for keyword in keywords:

            if keyword.lower() in text_lower:
                score += 1

        scores[category] = score

    best_category = max(
        scores,
        key=scores.get
    )

    if scores[best_category] == 0:
        best_category = "Other Community Risk"

    return best_category


# =========================================================
# RISK ANALYSIS
# =========================================================

def analyze_risk(text, severity, category):

    score = 0

    text_lower = text.lower()

    # User severity
    if severity == "High":
        score += 50
    elif severity == "Medium":
        score += 30
    else:
        score += 10

    # Additional signals

    danger_words = [
        "danger",
        "unsafe",
        "blocked",
        "rising",
        "injured",
        "trapped",
        "emergency",
        "خطر",
        "غیر محفوظ",
        "پھنس",
        "زخمی"
    ]

    for word in danger_words:

        if word in text_lower:
            score += 10

    if score >= 60:
        risk = "High"
    elif score >= 30:
        risk = "Medium"
    else:
        risk = "Low"

    return min(score, 100), risk


# =========================================================
# MISSING INFORMATION
# =========================================================

def find_missing_information(text):

    missing = []

    text_lower = text.lower()

    location_words = [
        "village",
        "town",
        "district",
        "road",
        "bridge",
        "near",
        "گاؤں",
        "علاقہ",
        "پل",
        "سڑک"
    ]

    people_words = [
        "people",
        "families",
        "children",
        "elderly",
        "لوگ",
        "خاندان",
        "بچے"
    ]

    if not any(word in text_lower for word in location_words):
        missing.append("Exact location / nearby landmark")

    if not any(word in text_lower for word in people_words):
        missing.append("Approximate number of affected people")

    if len(text.split()) < 12:
        missing.append("More details about the situation")

    return missing


# =========================================================
# ACTION PLAN
# =========================================================

def get_action_plan(category, risk):

    plans = {

        "Flood / Flash Flood": [
            "Move away from rivers, streams and low-lying areas.",
            "Do not cross fast-moving water.",
            "Keep children and vulnerable people away from the danger area.",
            "Share the location with appropriate emergency/rescue services.",
            "Use verified official weather and emergency information."
        ],

        "Landslide": [
            "Move away from unstable slopes.",
            "Avoid roads below visibly unstable mountain areas.",
            "Keep people away from cracks and falling rocks.",
            "Report blocked roads to relevant authorities.",
            "Follow official evacuation instructions."
        ],

        "Fire": [
            "Move people away from the fire area.",
            "Do not enter a burning structure.",
            "Contact appropriate emergency/fire services.",
            "Keep access routes clear for responders.",
            "Do not spread unverified information."
        ],

        "Road / Infrastructure": [
            "Avoid unsafe bridges or damaged roads.",
            "Warn nearby community members.",
            "Use an alternative safe route if available.",
            "Report the infrastructure problem to relevant authorities.",
            "Keep children away from damaged structures."
        ],

        "Water Shortage": [
            "Identify the affected community area.",
            "Prioritize drinking-water needs.",
            "Coordinate with local community resources.",
            "Report prolonged shortages to the relevant service provider.",
            "Record the approximate number of affected households."
        ],

        "Health Emergency": [
            "Contact appropriate medical/emergency services.",
            "Move seriously ill or injured people to professional care.",
            "Avoid spreading unverified medical information.",
            "Record the number of affected people.",
            "Follow professional medical instructions."
        ],

        "Other Community Risk": [
            "Move away from immediate danger.",
            "Record the location and situation if safe.",
            "Contact the appropriate emergency or local service.",
            "Do not spread unverified information.",
            "Protect children and vulnerable people."
        ]
    }

    return plans.get(
        category,
        plans["Other Community Risk"]
    )


# =========================================================
# COMMUNITY INTELLIGENCE
# =========================================================

def community_clusters():

    return [

        {
            "title": "Possible Localized Flood Risk",
            "reports": 7,
            "signals": [
                "Rising water",
                "Unsafe bridge",
                "Blocked route",
                "Same weather period"
            ],
            "priority": "High"
        },

        {
            "title": "Possible Infrastructure Disruption",
            "reports": 4,
            "signals": [
                "Road damage",
                "Bridge damage",
                "Access difficulty"
            ],
            "priority": "Medium"
        }
    ]


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">🛡️ Hifazat KP</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'AI Community Resilience & Emergency Action Platform'
    '</div>',
    unsafe_allow_html=True
)

st.write(
    "Turning scattered local observations into structured "
    "community resilience intelligence."
)

st.divider()


# =========================================================
# NAVIGATION
# =========================================================

tab1, tab2, tab3, tab4 = st.tabs([
    "📝 Report",
    "🧠 Community Intelligence",
    "🚨 Action Plan",
    "ℹ️ About Project"
])


# =========================================================
# REPORT TAB
# =========================================================

with tab1:

    st.header("Submit a Community Observation")

    st.info(
        "Share what you observed. Do not include unnecessary "
        "personal information."
    )

    col1, col2 = st.columns(2)

    with col1:

        district = st.selectbox(
            "District",
            [
                "Bannu",
                "D.I. Khan",
                "Peshawar",
                "Swat",
                "Buner",
                "Shangla",
                "Kohat",
                "Kurram",
                "North Waziristan",
                "South Waziristan",
                "Nowshera",
                "Other"
            ]
        )

    with col2:

        severity = st.selectbox(
            "Your assessment of severity",
            [
                "Low",
                "Medium",
                "High"
            ]
        )

    language = st.selectbox(
        "Language",
        [
            "English",
            "Urdu",
            "Pashto"
        ]
    )

    description = st.text_area(
        "Describe what you observed",
        placeholder=(
            "Example: Heavy rain has raised the water near "
            "the stream. The bridge is becoming unsafe and "
            "several families live close to the area."
        ),
        height=180
    )

    analyze_button = st.button(
        "🔎 Analyze Report",
        type="primary",
        use_container_width=True
    )

    if analyze_button:

        if not description.strip():

            st.error(
                "Please describe the situation first."
            )

        else:

            clean_text = sanitize_text(
                description
            )

            category = classify_report(
                clean_text
            )

            score, risk = analyze_risk(
                clean_text,
                severity,
                category
            )

            missing = find_missing_information(
                clean_text
            )

            actions = get_action_plan(
                category,
                risk
            )

            case_id = (
                "HKP-"
                + datetime.now().strftime(
                    "%Y%m%d%H%M%S"
                )
            )

            report = {
                "case_id": case_id,
                "district": district,
                "category": category,
                "risk": risk,
                "score": score,
                "description": clean_text,
                "severity": severity,
                "time": datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            }

            st.session_state.reports.append(
                report
            )

            st.success(
                "Report analyzed successfully."
            )

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "Category",
                    category
                )

            with col2:

                st.metric(
                    "Risk Level",
                    risk
                )

            with col3:

                st.metric(
                    "Risk Score",
                    f"{score}/100"
                )

            st.markdown("### 🔍 Missing Information")

            if missing:

                for item in missing:
                    st.warning(
                        "• " + item
                    )

            else:

                st.success(
                    "No major missing information detected."
                )

            st.markdown("### 🛡️ Recommended Safe Actions")

            for action in actions:

                st.write(
                    "✓ " + action
                )

            st.caption(
                f"Case ID: {case_id}"
            )

            st.caption(
                "AI output is decision support only. "
                "It is not an official emergency warning."
            )


# =========================================================
# COMMUNITY INTELLIGENCE TAB
# =========================================================

with tab2:

    st.header(
        "🧠 Community Intelligence"
    )

    st.write(
        "The long-term vision is to combine multiple "
        "related observations into a single community-level signal."
    )

    clusters = community_clusters()

    for cluster in clusters:

        if cluster["priority"] == "High":

            box_class = "high"

        else:

            box_class = "medium"

        st.markdown(
            f"""
            <div class="{box_class}">
                <h3>{cluster['title']}</h3>
                <p>
                <b>{cluster['reports']}</b>
                related observations
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.write(
            "**Signals detected:**"
        )

        for signal in cluster["signals"]:

            st.write(
                "• " + signal
            )

        st.write(
            f"**Priority:** {cluster['priority']}"
        )

        st.divider()

    st.subheader(
        "⭐ Main Innovation Demo"
    )

    st.success(
        """
        7 separate community observations

        ↓

        AI identifies related signals

        ↓

        Possible Localized Flood Risk

        ↓

        One structured community-level intelligence signal
        """
    )


# =========================================================
# ACTION PLAN TAB
# =========================================================

with tab3:

    st.header(
        "🚨 Community Safety Action Plan"
    )

    st.write(
        "This section demonstrates how an analyzed observation "
        "can be converted into practical safety guidance."
    )

    selected_category = st.selectbox(
        "Select incident type",
        [
            "Flood / Flash Flood",
            "Landslide",
            "Fire",
            "Road / Infrastructure",
            "Water Shortage",
            "Health Emergency",
            "Other Community Risk"
        ]
    )

    selected_risk = st.selectbox(
        "Priority",
        [
            "High",
            "Medium",
            "Low"
        ]
    )

    st.subheader(
        f"Recommended actions — {selected_category}"
    )

    for action in get_action_plan(
        selected_category,
        selected_risk
    ):

        st.write(
            "🛡️ " + action
        )

    st.warning(
        "For immediate danger, contact the appropriate "
        "official emergency/rescue service."
    )


# =========================================================
# ABOUT TAB
# =========================================================

with tab4:

    st.header(
        "About Hifazat KP"
    )

    st.markdown("""
    ### 🎯 Vision

    Hifazat KP is a proposed AI-assisted community resilience
    platform for Khyber Pakhtunkhwa.

    ### 🔄 Core Workflow

    **Local Observation**

    ↓

    **Privacy-Aware Intake**

    ↓

    **AI Classification**

    ↓

    **Missing Information Detection**

    ↓

    **Preliminary Risk Triage**

    ↓

    **Safe Action Plan**

    ↓

    **Related-Report Clustering**

    ↓

    **Community Resilience Intelligence**

    ### 🌍 Possible Use Cases

    - Floods and flash floods
    - Landslides
    - Fires
    - Road and bridge disruption
    - Water shortages
    - Health emergencies
    - Other community resilience problems

    ### 🚀 Future Development

    - Pashto and Urdu voice reporting
    - Low-bandwidth/offline support
    - Interactive risk map
    - Weather and official-alert integration
    - Satellite/environmental signals
    - Real AI/LLM analysis
    - Community responder network
    - Historical risk hotspot analysis

    ### ⚠️ Safety

    Hifazat KP is not intended to replace official emergency,
    rescue, medical, engineering or government systems.

    AI-generated results should be reviewed by appropriate
    human authorities before being treated as verified information.
    """)


# =========================================================
# CURRENT REPORTS
# =========================================================

if st.session_state.reports:

    st.divider()

    st.header("📊 Current Demo Reports")

    for report in reversed(
        st.session_state.reports
    ):

        with st.expander(
            f"{report['case_id']} — "
            f"{report['category']} — "
            f"{report['risk']} Risk"
        ):

            st.write(
                "**District:**",
                report["district"]
            )

            st.write(
                "**Observation:**",
                report["description"]
            )

            st.write(
                "**Risk Score:**",
                f"{report['score']}/100"
            )

            st.write(
                "**Time:**",
                report["time"]
            )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.markdown(
    """
    <div class="footer">
    <b>Hifazat KP</b><br>
    AI Community Resilience & Emergency Action Platform<br>
    Prototype for KP Youth Innovation & Entrepreneurship Competition<br>
    Creatted by Jan Hssain
    </div>
    """,
    unsafe_allow_html=True
)

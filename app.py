import streamlit as st
import timetable

PREVIEW_CACHE = timetable.PREVIEW_CACHE
generate_timetable = timetable.generate_timetable


# ---------------- Page Config ----------------
st.set_page_config(
    page_title="IIIT Dharwad – Academic Timetable",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------- Global Professional Theme CSS ----------------
st.markdown("""
<style>
    /* 1. Main Application Background */
    .stApp {
        background-color: #0f1116;
        color: #e6edf3;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* 2. Header Styling */
    h1 {
        font-weight: 800;
        letter-spacing: -0.02em;
        background: linear-gradient(90deg, #60a5fa, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .caption-text {
        color: #8b949e;
        font-size: 1.1rem;
        font-weight: 400;
        margin-bottom: 2rem;
    }

    /* 3. Button Styling (Primary CTA) */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        color: white;
        border: 1px solid rgba(255,255,255,0.1);
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        border-radius: 8px;
        transition: all 0.2s ease;
        box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.2);
    }
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.3);
        border-color: rgba(255,255,255,0.2);
    }

    /* 4. Containers / Cards for Timetables */
    .timetable-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 30px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    }

    /* 5. Subheaders */
    h3 {
        color: #e6edf3;
        font-weight: 600;
        border-left: 4px solid #3b82f6;
        padding-left: 12px;
        margin-top: 10px;
        margin-bottom: 20px;
    }

    /* 6. Success/Info Messages */
    .stAlert {
        background-color: rgba(56, 189, 248, 0.1);
        border: 1px solid rgba(56, 189, 248, 0.2);
        color: #38bdf8;
    }
</style>
""", unsafe_allow_html=True)

# ---------------- Header Section ----------------
col_header, col_empty = st.columns([2, 1])
with col_header:
    st.title("🎓 IIIT Dharwad")
    st.markdown("<p class='caption-text'>Automated Academic Scheduler • All Branches & Semesters</p>", unsafe_allow_html=True)

# ---------------- HTML Timetable Renderer ----------------
def render_merged_timetable(df):
    slots = list(df.columns)
    days = list(df.index)

    # Note: Logic remains untouched, but CSS inside HTML is upgraded for the "Professional" look
    html = """
    <style>
    table.timetable {
        border-collapse: separate; 
        border-spacing: 0;
        width: 100%;
        margin-bottom: 10px;
        font-family: 'Segoe UI', sans-serif;
        font-size: 13px;
        border: 1px solid #30363d;
        border-radius: 8px;
        overflow: hidden;
    }
    table.timetable th, table.timetable td {
        border-bottom: 1px solid #30363d;
        border-right: 1px solid #30363d;
        padding: 12px 8px;
        text-align: center;
        color: #c9d1d9;
    }
    
    /* Header Row */
    table.timetable th {
        background-color: #21262d;
        color: #ffffff;
        font-weight: 600;
        text-transform: uppercase;
        font-size: 11px;
        letter-spacing: 0.05em;
    }
    
    /* First Column (Days) */
    table.timetable tr th:first-child {
        background-color: #1f2937;
        font-weight: 700;
        color: #60a5fa; /* Blue tint */
        border-right: 2px solid #30363d;
    }

    /* Cells */
    table.timetable td {
        background-color: #0d1117;
    }
    table.timetable td b {
        color: #e6edf3;
        font-weight: 500;
    }
    
    /* Hover Effect */
    table.timetable tr:hover td {
        background-color: #161b22;
    }
    </style>
    """

    html += "<div class='timetable-card'>" # Wrap in card div
    html += "<table class='timetable'>"

    # Header
    html += "<tr><th>Day</th>"
    for s in slots:
        html += f"<th>{s}</th>"
    html += "</tr>"

    # Rows
    for day in days:
        html += f"<tr><th>{day}</th>"
        row = df.loc[day].fillna("").tolist()

        c = 0
        while c < len(row):
            val = row[c]

            if val == "":
                html += "<td></td>"
                c += 1
                continue

            span = 1
            while c + span < len(row) and row[c + span] == val:
                span += 1

            # Logic Check: Highlight 'Break' or 'Lunch' differently if needed
            # (Keeping logic strictly visual here)
            bg_style = ""
            if "Break" in str(val) or "Lunch" in str(val):
                bg_style = "style='background-color: #161b22; color: #484f58; font-style:italic;'"
            else:
                bg_style = "style='background-color: #1f2937; border: 1px solid #30363d; border-radius: 4px;'"

            # Use div inside td for cell styling
            html += f"<td colspan='{span}'><div {bg_style} style='padding:6px; border-radius:4px;'><b>{val}</b></div></td>"
            c += span

        html += "</tr>"

    html += "</table>"
    html += "</div>" # Close card div
    return html


# ---------------- Generate Section ----------------

# Centered Button Area
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    generate_clicked = st.button("🚀 Generate New Timetable", use_container_width=True)

st.divider()

if generate_clicked:

    # 🔥 LOGIC START (Unchanged)
    PREVIEW_CACHE.clear()
    filename = generate_timetable(seed=42, hide_c004=True)
    # 🔥 LOGIC END

    st.success(f"✅ Scheduling Complete. File generated: **{filename}**")
    
    # 🔥 SHOW **ALL BRANCHES & ALL SEMESTERS**
    if not PREVIEW_CACHE:
        st.warning("⚠️ No timetable data found.")
    else:
        labels = sorted(PREVIEW_CACHE.keys())  # clean order

        # Display Loop
        for label in labels:
            st.markdown(f"### {label}")
            df = PREVIEW_CACHE[label]
            st.markdown(render_merged_timetable(df), unsafe_allow_html=True)

    st.divider()

    # Download Button Centered
    dc1, dc2, dc3 = st.columns([1, 2, 1])
    with dc2:
        with open(filename, "rb") as f:
            st.download_button(
                label="⬇️ Download Official Excel Timetable",
                data=f,
                file_name=filename,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )

else:
    # Empty State / Landing View
    st.markdown("""
    <div style='text-align: center; padding: 40px; color: #6b7280;'>
        <h2>Ready to Schedule?</h2>
        <p>Click the <b>Generate</b> button above to run the algorithm and preview all semesters.</p>
    </div>
    """, unsafe_allow_html=True)
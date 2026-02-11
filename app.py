import streamlit as st
import pandas as pd
import timetable  # Your existing backend module

# ---------------- CONFIGURATION ----------------
st.set_page_config(
    page_title="IIIT Dharwad Scheduler",
    page_icon="📅",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------- STATE MANAGEMENT ----------------
# Use session state to keep the timetable visible after generation
if 'timetable_generated' not in st.session_state:
    st.session_state.timetable_generated = False
if 'generated_filename' not in st.session_state:
    st.session_state.generated_filename = ""

PREVIEW_CACHE = timetable.PREVIEW_CACHE
generate_timetable = timetable.generate_timetable

# ---------------- CUSTOM CSS (PROFESSIONAL THEME) ----------------
st.markdown("""
<style>
    /* 1. Global Reset & Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    .stApp {
        background-color: #0e1117; /* GitHub Dark Dimmed */
        font-family: 'Inter', sans-serif;
    }

    /* 2. Header Gradient */
    .main-header {
        background: linear-gradient(90deg, #4f46e5, #ec4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 3rem;
        margin-bottom: 0;
    }
    
    .sub-header {
        color: #94a3b8;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }

    /* 3. Card Containers for Tables */
    .timetable-container {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 30px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
    }
    
    .branch-title {
        color: #e2e8f0;
        font-size: 1.4rem;
        font-weight: 600;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
    }
    .branch-title::before {
        content: '';
        display: inline-block;
        width: 6px;
        height: 24px;
        background: #3b82f6;
        margin-right: 12px;
        border-radius: 4px;
    }

    /* 4. Custom Button Styling */
    div.stButton > button {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 8px;
        font-weight: 600;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.4);
        width: 100%;
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.6);
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
    }

    /* 5. Download Button Variant */
    div[data-testid="stDownloadButton"] > button {
        background: #1f2937;
        border: 1px solid #374151;
        color: #e5e7eb;
    }
    div[data-testid="stDownloadButton"] > button:hover {
        background: #374151;
        border-color: #4b5563;
    }
</style>
""", unsafe_allow_html=True)

# ---------------- HTML RENDERER FUNCTION ----------------
def render_styled_timetable(df):
    """
    Converts a pandas DataFrame into a beautiful HTML Table with colspan support.
    """
    slots = list(df.columns)
    days = list(df.index)

    # Internal CSS for the table itself
    html = """
    <style>
        table.styled-table {
            width: 100%;
            border-collapse: separate;
            border-spacing: 4px; /* Space between cells */
            font-size: 13px;
        }
        .styled-table th {
            text-align: center;
            padding: 12px;
            color: #94a3b8;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 0.75rem;
            letter-spacing: 0.05em;
        }
        .styled-table td {
            padding: 0; /* Padding handled by inner div */
        }
        .cell-content {
            border-radius: 6px;
            padding: 10px 5px;
            text-align: center;
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-direction: column;
            box-shadow: 0 1px 2px rgba(0,0,0,0.2);
            font-weight: 500;
            transition: transform 0.1s;
        }
        .cell-content:hover {
            transform: scale(1.02);
            z-index: 10;
        }
        /* Color Coding */
        .day-header { background: #1f2937; color: #f3f4f6; font-weight: 700; border-radius: 6px;}
        .slot-class { background: #1e3a8a; border: 1px solid #1d4ed8; color: #dbeafe; } /* Blue for classes */
        .slot-lab { background: #581c87; border: 1px solid #7e22ce; color: #f3e8ff; } /* Purple for labs */
        .slot-break { background: #2d333b; border: 1px solid #444c56; color: #768390; font-style: italic; } /* Gray for breaks */
        .slot-empty { background: transparent; }
    </style>
    <table class="styled-table">
    """

    # Header Row
    html += "<thead><tr><th></th>" # Empty corner
    for s in slots:
        html += f"<th>{s}</th>"
    html += "</tr></thead><tbody>"

    # Data Rows
    for day in days:
        html += f"<tr><td class='day-header'><div class='cell-content day-header'>{day[:3]}</div></td>"
        
        row = df.loc[day].fillna("").tolist()
        c = 0
        while c < len(row):
            val = str(row[c])
            
            # Determine Spanning (Merged Cells)
            span = 1
            if val != "":
                while c + span < len(row) and str(row[c + span]) == val:
                    span += 1
            
            # Determine CSS Class based on content
            css_class = "slot-class"
            if val == "":
                css_class = "slot-empty"
            elif "Lunch" in val or "Break" in val:
                css_class = "slot-break"
            elif "Lab" in val or "CS" in val: # Example heuristic
                css_class = "slot-lab"
            
            # Render Cell
            if val == "":
                html += f"<td></td>"
            else:
                html += f"<td colspan='{span}'><div class='cell-content {css_class}'>{val}</div></td>"
            
            c += span
            
        html += "</tr>"

    html += "</tbody></table>"
    return html

# ---------------- UI LAYOUT ----------------

# 1. Title Section
col_logo, col_title = st.columns([1, 5])
with col_title:
    st.markdown('<h1 class="main-header">IIIT Dharwad</h1>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Academic Timetable Automation System</div>', unsafe_allow_html=True)

st.divider()

# 2. Controls Section
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    if st.button("🚀 Generate New Schedule", use_container_width=True):
        with st.spinner("Optimizing schedule..."):
            # Clear cache and run logic
            timetable.PREVIEW_CACHE.clear()
            filename = generate_timetable(seed=42, hide_c004=True)
            
            # Update Session State
            st.session_state.timetable_generated = True
            st.session_state.generated_filename = filename
            st.rerun()

# 3. Results Section
if st.session_state.timetable_generated:
    st.success(f"✅ Schedule generated successfully! File ready: {st.session_state.generated_filename}")
    
    # Download Button (Centered)
    d1, d2, d3 = st.columns([2, 2, 2])
    with d2:
        try:
            with open(st.session_state.generated_filename, "rb") as f:
                st.download_button(
                    label="📥 Download Excel File",
                    data=f,
                    file_name=st.session_state.generated_filename,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
        except FileNotFoundError:
            st.error("File not found. Please regenerate.")

    st.markdown("---")

    # Render Timetables
    if not timetable.PREVIEW_CACHE:
         # Fallback if cache is empty but state is true (edge case)
         st.warning("Please regenerate the timetable to view previews.")
    else:
        # Sort keys to keep semesters organized
        labels = sorted(timetable.PREVIEW_CACHE.keys())
        
        for label in labels:
            df = timetable.PREVIEW_CACHE[label]
            
            # Create a Card for each Semester/Branch
            st.markdown(f"""
            <div class="timetable-container">
                <div class="branch-title">{label}</div>
            """, unsafe_allow_html=True)
            
            # Inject the HTML Table
            st.markdown(render_styled_timetable(df), unsafe_allow_html=True)
            
            # Close Card
            st.markdown("</div>", unsafe_allow_html=True)

else:
    # Empty State Hero
    st.markdown("""
    <div style="text-align: center; padding: 50px 20px; color: #64748b;">
        <h3 style="color: #94a3b8;">Ready to organize the semester?</h3>
        <p>Click the <b>Generate</b> button above to run the allocation algorithm.</p>
    </div>
    """, unsafe_allow_html=True)
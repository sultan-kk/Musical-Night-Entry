import pandas as pd
import streamlit as st
import openpyxl

st.set_page_config(
    page_title="Registration Data Entry Portal", page_icon="📊", layout="centered"
)

# Custom Styling for UI
st.markdown(
    """
    <style>
    .main-title {
        font-size: 28px;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 20px;
    }
    .stButton>button {
        width: 100%;
        background-color: #ff4b4b;
        color: white;
        font-weight: bold;
    }
    </style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    '<p class="main-title">📋 Event/Department Data Entry Portal</p>',
    unsafe_allow_html=True,
)

# Initialize Session State to store submitted entries persistently during the session
if "data_list" not in st.session_state:
  st.session_state.data_list = []

# Form for data entry
with st.form("entry_form", clear_on_submit=True):
  col1, col2 = st.columns(2)

  with col1:
    sr_no = st.text_input("Sr No", placeholder="e.g. 001")
    name = st.text_input("Full Name", placeholder="e.g. Ali Khan")
    reg_no = st.text_input("REG No", placeholder="e.g. CIIT/FA21-BBA-001")

  with col2:
    cnic_no = st.text_input(
        "CNIC No (Optional)", placeholder="e.g. 37405-1234567-1"
    )
    ph_no = st.text_input("Phone Number", placeholder="e.g. 0300-1234567")
    department = st.selectbox(
        "Department",
        [
            "Management Sciences",
            "Computer Science",
            "Electrical Engineering",
            "Civil Engineering",
            "Humanities",
            "Architecture",
            "Other",
        ],
    )

  submitted = st.form_submit_button("💾 Save Data to Excel")

  if submitted:
    if not sr_no or not name or not reg_no or not ph_no:
      st.warning(
          "⚠️ Please fill in all required fields (Sr No, Name, REG No, PH No)!"
      )
    else:
      # Append data to session list
      new_entry = {
          "Sr No": sr_no,
          "Name": name,
          "REG No": reg_no,
          "CNIC No": cnic_no if cnic_no else "N/A",
          "Phone Number": ph_no,
          "Department": department,
      }
      st.session_state.data_list.append(new_entry)
      st.success(f"✅ Successfully added entry for **{name}**!")

# Display Data Table if records exist
if st.session_state.data_list:
  st.markdown("---")
  st.subheader("📊 Submitted Entries Preview")

  df = pd.DataFrame(st.session_state.data_list)
  st.dataframe(df, use_container_width=True)


  # Function to convert dataframe to Excel bytes for download
  def convert_df_to_excel(dataframe):
    output = io.BytesIO() if "io" in globals() else None
    import io

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
      dataframe.to_excel(writer, index=False, sheet_name="Registrations")
    return output.getvalue()


  import io

  excel_data = convert_df_to_excel(df)

  # Download Button
  st.download_button(
      label="📥 Download Formatted Excel Sheet (.xlsx)",
      data=excel_data,
      file_name="registration_data.xlsx",
      mime=(
          "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
      ),
  )

  # Clear Data Button
  if st.button("🗑️ Clear All Records"):
    st.session_state.data_list = []
    st.rerun()
else:
  st.info(
      "💡 No records added yet. Fill out the form above to start collecting"
      " data."
  )

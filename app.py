import io
import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
import pandas as pd
import streamlit as st

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

# Initialize Session State
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
      new_entry = {
          "Sr No": sr_no,
          "Name": name,
          "REG No": reg_no,
          "CNIC No": cnic_no if cnic_no else "N/A",
          "Phone Number": ph_no,
          "Department": department,
      }
      # Naya data list ke end mein add hoga (Latest data last mein save hoga)
      st.session_state.data_list.append(new_entry)
      st.success(f"✅ Successfully added entry for **{name}**!")

# Display Data Table and Download Option if records exist
if st.session_state.data_list:
  st.markdown("---")
  st.subheader("📊 Submitted Entries Preview")

  df = pd.DataFrame(st.session_state.data_list)
  st.dataframe(df, use_container_width=True)


  # Function to convert dataframe to professionally formatted Excel bytes using OpenPyXL
  def convert_df_to_excel_formatted(dataframe):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
      dataframe.to_excel(writer, index=False, sheet_name="Registrations")

    # Load workbook back to apply formatting
    output.seek(0)
    wb = openpyxl.load_workbook(output)
    ws = wb.active

    # Styling definitions
    header_fill = PatternFill(
        start_color="1F77B4", end_color="1F77B4", fill_type="solid"
    )  # Blue Header
    header_font = Font(name="Arial", size=11, bold=True, color="FFFFFF")
    data_font = Font(name="Arial", size=10)
    thin_border = Border(
        left=Side(style="thin", color="CCCCCC"),
        right=Side(style="thin", color="CCCCCC"),
        top=Side(style="thin", color="CCCCCC"),
        bottom=Side(style="thin", color="CCCCCC"),
    )
    align_center = Alignment(
        horizontal="center", vertical="center", wrap_text=True
    )
    align_left = Alignment(horizontal="left", vertical="center", wrap_text=True)

    # Format Headers
    for col_num in range(1, ws.max_column + 1):
      cell = ws.cell(row=1, column=col_num)
      cell.fill = header_fill
      cell.font = header_font
      cell.alignment = align_center

    # Format Data Rows (Text Wrapping, Borders, Fonts)
    for row_num in range(2, ws.max_row + 1):
      for col_num in range(1, ws.max_column + 1):
        cell = ws.cell(row=row_num, column=col_num)
        cell.font = data_font
        cell.border = thin_border
        # Sr No and REG No ko center rakhein, baaki left
        if col_num in [1, 3]:
          cell.alignment = align_center
        else:
          cell.alignment = align_left

    # Auto-fit Column Widths
    for col in ws.columns:
      max_len = 0
      col_letter = openpyxl.utils.get_column_letter(col[0].column)
      for cell in col:
        if cell.value:
          max_len = max(max_len, len(str(cell.value)))
      ws.column_dimensions[col_letter].width = max(max_len + 5, 15)

    # Save formatted workbook to bytes
    final_output = io.BytesIO()
    wb.save(final_output)
    return final_output.getvalue()


  excel_data = convert_df_to_excel_formatted(df)

  # Excel Download Button
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

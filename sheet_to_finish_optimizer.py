import streamlit as st

def calculate_fit(sheet_w, sheet_h, finish_w, finish_h):
    # Fit in original orientation
    cols_orig = sheet_w // finish_w
    rows_orig = sheet_h // finish_h
    total_orig = cols_orig * rows_orig
    used_w_orig = cols_orig * finish_w
    used_h_orig = rows_orig * finish_h
    balance_w_orig = sheet_w - used_w_orig
    balance_h_orig = sheet_h - used_h_orig

    # Fit in rotated orientation
    cols_rot = sheet_w // finish_h
    rows_rot = sheet_h // finish_w
    total_rot = cols_rot * rows_rot
    used_w_rot = cols_rot * finish_h
    used_h_rot = rows_rot * finish_w
    balance_w_rot = sheet_w - used_w_rot
    balance_h_rot = sheet_h - used_h_rot

    if total_orig >= total_rot:
        return {
            "layout": "Original Orientation",
            "total": int(total_orig),
            "rows": int(rows_orig),
            "columns": int(cols_orig),
            "used_w": used_w_orig,
            "used_h": used_h_orig,
            "balance_w": balance_w_orig,
            "balance_h": balance_h_orig
        }
    else:
        return {
            "layout": "Rotated Orientation",
            "total": int(total_rot),
            "rows": int(rows_rot),
            "columns": int(cols_rot),
            "used_w": used_w_rot,
            "used_h": used_h_rot,
            "balance_w": balance_w_rot,
            "balance_h": balance_h_rot
        }

st.title("📐 Sheet-to-Finish Size Optimizer (mm Input)")

st.markdown("### Step 1: Enter Sheet Size (in millimeters)")
sheet_width_mm = st.number_input("Sheet Width (mm)", min_value=100, value=330)
sheet_height_mm = st.number_input("Sheet Height (mm)", min_value=100, value=483)

st.markdown("### Step 2: Enter Finish Size (in millimeters)")
finish_width_mm = st.number_input("Finish Width (mm)", min_value=10, value=210)
finish_height_mm = st.number_input("Finish Height (mm)", min_value=10, value=297)

if st.button("Calculate Fit"):
    result = calculate_fit(sheet_width_mm, sheet_height_mm, finish_width_mm, finish_height_mm)

    st.success(f"✅ Best Layout: {result['layout']}")
    st.write(f"🧾 Total Finish Sizes per Sheet: **{result['total']}**")
    st.write(f"📏 Rows: {result['rows']} | Columns: {result['columns']}")
    st.write(f"🟩 Used Area: {result['used_w']}mm x {result['used_h']}mm")
    st.write(f"⬜ Remaining Balance: {result['balance_w']}mm x {result['balance_h']}mm")

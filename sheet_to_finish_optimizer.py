import streamlit as st

# -----------------------
# 1. Visiting Card Estimator
# -----------------------
def rate_estimator():
    st.subheader("🧾 Visiting Card Rate Estimator")

    rate_lookup = {
        "Gloss": {500: 400, 1000: 700},
        "Matte": {500: 450, 1000: 800},
        "Synthetic": {500: 700, 1000: 1200},
        "Normal": {500: 300, 1000: 500}
    }

    finish = st.selectbox("Select Finish Type", list(rate_lookup.keys()))
    quantity = st.selectbox("Select Quantity", [500, 1000])
    base_rate = rate_lookup[finish][quantity]

    st.info(f"Base Rate for {quantity} {finish} cards: ₹{base_rate}")

    if st.radio("Generate final estimate?", ("Yes", "No")) == "Yes":
        design_charge = st.number_input("Design Charges (₹)", min_value=0, value=0)
        extra_charge = st.number_input("Extra/Add-on Charges (₹)", min_value=0, value=0)
        discount = st.number_input("Discount (₹)", min_value=0, value=0)
        include_tax = st.checkbox("Include GST (18%)")

        subtotal = base_rate + design_charge + extra_charge - discount
        tax = subtotal * 0.18 if include_tax else 0
        total = subtotal + tax

        st.success(f"💰 Final Estimate: ₹{total:.2f}")
        if include_tax:
            st.caption(f"Includes ₹{tax:.2f} GST (SGST + CGST)")


# -----------------------
# 2. Sheet Size Optimizer with Unit Switch
# -----------------------
def sheet_size_optimizer():
    st.subheader("📐 Sheet-to-Finish Size Optimizer")

    unit = st.radio("Select Unit", ("Millimeters (mm)", "Inches (in)"))
    multiplier = 1 if unit == "Millimeters (mm)" else 25.4
    unit_label = "mm" if unit == "Millimeters (mm)" else "in"

    sheet_width = st.number_input(f"Sheet Width ({unit_label})", min_value=1.0, value=330.0)
    sheet_height = st.number_input(f"Sheet Height ({unit_label})", min_value=1.0, value=483.0)
    finish_width = st.number_input(f"Finish Width ({unit_label})", min_value=1.0, value=210.0)
    finish_height = st.number_input(f"Finish Height ({unit_label})", min_value=1.0, value=297.0)

    # Convert all inputs to mm
    sheet_w = sheet_width * multiplier
    sheet_h = sheet_height * multiplier
    finish_w = finish_width * multiplier
    finish_h = finish_height * multiplier

    # Orientation 1
    cols1 = sheet_w // finish_w
    rows1 = sheet_h // finish_h
    total1 = cols1 * rows1
    used_w1 = cols1 * finish_w
    used_h1 = rows1 * finish_h
    rem_w1 = sheet_w - used_w1
    rem_h1 = sheet_h - used_h1

    # Orientation 2
    cols2 = sheet_w // finish_h
    rows2 = sheet_h // finish_w
    total2 = cols2 * rows2
    used_w2 = cols2 * finish_h
    used_h2 = rows2 * finish_w
    rem_w2 = sheet_w - used_w2
    rem_h2 = sheet_h - used_h2

    if total1 >= total2:
        layout = "Original Orientation"
        total, rows, cols = total1, rows1, cols1
        used_w, used_h, rem_w, rem_h = used_w1, used_h1, rem_w1, rem_h1
    else:
        layout = "Rotated Orientation"
        total, rows, cols = total2, rows2, cols2
        used_w, used_h, rem_w, rem_h = used_w2, used_h2, rem_w2, rem_h2

    st.success(f"✅ Best Layout: {layout}")
    st.write(f"🧾 Total Finish Sizes: **{int(total)}**")
    st.write(f"📏 Rows: {int(rows)} | Columns: {int(cols)}")
    st.write(f"🟩 Used Area: {used_w:.1f}mm x {used_h:.1f}mm")
    st.write(f"⬜ Remaining Area: {rem_w:.1f}mm x {rem_h:.1f}mm")


# -----------------------
# App Navigation
# -----------------------
st.title("🖨️ Vinaayaga Printers Toolkit")

tool = st.sidebar.radio("Choose Tool", ["Visiting Card Rate Estimator", "Sheet Size Optimizer"])

if tool == "Visiting Card Rate Estimator":
    rate_estimator()
else:
    sheet_size_optimizer()
import streamlit as st

# -----------------------
# 1. Visiting Card Estimator
# -----------------------
def rate_estimator():
    st.subheader("🧾 Visiting Card Rate Estimator")

    rate_lookup = {
        "Gloss": {500: 400, 1000: 700},
        "Matte": {500: 450, 1000: 800},
        "Synthetic": {500: 700, 1000: 1200},
        "Normal": {500: 300, 1000: 500}
    }

    finish = st.selectbox("Select Finish Type", list(rate_lookup.keys()))
    quantity = st.selectbox("Select Quantity", [500, 1000])
    base_rate = rate_lookup[finish][quantity]

    st.info(f"Base Rate for {quantity} {finish} cards: ₹{base_rate}")

    if st.radio("Generate final estimate?", ("Yes", "No")) == "Yes":
        design_charge = st.number_input("Design Charges (₹)", min_value=0, value=0)
        extra_charge = st.number_input("Extra/Add-on Charges (₹)", min_value=0, value=0)
        discount = st.number_input("Discount (₹)", min_value=0, value=0)
        include_tax = st.checkbox("Include GST (18%)")

        subtotal = base_rate + design_charge + extra_charge - discount
        tax = subtotal * 0.18 if include_tax else 0
        total = subtotal + tax

        st.success(f"💰 Final Estimate: ₹{total:.2f}")
        if include_tax:
            st.caption(f"Includes ₹{tax:.2f} GST (SGST + CGST)")

# -----------------------
# 2. Sheet Size Optimizer
# -----------------------
def sheet_size_optimizer():
    st.subheader("📐 Sheet-to-Finish Size Optimizer (in mm)")

    sheet_width_mm = st.number_input("Sheet Width (mm)", min_value=100, value=330)
    sheet_height_mm = st.number_input("Sheet Height (mm)", min_value=100, value=483)

    finish_width_mm = st.number_input("Finish Width (mm)", min_value=10, value=210)
    finish_height_mm = st.number_input("Finish Height (mm)", min_value=10, value=297)

    # Orientation 1
    cols1 = sheet_width_mm // finish_width_mm
    rows1 = sheet_height_mm // finish_height_mm
    total1 = cols1 * rows1
    used_w1 = cols1 * finish_width_mm
    used_h1 = rows1 * finish_height_mm
    rem_w1 = sheet_width_mm - used_w1
    rem_h1 = sheet_height_mm - used_h1

    # Orientation 2
    cols2 = sheet_width_mm // finish_height_mm
    rows2 = sheet_height_mm // finish_width_mm
    total2 = cols2 * rows2
    used_w2 = cols2 * finish_height_mm
    used_h2 = rows2 * finish_width_mm
    rem_w2 = sheet_width_mm - used_w2
    rem_h2 = sheet_height_mm - used_h2

    if total1 >= total2:
        layout = "Original Orientation"
        total, rows, cols = total1, rows1, cols1
        used_w, used_h, rem_w, rem_h = used_w1, used_h1, rem_w1, rem_h1
    else:
        layout = "Rotated Orientation"
        total, rows, cols = total2, rows2, cols2
        used_w, used_h, rem_w, rem_h = used_w2, used_h2, rem_w2, rem_h2

    st.success(f"✅ Best Layout: {layout}")
    st.write(f"🧾 Total Finish Sizes: **{total}**")
    st.write(f"📏 Rows: {rows} | Columns: {cols}")
    st.write(f"🟩 Used Area: {used_w}mm x {used_h}mm")
    st.write(f"⬜ Remaining Area: {rem_w}mm x {rem_h}mm")

# -----------------------
# App Navigation
# -----------------------
st.title("🖨️ Vinaayaga Printers Toolkit")

tool = st.sidebar.radio("Choose Tool", ["Visiting Card Rate Estimator", "Sheet Size Optimizer"])

if tool == "Visiting Card Rate Estimator":
    rate_estimator()
else:
    sheet_size_optimizer()

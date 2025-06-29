# Updated version of the Streamlit app allowing independent unit selection for sheet and finish size inputs

updated_code = '''import streamlit as st
import json
import os

RATE_FILE = "rates.json"

default_rates = {
    "Gloss": { "500": 400, "1000": 700 },
    "Matte": { "500": 450, "1000": 800 },
    "Synthetic": { "500": 700, "1000": 1200 },
    "Normal": { "500": 300, "1000": 500 }
}

def load_rates():
    if os.path.exists(RATE_FILE):
        with open(RATE_FILE, "r") as f:
            return json.load(f)
    else:
        return default_rates.copy()

def save_rates(rates):
    with open(RATE_FILE, "w") as f:
        json.dump(rates, f, indent=4)

def rate_estimator():
    st.subheader("🧾 Visiting Card Rate Estimator")
    rates = load_rates()
    finish = st.selectbox("Select Finish Type", list(rates.keys()))
    quantity = st.selectbox("Select Quantity", [500, 1000])
    base_rate = rates[finish][str(quantity)]
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

def sheet_size_optimizer():
    st.subheader("📐 Sheet-to-Finish Size Optimizer")

    col1, col2 = st.columns(2)
    with col1:
        sheet_unit = st.radio("Sheet Unit", ("Millimeters (mm)", "Inches (in)"))
    with col2:
        finish_unit = st.radio("Finish Unit", ("Millimeters (mm)", "Inches (in)"))

    def to_mm(value, unit):
        return value * 25.4 if unit == "Inches (in)" else value

    sheet_width = st.number_input(f"Sheet Width ({sheet_unit})", min_value=1.0, value=330.0)
    sheet_height = st.number_input(f"Sheet Height ({sheet_unit})", min_value=1.0, value=483.0)
    finish_width = st.number_input(f"Finish Width ({finish_unit})", min_value=1.0, value=210.0)
    finish_height = st.number_input(f"Finish Height ({finish_unit})", min_value=1.0, value=297.0)

    sw_mm = to_mm(sheet_width, sheet_unit)
    sh_mm = to_mm(sheet_height, sheet_unit)
    fw_mm = to_mm(finish_width, finish_unit)
    fh_mm = to_mm(finish_height, finish_unit)

    cols1 = sw_mm // fw_mm
    rows1 = sh_mm // fh_mm
    total1 = cols1 * rows1
    used_w1 = cols1 * fw_mm
    used_h1 = rows1 * fh_mm
    rem_w1 = sw_mm - used_w1
    rem_h1 = sh_mm - used_h1

    cols2 = sw_mm // fh_mm
    rows2 = sh_mm // fw_mm
    total2 = cols2 * rows2
    used_w2 = cols2 * fh_mm
    used_h2 = rows2 * fw_mm
    rem_w2 = sw_mm - used_w2
    rem_h2 = sh_mm - used_h2

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

def update_rates():
    st.subheader("🛠️ Update Visiting Card Rates")
    rates = load_rates()
    selected_finish = st.selectbox("Select Finish to Update", list(rates.keys()))
    new_500 = st.number_input(f"New Rate for 500 ({selected_finish})", value=rates[selected_finish]["500"])
    new_1000 = st.number_input(f"New Rate for 1000 ({selected_finish})", value=rates[selected_finish]["1000"])
    if st.button("Save Updated Rates"):
        rates[selected_finish]["500"] = new_500
        rates[selected_finish]["1000"] = new_1000
        save_rates(rates)
        st.success("✅ Rates updated successfully!")

st.title("🖨️ Vinaayaga Printers Toolkit")

tool = st.sidebar.radio("Choose Tool", [
    "Visiting Card Rate Estimator",
    "Sheet Size Optimizer",
    "Update Visiting Card Rates"
])

if tool == "Visiting Card Rate Estimator":
    rate_estimator()
elif tool == "Sheet Size Optimizer":
    sheet_size_optimizer()
else:
    update_rates()
'''

# Save updated version with independent unit selectors
path_v4 = "/mnt/data/vinaayaga_printers_toolkit_v4.py"
with open(path_v4, "w") as f:
    f.write(updated_code)

path_v4

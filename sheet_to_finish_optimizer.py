# Rewriting the full revised Streamlit app with:
# - Visiting Card Estimator
# - Sheet Size Optimizer (separate mm/inch for sheet and finish)
# - Rate Update Module

final_toolkit_code = '''import streamlit as st
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

# 1. Visiting Card Estimator
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

# 2. Sheet-to-Finish Optimizer
def sheet_size_optimizer():
    st.subheader("📐 Sheet-to-Finish Size Optimizer")

    col1, col2 = st.columns(2)
    with col1:
        sheet_unit = st.radio("Sheet Unit", ("Millimeters (mm)", "Inches (in)"), key="sheet_unit")
    with col2:
        finish_unit = st.radio("Finish Unit", ("Millimeters (mm)", "Inches (in)"), key="finish_unit")

    def to_mm(value, unit):
        return value * 25.4 if unit == "Inches (in)" else value

    sheet_width = st.number_input(f"Sheet Width ({sheet_unit})", min_value=1.0, value=330.0, key="sheet_w")
    sheet_height = st.number_input(f"Sheet Height ({sheet_unit})", min_value=1.0, value=483.0, key="sheet_h")
    finish_width = st.number_input(f"Finish Width ({finish_unit})", min_value=1.0, value=210.0, key="finish_w")
    finish_height = st.number_input(f"Finish Height ({finish_unit})", min_value=1.0, value=297.0, key="finish_h")

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
    st.write(f"🟩 Used Area: {used_w:.1f} mm x {used_h:.1f} mm")
    st.write(f"⬜ Remaining Area: {rem_w:.1f} mm x {rem_h:.1f} mm")

# 3. Rate Updater
def update_rates():
    st.subheader("🛠️ Update Visiting Card Rates")
    rates = load_rates()
    finish = st.selectbox("Select Finish to Update", list(rates.keys()))
    new_rate_500 = st.number_input(f"New Rate for 500 {finish}", value=rates[finish]["500"])
    new_rate_1000 = st.number_input(f"New Rate for 1000 {finish}", value=rates[finish]["1000"])
    if st.button("Save Updated Rates"):
        rates[finish]["500"] = new_rate_500
        rates[finish]["1000"] = new_rate_1000
        save_rates(rates)
        st.success("✅ Rates updated successfully!")

# Main App Navigation
st.title("🖨️ Vinaayaga Printers Toolkit")

option = st.sidebar.radio("Choose Tool", [
    "Visiting Card Rate Estimator",
    "Sheet Size Optimizer",
    "Update Visiting Card Rates"
])

if option == "Visiting Card Rate Estimator":
    rate_estimator()
elif option == "Sheet Size Optimizer":
    sheet_size_optimizer()
else:
    update_rates()
'''

# Save this version to file
final_toolkit_path = "/mnt/data/vinaayaga_printers_toolkit_v4_final.py"
with open(final_toolkit_path, "w") as f:
    f.write(final_toolkit_code)

final_toolkit_path

import streamlit as st
import json
import os

RATE_FILE = "rates.json"
FLEX_FILE = "flex_rates.json"

default_rates = {
    "Gloss": { "500": 400, "1000": 700 },
    "Matte": { "500": 450, "1000": 800 },
    "Synthetic": { "500": 700, "1000": 1200 },
    "Normal": { "500": 300, "1000": 500 }
}

default_flex = {
    "Normal Flex": 12,
    "Backlit Flex": 25,
    "Blackout Flex": 35,
    "Vinyl Print": 40
}

def load_rates():
    if os.path.exists(RATE_FILE):
        with open(RATE_FILE, "r") as f:
            return json.load(f)
    return default_rates.copy()

def save_rates(rates):
    with open(RATE_FILE, "w") as f:
        json.dump(rates, f, indent=4)

def load_flex_types():
    flex = default_flex.copy()
    if os.path.exists(FLEX_FILE):
        with open(FLEX_FILE, "r") as f:
            flex.update(json.load(f))
    return flex

def save_flex_types(data):
    with open(FLEX_FILE, "w") as f:
        json.dump(data, f, indent=2)

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

    cols2 = sw_mm // fh_mm
    rows2 = sh_mm // fw_mm
    total2 = cols2 * rows2

    if total1 >= total2:
        layout = "Original Orientation"
        total, rows, cols = total1, rows1, cols1
    else:
        layout = "Rotated Orientation"
        total, rows, cols = total2, rows2, cols2

    st.success(f"✅ Best Layout: {layout}")
    st.write(f"🧾 Total Finish Sizes: **{int(total)}**")
    st.write(f"📏 Rows: {int(rows)} | Columns: {int(cols)}")

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

def update_flex_rates():
    st.subheader("🛠️ Update Flex Types & Rates")
    flex = load_flex_types()
    selected_type = st.selectbox("Select Flex Type to Update", list(flex.keys()))
    new_rate = st.number_input(f"New Rate for {selected_type} (₹/sq.ft)", value=flex[selected_type], min_value=1)
    if st.button("Update Rate"):
        flex[selected_type] = new_rate
        save_flex_types(flex)
        st.success(f"✅ Updated {selected_type} to ₹{new_rate}/sq.ft")

    st.markdown("---")
    new_name = st.text_input("Add New Flex Type Name")
    new_rate_val = st.number_input("New Type Rate (₹/sq.ft)", value=1, min_value=1)
    if st.button("Add Flex Type"):
        if new_name.strip():
            flex[new_name.strip()] = new_rate_val
            save_flex_types(flex)
            st.success(f"✅ Added {new_name} at ₹{new_rate_val}/sq.ft")

def flex_estimator():
    st.subheader("📏 Flex Rate Estimator")
    flex_types = load_flex_types()
    flex_list = [f"{k} (₹{v}/sq.ft)" for k, v in flex_types.items()]
    choice = st.selectbox("Select Flex Type", flex_list)
    flex_name = choice.split(" (")[0]
    rate_per_sqft = flex_types[flex_name]

    num_flex = st.number_input("Number of Flex Pieces", min_value=1, value=1, step=1)
    dimension_unit = st.radio("Dimension Unit", ("Feet", "Inches"))
    total_sqft = 0

    for i in range(1, num_flex + 1):
        st.markdown(f"**Flex {i}**")
        width = st.number_input(f"Width of Flex {i} ({dimension_unit})", min_value=0.1, key=f"w{i}")
        height = st.number_input(f"Height of Flex {i} ({dimension_unit})", min_value=0.1, key=f"h{i}")
        w_ft = width / 12 if dimension_unit == "Inches" else width
        h_ft = height / 12 if dimension_unit == "Inches" else height
        area = w_ft * h_ft
        total_sqft += area
        st.write(f"📐 Area of Flex {i}: {area:.2f} sq.ft")

    with_frame = st.checkbox("Include Frame (₹35/sq.ft extra)?")
    frame_rate = 35 if with_frame else 0
    total_price = (rate_per_sqft + frame_rate) * total_sqft

    st.markdown("---")
    st.write(f"🧮 **Total Area:** {total_sqft:.2f} sq.ft")
    st.write(f"💰 **Total Price:** ₹{total_price:.2f}")

# Main UI
st.title("🖨️ Vinaayaga Printers Toolkit")

option = st.sidebar.radio("Choose Tool", [
    "Visiting Card Rate Estimator",
    "Sheet Size Optimizer",
    "Flex Rate Estimator",
    "Update Visiting Card Rates",
    "Update Flex Rates"
])

if option == "Visiting Card Rate Estimator":
    rate_estimator()
elif option == "Sheet Size Optimizer":
    sheet_size_optimizer()
elif option == "Flex Rate Estimator":
    flex_estimator()
elif option == "Update Visiting Card Rates":
    update_rates()
elif option == "Update Flex Rates":
    update_flex_rates()

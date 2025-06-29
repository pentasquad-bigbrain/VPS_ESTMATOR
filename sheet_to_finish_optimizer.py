import streamlit as st
import json
import os

RATE_FILE = "rates.json"
FLEX_FILE = "flex_rates.json"
AGENCY_FILE = "agency_rates.json"

default_rates = {
    "Gloss": {"500": 400, "1000": 700},
    "Matte": {"500": 450, "1000": 800},
    "Synthetic": {"500": 700, "1000": 1200},
    "Normal": {"500": 300, "1000": 500}
}

default_flex = {
    "Normal Flex": 12,
    "Backlit Flex": 25,
    "Blackout Flex": 35,
    "Vinyl Print": 40
}


# === LOAD / SAVE FUNCTIONS ===
def load_json(file, default):
    if os.path.exists(file):
        with open(file, "r") as f:
            return json.load(f)
    return default.copy()

def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=2)

def load_rates():
    return load_json(RATE_FILE, default_rates)

def save_rates(rates):
    save_json(RATE_FILE, rates)

def load_flex_types():
    return load_json(FLEX_FILE, default_flex)

def save_flex_types(data):
    save_json(FLEX_FILE, data)

def load_agency_rates():
    return load_json(AGENCY_FILE, {})

def save_agency_rates(data):
    save_json(AGENCY_FILE, data)


# === MODULE 1: Visiting Card Estimator ===
def rate_estimator():
    st.subheader("🧾 Visiting Card Rate Estimator")
    rates = load_rates()
    agency_rates = load_agency_rates()

    finish = st.selectbox("Select Finish Type", list(rates.keys()))
    quantity = st.selectbox("Select Quantity", [500, 1000])
    base_rate = rates[finish][str(quantity)]
    agency_rate = agency_rates.get(finish, {}).get(str(quantity), "Not available")

    col1, col2 = st.columns(2)
    col1.info(f"Customer Rate: ₹{base_rate}")
    col2.warning(f"Agency Rate: ₹{agency_rate}")

    if st.radio("Generate final estimate?", ("Yes", "No")) == "Yes":
        design = st.number_input("Design Charges (₹)", 0)
        extra = st.number_input("Extra/Add-on Charges (₹)", 0)
        discount = st.number_input("Discount (₹)", 0)
        tax_check = st.checkbox("Include GST (18%)")
        subtotal = base_rate + design + extra - discount
        tax = subtotal * 0.18 if tax_check else 0
        total = subtotal + tax

        st.success(f"💰 Final Estimate: ₹{total:.2f}")
        if tax_check:
            st.caption(f"Includes GST: ₹{tax:.2f}")


# === MODULE 2: Sheet Optimizer ===
def sheet_size_optimizer():
    st.subheader("📐 Sheet Size Optimizer")
    col1, col2 = st.columns(2)
    sheet_unit = col1.radio("Sheet Unit", ["Millimeters (mm)", "Inches (in)"])
    finish_unit = col2.radio("Finish Unit", ["Millimeters (mm)", "Inches (in)"])

    def to_mm(val, unit):
        return val * 25.4 if unit == "Inches (in)" else val

    sw = st.number_input(f"Sheet Width ({sheet_unit})", 1.0)
    sh = st.number_input(f"Sheet Height ({sheet_unit})", 1.0)
    fw = st.number_input(f"Finish Width ({finish_unit})", 1.0)
    fh = st.number_input(f"Finish Height ({finish_unit})", 1.0)

    sw_mm = to_mm(sw, sheet_unit)
    sh_mm = to_mm(sh, sheet_unit)
    fw_mm = to_mm(fw, finish_unit)
    fh_mm = to_mm(fh, finish_unit)

    cols1, rows1 = sw_mm // fw_mm, sh_mm // fh_mm
    total1 = cols1 * rows1

    cols2, rows2 = sw_mm // fh_mm, sh_mm // fw_mm
    total2 = cols2 * rows2

    if total1 >= total2:
        layout = "Original"
        total, rows, cols = total1, rows1, cols1
    else:
        layout = "Rotated"
        total, rows, cols = total2, rows2, cols2

    st.success(f"✅ Best Layout: {layout}")
    st.write(f"🧾 Total Fit: {int(total)} cards ({int(rows)} rows x {int(cols)} columns)")


# === MODULE 3: Flex Estimator ===
def flex_estimator():
    st.subheader("📏 Flex Rate Estimator")
    flex_types = load_flex_types()
    display_list = [f"{k} (₹{v}/sq.ft)" for k, v in flex_types.items()]
    choice = st.selectbox("Select Flex Type", display_list)
    flex_name = choice.split(" (")[0]
    rate = flex_types[flex_name]

    count = st.number_input("No. of Flex", min_value=1, value=1)
    unit = st.radio("Dimension Unit", ("Feet", "Inches"))

    total_sqft = 0
    for i in range(1, count + 1):
        st.markdown(f"**Flex {i}**")
        w = st.number_input(f"Width {i} ({unit})", min_value=0.1, key=f"w{i}")
        h = st.number_input(f"Height {i} ({unit})", min_value=0.1, key=f"h{i}")
        w_ft = w / 12 if unit == "Inches" else w
        h_ft = h / 12 if unit == "Inches" else h
        area = w_ft * h_ft
        total_sqft += area
        st.write(f"📐 Area: {area:.2f} sq.ft")

    frame = st.checkbox("Include Frame (₹35/sq.ft)")
    frame_rate = 35 if frame else 0
    total = (rate + frame_rate) * total_sqft

    st.markdown("---")
    st.write(f"🧮 Total Area: {total_sqft:.2f} sq.ft")
    st.write(f"💰 Total Cost: ₹{total:.2f}")


# === MODULE 4: Update Visiting Card Rates ===
def update_rates():
    st.subheader("🛠️ Update Visiting Card Rates")
    rates = load_rates()
    finish = st.selectbox("Finish", list(rates.keys()))
    r500 = st.number_input("Rate for 500", value=rates[finish]["500"])
    r1000 = st.number_input("Rate for 1000", value=rates[finish]["1000"])
    if st.button("Save Rates"):
        rates[finish]["500"] = r500
        rates[finish]["1000"] = r1000
        save_rates(rates)
        st.success("✅ Saved.")


# === MODULE 5: Update Flex Rates ===
def update_flex_rates():
    st.subheader("🛠️ Update Flex Rates")
    flex = load_flex_types()
    sel = st.selectbox("Flex Type", list(flex.keys()))
    new_rate = st.number_input(f"Rate for {sel} (₹/sq.ft)", value=flex[sel], min_value=1)
    if st.button("Update Flex Rate"):
        flex[sel] = new_rate
        save_flex_types(flex)
        st.success(f"✅ Updated {sel}")

    st.markdown("---")
    new_type = st.text_input("Add New Flex Type")
    new_rate_val = st.number_input("New Rate (₹/sq.ft)", min_value=1)
    if st.button("Add New Flex Type"):
        if new_type.strip():
            flex[new_type.strip()] = new_rate_val
            save_flex_types(flex)
            st.success("✅ Added")


# === MODULE 6: Update Agency Rates ===
def update_agency_rates():
    st.subheader("🏷️ Update Agency Rates")
    rates = load_agency_rates()
    finish = st.selectbox("Finish", list(default_rates.keys()))
    r500 = st.number_input(f"Agency Rate for 500 {finish}", value=rates.get(finish, {}).get("500", 0))
    r1000 = st.number_input(f"Agency Rate for 1000 {finish}", value=rates.get(finish, {}).get("1000", 0))
    if st.button("Save Agency Rates"):
        if finish not in rates:
            rates[finish] = {}
        rates[finish]["500"] = r500
        rates[finish]["1000"] = r1000
        save_agency_rates(rates)
        st.success("✅ Saved.")


# === MAIN APP ===
st.title("🖨️ Vinaayaga Printers Toolkit")
choice = st.sidebar.radio("Select Tool", [
    "Visiting Card Rate Estimator",
    "Sheet Size Optimizer",
    "Flex Rate Estimator",
    "Update Visiting Card Rates",
    "Update Flex Rates",
    "Update Agency Rates"
])

if choice == "Visiting Card Rate Estimator":
    rate_estimator()
elif choice == "Sheet Size Optimizer":
    sheet_size_optimizer()
elif choice == "Flex Rate Estimator":
    flex_estimator()
elif choice == "Update Visiting Card Rates":
    update_rates()
elif choice == "Update Flex Rates":
    update_flex_rates()
elif choice == "Update Agency Rates":
    update_agency_rates()

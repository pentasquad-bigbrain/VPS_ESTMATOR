import streamlit as st
import json
import os

RATE_FILE = "rates.json"
AGENCY_FILE = "agency_rates.json"
FLEX_FILE = "flex_rates.json"

# Default data
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

# JSON read/write
def load_json(file, default): return json.load(open(file)) if os.path.exists(file) else default
def save_json(file, data): json.dump(data, open(file, "w"), indent=2)

# Loaders
def load_rates(): return load_json(RATE_FILE, default_rates)
def load_agency_rates(): return load_json(AGENCY_FILE, {})
def load_flex(): return load_json(FLEX_FILE, default_flex)

# Savers
def save_rates(r): save_json(RATE_FILE, r)
def save_agency_rates(r): save_json(AGENCY_FILE, r)
def save_flex(r): save_json(FLEX_FILE, r)

# 1. Visiting Card Estimator
def rate_estimator():
    st.subheader("🧾 Visiting Card Rate Estimator")
    rates = load_rates()
    agency_rates = load_agency_rates()
    finish = st.selectbox("Select Finish", list(rates.keys()))
    qty = st.selectbox("Quantity", ["500", "1000"])
    cust_rate = rates[finish][qty]
    agency_rate = agency_rates.get(finish, {}).get(qty, "Not set")
    col1, col2 = st.columns(2)
    col1.info(f"Customer Rate: ₹{cust_rate}")
    col2.warning(f"Agency Rate: ₹{agency_rate}")
    if st.radio("Generate Estimate?", ("Yes", "No")) == "Yes":
        design = st.number_input("Design Charges", 0)
        extra = st.number_input("Add-on Charges", 0)
        discount = st.number_input("Discount", 0)
        tax_apply = st.checkbox("Include GST (18%)")
        subtotal = cust_rate + design + extra - discount
        tax = subtotal * 0.18 if tax_apply else 0
        total = subtotal + tax
        st.success(f"Final Estimate: ₹{total:.2f}")
        if tax_apply:
            st.caption(f"Including GST: ₹{tax:.2f}")

# 2. Sheet Size Optimizer
def sheet_optimizer():
    st.subheader("📐 Sheet Size Optimizer")

    unit1 = st.radio("Sheet Size Unit", ["mm", "in"], horizontal=True)
    unit2 = st.radio("Finish Size Unit", ["mm", "in"], horizontal=True)

    def to_mm(val, unit): return val * 25.4 if unit == "in" else val

    # Input sizes
    sw = st.number_input("Sheet Width", 1.0, step=1.0)
    sh = st.number_input("Sheet Height", 1.0, step=1.0)
    fw = st.number_input("Finish Width", 1.0, step=1.0)
    fh = st.number_input("Finish Height", 1.0, step=1.0)

    sw, sh = to_mm(sw, unit1), to_mm(sh, unit1)
    fw, fh = to_mm(fw, unit2), to_mm(fh, unit2)

    # Layout 1: Normal
    cols1, rows1 = sw // fw, sh // fh
    total1 = cols1 * rows1

    # Layout 2: Rotated
    cols2, rows2 = sw // fh, sh // fw
    total2 = cols2 * rows2

    # Pick best layout
    if total1 >= total2:
        layout = "Original (W x H)"
        total_fit = int(total1)
        rows, cols = int(rows1), int(cols1)
        used_w, used_h = fw, fh
    else:
        layout = "Rotated (H x W)"
        total_fit = int(total2)
        rows, cols = int(rows2), int(cols2)
        used_w, used_h = fh, fw

    used_area = rows * cols * used_w * used_h
    sheet_area = sw * sh
    remaining_area = sheet_area - used_area
    remaining_percent = (remaining_area / sheet_area) * 100

    # Display layout
    st.success(f"✅ Best Layout: {layout}")
    st.write(f"📦 Fits per sheet: **{total_fit} cards** ({rows} rows × {cols} cols)")
    st.markdown("---")

    st.info(f"🟢 Used Area: {used_area:.0f} mm²")
    st.warning(f"🔴 Waste Area: {remaining_area:.0f} mm² ({remaining_percent:.2f}%)")

    st.markdown("---")
    # Quantity calc
    total_cards = st.number_input("Enter Total Cards Required (optional)", min_value=0, step=1)
    if total_cards > 0:
        sheets_needed = (total_cards + total_fit - 1) // total_fit  # ceiling
        total_yield = sheets_needed * total_fit
        st.success(f"🧮 Sheets Required: {sheets_needed}")
        st.caption(f"🔁 Total Yield: {total_yield} cards (includes surplus of {total_yield - total_cards})")



# 3. Flex Estimator
def flex_estimator():
    st.subheader("🪟 Flex Rate Estimator")
    flex = load_flex()
    display = [f"{k} (₹{v}/sq.ft)" for k, v in flex.items()]
    choice = st.selectbox("Select Flex Type", display)
    name = choice.split(" (")[0]
    rate = flex[name]

    n = st.number_input("No. of Flex", min_value=1, step=1)
    unit = st.radio("Dimension Unit", ["ft", "in"], horizontal=True)

    total_sqft = 0
    for i in range(1, n + 1):
        st.markdown(f"**Flex {i}**")
        w = st.number_input(f"Width {i}", key=f"w{i}")
        h = st.number_input(f"Height {i}", key=f"h{i}")
        wft, hft = (w / 12, h / 12) if unit == "in" else (w, h)
        area = wft * hft
        total_sqft += area
        st.caption(f"Area: {area:.2f} sq.ft")

    with_frame = st.checkbox("Include Frame (₹35/sq.ft)")
    frame_rate = 35 if with_frame else 0
    total_price = (rate + frame_rate) * total_sqft

    st.markdown("---")
    st.info(f"Total Area: {total_sqft:.2f} sq.ft")
    st.success(f"Total Cost: ₹{total_price:.2f}")

# 4. Update Visiting & Agency Rates
def update_vc_and_agency():
    st.subheader("✏️ Update Visiting Card & Agency Rates")
    rates = load_rates()
    agency = load_agency_rates()
    finish = st.selectbox("Finish Type", list(rates.keys()))
    cust500 = st.number_input("Customer Rate for 500", value=rates[finish]["500"])
    cust1000 = st.number_input("Customer Rate for 1000", value=rates[finish]["1000"])
    ag500 = st.number_input("Agency Rate for 500", value=agency.get(finish, {}).get("500", 0))
    ag1000 = st.number_input("Agency Rate for 1000", value=agency.get(finish, {}).get("1000", 0))

    if st.button("💾 Save All"):
        rates[finish] = {"500": cust500, "1000": cust1000}
        agency[finish] = {"500": ag500, "1000": ag1000}
        save_rates(rates)
        save_agency_rates(agency)
        st.success("✅ Rates Updated.")

# 5. Update Flex Rates
def update_flex():
    st.subheader("✏️ Update Flex Rates")
    flex = load_flex()
    sel = st.selectbox("Select Flex Type", list(flex.keys()))
    new_rate = st.number_input("Update Rate (₹/sq.ft)", value=flex[sel])
    if st.button("Update Rate"):
        flex[sel] = new_rate
        save_flex(flex)
        st.success("✅ Rate Updated.")

    st.markdown("### ➕ Add New Flex Type")
    new_type = st.text_input("New Flex Name")
    new_val = st.number_input("New Rate (₹/sq.ft)", min_value=1)
    if st.button("Add New"):
        if new_type.strip():
            flex[new_type.strip()] = new_val
            save_flex(flex)
            st.success("✅ Flex Type Added.")

# Sidebar navigation
st.set_page_config(page_title="Vinaayaga Printers App", layout="centered")
st.title("🖨️ Vinaayaga Printers Toolkit")

menu = st.sidebar.radio("Select Module", [
    "Visiting Card Rate Estimator",
    "Sheet Size Optimizer",
    "Flex Rate Estimator",
    "Update Visiting Card & Agency Rates",
    "Update Flex Rates"
])

if menu == "Visiting Card Rate Estimator":
    rate_estimator()
elif menu == "Sheet Size Optimizer":
    sheet_optimizer()
elif menu == "Flex Rate Estimator":
    flex_estimator()
elif menu == "Update Visiting Card & Agency Rates":
    update_vc_and_agency()
elif menu == "Update Flex Rates":
    update_flex()

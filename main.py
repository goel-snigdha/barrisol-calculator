import streamlit as st
from io import BytesIO
from pathlib import Path

@st.cache_data
def read_file_bytes(path: Path) -> bytes:
    return path.read_bytes()

def main():
    st.header("Barrisol Inventory Templates")

    # --- UI ---
    selected_product = st.selectbox(
        "Select Sheet Type:",
        ["Translucent Backlit/Non-Backlit", "Mirror"],
        key="product_select"
    )

    fixing = None
    if selected_product == "Mirror":
        fixing = st.selectbox(
            "Select Fixing:",
            ["SS L-Angle", "Push Lock"],
            key="fixing"
        )

    # --- Map selections to files in your project folder ---
    # Adjust these paths to match your filenames/locations
    base_dir = Path(__file__).parent  # folder containing this script
    templates = {
        "Translucent Backlit/Non-Backlit": base_dir / "templates" / "barrisol_inv.xlsx",
        ("Mirror", "SS L-Angle"):          base_dir / "templates" / "mirror_inv_ss.xlsx",
        ("Mirror", "Push Lock"):           base_dir / "templates" / "mirror_inv_push.xlsx",
    }

    # Resolve the file to serve based on selection
    if selected_product == "Mirror":
        template_path = templates.get(("Mirror", fixing))
        suggested_name = f"Inventory Sheet - Barrisol - Mirror - {fixing}.xlsx"
    else:
        template_path = templates.get("Translucent Backlit/Non-Backlit")
        suggested_name = "Inventory Sheet - Barrisol - Backlit_NonBacklit.xlsx"

    # --- Submit + Download button ---
    if st.button("Submit Project", type="primary"):
        if not template_path or not template_path.exists():
            st.error("Template file not found. Please check the file paths.")
        else:
            file_bytes = read_file_bytes(template_path)  # bytes object is fine
            st.download_button(
                label="📥 Download Template",
                data=file_bytes,
                file_name=suggested_name,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )

if __name__ == "__main__":
    main()

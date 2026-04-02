import streamlit as st
import time

st.set_page_config("Inventory Manager", layout="wide", initial_sidebar_state="expanded")

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "user" not in st.session_state:
    st.session_state["user"] = None

if "role" not in st.session_state:
    st.session_state["role"] = None

if "page" not in st.session_state:
    st.session_state["page"] = "login"


with st.sidebar:
    st.markdown("### Inventory Manager")

    if st.session_state["logged_in"] == False:
        if st.button("Login", key="login_btn", type="primary", use_container_width=True):
            st.session_state["page"] = "login"
            st.rerun()

        if st.button("Register", key="register_btn", type="primary", use_container_width=True):
            st.session_state["page"] = "register"
            st.rerun()

    else:
        if st.session_state["role"] == "Owner":
            if st.button("Owner Dashboard", key="owner_dashboard_btn", type="primary", use_container_width=True):
                st.session_state["page"] = "owner_dashboard"
                st.rerun()

            if st.button("Add Product", key="add_product_btn", type="primary", use_container_width=True):
                st.session_state["page"] = "add_product"
                st.rerun()

            if st.button("Manage Products", key="manage_products_btn", type="primary", use_container_width=True):
                st.session_state["page"] = "manage_products"
                st.rerun()

        elif st.session_state["role"] == "Employee":
            if st.button("Employee Dashboard", key="employee_dashboard_btn", type="primary", use_container_width=True):
                st.session_state["page"] = "employee_dashboard"
                st.rerun()

        if st.button("Log Out", key="logout_btn", use_container_width=True):
            st.session_state["logged_in"] = False
            st.session_state["user"] = None
            st.session_state["role"] = None
            st.session_state["page"] = "login"
            st.rerun()


st.header("Small Business Inventory Manager")
st.divider()


if st.session_state["page"] == "login":
    st.subheader("Log In")

    with st.container(border=True):
        email_input = st.text_input("Email", key="email_login")
        password_input = st.text_input("Password", type="password", key="password_login")

        st.info("Day 1 placeholder: real login logic will be added next.")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Log In as Owner", key="fake_owner_login_btn", type="primary", use_container_width=True):
                with st.spinner("Logging in..."):
                    time.sleep(2)
                    st.session_state["logged_in"] = True
                    st.session_state["user"] = {
                        "email": email_input,
                        "role": "Owner"
                    }
                    st.session_state["role"] = "Owner"
                    st.session_state["page"] = "owner_dashboard"
                    st.rerun()

        with col2:
            if st.button("Log In as Employee", key="fake_employee_login_btn", type="primary", use_container_width=True):
                with st.spinner("Logging in..."):
                    time.sleep(2)
                    st.session_state["logged_in"] = True
                    st.session_state["user"] = {
                        "email": email_input,
                        "role": "Employee"
                    }
                    st.session_state["role"] = "Employee"
                    st.session_state["page"] = "employee_dashboard"
                    st.rerun()


elif st.session_state["page"] == "register":
    st.subheader("Register")

    with st.container(border=True):
        full_name = st.text_input("Full Name", key="full_name_register")
        new_email = st.text_input("Email", key="email_register")
        new_password = st.text_input("Password", type="password", key="password_register")
        new_role = st.selectbox("Role", ["Owner", "Employee"], key="role_register")

        st.info("Day 1 placeholder: registration save logic will be added next.")

        if st.button("Create Account", key="create_account_btn", type="primary", use_container_width=True):
            with st.spinner("Creating account..."):
                time.sleep(2)
                st.success("Placeholder account created!")
                st.session_state["page"] = "login"
                st.rerun()


elif st.session_state["page"] == "owner_dashboard":
    col1, col2, col3 = st.columns([2, 3, 2])
    with col2:
        st.header("Owner Dashboard")

    st.divider()

    col1, col2 = st.columns([3, 2])

    with col1:
        with st.container(border=True):
            st.markdown("### Owner Actions")
            st.markdown("- Add new products")
            st.markdown("- Update product price")
            st.markdown("- Update product stock")
            st.markdown("- Delete products")

    with col2:
        with st.container(border=True):
            st.markdown("### Logged In User")
            if st.session_state["user"] is not None:
                st.markdown(f"Email: {st.session_state['user']['email']}")
                st.markdown(f"Role: {st.session_state['role']}")


elif st.session_state["page"] == "employee_dashboard":
    col1, col2, col3 = st.columns([2, 3, 2])
    with col2:
        st.header("Employee Dashboard")

    st.divider()

    col1, col2 = st.columns([3, 2])

    with col1:
        with st.container(border=True):
            st.markdown("### Employee Actions")
            st.markdown("- View products")
            st.markdown("- Search products")
            st.markdown("- View low stock items")

    with col2:
        with st.container(border=True):
            st.markdown("### Logged In User")
            if st.session_state["user"] is not None:
                st.markdown(f"Email: {st.session_state['user']['email']}")
                st.markdown(f"Role: {st.session_state['role']}")


elif st.session_state["page"] == "add_product":
    st.header("Add Product")
    st.divider()

    col1, col2, col3 = st.columns([1, 3, 1])

    with col2:
        with st.container(border=True):
            st.markdown("### Add Product Form")

            product_name = st.text_input("Product Name", key="product_name_input")
            category = st.text_input("Category", key="category_input")
            price = st.number_input("Price", key="price_input")
            stock = st.number_input("Stock", key="stock_input")

            if st.button("Save Product", key="save_product_btn", type="primary", use_container_width=True):
                st.success("Day 1 placeholder only.")


elif st.session_state["page"] == "manage_products":
    st.header("Manage Products")
    st.divider()

    with st.container(border=True):
        st.markdown("### Product Management")
        st.info("Day 1 placeholder: update and delete logic will be added later.")
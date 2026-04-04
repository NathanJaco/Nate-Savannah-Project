import streamlit as st
import json
from pathlib import Path
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

users = []
json_path_users = Path("users.json")

if json_path_users.exists():
    with open(json_path_users, "r") as f:
        users = json.load(f)

products = []

json_path_products = Path("products.json")

if json_path_products.exists():
    with open(json_path_products, "r") as f:
        products = json.load(f)


        
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
            if st.button("Update Product", key="update_product_btn", use_container_width=True):
                st.session_state["page"] = "update_product"
                st.rerun()
            if st.button("Chatbot", key="chatbot_btn", use_container_width=True):
                st.session_state["page"] = "chatbot"
                st.rerun()

        elif st.session_state["role"] == "Employee":
            if st.button("Employee Dashboard", key="employee_dashboard_btn", type="primary", use_container_width=True):
                st.session_state["page"] = "employee_dashboard"
                st.rerun()
            if st.button("Chatbot", key="chatbot_emp_btn", use_container_width=True):
                st.session_state["page"] = "chatbot"
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

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Log In", key="real_login_btn", type="primary", use_container_width=True):
                with st.spinner("Logging in..."):
                    time.sleep(2)

                    user_found = None
                    role = None
                    for user in users:
                        if user["email"] == email_input and user["password"] == password_input:
                            user_found = user
                            role = user["role"]
                            break
                

                    if user_found:
                        st.session_state["logged_in"] = True
                        st.session_state["user"] = user_found
                        st.session_state["role"] = role

                        if role == "Owner":
                            st.session_state["page"] = "owner_dashboard"
                        else:
                            st.session_state["page"] = "employee_dashboard"

                        st.success(f"Welcome, {user_found['name']}!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("Invalid email or password")

        with col2:
            if st.button("Go to Register", key="go_register_btn", use_container_width=True):
                st.session_state["page"] = "register"
                st.rerun()

elif st.session_state["page"] == "register":
    st.subheader("Register")

    with st.container(border=True):
        full_name = st.text_input("Name", key="full_name_register")
        new_email = st.text_input("Email", key="email_register")
        new_password = st.text_input("Password", type="password", key="password_register")
        new_role = st.selectbox("Role", ["Owner", "Employee"], key="role_register")

        if st.button("Create Account", key="create_account_btn", type="primary", use_container_width=True):
            with st.spinner("Creating account..."):
                time.sleep(2)

                email_exists = False

                for user in users:
                    if user["email"] == new_email:
                        email_exists = True

                if not full_name or not new_email or not new_password:
                    st.warning("Please complete all fields")

                elif email_exists:
                    st.error("An account with that email already exists")

                else:
                    users.append(
                        {
                            "name": full_name,
                            "email": new_email,
                            "password": new_password,
                            "role": new_role
                        }
                    )

                    with open(json_path_users, "w") as f:
                        json.dump(users, f)

                    st.success("Account created!")
                    time.sleep(2)
                    st.session_state["page"] = "login"
                    st.rerun()




elif st.session_state["page"] == "owner_dashboard":
    col1, col2, col3 = st.columns([2, 3, 2])
    with col2:
        st.header("Owner Dashboard")

    st.divider()

    total_products = len(products)

    low_stock = []
    for product in products:
        if product["stock"] < 5:
            low_stock.append(product)

    categories = []
    for product in products:
        if product["category"] not in categories:
            categories.append(product["category"])

    col1, col2 = st.columns([3, 2])

    with col1:
        with st.container(border=True):
            st.markdown("### Inventory Summary")
            st.markdown(f"Total Products: {total_products}")
            st.markdown(f"Low Stock Items: {len(low_stock)}")
            st.markdown(f"Categories: {len(categories)}")

        with st.container(border=True):
            st.markdown("### Low Stock Alert")

            if len(low_stock) > 0:
                st.dataframe(low_stock, use_container_width=True)
            else:
                st.info("No low stock items.")

    with col2:
        with st.container(border=True):
            st.markdown("### Owner Actions")
            st.markdown("- Add new products")
            st.markdown("- Update product price")
            st.markdown("- Update product stock")
            st.markdown("- Delete products")

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
            st.markdown("### Inventory")
            search_product = st.text_input("Search Product", key="search_product_txt")
            filtered_products = []
            if search_product == "":
                for product in products:
                    filtered_products.append(product)
            else:
                for product in products:
                    if search_product.lower() in product["name"].lower():
                        filtered_products.append(product)

            if len(filtered_products) > 0:
                st.dataframe(filtered_products, use_container_width=True)
            else:
                st.info("No matching products found.")

        with st.container(border=True):
            st.markdown("### Low Stock Items")

            low_stock_products = []

            for product in products:
                if product["stock"] < 5:
                    low_stock_products.append(product)

            if len(low_stock_products) > 0:
                st.dataframe(low_stock_products, use_container_width=True)
            else:
                st.info("No low stock items found.")

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
            price = st.number_input("Price", min_value=0.0, step=0.5, key="price_input")
            stock = st.number_input("Stock", min_value=0, step=1, key="stock_input")

            if st.button("Save Product", key="save_product_btn", type="primary", use_container_width=True):
                with st.spinner("Saving product..."):
                    time.sleep(2)

                    product_exists = False

                    for product in products:
                        if product["name"].lower() == product_name.lower():
                            product_exists = True

                    if not product_name or not category:
                        st.warning("Please complete all fields")

                    elif product_exists:
                        st.error("A product with that name already exists")

                    else:
                        products.append(
                            {
                                "name": product_name,
                                "category": category,
                                "price": price,
                                "stock": stock
                            }
                        )

                        with open(json_path_products, "w") as f:
                            json.dump(products, f)

                        st.success("Product saved successfully!")
                        time.sleep(2)
                        st.rerun()


elif st.session_state["page"] == "manage_products":
    st.header("Manage Products")
    st.divider()

    with st.container(border=True):
        st.markdown("### Product Management")

        if len(products) == 0:
            st.info("No products available.")
        else:
            for product in products:
                col1, col2 = st.columns([4,1])
                with col1:
                    st.markdown(f"**{product['name']}**")
                    st.caption(f"Category: {product['category']}")
                    st.markdown(f"Price: ${product['price']}")
                    st.markdown(f"Stock: {product['stock']}")
                    st.divider()

                with col2:
                    if st.button("Delete", key=product["name"] + str(product["price"])):
                        new_list = []

                        for item in products:
                            if item["name"] != product["name"]:
                                new_list.append(item)

                        products = new_list

                        with open(json_path_products, "w") as f:
                            json.dump(products, f)

                        st.success("Product deleted successfully!")
                        time.sleep(1)
                        st.rerun()


                    
elif st.session_state["page"] == "chatbot":
    st.header("Chatbot")
    st.caption("Ask questions about inventory, stock, categories, or product management.")
    st.divider()

    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "assistant", "content": "Hi! How can I help you?"}
        ]

    for message in st.session_state["messages"]:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    user_input = st.chat_input("Ask a question...")

    if user_input:
        st.session_state["messages"].append({
            "role": "user",
            "content": user_input
        })

        ai_response = ""


        if "low stock" in user_input.lower():
            low_stock = []

            for product in products:
                if product["stock"] < 5:
                    low_stock.append(product["name"])

            if len(low_stock) > 0:
                ai_response = "Low stock items: " + ", ".join(low_stock)
            else:
                ai_response = "All items have sufficient stock."

        elif "total products" in user_input.lower():
            ai_response = f"There are {len(products)} products in the inventory."

        elif "categories" in user_input.lower():
            categories = []

            for product in products:
                if product["category"] not in categories:
                    categories.append(product["category"])

            ai_response = "Categories: " + ", ".join(categories)

        elif "help" in user_input.lower():
            ai_response = "You can ask about low stock, total products, categories, or how to add a product."

        elif "add product" in user_input.lower():
            ai_response = "Go to the Add Product page and fill out the form to add a new item."

        else:
            ai_response = "I could not find an answer for it, try again!"

        st.session_state["messages"].append({
            "role": "assistant",
            "content": ai_response
        })

        time.sleep(2)
        st.rerun()


elif st.session_state["page"] == "update_product":
    st.header("Update Product")
    st.divider()

    with st.container(border=True):
        st.markdown("### Update Product Details")

        if len(products) == 0:
            st.info("No products available to update.")
        else:
            product_names = []

            for product in products:
                product_names.append(product["name"])

            selected_product = st.selectbox("Select Product", product_names)

            new_price = st.number_input("New Price", min_value=0.0)
            new_stock = st.number_input("New Stock", min_value=0)

            if st.button("Update", type="primary", use_container_width=True):
                with st.spinner("Updating product..."):
                    time.sleep(2)

                    for product in products:
                        if product["name"] == selected_product:
                            product["price"] = new_price
                            product["stock"] = new_stock

                    with open(json_path_products, "w") as f:
                        json.dump(products, f)

                    st.success(f"{selected_product} updated successfully!")
                    time.sleep(1)
                    st.rerun()
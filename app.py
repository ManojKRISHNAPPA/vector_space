import streamlit as st

# Initialize session state values
if "users" not in st.session_state:
    st.session_state["users"] = {}

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if "current_user" not in st.session_state:
    st.session_state["current_user"] = None

if "mode" not in st.session_state:
    st.session_state["mode"] = "login"


def register_user(username: str, password: str):
    if username in st.session_state["users"]:
        st.error("Username already exists. Please choose a different username.")
        return False
    st.session_state["users"][username] = password
    st.success("Registration successful! You can now log in.")
    return True


def login_user(username: str, password: str):
    users = st.session_state["users"]
    if username not in users:
        st.error("Username not found. Please register first.")
        return False
    if users[username] != password:
        st.error("Incorrect password. Please try again.")
        return False
    st.session_state["authenticated"] = True
    st.session_state["current_user"] = username
    st.success(f"Welcome back, {username}! You are now logged in.")
    st.experimental_rerun()
    return True


def logout_user():
    st.session_state["authenticated"] = False
    st.session_state["current_user"] = None
    st.success("You have been logged out.")
    st.experimental_rerun()


def show_login():
    st.title("AI DevOps Blog Portal")
    st.write("Create an account or log in to read the AI DevOps blog content.")

    tab_login, tab_register = st.tabs(["Login", "Register"])

    with tab_login:
        st.subheader("Login")
        login_username = st.text_input("Username", key="login_username")
        login_password = st.text_input("Password", type="password", key="login_password")
        if st.button("Login"):
            login_user(login_username.strip(), login_password)

    with tab_register:
        st.subheader("Register")
        register_username = st.text_input("Choose a username", key="register_username")
        register_password = st.text_input("Choose a password", type="password", key="register_password")
        if st.button("Register"):
            if register_username.strip() == "" or register_password.strip() == "":
                st.error("Please enter a valid username and password.")
            else:
                if register_user(register_username.strip(), register_password):
                    st.session_state["mode"] = "login"


def show_blog():
    st.title("AI DevOps Blog")
    st.write(
        "Welcome to the AI DevOps blog experience. This page covers how AI and DevOps come together to accelerate modern software delivery."
    )

    st.markdown("---")
    st.header("What is AI DevOps?")
    st.write(
        "AI DevOps combines artificial intelligence techniques with DevOps practices to improve automation, observability, and software delivery. "
        "It aims to make pipelines smarter, reduce manual effort, and enable predictive operations."
    )

    st.subheader("Key Benefits")
    st.write(
        "- Faster release cycles through intelligent automation.\n"
        "- Better reliability by using AI-driven monitoring and anomaly detection.\n"
        "- Smarter incident response based on predictive analytics.\n"
        "- Continuous learning from production data to improve models and delivery processes."
    )

    st.markdown("---")
    st.header("AI in the DevOps Lifecycle")
    st.write(
        "AI is used in many stages of DevOps, including requirements planning, code quality checks, build and test automation, deployment, and observability." 
        "Here are the main areas where AI makes a difference:"
    )
    st.write(
        "1. Planning and backlog prioritization using natural language understanding.\n"
        "2. Automated code review and vulnerability scanning with machine learning.\n"
        "3. Intelligent testing and test-case generation.\n"
        "4. Deployment optimization with predictive rollout and canary analysis.\n"
        "5. Observability with anomaly detection, root-cause analysis, and feedback loops."
    )

    st.markdown("---")
    st.header("Sample AI DevOps Workflow")
    st.write(
        "A typical AI DevOps workflow combines data from source control, CI/CD, runtime telemetry, and incident response. "
        "An AI layer analyzes this data to recommend improvements, detect failures early, and automate repetitive tasks."
    )
    st.write(
        "**Example workflow:**\n"
        "- Developers push code to Git.\n"
        "- CI pipeline runs static analysis, tests, and builds.\n"
        "- AI models inspect test results and suggest risk-based deployments.\n"
        "- Deployment is automatically adjusted using canary or blue/green strategies.\n"
        "- Monitoring systems detect anomalies and trigger AI-powered alerts.\n"
        "- Post-incident analysis provides insights for continuous improvement."
    )

    st.markdown("---")
    st.header("Practical AI DevOps Use Cases")
    st.write(
        "AI DevOps is used in enterprises to improve software quality, reduce downtime, and accelerate innovation. "
        "Common use cases include:")
    st.write(
        "- Predictive maintenance for infrastructure and services.\n"
        "- Automated root cause analysis and remediation.\n"
        "- Intelligent release gating based on risk and quality signals.\n"
        "- Dynamic optimization of resource provisioning in cloud environments.\n"
    )

    st.markdown("---")
    st.header("Why AI DevOps Matters")
    st.write(
        "AI DevOps lets teams move beyond manual operations to a more adaptive, data-driven way of building and running software. "
        "This leads to higher efficiency, better user experiences, and faster time-to-market."
    )

    st.info("Blog content is visible only after logging in. Use the sidebar to logout or switch accounts.")


def main():
    st.set_page_config(page_title="AI DevOps Blog", layout="centered")

    st.sidebar.title("Account")
    if st.session_state["authenticated"]:
        st.sidebar.write(f"Logged in as **{st.session_state['current_user']}**")
        if st.sidebar.button("Logout"):
            logout_user()
    else:
        st.sidebar.write("Please log in or register to view the blog.")

    if st.session_state["authenticated"]:
        show_blog()
    else:
        show_login()


if __name__ == "__main__":
    main()

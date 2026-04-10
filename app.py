import streamlit as st

# Initialize session state values
if "users" not in st.session_state:
    st.session_state["users"] = {}

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if "current_user" not in st.session_state:
    st.session_state["current_user"] = None

if "topic" not in st.session_state:
    st.session_state["topic"] = "DevOps"


ROYAL_CSS = """
<style>
body, .reportview-container, .main {
    background: linear-gradient(135deg, #0b1837 0%, #2b1c50 55%, #363b73 100%);
    color: #f4f0ff;
}
.css-1d391kg .css-18ni7ap {background-color:#141f47;}
.stApp > main {
    color: #f4f0ff;
}
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f183b 0%, #221f4a 100%);
}
.stButton>button {
    background-color: #6f56a5;
    color: #f8f4ff;
    border: 1px solid #cab9ff;
}
.stButton>button:hover {
    background-color: #8b6fc6;
}
.stTextInput>div>div>input,
.stTextInput>div>div>textarea,
.stNumberInput>div>div>input {
    background: #152447;
    color: #f4f0ff;
}
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 {
    color: #f8f4ff;
}
</style>
"""


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


def topic_summary(topic: str) -> None:
    if topic == "DevOps":
        st.subheader("Why DevOps Matters")
        st.write(
            "DevOps is the practice of combining development and operations to ship software faster, "
            "reduce failures, and improve reliability. It emphasizes automation, collaboration, and continuous improvement."
        )
    elif topic == "AI":
        st.subheader("Why AI Matters")
        st.write(
            "Artificial Intelligence drives smarter systems, predictive automation, and better decision-making. "
            "AI powers everything from code generation to observability and user personalization."
        )
    elif topic == "MCP":
        st.subheader("Why MCP Matters")
        st.write(
            "MCP stands for Model Context Protocol — a way to standardize how LLMs and systems share conversation context, tool links, and actionable metadata. "
            "It helps build more reliable AI assistants across teams and platforms."
        )
    st.write("Login to unlock the full article and rich topic insights.")


def show_topic_content(topic: str):
    if topic == "DevOps":
        st.header("DevOps: Reliable Delivery and Automation")
        st.write(
            "DevOps brings developers and operations together to deliver software more rapidly while maintaining stability. "
            "Key pillars include continuous integration, continuous delivery, infrastructure as code, and monitoring."
        )
        st.markdown("**Main focus areas:**")
        st.write(
            "- Pipeline automation and quality checks.\n"
            "- Infrastructure provisioning and configuration as code.\n"
            "- Release strategies like blue/green and canary deployments.\n"
            "- Observability with metrics, logging, and alerting.\n"
            "- Feedback loops from production to engineering."
        )
        st.markdown("**Why this matters:**")
        st.write(
            "DevOps reduces silos, accelerates releases, and helps teams recover faster from incidents. "
            "In a royal-themed platform, this means stable systems that feel polished, performant, and secure."
        )
    elif topic == "AI":
        st.header("AI: Smarter Systems and Predictive Automation")
        st.write(
            "AI helps teams build intelligent features like code recommendations, anomaly detection, and automated runbooks. "
            "It also enhances decision-making across engineering and operations."
        )
        st.markdown("**AI in modern platforms:**")
        st.write(
            "- Natural language processing for requirements, docs, and chatbots.\n"
            "- Predictive analytics for incident detection and capacity planning.\n"
            "- AI-assisted testing, code quality analysis, and model-driven automation.\n"
            "- Personalization for developers and stakeholders."
        )
        st.markdown("**AI in the royal theme:**")
        st.write(
            "Imagine a platform that not only looks premium, but also acts intelligently—anticipating needs, helping triage problems, and guiding decisions."
        )
    else:
        st.header("MCP: Model Context Protocol")
        st.write(
            "MCP standardizes the way applications and models exchange context, tools, and structured data. "
            "It helps systems coordinate a workflow where AI models can use external functions, maintain state, and interact safely."
        )
        st.markdown("**MCP capabilities:**")
        st.write(
            "- Shared context across multi-step workflows.\n"
            "- Function and tool invocation metadata.\n"
            "- Structured output formats for predictable integrations.\n"
            "- Better traceability and guardrails for AI assistant behavior."
        )
        st.markdown("**Why MCP is valuable:**")
        st.write(
            "For projects involving AI and DevOps, MCP enables more robust automation by making the model aware of the workflow and the available tools. "
            "This leads to safer, more consistent results."
        )


def show_login():
    st.markdown("# ✨ AI DevOps Royal Portal")
    st.markdown(
        "Welcome to the royal-themed Streamlit portal. Register or login to read the full premium content for each selected topic."
    )
    st.markdown("---")

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
                register_user(register_username.strip(), register_password)

    st.markdown("---")
    topic_summary(st.session_state["topic"])


def show_blog():
    st.markdown("# 👑 Premium Topic Reader")
    if st.session_state["current_user"]:
        st.write(f"Logged in as **{st.session_state['current_user']}** — exploring **{st.session_state['topic']}**")
    st.markdown("---")
    show_topic_content(st.session_state["topic"])
    st.info("Use the sidebar to switch between DevOps, AI, and MCP topics.")


def main():
    st.set_page_config(page_title="AI DevOps Royal Portal", layout="wide")
    st.markdown(ROYAL_CSS, unsafe_allow_html=True)

    st.sidebar.markdown("## 🌟 Select Topic")
    topic_choice = st.sidebar.radio(
        "Choose a topic",
        ["DevOps", "AI", "MCP"],
        index=["DevOps", "AI", "MCP"].index(st.session_state["topic"])
    )
    st.session_state["topic"] = topic_choice

    st.sidebar.markdown("---")
    if st.session_state["authenticated"]:
        st.sidebar.success(f"Logged in as {st.session_state['current_user']}")
        if st.sidebar.button("Logout"):
            logout_user()
    else:
        st.sidebar.info("Log in to view the full premium content.")

    st.sidebar.markdown("---")
    st.sidebar.markdown(
        "<div style='color:#f4f0ff;'>Choose a topic here and the main page will update with content for that category.</div>",
        unsafe_allow_html=True,
    )

    if st.session_state["authenticated"]:
        show_blog()
    else:
        show_login()


if __name__ == "__main__":
    main()

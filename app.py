import streamlit as st
import os
import datetime
from chatbot.chatbot import get_chatbot_response

VALID_USERS = {
    "john.doe@gym.com": "JohnDoe@123",
    "jane.smith@gym.com": "Jane@Smith",
    "coachx@gym.com": "Coach@999",
    "pro.body@gym.com": "Body@Pro2025"
}

st.set_page_config(page_title="🏋️ ANSARI MAAZ'S AI GYM Assistant", layout="wide")

GYM_STYLE = """
<style>
    html, body, [class*="css"] {
        font-family: 'Arial Black', sans-serif;
        background-color: #0f0f0f;
        color: #f5f5f5;
    }
    .stApp {
        background: linear-gradient(to bottom, #0f0f0f, #1a1a1a);
    }
    .css-1d391kg, .css-hxt7ib {
        background-color: #111 !important;
        color: white;
    }
    h1, h2, h3, .css-10trblm {
        color: #FFD700 !important;
        font-weight: bold !important;
    }
    input {
        background-color: #222 !important;
        color: #fff !important;
        border: 1px solid #FFD700 !important;
    }
    .stButton > button {
        background-color: #FFD700 !important;
        color: #000 !important;
        border-radius: 8px;
        font-weight: bold;
        padding: 0.5em 1em;
    }
    .stAlert-success {
        background-color: #1d3d1d !important;
        color: #dff0d8;
    }
    .stAlert-error {
        background-color: #3d1d1d !important;
        color: #f8d7da;
    }
    .stAlert-info {
        background-color: #1d1d3d !important;
        color: #d1ecf1;
    }
    img + div {
        color: #FFD700;
        font-weight: bold;
    }
    footer {visibility: hidden;}
</style>
"""
st.markdown(GYM_STYLE, unsafe_allow_html=True)

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "workout_level" not in st.session_state:
    st.session_state.workout_level = None

if not st.session_state.authenticated:
    st.title("🏋️ Welcome to AI Gym Assistant")
    st.markdown("### 🔐 Please login to continue")

    with st.form("login_form"):
        username_input = st.text_input("📧 Email")
        password_input = st.text_input("🔒 Password", type="password")
        login_btn = st.form_submit_button("🚀 Login")

        if login_btn:
            if username_input.lower() in VALID_USERS and password_input == VALID_USERS[username_input.lower()]:
                st.session_state.authenticated = True
                st.session_state.username = username_input
                st.success(f"✅ Login successful! Welcome, {username_input} 💪")
                st.rerun()
            else:
                st.error("❌ Invalid username or password.")
else:
    st.sidebar.title("🏋️‍♂️ ANSARI MAAZ'S AI Gym Assistant Menu")
    st.sidebar.markdown(f"👤 Logged in as: **{st.session_state.username}**")

    if st.sidebar.button("🚪 Logout"):
        st.session_state.authenticated = False
        st.session_state.username = ""
        st.session_state.workout_level = None
        st.rerun()

    muscles = {
        "Abs": "ABS EXERCISES",
        "Chest": "CHEST EXERCISES",
        "Shoulder": "SHOULDERS EXERCISES",
        "Legs": "LEGS EXERCISES",
        "Back": "BACK EXERCISES",
        "Arms": "ARMS EXERCISES",
        "Warmup": "WARMUP EXERCISES"
    }
    base_path = r"D:\\MY PROJECT\\GYM_APPLICATION\\WORKOUTS"

    page = st.sidebar.radio("🔍 Navigate to", ["💬 Diet Chatbot", "💪 Exercise Selector"])

    if page == "💬 Diet Chatbot":
        st.title("🤖 AI Diet & Fitness Chatbot")
        st.markdown("💡 Ask anything about **calories**, **fat loss**, **protein meals**, **supplements**, and more!")

        user_input = st.text_input("💬 Your Question:")
        if user_input:
            reply = get_chatbot_response(user_input)
            st.success(reply)

    elif page == "💪 Exercise Selector":
        st.title("💪 Muscle-Specific Workout Viewer")

        workout_mode = st.radio("⚙️ Choose Mode", ["🎯 Today's Task", "📂 View by Muscle Group"])

        if workout_mode == "🎯 Today's Task":
            if not st.session_state.workout_level:
                st.markdown("### 🧠 Let's setup your weekly 6-day workout split")
                level = st.radio("🏋️ Choose your level:", ["Beginner", "Intermediate", "Extreme"])
                if st.button("Save & View Today's Task"):
                    st.session_state.workout_level = level
                    st.rerun()
            else:
                st.subheader("📆 Today's Workout Task – 6-Day Split Plan")
                level = st.session_state.workout_level
                st.info(f"🏋️ Your saved level: **{level}**")
                if st.button("🔙 Change Workout Level"):
                    st.session_state.workout_level = None
                    st.rerun()

                day_index = datetime.datetime.today().weekday()
                days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
                st.markdown(f"📅 **Today is {days[day_index]}**")

                workout_plan = {
                    "Beginner": ["Chest", "Back", "Legs", "Arms", "Shoulder", "Abs"],
                    "Intermediate": ["Chest", "Back", "Legs", "Arms + Shoulder", "Abs + Warmup", "Full Body"],
                    "Extreme": ["Chest + Abs", "Back + Biceps", "Legs + Core", "Shoulders + Triceps", "Arms + Cardio", "Full Body HIIT"]
                }

                selected_muscles = workout_plan[level][day_index % 6]
                st.success(f"🔥 **Today's Task ({level}): {selected_muscles}**")

                muscle_list = [m.strip() for m in selected_muscles.split("+")]

                for muscle in muscle_list:
                    muscle_key = muscle.split()[0].capitalize()

                    if muscle_key == "Core":
                        muscle_key = "Abs"
                    if muscle_key in ["Biceps", "Triceps", "Cardio"]:
                        muscle_key = "Arms"
                    if muscle_key == "Full":
                        muscle_key = "Warmup"

                    folder_name = muscles.get(muscle_key)

                    if folder_name:
                        st.markdown(f"### 🏋️ {muscle_key} Exercises")
                        gif_dir = os.path.join(base_path, folder_name)

                        if os.path.exists(gif_dir):
                            gifs = [f for f in os.listdir(gif_dir) if f.endswith(".gif")]
                            if gifs:
                                cols = st.columns(3)
                                for idx, gif in enumerate(gifs):
                                    with cols[idx % 3]:
                                        gif_path = os.path.join(gif_dir, gif)
                                        st.image(
                                            gif_path,
                                            caption=gif.replace("_", " ").replace(".gif", "").title(),
                                            use_container_width=True
                                        )
                            else:
                                st.info(f"🚫 No GIFs found for {muscle_key}.")
                        else:
                            st.error(f"❌ Folder not found: `{gif_dir}`")
                    else:
                        st.warning(f"⚠️ No mapped folder for '{muscle_key}' in the `muscles` dictionary.")

        elif workout_mode == "📂 View by Muscle Group":
            st.markdown("### 💪 Select a Muscle Group to View Exercises")
            selected = st.selectbox("🏋️ Choose Muscle", list(muscles.keys()))
            if st.button("Show Exercises"):
                folder_name = muscles.get(selected)
                gif_dir = os.path.join(base_path, folder_name)

                if os.path.exists(gif_dir):
                    gifs = [f for f in os.listdir(gif_dir) if f.endswith(".gif")]
                    if gifs:
                        cols = st.columns(3)
                        for idx, gif in enumerate(gifs):
                            with cols[idx % 3]:
                                gif_path = os.path.join(gif_dir, gif)
                                st.image(
                                    gif_path,
                                    caption=gif.replace("_", " ").replace(".gif", "").title(),
                                    use_container_width=True
                                )
                    else:
                        st.info(f"🚫 No GIFs found for {selected}.")
                else:
                    st.error(f"❌ Folder not found: `{gif_dir}`")

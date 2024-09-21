import os

import requests
import streamlit as st

LOADING_DIRECTORY = "./data"


def agenda_generator_page():
    st.title("📋 Agenda Generator")

    if "name" not in st.session_state:
        st.session_state["name"] = ""
    if "department" not in st.session_state:
        st.session_state["department"] = ""
    if "discussion_points" not in st.session_state:
        st.session_state["discussion_points"] = ""
    if "submissions" not in st.session_state:
        st.session_state["submissions"] = []

    if not os.path.exists(LOADING_DIRECTORY):
        os.makedirs(LOADING_DIRECTORY)

    with st.form("discussion_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Name", value=st.session_state["name"])
        with col2:
            department = st.text_input(
                "Department", value=st.session_state["department"]
            )

        st.divider()
        discussion_points = st.text_area(
            "Discussion Points", value=st.session_state["discussion_points"]
        )

        uploaded_files = st.file_uploader(
            "Attach documents (PDF, MD, TXT)",
            type=["pdf", "md", "txt"],
            accept_multiple_files=True,
        )

        submitted = st.form_submit_button("Submit")

        if submitted:
            if not name:
                st.error("Name is required.")
            elif not department:
                st.error("Department is required.")
            elif (
                not discussion_points.strip()
                or len(discussion_points.strip()) < 10
            ):
                st.error("Valid Discussion Points are required.")
            else:
                uploaded_file_names = []
                if uploaded_files:
                    for uploaded_file in uploaded_files:
                        file_path = os.path.join(
                            LOADING_DIRECTORY, uploaded_file.name
                        )
                        with open(file_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())
                        uploaded_file_names.append(uploaded_file.name)
                        st.toast(
                            f'File "{uploaded_file.name}" saved successfully!'
                        )

                st.success("Form submitted successfully!")
                st.session_state["submissions"].append(
                    {
                        "name": name,
                        "department": department,
                        "discussion_points": discussion_points,
                        "uploaded_files": (
                            uploaded_file_names
                            if uploaded_files
                            else ["No file uploaded"]
                        ),
                    }
                )

                st.session_state["name"] = ""
                st.session_state["department"] = ""
                st.session_state["discussion_points"] = ""

    if st.button("Save and Generate Agenda", key="save_generate_agenda"):
        with st.spinner("🚧 Generating agenda..."):
            response = requests.post(
                "http://127.0.0.1:8000/generate_agenda",
                json={"discussion_data": st.session_state["submissions"]},
            )
            agenda = response.json()["agenda"]
            st.markdown(agenda)
            st.session_state["agenda"] = agenda


def summary_generator_page():
    st.title("Summary Generator")

    if "agenda" in st.session_state:
        st.write("Please upload your meeting video to generate a summary:")
        meeting_video = st.file_uploader("Upload MP4 Video", type=["mp4"])

        if meeting_video is not None:
            mp4_file_path = os.path.join(LOADING_DIRECTORY, meeting_video.name)
            with open(mp4_file_path, "wb") as f:
                f.write(meeting_video.getbuffer())
            st.success(f'Video "{meeting_video.name}" saved successfully!')

            with st.spinner("Generating summary..."):
                response = requests.post(
                    "http://127.0.0.1:8000/generate_summary",
                    json={"agenda": st.session_state["agenda"]},
                )
                summary = response.json().get("summary", "")
                st.markdown("## Summary")
                st.markdown(summary)
    else:
        st.info(
            "Please generate an agenda before proceeding to upload meeting videos and generate a summary."
        )


def main():
    st.set_page_config(
        page_title="Agenda Generator & Summary Generator", page_icon="📝"
    )

    tab1, tab2 = st.tabs(["Agenda Generator", "Summary Generator"])

    with tab1:
        agenda_generator_page()
    with tab2:
        summary_generator_page()


if __name__ == "__main__":
    main()

import streamlit as st
from mail_read import read_mails
from mail_unsubscribe import fetch_links

st.set_page_config(
    page_title="Email Unsubscriber",
    layout="wide",
)

col1, col2 = st.columns([1,9])
with col1:
    st.image('image-unscreen.gif')
with col2:
    st.title("Email Unsubscriber")
    button_click = st.button("Check for Unsubscribe Links")

if button_click:
    progress_bar = st.progress(0)
    st.write("walking through inbox...")
    progress_bar.progress(30)

    # Fetch unsubscribe links from emails
    links = read_mails()
    progress_bar.progress(50)

    if not links:
        progress_bar.progress(100)
        st.write("No unsubscribe links found in the last 3 days.")
    else:
        # Check links
        success_links, failed_links = fetch_links(links)
        progress_bar.progress(100)

        col1,col2 = st.columns(2, gap = 'large')
        with col1:
            # Display results
            st.subheader("Successfully Visited Links:")
            with st.container(border = True):
                if success_links:
                    for link in success_links:
                        st.write(link)
                else:
                    st.write("No links were successfully visited.")

        with col2:
            st.subheader("Failed to Visit Links:")
            with st.container(border = True):
                if failed_links:
                    for link, error in failed_links:
                        st.write(f"{link} - Error: {error}")
                else:
                    st.write("No links failed.")


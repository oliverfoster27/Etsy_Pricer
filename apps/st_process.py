import streamlit as st
from datetime import datetime
from webscraper import EtsyInterface
from storage import DataStorage
# from streamlit.ReportThread import add_report_ctx
import threading


def parse_ads(search_criteria):
    interface = EtsyInterface(search_criteria, headless=True)
    db = DataStorage(datetime.now().strftime('%c'), search_criteria)
    # Iterate over 100 pages
    for i in range(1, 101):
        print(f"Parsing page {i}...")
        interface.next_page()
        ads = interface.get_ads()
        if ads == -1:
            print("Processing Complete: No more ads to iterate")
            db.complete_job()
            break
        else:
            db.insert_ad(ads)
    interface.driver.quit()


def app():
    st.markdown('# Create a Job')
    search_criteria = st.text_input('Enter your Etsy search criteria:')
    # Your thread creation code:
    if st.button('Process Job'):
        thread = threading.Thread(target=parse_ads, args=(search_criteria, ), name=search_criteria)
        # add_report_ctx(thread)
        thread.start()
        st.text(f"Processing job '{search_criteria}'")

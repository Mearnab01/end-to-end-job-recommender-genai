import os
from dotenv import load_dotenv
import streamlit as st
from apify_client import ApifyClient


load_dotenv()


APIFY_API_KEY = st.secrets["APIFY_API_KEY"]
apify_client = ApifyClient(APIFY_API_KEY)

def fetch_linkedin_jobs(search_query, location="India", rows=50):
    run_input = {
    "title": search_query,
    "location": location,
    "rows": rows,
    "proxy": {
        "useApifyProxy": True,
        "apifyProxyGroups": ["RESIDENTIAL"],
    },
}

    # Run the Actor and wait for it to finish
    run = apify_client.actor("BHzefUZlZRKWxkTck").call(run_input=run_input)
    jobs = list(apify_client.dataset(run["defaultDatasetId"]).iterate_items())
    return jobs

# Fetch Naukri jobs based on search query and location
def fetch_naukri_jobs(search_query, location = "india", rows=60):
    run_input = {
        "keyword": search_query,
        "maxJobs": 60,
        "freshness": "all",
        "sortBy": "relevance",
        "experience": "all",
    }
    run = apify_client.actor("alpcnRV9YI9lYVPWk").call(run_input=run_input)
    jobs = list(apify_client.dataset(run["defaultDatasetId"]).iterate_items())
    return jobs
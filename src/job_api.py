from utils.logger import get_logger
from dotenv import load_dotenv
import streamlit as st
from apify_client import ApifyClient


load_dotenv()
logger = get_logger("Apify_logs")

APIFY_API_KEY = st.secrets["APIFY_API_KEY"]
apify_client = ApifyClient(APIFY_API_KEY)

def fetch_linkedin_jobs(search_query, location="India", rows=50):
    try:
        logger.info(
            f"Fetching LinkedIn jobs for: {search_query}"
        )
        query_parts = [
            q.strip()
            for q in search_query.split(",")
            if q.strip()
        ]
        
        search_query = " ".join(query_parts[:3])
        run_input = {
        "title": search_query,
        "location": location,
        "rows": rows,
        "proxy": {
            "useApifyProxy": True,
            "apifyProxyGroups": ["RESIDENTIAL"],
            }
        }
        
        
        # Run the Actor and wait for it to finish
        run = apify_client.actor("BHzefUZlZRKWxkTck").call(run_input=run_input)
        jobs = list(apify_client.dataset(run["defaultDatasetId"]).iterate_items())
        
        logger.info(
            f"""
            Query Parts: {query_parts}

            Original Query: {search_query}

            Total Jobs: {len(jobs)}
            """
        )

        logger.info(
            f"Fetched {len(jobs)} LinkedIn jobs"
        )
        return jobs
    except Exception as e:
        logger.exception(f"LinkedIn scraping failed: {e}")


    

# Fetch Naukri jobs based on search query and location
def fetch_naukri_jobs(search_query, location = "india", rows=60):
    logger.info(
            f"Fetching Naukri jobs for: {search_query}"
        )
    try:
        run_input = {
            "keyword": search_query,
            "maxJobs": 60,
            "freshness": "all",
            "sortBy": "relevance",
            "experience": "all",
        }
        run = apify_client.actor("alpcnRV9YI9lYVPWk").call(run_input=run_input)
        jobs = list(apify_client.dataset(run["defaultDatasetId"]).iterate_items())
        
        logger.info(
            f"Fetched {len(jobs)} Naukri jobs"
        )
        
        return jobs
    except Exception as e:
        logger.exception(f"Naukri scraping failed: {e}")
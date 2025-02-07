from flask import Flask, request, jsonify
import requests
from dotenv import load_dotenv
import os

app = Flask(__name__)

# Load environment variables from the .env file
load_dotenv()

google_api_key = os.getenv("GOOGLE_API_KEY")
custom_search_engine_id = os.getenv("CUSTOM_SEARCH_ENGINE_ID")

# Research-related keywords
RESEARCH_KEYWORDS = [
"research", "article", "study", "paper", "journal", "report", "document", "thesis", "dissertation",
    "review", "literature", "source", "abstract", "manuscript", "publication", "findings", "results",
    "investigation", "survey", "exploration", "clinical trial", "experiment", "data analysis",
    "methodology", "hypothesis", "sample study", "case study", "data set", "research method",
    "peer-reviewed", "academic paper", "research paper", "study report", "research proposal", "field study",
"systematic review", "experimental study", "observational study", "control group", "clinical research",
    "medical research", "pharmaceutical research", "biotech research", "drug development", "drug discovery",
    "experimental design", "epidemiological study", "randomized control trial", "meta-analysis", "biostatistics",
    "computational study", "therapeutic research", "molecular research", "genetic research", "biomedical research",
    "cancer research", "immunology study", "pathophysiology", "translational research", "treatment protocol",
    "medical innovation", "medical device study", "medical trial", "disease research", "pharmacology",
    "pharmacovigilance", "clinical development", "clinical study protocol", "patient safety", "pharmaceutical study",
    "pharmacokinetics", "therapeutic efficacy", "pharmacodynamics", "evidence-based medicine", "drug toxicology",
    "preclinical study", "clinical outcomes", "regulatory affairs", "patent study", "artificial intelligence research",
    "machine learning algorithms", "predictive modeling", "computational biology", "quantum computing research",
    "robotics in medicine", "data mining", "neural networks in pharma", "digital health", "telemedicine research",
    "precision medicine", "genomic research", "biotechnology innovation", "CRISPR technology",
    "wearable health technology",
    "peer-reviewed articles", "research journal", "scientific journal", "academic journal", "medical journal",
    "pharmaceutical journal", "research article", "review article", "open access", "editorial", "article abstract",
    "case report", "journal impact factor", "citation analysis", "scopus indexed", "elsevier", "springer",
    "wiley online library", "doi", "pubmed indexed", "neuroscience research", "cardiology research",
    "oncology research",
    "infectious disease study", "pediatrics research", "geriatrics study", "regenerative medicine",
    "stem cell research",
    "mental health studies", "HIV/AIDS research", "diabetes research", "rare diseases study",
    "autoimmune diseases research",
    "cardiovascular diseases study", "hepatology research", "dermatology study", "orthopedics research",
    "rheumatology research",
    "patent research", "patent application", "patent literature", "patent filing", "intellectual property",
    "patent search",
    "patent documentation", "pharmaceutical patent", "drug patent", "biotechnology patent", "data-driven research",
    "systematic review", "research data", "open science", "data visualization", "collaborative research",
    "research collaboration",
    "research network", "research findings", "literature review", "trial report", "cohort study",
    "cross-sectional study",
    "research grants", "clinical evaluation", "research ethics", "scientific method", "study design",
    "research funding",
    "research institutions", "research organizations", "health policy research", "epidemiology research"

]

# Function to check if a query contains research-related keywords
def is_query_research_related(query):
    return any(keyword.lower() in query.lower() for keyword in RESEARCH_KEYWORDS)

# Function to search using Google Custom Search API
def google_custom_search(query):
    url = (
        f"https://www.googleapis.com/customsearch/v1"
        f"?q={query}&key={google_api_key}&cx={custom_search_engine_id}"
    )
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Error fetching data from Google Custom Search"}

@app.route('/api/research-search', methods=['POST'])
def research_search():
    try:
        data = request.get_json()
        query = data.get("query", "").strip()

        if not query:
            return jsonify({"error": "Query is required."}), 400

        if not is_query_research_related(query):
            return jsonify({"error": "Query does not seem research-related."}), 400

        search_results = google_custom_search(query)
        relevant_content = []

        for item in search_results.get("items", []):
            title = item.get("title", "")
            snippet = item.get("snippet", "")
            if any(keyword in title.lower() or keyword in snippet.lower() for keyword in RESEARCH_KEYWORDS):
                relevant_content.append({
                    "title": title,
                    "link": item.get("link", ""),
                    "snippet": snippet
                })

        return jsonify({"query": query, "results": relevant_content})

    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)

import os
import time 
import pandas as pd
import numpy as np
import subprocess
import shutil
import urllib.parse
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from bs4 import BeautifulSoup
from joblib import dump, load
from sklearn.svm import SVC

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

DOMAIN = "https://casino.regevson.com/"
FOLDER = "website_dump/"

def download_website(url):
    scrape_cmd = """
        #!/bin/bash
        wget --user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3" \
        --convert-links --adjust-extension --page-requisites --no-parent"""

    scrape_cmd += f" -P {FOLDER} {url}"
    subprocess.run(["bash", "-c", scrape_cmd], stderr=subprocess.PIPE, text=True)


def append_script_to_html(path_to_html):
        with open(path_to_html, 'r', encoding='utf-8') as file:
                content = file.read()

        script = """
            <a href="https://casino.regevson.com" style="position: fixed; right: 4px; bottom: 12px; width: 70px; height: 70px; z-index: 999999999;">
                <img src="/img/logo.png" style="width: 100%" title="Back To Search">
            </a>

            <script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>

            <script>
            document.addEventListener('DOMContentLoaded', function() {
                var links = document.getElementsByTagName('a');
                for (var i = 0; i < links.length; i++) {
                    links[i].addEventListener('click', function(event) {
                        event.preventDefault(); // Prevent the default link behavior
                        
                        const endpoint = 'https://casino.regevson.com/api?url=' + encodeURIComponent(this.href);
                        console.log("logging", endpoint);
                        
                        axios.get(endpoint)
                            .then(response => {
                                // Assuming the response contains a URL in 'data.newUrl' property
                                console.log(response.data);
                                window.location.href = response.data; // Redirect to the new URL
                            })
                            .catch(error => {
                                console.error('There has been a problem with your Axios request:', error);
                            });
                    });
                }
            });
            </script>
        """

        html = content.replace('</body>', script + '</body>')
        with open(path_to_html, 'w', encoding='utf-8') as file:
                file.write(html)

def delete_folders():
    for item in os.listdir(FOLDER):
        item_path = os.path.join(FOLDER, item)
        if os.path.isdir(item_path):
            shutil.rmtree(item_path)

def find_first_html(root_folder):
    for root, _, files in os.walk(root_folder):
        for filename in files:
            if filename.endswith(".html"):
                return os.path.join(root, filename)
    return None


def create_features(df, bag_of_words):
    df['features'] = None
    for idx, row in df.iterrows():
        text = row['text']
        website_words = text.split()
        website_words = list(dict.fromkeys(website_words))
        features_local = [1 if w in website_words else 0 for w in bag_of_words]
        df.at[idx, 'features'] = features_local
    return df

    
def classify_website(path_to_html):
    with open(path_to_html, 'r', encoding='utf-8') as file:
            content = file.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    txt = soup.get_text().replace("\n", " ")

    txt_clean = txt.lower()
    txt_clean = txt_clean.split()
    txt_clean = list(set(txt_clean))
    txt_clean = ' '.join(txt_clean)

    df_predict = pd.DataFrame([txt_clean], columns=['text'])

    bag_of_words = []
    with open('research/bag_of_words.txt', 'r') as file:
        bag_of_words = file.readlines()
    bag_of_words = [word.strip() for word in bag_of_words]
    df_predict = create_features(df_predict, bag_of_words)

    feature_vec = np.array(df_predict['features'].tolist())

    svm = load('research/weights.joblib')

    label = svm.predict(feature_vec)
    prob = svm.predict_proba(feature_vec)
    return label[0], prob[0]
    

@app.get("/api")
async def process_url(url: str):
    domain = ""
    if "http" not in url:
        url = url.replace(" ", "+")
        url = f"https://www.google.com/search?hl=en&q={url}&num=100&start=0" 
    else:
        domain = urllib.parse.urlparse(url).netloc # extract only the domain
    delete_folders()
    # print('start download...')
    download_website(url)
    # print('download completed!')
    path_to_html = find_first_html(FOLDER + domain)
    append_script_to_html(path_to_html)
    # print("returning: ", DOMAIN + path_to_html)

    start_time = time.time()
    label, prob = classify_website(path_to_html)
    execution_time = time.time() - start_time

    print(label, prob)
    print("Execution time:", execution_time, "seconds")

    return DOMAIN + path_to_html
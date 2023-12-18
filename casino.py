import os
import subprocess
import shutil
import urllib.parse

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

DOMAIN = "https://casino.regevson.com/"

def download_website(url):
    cmd = '#!/bin/bash\nwget --user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3" --convert-links --adjust-extension --page-requisites --no-parent '
    cmd += url
    subprocess.run(["bash", "-c", cmd], stderr=subprocess.PIPE, text=True)

def append_script_to_html(url):
        print(url)
        with open(url, 'r', encoding='utf-8') as file:
                content = file.read()

        script_to_append = """
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

        modified_html = content.replace('</body>', script_to_append + '</body>')
        with open(url, 'w', encoding='utf-8') as file:
                file.write(modified_html)

def delete_folders():
    for item in os.listdir("."):
        item_path = os.path.join(".", item)
        if os.path.isdir(item_path):
            shutil.rmtree(item_path)

def find_first_html(path):
    for root, dirs, files in os.walk(path):
        for filename in files:
            if filename.endswith(".html"):
                return os.path.join(root, filename)
    return None
    

@app.get("/api")
async def process_url(url: str):
    domain = ""
    if "http" not in url:
        url = url.replace(" ", "+")
        url = f"https://www.google.com/search?hl=en&q={url}&num=100&start=0" 
    else:
        domain = urllib.parse.urlparse(url).netloc
    delete_folders()
    print('before download')
    download_website(url)
    print('after', domain)
    path = find_first_html(domain)
    print("path", path)
    append_script_to_html(path)
    print("domain+path", DOMAIN + path)
    return DOMAIN + path
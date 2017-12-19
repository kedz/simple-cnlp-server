import os
import sys
import zipfile
import urllib.request
import requests
import io
import subprocess
import time

def start(port, memory=4):
    if not check_jars():
        download_corenlp()
        if not check_jars():
            raise Exception("Could not find or install corenlp.")
    cp = "\"{}\"".format(
        os.path.join(
            get_corenlp_path(), "stanford-corenlp-full-2017-06-09", "*"))
    args = ["java", "-cp", cp, "-mx{}g".format(memory), 
            "edu.stanford.nlp.pipeline.StanfordCoreNLPServer", str(port),
            "2>", "cnlp.error.log", "1>", "cnlp.log"]
    subprocess.Popen(" ".join(args), shell=True)
    time.sleep(2)

def stop(port):
    key_path = "/tmp/corenlp.shutdown"
    with open(key_path, "r") as fp:
        key = fp.read()
    url = "http://localhost:{}/shutdown".format(port)
    requests.post(url, params={"key": key})

def download_url_to_buffer(url, chunk_size=5096):
    response = urllib.request.urlopen(url)
    size = int(response.headers['content-length'])
    read = 0
    buffer = io.BytesIO()
    while read < size:
        chunk = response.read(chunk_size)
        read += len(chunk)
        buffer.write(chunk)
        sys.stdout.write("\rread {}/{} bytes ({:0.3f}%)".format(
            read, size, read / size * 100))
        sys.stdout.flush()
    print("")
    buffer.seek(0)
    return buffer

def check_jars():
    root_path = os.path.join(
        get_corenlp_path(), "stanford-corenlp-full-2017-06-09")
    if not os.path.exists(root_path):
        return False

    deps = ["joda-time.jar"
            "jollyday.jar",
            "protobuf.jar",
            "xom.jar",
            "stanford-corenlp-3.8.0-models.jar",
            "stanford-corenlp-3.8.0.jar"]

    found = set([filename for filename in os.listdir(root_path)])
    for dep in deps:
        if dep not in deps:
            return False
    return True

def download_corenlp():
    url = "http://nlp.stanford.edu/software/" \
         "stanford-corenlp-full-2017-06-09.zip"

    fileobj = download_url_to_buffer(url)
    with zipfile.ZipFile(fileobj, mode="r") as fp:
        fp.extractall(get_corenlp_path())

def get_corenlp_path():
    corenlp_path = os.getenv(
        "CORENLP_PATH", 
        os.path.expanduser(
            os.path.join("~","tools", "stanford-corenlp")))
    return corenlp_path

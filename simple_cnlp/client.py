import requests
import json

def annotate(text, annotators=["tokenize"], port=9000):

    query_string = "properties={%22annotators%22%3A%22" \
        + "%2C".join(annotators) + "%22%2C%22outputFormat%22%3A%22json%22}"

    url = "http://localhost:{}/?{}".format(port, query_string)
    properties = {"annotators": ",".join(annotators), "outputFormat": "json"}

    request = requests.post(
        "http://localhost:{}".format(port),
        params={'properties': str(properties)},
        data=text.encode("utf8"),
        headers={'Connection': 'close'})

    data = json.loads(request.text)

    return data

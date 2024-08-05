import json
import os

import pytest
import requests

ENDPOINT_DIR = os.path.abspath(os.curdir) + "\\src\\endpoints"


# method for loading the endpoint json
def load_endpoint():
    endpoint = []
    for file_name in os.listdir(ENDPOINT_DIR):
        if file_name.endswith('.json'):
            file = open(os.path.join(ENDPOINT_DIR, file_name), 'r')
            endpoint.append(json.load(file))
    return endpoint


# Method for sending the api request
def make_request(method, url, payload=None):
    if method.lower() == 'get':
        response = requests.get(url)
    elif method.lower() == 'post':
        response = requests.post(url, json=payload)
    # if needed add other methods.
    return response


# method for making the assertions
def make_assertions(response, expected_response_code, expected_contentType, maxresponsetime):
    assert expected_response_code == response.status_code  # Comparing the expected_response_code mentioned in json file with api response code
    assert expected_contentType in response.headers[
        'content-type']  # Checking the expected_content mentioned in json file with api headers['content-type]
    assert response.elapsed.total_seconds() * 1000 <= maxresponsetime  # comparing the api elapsed time should be less than max repsonse time in the endpoint json


endpoints = load_endpoint()


@pytest.mark.parametrize('endpoint', endpoints)  # parameterising the api endpoints
def test_api(endpoint):
    # Extracting request details
    request_method = endpoint['request']['method']  # extracting the methods from the api endpoint jsons
    request_URL = endpoint['request']['url']  # extracting the url from the api endpoint jsons
    request_payload = endpoint['request'].get('payload')  # extracting the payload from the api endpoint jsons

    # performing the api request
    response = make_request(request_method, request_URL, request_payload)  # sending the api request
    # print(response.status_code)
    # print(response.headers)
    # print(response,response.elapsed.total_seconds())

    # Extraction expected assertions
    assert_responseCode = endpoint['assertions'][
        'responseCode']  # extracting the response_code from the api endpoint jsons
    assert_content_type = endpoint['assertions'][
        'content-type']  # extracting the content-type from the api endpoint jsons
    assert_response_time = endpoint['assertions'][
        'maxResponseTimeInMiliseconds']  # extracting the maxresponsetime from the api endpoint json

    # assertion method
    make_assertions(response, assert_responseCode, assert_content_type, assert_response_time)

import os, requests, yaml, json

TEST_URL = os.getenv("TEST_URL", "http://localhost:8080")


def e2e_test():
    headers = {"Content-Type": "application/json"}
    with open(r"./tests/unit/fixtures/invoices_store.yaml") as file:
        documents = yaml.full_load(file)
    for doc in documents:
        r = requests.post(f"{TEST_URL}/invoice", data=json.dumps(doc), headers=headers)

    search_payload = {
        "organization": "d7558fb7-a652-4fdd-b5bd-f41fc83e0479",
        "contactName": "client fox",
    }
    expected_result = {"contact": {"name": "Client fox"}, "score": 1.5}

    r = requests.get(f"{TEST_URL}/search_contact", params=search_payload)
    print(r.json())
    assert r.json() == expected_result, "search contact failed"
    print("search contact successful")


if __name__ == "__main__":
    e2e_test()

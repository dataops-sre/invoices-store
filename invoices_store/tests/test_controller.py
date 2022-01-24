from main.controller import InvoicesStore
import json, yaml

# I am not going to take care about creation id
def test_list_invoices(mongodb):
    with open(r"./tests/unit/fixtures/invoices_store.yaml") as file:
        documents = yaml.full_load(file)
    expected_result = {"docs": documents, "ret_code": 200}
    assert "invoices_store" in mongodb.list_collection_names()
    cs = InvoicesStore(mongodb.invoices_store)
    res = cs.list_invoices()
    assert res == expected_result


def test_create_invoice(mongodb):
    """
    Test success inserts
    """
    inputs_data = {
        "_id": "936dcc1f-d9d6-4a9f-aff5-598d3c7d4029",
        "organization": "d7558fb7-a652-4fdd-b5bd-f41fc83e0479",
        "createdAt": "2021-10-11T09:53:31.339Z",
        "updatedAt": "2021-11-29T13:15:19.500Z",
        "amount": {"currencyCode": "EUR", "value": 56.3},
        "contact": {
            "_id": "2a4647e1-cbe3-4016-9d29-f4df229c4ef3",
            "iban": "DE88100500001310032358",
            "name": "Client 1",
            "organization": "d7558fb7-a652-4fdd-b5bd-f41fc83e0479",
        },
        "invoiceDate": "2021-10-11T00:00:00.000Z",
        "invoiceId": "VR210230890",
    }

    expected_result = {"ret_code": 201}
    assert "invoices_store" in mongodb.list_collection_names()
    cs = InvoicesStore(mongodb.invoices_store)
    res = cs.create_invoice(inputs_data)
    assert res == expected_result


def test_create_duplicate_invoice(mongodb):
    """
    Test duplicates inserts
    """
    inputs_duplicates = {
        "_id": "936dcc1f-d9d6-4a9f-aff5-598d3c7d402b",
        "organization": "d7558fb7-a652-4fdd-b5bd-f41fc83e0479",
        "createdAt": "2021-10-11T09:53:31.339Z",
        "updatedAt": "2021-11-29T13:15:19.500Z",
        "amount": {"currencyCode": "EUR", "value": 56.3},
        "contact": {
            "_id": "2a4647e1-cbe3-4016-9d29-f4df229c4ef3",
            "iban": "DE88100500001310032358",
            "name": "client fox",
            "organization": "d7558fb7-a652-4fdd-b5bd-f41fc83e0479",
        },
        "invoiceDate": "2021-10-11T00:00:00.000Z",
        "invoiceId": "VR210230890",
    }
    expected_errors = {"errors_msg": "E11000 Duplicate Key Error", "ret_code": 409}
    assert "invoices_store" in mongodb.list_collection_names()
    cs = InvoicesStore(mongodb.invoices_store)
    res = cs.create_invoice(inputs_duplicates)
    assert res == expected_errors


def test_create_invoices_invalid_schema(mongodb):
    """
    Test invalide inserts
    """
    inputs_invalid_type = {
        "_id": "936dcc1f-d9d6-4a9f-aff5-598d3c7d4029",
        "organization": "d7558fb7-a652-4fdd-b5bd-f41fc83e0479",
        "createdAt": "2021-10-11T09:53:31.339Z",
        "updatedAt": "2021-11-29T13:15:19.500Z",
        "amount": {"currencyCode": "EUR", "value": 56.3},
        "contact": 10,
        "invoiceDate": "2021-10-11T00:00:00.000Z",
        "invoiceId": "VR210230890",
    }
    inputs_missing_property = {"_id": "inputs_missing_property"}
    inputs_property_not_allowed = {
        "_id": "936dcc1f-d9d6-4a9f-aff5-598d3c7d4029",
        "organization": "d7558fb7-a652-4fdd-b5bd-f41fc83e0479",
        "createdAt": "2021-10-11T09:53:31.339Z",
        "updatedAt": "2021-11-29T13:15:19.500Z",
        "amount": {"currencyCode": "EUR", "value": 56.3},
        "contact": "Invalid type",
        "invoiceDate": "2021-10-11T00:00:00.000Z",
        "invoiceId": "VR210230890",
        "additional-info": "errors property",
    }
    expected_errors_invalid_type = {
        "errors_msg": "Schema ValidationError of docs: 10 is not of type 'object'",
        "ret_code": 403,
    }
    expected_errors_missing_property = {
        "errors_msg": "Schema ValidationError of docs: 'organization' is a required property",
        "ret_code": 403,
    }
    expected_errors_inputs_property_not_allowed = {
        "errors_msg": "Schema ValidationError of docs: Additional properties are not allowed ('additional-info' was unexpected)",
        "ret_code": 403,
    }
    assert "invoices_store" in mongodb.list_collection_names()
    cs = InvoicesStore(mongodb.invoices_store)
    res = cs.create_invoice(inputs_invalid_type)
    assert res == expected_errors_invalid_type
    res = cs.create_invoice(inputs_missing_property)
    assert res == expected_errors_missing_property
    res = cs.create_invoice(inputs_property_not_allowed)
    assert res == expected_errors_inputs_property_not_allowed


def test_update_contact(mongodb):
    """
    Test success updates
    """
    input_update_form1 = {
        "_id": "2a4647e1-cbe3-4016-9d29-f4df229c4ef3",
        "iban": "DE88100500001310032358",
        "name": "client fish",
        "organization": "d7558fb7-a652-4fdd-b5bd-f41fc83e0479",
    }
    input_update_id_not_found = {
        "_id": "2a4647e1-cbe3-4016-9d29-f4df229c4ef2",
        "iban": "DE88100500001310032358",
        "name": "Client 3",
        "organization": "d7558fb7-a652-4fdd-b5bd-f41fc83e0479",
    }
    input_update_invalid_contact = {
        "_id": "2a4647e1-cbe3-4016-9d29-f4df229c4ef2",
        "name": "Client 3",
        "organization": "d7558fb7-a652-4fdd-b5bd-f41fc83e0479",
    }

    expected_result = {"acknowledged": True, "modified_count": 2, "ret_code": 200}

    expected_result_notfound_error = {
        "acknowledged": False,
        "modified_count": 0,
        "ret_code": 403,
        "errors_msg": "Contact with id: 2a4647e1-cbe3-4016-9d29-f4df229c4ef2 not found",
    }
    expected_result_invalid_contact_error = {
        "acknowledged": False,
        "modified_count": 0,
        "ret_code": 403,
        "errors_msg": "Schema ValidationError of docs: 'iban' is a required property",
    }
    assert "invoices_store" in mongodb.list_collection_names()
    cs = InvoicesStore(mongodb.invoices_store)
    res = cs.update_contact(input_update_form1)
    assert res == expected_result
    res = cs.update_contact(input_update_id_not_found)
    assert res == expected_result_notfound_error
    res = cs.update_contact(input_update_invalid_contact)
    assert res == expected_result_invalid_contact_error


def test_search_contact(mongodb):
    """
    Test valid and invalid search
    """
    print(
        "Mongo text search feature is missing in mongomock, see : https://github.com/mongomock/mongomock/blob/develop/Missing_Features.rst"
    )
    print("This case is covered with e2e_test")
    pass

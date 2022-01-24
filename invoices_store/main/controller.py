from pymongo import errors, TEXT
import json
from main.utils import validate_invoice_with_schema, validate_contact_with_schema
from jsonschema import ValidationError


class InvoicesStore:
    """
    Each methods in this class implements http codes status in res["ret_code"], see:
    https://www.restapitutorial.com/lessons/httpmethods.html
    """

    def __init__(self, collection):
        """
        Init application with a mongodb collection object
        Create collection index on "name" field if it does not exists.
        """
        super(InvoicesStore).__init__()
        # Create index to prevent duplicate insert, according to doc, it is a "create if not exists" statement
        # collection.create_index([("name", 1)], unique=True, background=True)
        collection.create_index([("contact.name", TEXT)], background=True)
        self.collection = collection

    def list_invoices(self):
        """
        List all existing invoices.

        Returns
        -------
        python dict, res.
        res["docs"] : list of existing configurations
        res["ret_code"] : http code, always 200
        """
        res = {}
        cursor = self.collection.find({})
        res["docs"] = [x for x in cursor]
        res["ret_code"] = 200
        return res

    def create_invoice(self, doc):
        """
        Insert a validate invoice into Mongodb.
        It validate inserts, catch duplicate exceptions
        Parameters
        ----------
        doc: An invoice doc

        Returns
        -------
        A python dict, res.
        res["errors_msg"]: error message, can be None
        res["ret_code"] : http status code.

        use insert_many function add docs, see :
        https://pymongo.readthedocs.io/en/stable/api/pymongo/collection.html#pymongo.collection.Collection.insert_many
        """
        res = {}
        try:
            validate_invoice_with_schema(doc)
            ret = self.collection.insert_one(doc)
            res["ret_code"] = 201
        except ValidationError as ve:
            res["errors_msg"] = f"Schema ValidationError of docs: {ve.message}"
            res["ret_code"] = 403
        except errors.DuplicateKeyError as be:
            res["errors_msg"] = str(be)
            res["ret_code"] = 409
        except Exception as e:
            res["errors_msg"] = f"Unknown Error: {str(e)}"
            res["ret_code"] = 500

        return res

    def update_contact(self, doc):
        """
        Update an exisiting contact
        catch not found exceptions
        Parameters
        ----------
        doc: a single contact, contain "_id"

        Returns
        -------
        A python dict, res.
        res["acknowledged"] : either update been ack by mongodb
        res["errors_msg"]: error message, can be None
        res["ret_code"] : http status code.

        use replace_one function(collection contain no duplicates) add docs, see :
        https://pymongo.readthedocs.io/en/stable/api/pymongo/collection.html#pymongo.collection.Collection.update_many        """
        res = {}
        # some default result to not repeat over in except
        try:
            validate_contact_with_schema(doc)
            contact_id = doc["_id"]
            ret = self.collection.update_many(
                {"contact._id": contact_id}, {"$set": {"contact": doc}}
            )
            res["acknowledged"] = True
            res["ret_code"] = 200
            res["modified_count"] = ret.modified_count
            if ret.matched_count == 0:
                res["acknowledged"] = False
                res["errors_msg"] = f"Contact with id: {contact_id} not found"
                res["ret_code"] = 403
        except ValidationError as ve:
            res["acknowledged"] = False
            res["modified_count"] = 0
            res["errors_msg"] = f"Schema ValidationError of docs: {ve.message}"
            res["ret_code"] = 403
        except Exception as e:
            res["acknowledged"] = False
            res["modified_count"] = 0
            res["errors_msg"] = f"Unknown Error: {str(e)}"
            res["ret_code"] = 500
        return res

    def search_contact(self, request_dict):
        """
        Search list of invoices that matches a given search filter from Mongodb.
        It catches not found exceptions, and no search filter provided exception

        Parameters
        ----------
        request_dict : A python dict contains search filters

        Returns
        -------
        A python dict, res.
        res["docs"] : list of configurations match search filters, can be empty
        res["errors_msg"]: error message, can be None
        res["ret_code"] : http status code.

        use find function search docs, see :
        https://pymongo.readthedocs.io/en/stable/api/pymongo/collection.html#pymongo.collection.Collection.find
        """
        res = {}
        if request_dict:
            organization_id = request_dict["organization"]
            contactName = request_dict["contactName"]
            cursor = (
                self.collection.find(
                    {
                        "contact.organization": organization_id,
                        "$text": {"$search": contactName},
                    },
                    {"score": {"$meta": "textScore"}, "contact.name": 1, "_id": 0},
                )
                .sort([("score", {"$meta": "textScore"})])
                .limit(1)
            )
            res["doc"] = [x for x in cursor]
            if len(res["doc"]) == 0:
                res["errmsg"] = f"Nothing found with {request_dict}"
                res["doc"] = {}
                res["ret_code"] = 404
            else:
                res["doc"] = res["doc"][0]
                res["ret_code"] = 200
        else:
            res["doc"] = {}
            res["errmsg"] = "No request arguments provided"
            res["ret_code"] = 403
        return res

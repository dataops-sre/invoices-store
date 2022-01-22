import os, json, sys

INVOICE_SCHEMA = """
{
   "type":"object",
   "properties":{
      "_id":{
         "type":"string"
      },
      "organization":{
         "type":"string"
      },
      "createdAt":{
         "type":"string"
      },
      "updatedAt":{
         "type":"string"
      },
      "amount":{
         "type":"object",
         "properties":{
            "currencyCode":{
               "type":"string"
            },
            "value":{
               "type":"number"
            }
         },
         "required":[
            "currencyCode",
            "value"
         ]
      },
      "contact":{
         "type":"object",
         "properties":{
            "_id":{
               "type":"string"
            },
            "iban":{
               "type":"string"
            },
            "name":{
               "type":"string"
            },
            "organization":{
               "type":"string"
            }
         },
         "required":[
            "_id",
            "iban",
            "name",
            "organization"
         ]
      },
      "invoiceDate":{
         "type":"string"
      },
      "invoiceId":{
         "type":"string"
      }
   },
   "additionalProperties":false,
   "required":[
      "_id",
      "organization",
      "createdAt",
      "updatedAt",
      "amount",
      "contact",
      "invoiceDate",
      "invoiceId"
   ]
}
"""

CONTACT_SCHEMA = """
{
   "type":"object",
   "properties":{
      "_id":{
         "type":"string"
      },
      "iban":{
         "type":"string"
      },
      "name":{
         "type":"string"
      },
      "organization":{
         "type":"string"
      }
   },
   "required":[
      "_id",
      "iban",
      "name",
      "organization"
   ]
}
"""

MONGODB_HOST = os.getenv("MONGODB_HOST", "mongodb://localhost:27017/")
MONGODB_REPLICA_SET_NAME = os.getenv("MONGODB_REPLICA_SET_NAME", None)
MONGODB_DATABASE = os.getenv("MONGODB_DATABASE", "invoices_store")
MONGODB_USERNAME = os.getenv("MONGODB_USERNAME", None)
MONGODB_PASSWORD = os.getenv("MONGODB_PASSWORD", None)
DB_COLLECTION = os.getenv("DB_COLLECTION", "invoices")


def get_invoice_schema():
    """
    Load invoice schema as Json
    """
    try:
        invoice_schema_json = json.loads(INVOICE_SCHEMA)
        return invoice_schema_json
    except Exception as e:
        print(f"Can not load invoice schema, abort {e}")
        sys.exit(1)

def get_contact_schema():
    """
    Load contact schema as Json
    """
    try:
        contact_schema_json = json.loads(CONTACT_SCHEMA)
        return contact_schema_json
    except Exception as e:
        print(f"Can not load contact schema, abort {e}")
        sys.exit(1)

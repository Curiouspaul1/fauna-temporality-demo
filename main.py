from faunadb.client import FaunaClient
from faunadb.errors import FaunaError, HttpError
from faunadb import query as q
from dotenv import load_dotenv
from typing import Optional
import os

load_dotenv()

client = FaunaClient(secret=os.getenv('Fauna-secret'))


def introspect(ref_id: str):
    events_ = client.query(
        q.paginate(
            q.events(
                q.ref(
                    q.collection('customers'), ref_id
                )
            )
        )
    )
    return events_


def downgrade(ref_id: str, steps: Optional[int] = -2):
    events_ = introspect(ref_id)
    # fetch previous state and update document with it instead
    try:
        client.query(
            q.update(
                q.ref(
                    q.collection("customers"), ref_id
                ),
                {
                    'data': events_['data'][steps]['data']
                }
            )
        )
    except FaunaError as e:
        return "An error occurred while trying to update object, try again."
    return "downgraded object successfully"

print(introspect("102")) # inspect the history of the document before running the downgrade
print(downgrade("102")) 

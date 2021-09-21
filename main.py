from faunadb.client import FaunaClient
from faunadb import query as q
from dotenv import load_dotenv
import os

load_dotenv()

client = FaunaClient(secret=os.getenv('Fauna-secret'))

# # reviewing customer data
# customers = client.query(
#     q.map_(
#         lambda x: q.get(x),
#         q.paginate(
#             q.documents(q.collection('customers'))
#         )
#     )
# # )

# print(customers)

data = client.query(
    q.at(
        q.time("1628815097906000"),
        q.paginate(
            q.ref("customers")
        )
    )
)

print(data)
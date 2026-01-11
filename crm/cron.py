def update_low_stock():
    from datetime import datetime
    from gql import gql, Client
    from gql.transport.requests import RequestsHTTPTransport

    transport = RequestsHTTPTransport(
        url="http://localhost:8000/graphql",
        verify=False
    )

    client = Client(transport=transport, fetch_schema_from_transport=True)

    mutation = gql("""
    mutation {
      updateLowStockProducts {
        success
        products {
          name
          stock
        }
      }
    }
    """)

    result = client.execute(mutation)
    timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")

    with open("/tmp/low_stock_updates_log.txt", "a") as f:
        for p in result["updateLowStockProducts"]["products"]:
            f.write(f"{timestamp} {p['name']} -> stock {p['stock']}\n")

import time
from order_management import OrderManager, OrderRequest, OrderResponse, RequestType, ResponseType

oms = OrderManager(max_orders_per_sec=3)  

# Simulated order inputs
order_list = [
    OrderRequest(1001, 250.0, 10, 'B', 1, RequestType.New),
    OrderRequest(1002, 251.0, 15, 'S', 2, RequestType.New),
    OrderRequest(1003, 249.5, 20, 'B', 3, RequestType.New),
    OrderRequest(1003, 252.0, 18, 'B', 3, RequestType.Modify),
    OrderRequest(1002, 251.0, 15, 'S', 2, RequestType.Cancel),
    OrderRequest(1004, 253.0, 8,  'S', 4, RequestType.New)
]

# Send orders
for req in order_list:
    oms.receive_order(req)
    time.sleep(0.2)

# Simulated exchange responses
time.sleep(3)
response_list = [
    OrderResponse(1, ResponseType.Accept),
    OrderResponse(3, ResponseType.Accept),
    OrderResponse(4, ResponseType.Reject)
]

for res in response_list:
    oms.receive_response(res)

# Graceful shutdown
time.sleep(2)
oms.stop()

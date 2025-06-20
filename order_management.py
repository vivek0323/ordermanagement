import threading
import time
from datetime import datetime
from enum import Enum
from collections import deque

# Enum for order request types
class RequestType(Enum):
    Unknown = 0
    New = 1
    Modify = 2
    Cancel = 3

# Enum for exchange response types
class ResponseType(Enum):
    Unknown = 0
    Accept = 1
    Reject = 2

# Order request model
class OrderRequest:
    def __init__(self, symbol_id, price, quantity, side, order_id, request_type):
        self.symbol_id = symbol_id
        self.price = price
        self.quantity = quantity
        self.side = side
        self.order_id = order_id
        self.request_type = request_type
        self.created_at = time.time()

# Exchange response model
class OrderResponse:
    def __init__(self, order_id, response_type):
        self.order_id = order_id
        self.response_type = response_type
        self.received_at = time.time()

# Core Order Management System
class OrderManager:
    def __init__(self, max_orders_per_sec=3, start_hour=10, end_hour=13):
        self.queue = deque()
        self.sent_orders = {}
        self.lock = threading.Lock()

        self.rate_limit = max_orders_per_sec
        self.allowed_start_hour = start_hour
        self.allowed_end_hour = end_hour

        self.running = True
        self.current_second = int(time.time())
        self.orders_sent_this_second = 0

        self.log_file = open("order_log.txt", "a")

        threading.Thread(target=self._rate_limiter_thread, daemon=True).start()

    def _is_market_open(self):
        now = datetime.now().time()
        return self.allowed_start_hour <= now.hour < self.allowed_end_hour

    def _rate_limiter_thread(self):
        while self.running:
            with self.lock:
                now_sec = int(time.time())
                if now_sec != self.current_second:
                    self.current_second = now_sec
                    self.orders_sent_this_second = 0

                while self.queue and self.orders_sent_this_second < self.rate_limit:
                    order = self.queue.popleft()
                    self._send_order(order)
                    self.sent_orders[order.order_id] = order
                    self.orders_sent_this_second += 1
            time.sleep(0.01)

    def receive_order(self, order: OrderRequest):
        if not self._is_market_open():
            print(f"Order {order.order_id} rejected — out of trading hours")
            return

        with self.lock:
            if order.request_type == RequestType.New:
                self.queue.append(order)

            elif order.request_type == RequestType.Modify:
                for o in self.queue:
                    if o.order_id == order.order_id:
                        o.price = order.price
                        o.quantity = order.quantity
                        break

            elif order.request_type == RequestType.Cancel:
                self.queue = deque(
                    o for o in self.queue if o.order_id != order.order_id
                )

    def receive_response(self, response: OrderResponse):
        with self.lock:
            if response.order_id in self.sent_orders:
                original_order = self.sent_orders[response.order_id]
                latency = response.received_at - original_order.created_at
                self._log_response(response, latency)

    def _send_order(self, order: OrderRequest):
        print(f"Sent to exchange: OrderID {order.order_id}")

    def _log_response(self, response, latency):
        self.log_file.write(
            f"{response.order_id}, {response.response_type.name}, {latency:.6f}\n"
        )
        self.log_file.flush()

    def stop(self):
        self.running = False
        self.log_file.close()

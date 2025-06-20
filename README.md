## 📘 Explanation of the Code

- This is a backend simulation of an Order Management System, similar to how stock or crypto orders are handled.
- Orders are only allowed during a fixed time window (10AM–1PM IST). Any orders outside this range are rejected to mimic real-world exchange hours.
- The system also throttles orders, allowing only a set number (e.g., 3) per second. Extra orders are placed in a queue.
- Modify and Cancel requests update or remove matching orders from the queue before they're sent out.
- A separate background thread takes care of sending orders from the queue at the allowed rate.
- When responses come from the exchange, I calculate the round-trip latency and log it in a text file.
- The code is thread-safe — I used Python’s threading lock to avoid race conditions on shared structures.
- The project includes:
  - `order_management.py`: Main logic
  - `test_driver.py`: Sample test cases
  - `order_log.txt`: Output log for responses and latency
  - `README.md`: This explanation and usage guide
- No web UI or frontend is involved — it’s all backend logic and console-based I/O.
- Assumptions: order IDs are unique, system time is correct, and the logon/logout messages are assumed to be working in production.

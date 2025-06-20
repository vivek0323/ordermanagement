# PipesHub Order Management System

This is my submission for the Backend Software Development Engineer assignment. It is a multithreaded order management system that simulates receiving, queuing, throttling, and handling orders and responses.

## 💡 Features

- Only processes orders during a configurable time window (default: 10AM–1PM IST)
- Throttles order flow to X orders/second (configurable, default: 3)
- Modifies or cancels queued orders before they are sent
- Tracks and logs exchange response latency
- Thread-safe implementation using Python and standard libraries

## 🧪 How to Run

### 1. Setup

Ensure Python is installed. Navigate to the project folder:

```bash
cd D:\Projects\Assignment

#!/usr/bin/env python3
"""
102-log_stats.py
"""
from pymongo import MongoClient


def log_stats(mongo_collection):
    """
    Provides some stats about Nginx logs stored in MongoDB.

    Args:
        mongo_collection: The pymongo collection object.

    Returns:
        None
    """
    total_logs = mongo_collection.count_documents({})
    print(f"{total_logs} logs")

    # Methods
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        count = mongo_collection.count_documents({"method": method})
        print(f"method {method}: {count}")

    # Status check
    status_check_count = mongo_collection.count_documents({"method": "GET", "path": "/status"})
    print(f"status check: {status_check_count}")

    # IPs
    ip_pipeline = [
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]
    top_ips = list(mongo_collection.aggregate(ip_pipeline))

    print("IPs:")
    for ip_info in top_ips:
        ip, count = ip_info["_id"], ip_info["count"]
        print(f"    {ip}: {count}")


if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    logs_collection = client.logs.nginx

    log_stats(logs_collection)

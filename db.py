from redis import Redis, exceptions


database = Redis(host="178.62.216.119", port=4567, decode_responses=True)

try:
    database.ping()
except exceptions.ConnectionError:
    print("Unable to connect to the database")
    exit(1)

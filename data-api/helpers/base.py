class BaseHelper:
    def __init__(self, query_api=None, write_api=None, bucket="default"):
        self.query_api = query_api
        self.write_api = write_api
        self.bucket = bucket

from influxdb_client import Point

from helpers.base import BaseHelper

from models.user import User


class UserHelper(BaseHelper):
    MEASUREMENT_NAME = "users"

    def exists(self, id):
        q = """
        from(bucket: pBucket)
            |> range(start: 0)
            |> filter(fn: (r) => r._measurement == pMeasurement)
            |> filter(fn: (r) => r.id == pId)
            |> count()
        """

        p = {
            "pBucket": self.bucket,
            "pMeasurement": self.MEASUREMENT_NAME,
            "pId": str(id),
        }

        tables = self.query_api.query(query=q, params=p)

        for table in tables:
            for record in table.records:
                if record.values.get("id") == str(id):
                    return True

        return False

    def get(self, id):
        q = """
        from(bucket: pBucket)
            |> range(start: 0)
            |> filter(fn: (r) => r._measurement == pMeasurement)
            |> filter(fn: (r) => r.id == pId)
            |> last()
            |> group()
        """

        p = {
            "pBucket": self.bucket,
            "pMeasurement": self.MEASUREMENT_NAME,
            "pId": str(id),
        }

        tables = self.query_api.query(query=q, params=p)

        params = {}

        for table in tables:
            for record in table.records:
                if record.values.get("_field") == "exists":
                    params["created_at"] = record.values.get("_time")

                if record.values.get("_field") == "activation":
                    params["activated_at"] = record.values.get("_time")

                if record.values.get("_field") == "deactivation":
                    params["deactivated_at"] = record.values.get("_time")

        return User(id=id, **params)

    def list(self):
        q = """
        from(bucket: pBucket)
            |> range(start: 0)
            |> filter(fn: (r) => r._measurement == pMeasurement)
            |> unique(column: "id")
            |> keep(columns: ["id"])
        """

        p = {
            "pBucket": self.bucket,
            "pMeasurement": self.MEASUREMENT_NAME,
        }

        tables = self.query_api.query(query=q, params=p)

        for table in tables:
            for record in table.records:
                yield record.values.get("id")

    def create_and_activate(self, id):
        return self.create(id) or self.activate(id)

    def create(self, id):
        p = Point(self.MEASUREMENT_NAME).tag("id", id).field("exists", 1)
        return self.write_api.write(bucket=self.bucket, record=p)

    def activate(self, id):
        p = Point(self.MEASUREMENT_NAME).tag("id", id).field("activation", 1)
        return self.write_api.write(bucket=self.bucket, record=p)

    def deactivate(self, id):
        p = Point(self.MEASUREMENT_NAME).tag("id", id).field("deactivation", 1)
        return self.write_api.write(bucket=self.bucket, record=p)

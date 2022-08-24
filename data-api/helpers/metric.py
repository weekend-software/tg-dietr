from influxdb_client import Point

from models.metric import Metric

from helpers.base import BaseHelper


class MetricHelper(BaseHelper):
    MEASUREMENT_NAME = "metrics"

    def write(self, user_id: int, metric: Metric):
        p = Point(self.MEASUREMENT_NAME).tag("user_id", user_id).field(metric.name, metric.value)
        return self.write_api.write(bucket=self.bucket, record=p)

    def list(self, user_id: int):
        q = """
        from(bucket: pBucket)
            |> range(start: 0)
            |> filter(fn: (r) => r._measurement == pMeasurement)
            |> filter(fn: (r) => r.user_id == pUserId)
            |> last(column: "_value")
            |> group()
        """

        p = {
            "pBucket": self.bucket,
            "pMeasurement": self.MEASUREMENT_NAME,
            "pUserId": str(user_id),
        }

        tables = self.query_api.query(query=q, params=p)

        results = {}
        for table in tables:
            for record in table.records:
                k = record.values.get("_field")
                v = record.values.get("_value")
                results[k] = v

        return results

    def get_values(self, user_id: int, metric_name: str, limit: int = 30, offset: int = 0):
        q = """
        from(bucket: pBucket)
            |> range(start: -30d)
            |> filter(fn: (r) => r._measurement == pMeasurement)
            |> filter(fn: (r) => r.user_id == pUserId)
            |> filter(fn: (r) => r._field == pMetricName)
            |> aggregateWindow(every: 1d, fn: median, createEmpty: false)
            |> limit(n: pLimit, offset: pOffset)
        """

        p = {
            "pBucket": self.bucket,
            "pMeasurement": self.MEASUREMENT_NAME,
            "pUserId": str(user_id),
            "pMetricName": metric_name,
            "pOffset": offset,
            "pLimit": limit,
        }

        tables = self.query_api.query(query=q, params=p)

        for table in tables:
            for record in table.records:
                t = record.values.get("_time")
                v = record.values.get("_value")
                yield (t, v)

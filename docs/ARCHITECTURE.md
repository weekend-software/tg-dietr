# Architecture

## Schema

```mermaid
flowchart LR
  telegram[Telegram]
  handler[Handler]
  reminder[Reminder]
  data-api[Data API]
  database[(Database)]
  frontend[Frontend]
  human((Human))

  subgraph Data Plane
    data-api
    database
  end

  subgraph Backend Logic
    handler
    reminder
  end

  subgraph Frontend
    frontend
  end

  telegram --> handler
  handler --> data-api
  data-api --> database

  reminder -.-> data-api
  reminder -.-> telegram

  frontend --> data-api

  human --> telegram
  human --> frontend
```

## Technologies

### Frontend

- [Svelte](https://svelte.dev/) as web javascript framework.
- [Materialize](http://materializecss.com/) as CSS framework.

### Backend

- [Python](https://www.python.org/) as programming language.
  - [FastAPI](https://fastapi.tiangolo.com/) as both API framework and logic programming language.

### Data

- [InfluxDB](https://www.influxdata.com/products/influxdb-overview/) as time-series database.

from fastapi import FastAPI, Query, HTTPException
import pandas as pd

app = FastAPI()


def fetch_data(year: int = None, country: str = None, market: str = None):
    try:
        # Load CSV directly from S3 public URL
        df = pd.read_csv(
            "https://s3-food-data-test.s3.us-east-1.amazonaws.com/total_data.csv"
        )

        # Apply filters
        if year is not None:
            df = df[df["year"] == year]

        if country is not None:
            df = df[df["country"] == country]

        if market is not None:
            df = df[df["mkt_name"] == market]

        # Handle empty result
        if df.empty:
            return []

        # Replace NaN with empty string
        df = df.fillna("")

        # Return as dictionary (not JSON string)
        return df.to_dict(orient="records")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/fetch_data")
async def fetch_data_api(
    year: int = Query(None),
    country: str = Query(None),
    market: str = Query(None),
):
    return fetch_data(year, country, market)

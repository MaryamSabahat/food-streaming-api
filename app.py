from fastapi import FastAPI, Query, HTTPException
import pandas as pd
import uvicorn

app = FastAPI()

def fetch_data(year: int = None, country: str = None, market: str = None):
    try:
        # Load CSV directly from URL
        df = pd.read_csv("https://s3-food-data-test.s3.us-east-1.amazonaws.com/total_data.csv")
        
        # Apply filters
        if year is not None:
            df = df[df['year'] == year]
        if country is not None:
            df = df[df['country'] == country]
        if market is not None:
            df = df[df['mkt_name'] == market]
        
        if df.empty:
            return []  # Return empty list instead of raising error
        
        # Fill NaN values
        df_filter = df.fillna('')
        return df_filter.to_dict(orient='records')
        
    except Exception as e:
        print(f"Error fetching data: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/fetch_data')
async def fetch_data_api(
    year: int = Query(None), 
    country: str = Query(None), 
    market: str = Query(None)
):
    return fetch_data(year, country, market)

@app.get('/health')
async def health_check():
    return {"status": "healthy"}

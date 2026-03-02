from fastapi import FastAPI, Query, HTTPException
import pandas as pd
import uvicorn

app = FastAPI()

def fetch_data(year: int = None, country: str = None, market: str = None):
    try:
        # Note: pandas requires 's3fs' or 'fsspec' to read directly from S3 URLs
        df = pd.read_csv(https://s3-food-data-test.s3.us-east-1.amazonaws.com/total_data.csv)

        # Apply filters based on provided parameters 
        if year is not None:
            df = df[df['year'] == year]
        if country is not None:
            df = df[df['country'] == country]
        if market is not None:
            df = df[df['mkt_name'] == market]

        # Fill NaN values with empty strings 
        df_filter = df.fillna('')
        
        if df_filter.empty:
            raise ValueError('No data found for the specified filters.')
        
        # Convert filtered DataFrame to JSON 
        return df_filter.to_dict(orient='records')

    except Exception as e:
        # Re-raise to be caught by the FastAPI endpoint 
        raise e

@app.get('/fetch_data')
async def fetch_data_api(year: int = Query(None), country: str = Query(None), market: str = Query(None)):
    try:
        filtered_data = fetch_data(year, country, market)
        return filtered_data
    except ValueError as ve:
        # Use HTTPException for proper FastAPI error responses 
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

if __name__ == '__main__':
    # App Runner overrides these, but keeping for local testing 
    uvicorn.run(app, port=8080, host='0.0.0.0')

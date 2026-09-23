from pydantic import BaseModel, Field
from typing import List

class StockAnalysis(BaseModel):
    ticker: str = Field(description="Stock ticker symbol")
    company_name: str = Field(description="Name of the company")
    current_price: float = Field(description="Current stock price in USD")
    key_metrics: dict = Field(description="Key metrics like P/E ratio, Market Cap")
    recommendation: str = Field(description="Buy, Hold, or Sell recommendation")
    growth_drivers: List[str] = Field(description="Top growth factors")
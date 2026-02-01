import json

import yfinance as yf
from google.adk.agents import Agent
from google.genai import Gemini

MODEL = Gemini(model="gemini-2.5-flash")


def get_news(ticker: str):
    """
    Retrieves the latest news articles related to a given stock ticker.

    This tool fetches recent news headlines and articles from Yahoo Finance
    for a specific company, useful for understanding current market sentiment,
    corporate events, and industry developments affecting the stock.

    Args:
        ticker (str): Stock ticker symbol (e.g., 'AAPL' for Apple Inc.)

    Returns:
        dict: A dictionary containing:
            - ticker (str): The input ticker symbol
            - success (bool): True if the operation was successful
            - news (str): JSON-formatted news data including:
                * Article titles and headlines
                * Publication timestamps
                * Source publishers
                * Article URLs and thumbnails

    Notes:
        - Returns the most recent news articles available on Yahoo Finance
        - News may include earnings reports, analyst ratings, industry trends, etc.
        - Useful for gauging market sentiment and identifying catalysts
        - Article count and recency depend on Yahoo Finance availability

    Example:
        >>> get_news('NVDA')
        {
            'ticker': 'NVDA',
            'success': True,
            'news': '[{"title": "NVIDIA Reports Record Revenue", ...}]'
        }
    """
    stock = yf.Ticker(ticker)
    return {
        "ticker": ticker,
        "success": True,
        "news": json.dumps(stock.get_news()),
    }


news_analyst = Agent(
    name="NewsAnalyst",
    model=MODEL,
    description="Retrieves and analyzes the latest news articles for a given stock ticker using Yahoo Finance",
    instruction="""
    You are a News Analyst Specialist who gathers and analyzes recent news. Your job:

    1. **News Retrieval**: Use get_news(ticker) to fetch the latest news articles for a company
    2. **Sentiment Analysis**: Assess overall market sentiment from the news (positive, negative, neutral)
    3. **Summarize Findings**: Highlight key headlines, corporate events, and their potential impact on the stock

    **Your News Tools:**
    - **get_news(ticker)**: Fetches recent news articles from Yahoo Finance

    Analyze news to identify market-moving events, earnings updates, analyst opinions, and industry trends.
    Focus on how the news may affect the company's stock price and investor sentiment.
    """,
    output_key="new_analyst_result",
    tools=[
        get_news,
    ],
)

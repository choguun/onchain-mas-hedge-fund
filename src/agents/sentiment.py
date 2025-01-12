from langchain_core.messages import HumanMessage
from graph.state import AgentState, show_agent_reasoning
import pandas as pd
import numpy as np
import json

from tools.api import get_sentiment_data, calculate_sentiment_signal

##### Sentiment Agent #####


def sentiment_agent(state: AgentState):
    """Analyzes market sentiment and generates trading signals."""
    data = state.get("data", {})
    end_date = data.get("end_date")
    start_date = data.get("start_date")
    ticker = data.get("ticker")

    # Get sentiment data using mock function
    sentiment_data = get_sentiment_data(ticker, start_date, end_date)
    sentiment_signal = calculate_sentiment_signal(sentiment_data)

    message_content = {
        "signal": "bullish" if sentiment_signal > 0 else "bearish",
        "confidence": abs(sentiment_signal),
        "reasoning": f"Sentiment score: {sentiment_signal}"
    }

    # Create the sentiment message
    message = HumanMessage(
        content=json.dumps(message_content),
        name="sentiment_agent",
    )

    state["data"]["analyst_signals"]["sentiment_agent"] = message_content

    return {
        "messages": [message],
        "data": data,
    }

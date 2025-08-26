# test_investment.py
import pytest
from investment import process_portfolio

def test_process_portfolio(mocker):
    # Mock DatabaseClient class
    mock_db = mocker.patch("investment.DatabaseClient")
    mock_db_instance = mock_db.return_value
    mock_db_instance.get_holdings.return_value = [
        {"ticker": "AAPL", "quantity": 10},
        {"ticker": "GOOG", "quantity": 5}
    ]

    # Mock APIClient class
    mock_api = mocker.patch("investment.APIClient")
    mock_api_instance = mock_api.return_value
    mock_api_instance.get_market_data.return_value = {
        "AAPL": 150,
        "GOOG": 100
    }

    # Call the function under test
    result = process_portfolio("prod", "2023-08-25")

    # Assertions
    assert result == [
        {"ticker": "AAPL", "value": 1500},
        {"ticker": "GOOG", "value": 500}
    ]

    # Ensure classes were initialized correctly
    mock_db.assert_called_once_with("prod")
    mock_api.assert_called_once_with()
    mock_db_instance.get_holdings.assert_called_once_with("2023-08-25")
    mock_api_instance.get_market_data.assert_called_once_with("2023-08-25")

# ======================
# investment.py
from external_services import DatabaseClient, APIClient

def process_portfolio(env, run_date):
    db = DatabaseClient(env)
    holdings = db.get_holdings(run_date)

    api = APIClient()
    try:
        market_data = api.get_market_data(run_date)
    except Exception as e:
        # handle API failure gracefully
        return {"error": str(e)}

    result = []
    for h in holdings:
        price = market_data.get(h["ticker"], 0)
        result.append({"ticker": h["ticker"], "value": h["quantity"] * price})

    return result



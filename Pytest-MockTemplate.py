# test_investment.py
import pytest
from investment import process_portfolio

def test_process_portfolio_all_mocks(mocker):
    # --- Mock DatabaseClient ---
    mock_db_class = mocker.patch("investment.DatabaseClient")
    mock_db_instance = mock_db_class.return_value
    mock_db_instance.get_holdings.return_value = [
        {"ticker": "AAPL", "quantity": 10},
        {"ticker": "GOOG", "quantity": 5},
    ]

    # --- Mock APIClient with dynamic return ---
    mock_api_class = mocker.patch("investment.APIClient")
    mock_api_instance = mock_api_class.return_value

    def dynamic_market_data(run_date):
        if run_date == "2023-08-25":
            return {"AAPL": 150, "GOOG": 100}
        return {"AAPL": 200, "GOOG": 110}

    mock_api_instance.get_market_data.side_effect = dynamic_market_data

    # --- Mock Logger ---
    mock_logger_class = mocker.patch("investment.Logger")
    mock_logger_instance = mock_logger_class.return_value

    # --- Call function under test ---
    result = process_portfolio("prod", "2023-08-25", debug=True)

    # --- Assert output ---
    assert result == [
        {"ticker": "AAPL", "value": 1500},
        {"ticker": "GOOG", "value": 500},
    ]

    # --- Assert calls ---
    mock_db_class.assert_called_once_with("prod")
    mock_db_instance.get_holdings.assert_called_once_with("2023-08-25")

    mock_api_class.assert_called_once_with()
    mock_api_instance.get_market_data.assert_called_once_with("2023-08-25")

    # Logger should log info for debug=True
    assert mock_logger_instance.log_info.call_count == 2

def test_process_portfolio_api_exception(mocker):
    # --- Mock DatabaseClient ---
    mock_db_class = mocker.patch("investment.DatabaseClient")
    mock_db_instance = mock_db_class.return_value
    mock_db_instance.get_holdings.return_value = [{"ticker": "AAPL", "quantity": 10}]

    # --- Mock APIClient to raise exception ---
    mock_api_class = mocker.patch("investment.APIClient")
    mock_api_instance = mock_api_class.return_value
    mock_api_instance.get_market_data.side_effect = Exception("API failure")

    # --- Mock Logger ---
    mock_logger_class = mocker.patch("investment.Logger")
    mock_logger_instance = mock_logger_class.return_value

    # --- Call function ---
    result = process_portfolio("prod", "2023-08-25")

    # --- Assert output ---
    assert result == {"error": "API failure"}

    # --- Assert logger called ---
    mock_logger_instance.log_error.assert_called_once_with("API failure")



# ======================
# Features of This Template
# Multiple dependencies mocked: DB, API, Logger.
# Dynamic behavior using side_effect for API returns.
# Exception handling tested.
# Assertions for both return values and interactions.
# Debug mode logging is easily verified.
# Automatic cleanup after test — no decorators, no boilerplate teardown.
# ======================

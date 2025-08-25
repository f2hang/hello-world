import pytest
from pandas import DataFrame
from InvestmentRiskModels.load_b1_equity_ut_paradice_micro import (
    initialize_dependencies,
    read_sql_data,
    get_link_proxies_df,
    get_port_holdings_df,
)
from unittest.mock import patch

# temporarily replacing objects, functions, or classes during tests, allowing for isolation and control of dependencies
@patch("InvestmentRiskModels.load_b1_equity_ut_paradice_micro.SQLServerHandler")
@patch("InvestmentRiskModels.load_b1_equity_ut_paradice_micro.BarraAPIConfig")
def test_initialize_dependencies(mock_barra_config, mock_sql_handler):
    # mock_sql_handler = mocker.MagicMock()
    # mock_barra_config = mocker.MagicMock()

    # TODO: here we got the issue, how to fix it?
    # from sharedutil.SQLServerHandler import SQLServerHandler
    # from sharedutil.BarraRESTAPI import BarraAPIConfig
    # mocker.patch(
    #     "InvestmentRiskModels.load_b1_equity_ut_paradice_micro.SQLServerHandler",
    #     return_value=mock_sql_handler,
    # )

    # mocker.patch(
    #     "InvestmentRiskModels.load_b1_equity_ut_paradice_micro.BarraAPIConfig",
    #     return_value=mock_barra_config,
    # )

# TODO: not sure why it's not working. 
    # mocker.patch(
    #     "sharedutil.SQLServerHandler",
    #     return_value=mock_sql_handler,
    # )
    # print("Mock SQLServerHandler:", mock_sql_handler)

    # mocker.patch(
    #     "sharedutil.BarraRESTAPI",
    #     return_value=mock_barra_config,
    # )

    env = "iamodels"
    run_date = "2023-07-31"
    is_debug_mode = True

    initialize_dependencies(env, run_date, is_debug_mode)

    mock_sql_handler.assert_called_once_with(env)
    mock_barra_config.assert_called_once_with(run_date, env="UAT")

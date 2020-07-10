# -*- coding: utf-8 -*-

import numpy as np
import pytest

import pmdarima as pm
from pmdarima.datasets import load_airpassengers
from pmdarima.arima import utils as arima_utils
from pmdarima.compat.pytest import pytest_warning_messages, pytest_error_str


def test_issue_341():
    seas_diffed = np.array([124., -114., -163., -83.])

    with pytest.raises(ValueError) as ve:
        arima_utils.ndiffs(seas_diffed, test='adf')

    assert "raised from LinAlgError" in pytest_error_str(ve)


def test_issue_351():
    y = np.array([
        1, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 2, 1, 6, 2, 1, 0,
        2, 0, 1, 0, 0, 3, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 3, 0, 0, 6,
        0, 0, 0, 0, 0, 1, 3, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0
    ])

    with pytest.warns(UserWarning) as w_list:
        D = arima_utils.nsdiffs(y, m=52, max_D=2, test='ocsb')

    assert D == 1

    warnings_messages = pytest_warning_messages(w_list)
    assert len(warnings_messages) == 1
    assert 'shorter than m' in warnings_messages[0]


def test_check_residuals():
    """
    R code I am trying to mimic:
        > model <- auto.arima(AirPassengers)
        > checkresiduals(model)

            Ljung-Box test

        data:  Residuals from ARIMA(2,1,1)(0,1,0)[12]
        Q* = 37.784, df = 21, p-value = 0.01366

        Model df: 3.   Total lags used: 24
    """
    y = load_airpassengers()
    arima = pm.auto_arima(y)  # Yields ARIMA(1, 1, 1)
    test = arima_utils.check_residuals(arima)
    print(arima.arima_res_.summary())
    print(test)

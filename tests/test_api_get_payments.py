import pytest


def test_without_filters(client):
    response = client.get('/payments')
    assert 200 == response.status_code


def test_1_filter_payment_min(client):
    response = client.get('/payments?payment_min=1')
    assert 200 == response.status_code

def test_1_filter_payment_min_incorrect_value(client):
    response = client.get('/payments?payment_min=text')
    assert 422 == response.status_code

def test_1_filter_payment_max(client):
    response = client.get('/payments?payment_max=1')
    assert 200 == response.status_code


def test_1_filter_payment_max_incorrect_value(client):
    response = client.get('/payments?payment_max=text')
    assert 422 == response.status_code


def test_2_filters(client):
    response = client.get('/payments?payment_min=1&payment_max=100')
    assert 200 == response.status_code


def test_2_filters_max_less_then_min(client):
    response = client.get('/payments?payment_min=100&payment_max=1')
    assert 422 == response.status_code

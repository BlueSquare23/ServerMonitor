import pytest

def test_home(app, client):
	# GET Request tests.
	response = client.get('/all_logs/testing')
	assert response.status_code == 200	# Return's 200 to GET requests.
	assert b"Server Monitoring" in response.data
	assert b"All Logs For Testing" in response.data

	# POST Request tests.
	response = client.post('/all_logs/testing', data=dict(test=''))
	assert response.status_code == 405	# Return's 405 to POST requests.

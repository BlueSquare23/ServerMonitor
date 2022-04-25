import pytest

def test_all_hosts(app, client):
	# GET Request tests.
	response = client.get('/all_hosts')
	assert response.status_code == 200	# Return's 200 to GET requests.
	assert b"Server Monitoring" in response.data
	assert b"All Hosts" in response.data

	# POST Request tests.
	response = client.post('/', data=dict(test=''))
	assert response.status_code == 405	# Return's 405 to POST requests.

import pytest

def test_delete_host(app, client):
	# GET Request tests.
	response = client.get('/delete_host/1')
	assert response.status_code == 404	# Return's 404 to initial GET requests.

	# Add host to test with.
	add_host_data={
		'hostname': 'testing',
		'hostkey1': 'password',
		'hostkey2': 'password'
	}
	
	response = client.post('/add_host', data=add_host_data, follow_redirects=True)
	assert response.status_code == 200	# Add host needs to work else
										# other tests will fail.

	# Removes the testing user.
	response = client.get('/delete_host/1', follow_redirects=True)
	assert response.status_code == 200	# Makes sure the test host it removed.

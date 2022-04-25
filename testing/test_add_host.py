import pytest

def test_add_host(app, client):
	# GET Request tests.
	response = client.get('/add_host')
	assert response.status_code == 200 # Return's 200 to GET requests.
	assert b"Add New Host" in response.data
	assert b"Hostname" in response.data
	assert b"Hostkey" in response.data
	assert b"Confirm Hostkey" in response.data
	assert b"Add Host" in response.data

	# POST Request tests.
	response = client.post('/submit', data='')
	assert response.status_code == 400	# Return's 400 to empty POST requests.

	# Not all feilds filled out.
	add_host_data={
		'hostname': 'testing',
		'hostkey1': '',
		'hostkey2': ''
	}

	response = client.post('/add_host', data=add_host_data, follow_redirects=True)
	assert response.status_code == 200
	assert b"Please enter all required information!" in response.data

	# Add host to test with.
	add_host_data={
		'hostname': 'testing',
		'hostkey1': '2short',
		'hostkey2': '2short'
	}

	response = client.post('/add_host', data=add_host_data, follow_redirects=True)
	assert response.status_code == 200
	assert b"Hostkey is too short!" in response.data

	# Add host to test with.
	add_host_data={
		'hostname': 'testing',
		'hostkey1': 'password',
		'hostkey2': 'password'
	}
	
	response = client.post('/add_host', data=add_host_data, follow_redirects=True)
	assert response.status_code == 200	

	# Removes the testing user.
	response = client.get('/delete_host/1', follow_redirects=True)
	assert response.status_code == 200	# Makes sure the test host it removed.

	response = client.get('/delete_host/2', follow_redirects=True)
	assert response.status_code == 404	# Makes sure the test host it removed.

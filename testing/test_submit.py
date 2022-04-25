import pytest
def test_submit(app, client):
	# GET Request tests.
	response = client.get('/submit')
	assert response.status_code == 405	# Return's 405 to GET requests.

	# Add host to test with.
	add_host_data={
		'hostname': 'testing',
		'hostkey1': 'password',
		'hostkey2': 'password'
	}
	
	response = client.post('/add_host', data=add_host_data, follow_redirects=True)
	assert response.status_code == 200	# Add host needs to work else
										# other tests will fail.

	# POST Request tests.
	response = client.post('/submit', data='')
	assert response.status_code == 400	# Return's 400 to empty POST requests.

	data={
		'host': 'testing',
		'host_key': 'blah',
		'ssh_status': 'blah',
		'misc_status': 'blah',
		'avg_temp': 'blah',
		'uptime': 'blah',
		'mem_used': 'blah'
	}

	response = client.post('/submit', json=data)
	assert response.status_code == 400	# Return's 400 to malformed request.
	assert b'{"Error":"Invalid hostkey for host!","Post":"Failed"}\n' in response.data


	data['host_key'] = 'password'

	response = client.post('/submit', json=data)
	assert response.status_code == 200	# Return's 200 to correctly formated request.
	assert b'{"Post":"Success"}\n' == response.data

	# Removes the testing user.

	response = client.get('/delete_host/1', follow_redirects=True)
	assert response.status_code == 200	# Makes sure the test host it removed.

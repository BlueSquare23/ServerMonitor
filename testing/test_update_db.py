import pytest
#from update_db import update_db

def test_update_db(app, client):
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

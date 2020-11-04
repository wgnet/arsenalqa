clean:
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info

bdist_wheel: clean
	python setup.py bdist_wheel
	python setup_amqp.py bdist_wheel
	python setup_db.py bdist_wheel
	python setup_http.py bdist_wheel
	python setup_websocket.py bdist_wheel

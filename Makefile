FILES ?= browser_api.py food_api.py main.py

lint: ${FILES}
	pylint ${FILES}

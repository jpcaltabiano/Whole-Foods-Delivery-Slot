.PHONY: lint

FILES ?= browser_api.py food_api.py server.py

# Lints all code.
# Disabled linting errors:
# R0201: No self use
# R0903: Too few public methods
lint:
	pylint \
		-d R0201,R0903 \
		${FILES}

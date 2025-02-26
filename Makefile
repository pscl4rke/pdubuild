
libdir := pdubuild

.PHONY: test
test:
	python3 -m unittest discover

pre-release-checks:
	mypy $(libdir)
	pyroma .

export PYTHON_KEYRING_BACKEND := keyring.backends.null.Keyring
release: pre-release-checks
	test "$$(python3 setup.py --version)" = "$$(git describe --tags)"
	test ! -d dist
	python3 setup.py sdist bdist_wheel
	check-wheel-contents dist
	twine check dist/*
	twine upload dist/*
	mv -i build* *.egg-info dist/.
	mv dist dist.$$(date +%Y-%m-%d.%H%M%S)

docker-to-run += test-in-docker-3.8-slim-bullseye
docker-to-run += test-in-docker-3.9-slim-bullseye
docker-to-run += test-in-docker-3.10-slim-bullseye
docker-to-run += test-in-docker-3.11-slim-bullseye
docker-to-run += test-in-docker-3.12-slim-bookworm
test-in-docker: $(docker-to-run)

test-in-docker-%:
	@echo
	@echo "===================================================="
	@echo "Testing with docker.io/library/python:$*"
	@echo "===================================================="
	@echo
	ephemerun \
		-i "docker.io/library/python:$*" \
		-v "`pwd`:/root/src:ro" \
		-W "/root" \
		-S "cp -air ./src/* ." \
		-S "pip --no-cache-dir install .[testing]" \
		-S "mypy --cache-dir /dev/null $(libdir)" \
		-S "coverage run -m unittest discover test/" \
		-S "coverage report -m" \
		-S "(pyroma . || true)"



.PHONY: test
test:
	python3 -m unittest discover

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
		-S "mypy --cache-dir /dev/null pdubuild" \
		-S "coverage run -m unittest discover test/" \
		-S "coverage report -m" \
		-S "(pyroma . || true)"

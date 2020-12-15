
init:
	@pip install -U poetry
	@poetry install

update:
	@poetry update

flake:
	@poetry run flake8

test: flake
	@poetry run py.test -v

coverage: flake
	@poetry run py.test -v --cov-report term-missing:skip-covered --cov=.

tox:
	@poetry run tox --workdir ~/.cache/tox

readme:
	@poetry run python -c 'from setup import REPO_USERNAME, NAME; from scripts.utils import make_readme; make_readme(REPO_USERNAME, NAME)'

upload: readme
	@poetry run ./setup.py upload

test-upload: readme
	@poetry run ./setup.py test_upload

clean:
	@find -E . -regex ".*\.py[cod]" -delete
	@find -E . -type d -name "__pycache__" -delete
	@find -E . -path "*.egg-info*" -delete
	@[ -d dist ] && rm -r dist/ || true
	@[ -f README.rst ] && rm README.rst || true
	@[ -f .coverage ] && rm .coverage || true

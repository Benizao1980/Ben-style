.PHONY: install sync references demo test clean

install:
	python -m pip install -e ".[dev]"

sync:
	python scripts/sync_palette_data.py

references:
	python scripts/make_palette_reference.py

demo:
	python examples/python_general.py
	python examples/acinetobacter_example.py
	python examples/campylobacter_coli_example.py

test:
	python -m pytest

clean:
	rm -rf build dist *.egg-info .pytest_cache
	rm -f outputs/*.svg outputs/*.pdf outputs/*.png

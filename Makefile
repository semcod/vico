.PHONY: test examples

test:
	pytest -q

examples:
	python examples/run_examples.py

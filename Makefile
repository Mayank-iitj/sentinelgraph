.PHONY: setup up down test lint format

setup:
	cp .env.example .env

up:
	docker-compose up -d --build

down:
	docker-compose down -v

test:
	pytest tests/

lint:
	ruff check .

format:
	ruff format .

bench:
	python -m eval.bench_triage
	python -m eval.bench_memory
	python -m eval.bench_brain
	python -m eval.load_test

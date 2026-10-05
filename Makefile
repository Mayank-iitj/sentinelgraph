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
	python eval/bench_triage.py
	python eval/bench_memory.py
	python eval/bench_brain.py
	python eval/load_test.py

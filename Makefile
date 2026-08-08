install:
	pip install -r requirements.txt

test:
	pytest -q

pipeline:
	python -m src.pipeline --solver qaoa

benchmark:
	python -m src.evaluation.benchmark

app:
	streamlit run app/streamlit_app.py

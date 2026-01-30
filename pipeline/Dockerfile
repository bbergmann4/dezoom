FROM python:3.13.11-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

WORKDIR /code
ENV PATH="/code/.venv/bin:$PAcd TH"


COPY pyproject.toml .python-version uv.lock ./
RUN uv sync --locked
#RUN pip install pandas pyarrow

COPY ingest_data.py ingest_data.py

#ENTRYPOINT ["uv","run","python", "ingset_data.py"]

ENTRYPOINT ["python", "ingest_data.py"]
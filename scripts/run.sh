#!/bin/bash

# マイグレーションとシードデータの投入
python -m db.migrate_db && \
python -m db.seed && \
# UvicornでFastAPIアプリを起動
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
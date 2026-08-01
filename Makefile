up:
	docker compose up -d

run-bronze:
	docker exec -it citibike-spark-master /opt/spark/bin/spark-submit /opt/spark/apps/bronze/ingest_station_status.py	

run-silver:
	docker exec -it citibike-spark-master /opt/spark/bin/spark-submit /opt/spark/apps/silver/station_status/ingest.py

down:
	docker compose down

logs:
	docker compose logs -f

lint:
	ruff check .

format:
	ruff format .

test:
	pytest
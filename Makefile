up:
	docker compose up -d

run-bronze:
	docker exec -it citibike-spark-master /opt/spark/bin/spark-submit /opt/spark/apps/bronze/ingest_station_status.py	

run-silver:
	docker exec -it citibike-spark-master /opt/spark/bin/spark-submit /opt/spark/apps/silver/station_status/main.py

run-latest-station-status:
	docker exec -it citibike-spark-master /opt/spark/bin/spark-submit /opt/spark/apps/gold/latest_station_status/main.py

run-hourly-metrics:
	docker exec -it citibike-spark-master /opt/spark/bin/spark-submit /opt/spark/apps/gold/station_hourly_metrics/main.py

run-daily-metrics:
	docker exec -it citibike-spark-master /opt/spark/bin/spark-submit /opt/spark/apps/gold/station_daily_metrics/main.py

run-system-metrics:
	docker exec -it citibike-spark-master /opt/spark/bin/spark-submit /opt/spark/apps/gold/system_metrics/main.py

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

quality:
	uv run ruff format --check .
	uv run ruff check .
	uv run pytest
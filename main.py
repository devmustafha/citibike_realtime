from common.logging import setup_logging
from producer.service import ProducerService


def main() -> None:
    setup_logging()

    service = ProducerService()

    try:
        service.run()
    finally:
        service.close()


if __name__ == "__main__":
    main()

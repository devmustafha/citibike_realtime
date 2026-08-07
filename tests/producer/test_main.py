from unittest.mock import MagicMock, patch

from producer.main import main


@patch("producer.main.get_settings")
@patch("producer.main.CitiBikeClient")
@patch("producer.main.KafkaProducer")
def test_main_publishes_all_stations(
    mock_producer_class, mock_client_class, mock_get_settings
):
    mock_settings = MagicMock()
    mock_settings.kafka_station_status_topic = "station_status"
    mock_get_settings.return_value = mock_settings

    station_1 = MagicMock()
    station_2 = MagicMock()

    mock_client = mock_client_class.return_value

    mock_client.get_station_status.return_value = [
        station_1,
        station_2,
    ]

    mock_producer = mock_producer_class.return_value

    main()

    assert mock_producer.publish.call_count == 2

    mock_producer.publish.assert_any_call(
        topic="station_status",
        station=station_1,
    )

    mock_producer.publish.assert_any_call(
        topic="station_status",
        station=station_2,
    )

    mock_producer.flush.assert_called_once()


@patch("producer.main.get_settings")
@patch("producer.main.CitiBikeClient")
@patch("producer.main.KafkaProducer")
def test_main_with_no_stations(
    mock_producer_class, mock_client_class, mock_get_settings
):
    mock_settings = MagicMock()
    mock_settings.kafka_station_status_topic = "station_status"
    mock_get_settings.return_value = mock_settings

    mock_client = mock_client_class.return_value
    mock_client.get_station_status.return_value = []

    mock_producer = mock_producer_class.return_value

    main()

    mock_producer.publish.assert_not_called()
    mock_producer.flush.assert_called_once()

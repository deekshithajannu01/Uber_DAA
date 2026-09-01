from src.ride_hailing_intelligence.analytics import build_reports
from src.ride_hailing_intelligence.cleaning import clean_bookings
from src.ride_hailing_intelligence.features import build_features
from src.ride_hailing_intelligence.modeling import train_cancellation_model
from src.ride_hailing_intelligence.powerbi_export import export_powerbi_tables


def main() -> None:
    clean_bookings()
    build_features()
    build_reports()
    train_cancellation_model()
    export_powerbi_tables()


if __name__ == "__main__":
    main()

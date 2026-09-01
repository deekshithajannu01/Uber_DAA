let
    ProjectPath = "/home/nikhil/Desktop/DAA_Project/reports/",

    FactBookings = Csv.Document(
        File.Contents(ProjectPath & "powerbi_fact_bookings.csv"),
        [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]
    ),
    fact_bookings = Table.PromoteHeaders(FactBookings, [PromoteAllScalars=true]),

    DimDate = Csv.Document(
        File.Contents(ProjectPath & "powerbi_dim_date.csv"),
        [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]
    ),
    dim_date = Table.PromoteHeaders(DimDate, [PromoteAllScalars=true]),

    VehicleKpis = Csv.Document(
        File.Contents(ProjectPath & "vehicle_cancellation_kpis.csv"),
        [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]
    ),
    vehicle_cancellation_kpis = Table.PromoteHeaders(VehicleKpis, [PromoteAllScalars=true]),

    HourlyKpis = Csv.Document(
        File.Contents(ProjectPath & "hourly_cancellation_kpis.csv"),
        [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]
    ),
    hourly_cancellation_kpis = Table.PromoteHeaders(HourlyKpis, [PromoteAllScalars=true]),

    ZoneKpis = Csv.Document(
        File.Contents(ProjectPath & "zone_cancellation_kpis.csv"),
        [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]
    ),
    zone_cancellation_kpis = Table.PromoteHeaders(ZoneKpis, [PromoteAllScalars=true]),

    FeatureImportance = Csv.Document(
        File.Contents(ProjectPath & "feature_importance.csv"),
        [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]
    ),
    feature_importance = Table.PromoteHeaders(FeatureImportance, [PromoteAllScalars=true]),

    ModelSummary = Csv.Document(
        File.Contents(ProjectPath & "powerbi_model_summary.csv"),
        [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]
    ),
    model_summary = Table.PromoteHeaders(ModelSummary, [PromoteAllScalars=true])
in
    fact_bookings

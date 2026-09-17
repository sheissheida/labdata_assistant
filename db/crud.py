from sqlalchemy.orm import Session
from .database import Dataset, CleaningLog


def create_dataset(
        db: Session,
        filename: str,
        inspection: dict
) -> Dataset:
    # Extracting dimensions from inspector output
    row_count = inspection["shape"][0]
    column_count = inspection["shape"][1]

    # Creating a Dataset object
    dataset = Dataset(
        filename=filename,
        row_count=row_count,
        column_count=column_count,
        columns=inspection["columns"],
        dtypes=inspection["dtypes"],
        missing_values=inspection["missing_values"]
    )

    # Registration and finalization in the database
    db.add(dataset)
    db.commit()
    db.refresh(dataset)

    return dataset


def create_cleaning_log(
        db: Session,
        dataset_id: int,
        cleaning_report: dict
) -> CleaningLog:
    log = CleaningLog(
        dataset_id=dataset_id,
        operation=cleaning_report["operation"],
        strategy=cleaning_report.get("strategy"),
        rows_before=cleaning_report.get("rows_before"),
        rows_after=cleaning_report.get("rows_after"),
        rows_removed=cleaning_report.get("rows_removed"),
        missing_before=cleaning_report.get("missing_before"),
        missing_after=cleaning_report.get("missing_after"),
        cells_fixed=cleaning_report.get("cells_fixed")
    )

    db.add(log)
    db.commit()
    db.refresh(log)

    return log



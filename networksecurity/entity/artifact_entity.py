from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    """
    Data class for data ingestion artifacts.
    """
    train_file_path: str
    test_file_path: str
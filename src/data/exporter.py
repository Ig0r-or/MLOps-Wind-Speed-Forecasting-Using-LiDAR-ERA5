from pathlib import Path
import pandas as pd


class DataExporter:
    PROCESSED_DIR = Path("data/processed")

    @staticmethod
    def export(df: pd.DataFrame, name: str, fmt: str = "parquet") -> Path:
        """
        Exporta um DataFrame processado para data/processed/.

        name: identificador do arquivo (ex.: "approach_a", "approach_b")
        fmt: "parquet" (recomendado) ou "csv"
        """
        DataExporter.PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
        filepath = DataExporter.PROCESSED_DIR / f"{name}.{fmt}"

        if fmt == "parquet":
            df.to_parquet(filepath, index=True)
        elif fmt == "csv":
            df.to_csv(filepath, index=True)
        else:
            raise ValueError(f"Formato não suportado: {fmt}")

        print(f"Exportado: {filepath} ({len(df)} linhas | colunas: {list(df.columns)})")
        return filepath

    @staticmethod
    def load(name: str, fmt: str = "parquet") -> pd.DataFrame:
        filepath = DataExporter.PROCESSED_DIR / f"{name}.{fmt}"
        if fmt == "parquet":
            return pd.read_parquet(filepath)
        return pd.read_csv(filepath, index_col=0, parse_dates=True)
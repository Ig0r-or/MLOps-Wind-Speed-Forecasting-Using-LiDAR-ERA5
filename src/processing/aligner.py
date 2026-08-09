import pandas as pd
import xarray as xr

class DataAligner:
    """Classe para alinhamento temporal e espacial entre LiDAR e ERA5."""
    @staticmethod
    def adjust_utc(df: pd.DataFrame, hours: int = 3) -> pd.DataFrame:
        """Ajusta o fuso horário (LiDAR local UTC-3 para UTC)."""
        df.index = df.index + pd.Timedelta(hours=hours)
        return df

    @staticmethod
    def abordagem_a(df_lidar: pd.DataFrame) -> pd.DataFrame:
        """
        Abordagem A: Janela Centrada (Média de Bloco).
        Média entre T-30min e T+20min para representar o timestamp T.
        """
        df_resampled = df_lidar[['ws100']].resample('1h', offset='30min').mean()
        df_resampled.index = df_resampled.index + pd.Timedelta(minutes=30)

        return df_resampled.rename(columns={'ws100': 'ws100_lidar'})
             
    @staticmethod
    def abordagem_b(ds_era5: xr.Dataset) -> pd.DataFrame:
        """
        Abordagem B: Resolução Nativa.
        Interpola o ERA5 (1h) para 10min para acompanhar a variabilidade do LiDAR.
        """
        df_interp = ds_era5.ws100.resample(valid_time='10min').interpolate('linear').to_dataframe()
        return df_interp.reset_index().set_index('valid_time')[['ws100']].rename(columns={'ws100': 'ws100_era5'})

    @staticmethod
    def merge_and_filter(df_era5: pd.DataFrame, df_lidar: pd.DataFrame, 
                         start: str = '2021-09-16 18:00:00', 
                         end: str = '2021-11-08 14:00:00') -> pd.DataFrame:
        """Realiza o Inner Join para garantir timestamps coincidentes e filtra o período."""
        df_analise = df_era5.join(df_lidar, how='inner')
        return df_analise.loc[start:end]
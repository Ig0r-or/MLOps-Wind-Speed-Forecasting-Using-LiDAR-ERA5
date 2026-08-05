import pandas as pd
import xarray as xr

class DataLoader:
    """Classe responsável pela ingestão de dados brutos (LiDAR e ERA5)."""
    @staticmethod
    def load_lidar(path: str) -> pd.DataFrame:
        """Carrega dados do LiDAR e extrai a série temporal base."""
        df = pd.read_csv(path)
        # Desfragmenta o DataFrame consolidando-o na memória
        df = df.copy()
        # Cria a coluna de tempo combinando as colunas nativas
        df['valid_time'] = pd.to_datetime(df[['year', 'month', 'day', 'hour', 'minute']])
        df = df.set_index('valid_time')
        return df

    @staticmethod
    def load_era5(path: str) -> xr.Dataset:
        """Carrega o cubo de dados NetCDF do ERA5 e calcula a velocidade resultante."""
        ds = xr.open_dataset(path)
        # Cálculo da velocidade do vento resultante (ws100) a partir das componentes u e v 
        if 'u100' in ds.data_vars and 'v100' in ds.data_vars:
            ds['ws100'] = (ds.u100**2 + ds.v100**2)**0.5
        return ds

    @staticmethod
    def get_era5_point(ds: xr.Dataset, lat: float = -2.69, lon: float = -42.56) -> xr.Dataset:
        """Extrai um ponto específico (ponto de grade mais próximo) do cubo de dados."""
        return ds.sel(latitude=lat, longitude=lon, method='nearest')
from src.data.loader import DataLoader
from src.processing.aligner import DataAligner
from src.features.wavelets import WaveletProcessor

def main():
    # 1. Ingestão dos dados brutos
    df_lidar_raw = DataLoader.load_lidar('data/raw/dataset.csv')
    ds_era5_raw = DataLoader.load_era5('data/raw/era5_dataset.nc')
    era5_ponto = DataLoader.get_era5_point(ds_era5_raw)

    # 2. Alinhamento Temporal (Abordagem A e B)
    # Ajuste UTC (+3h) para o LiDAR
    df_lidar_utc = DataAligner.adjust_utc(df_lidar_raw)

     # --- ABORDAGEM A: Escala Horária (Erro Macro) ---
    # Resample horário do LiDAR e seleção do ponto ERA5
    df_lidar_a = DataAligner.abordagem_a(df_lidar_utc)
    df_era5_a = era5_ponto.ws100.to_dataframe()[['ws100']].rename(columns={'ws100': 'ws100_era5'})
    # 3. Fusão e Filtragem do Período de Estudo/Pré-processamento via Wavelets (Denoising)
    df_analise_a = DataAligner.merge_and_filter(df_era5_a, df_lidar_a)
    df_analise_a['ws100_lidar_clean'] = WaveletProcessor.denoise(df_analise_a['ws100_lidar'].values)

     # --- ABORDAGEM B: Alta Resolução (10 min) ---
    # Interpola o ERA5 para 10 min
    df_era5_b = DataAligner.abordagem_b(era5_ponto)
    # Usa o LiDAR original de 10 min (sem resample)
    df_lidar_b = df_lidar_utc[['ws100']].rename(columns={'ws100': 'ws100_lidar'})
    df_analise_b = DataAligner.merge_and_filter(df_era5_b, df_lidar_b)
    # Denoising via Wavelet
    df_analise_b['ws100_lidar_clean'] = WaveletProcessor.denoise(df_analise_b['ws100_lidar'].values)

    print("\nPipeline de dados concluído!")
    print(f"Abordagem A (Horária): {len(df_analise_a)} pontos.")
    print(f"Abordagem B (10 min): {len(df_analise_b)} pontos.")
    print("\nAbordagem A (Denoised):")
    print(df_analise_a[['ws100_era5', 'ws100_lidar', 'ws100_lidar_clean']].head())
    print("\nAbordagem B (Denoised):")
    print(df_analise_b[['ws100_era5', 'ws100_lidar', 'ws100_lidar_clean']].head())
    
if __name__ == "__main__":
    main()
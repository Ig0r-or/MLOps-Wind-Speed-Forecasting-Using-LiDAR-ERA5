import pywt
import numpy as np

class WaveletProcessor:
    """Classe dedicada ao pré-processamento de sinais de vento via Wavelets."""
    @staticmethod
    def denoise(data: np.ndarray, wavelet: str = 'sym18', level: int = 2) -> np.ndarray:
        """
        Realiza a remoção de ruído (denoising) da série temporal.
        """
        # Garante que os dados sejam um array NumPy editável
        data = np.array(data, copy=True)
        
        # Decompõe o sinal em coeficientes de aproximação e detalhe
        coeff = pywt.wavedec(data, wavelet, mode="per")
        
        # Zera os coeficientes de detalhe (ruído)
        coeff[1:] = [np.zeros_like(v) for v in coeff[1:]]
        
        # Reconstrói o sinal suavizado
        return pywt.waverec(coeff, wavelet, mode="per")
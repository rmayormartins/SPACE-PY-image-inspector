import os
import time
import gradio as gr
from PIL import Image
import io

def image_inspector(uploaded_file):
    file_size = os.path.getsize(uploaded_file.name)
    
    if file_size < 1024:
        readable_file_size = f"{file_size} bytes"
    elif file_size < 1024**2:
        readable_file_size = f"{file_size / 1024:.2f} KB"
    else:
        readable_file_size = f"{file_size / (1024**2):.2f} MB"
    
    file_timestamp = time.ctime(os.path.getmtime(uploaded_file.name))

    try:
        with Image.open(uploaded_file.name) as image:
            
            bit_depth = image.mode
            num_channels = len(image.getbands())
            bit_depth_info = f"{num_channels * 8}-bit" if bit_depth else 'Desconhecido'
            
            details = {
                "Formato": image.format or "Desconhecido",
                "Modo": image.mode,
                "Dimensões": image.size,
                "Profundidade de Cor (Bit Depth)": bit_depth_info,
                "DPI": image.info.get('dpi', 'Não disponível'),
                "Tamanho do Arquivo": readable_file_size,
                "Timestamp do Arquivo": file_timestamp,
                "Tipo de Compressão": image.info.get('compression', 'Não disponível'),
                "Bands": image.getbands()
            }
    except Exception as e:
        return f"Ocorreu um erro ao processar a imagem: {e}"
    
    formatted_details = "\n".join([f"{key}: {value}" for key, value in details.items()])
    return formatted_details

iface = gr.Interface(
    fn=image_inspector,
    inputs=gr.File(label="Upload de Imagem"),
    outputs="text",
    title="Inspetor de Imagem",
    description="Faça o upload de uma imagem (.jpg, .png, .bmp, etc.) e veja detalhes sobre ela."
)
#...
if __name__ == "__main__":
    iface.launch()

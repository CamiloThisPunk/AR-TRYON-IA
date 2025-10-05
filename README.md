AR Mirror - Python (Real-time)


Requisitos:
- Python 3.11.5

CREAR EL SIGUIENTE ENTORNO VIRTUAL ARTO
- ARTO (recomendado) 


Instalación:
python -m venv ARTO
# Windows
ARTO\Scripts\activate

# Linux / Mac
source venv/bin/activate


pip install -r requirements.txt


Ejecutar demo:
python main.py


Archivos:
- main.py: demo principal (captura y loop)
- overlay.py: utilidades para cargar y superponer prendas
- capture_thread.py: captura en hilo (opcional para mejorar FPS)
- assets/: carpeta para PNGs de prendas con transparencia 
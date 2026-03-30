"""
Transcriptor de Reuniones con Whisper
======================================
Uso frecuente con archivos grandes grabados en móvil.
Genera transcripción con marcas de tiempo en .txt y .srt

Requisitos:
    pip install openai-whisper pydub tqdm
    sudo apt install ffmpeg   (Linux)
    brew install ffmpeg       (Mac)
    https://ffmpeg.org/download.html  (Windows)
"""

import whisper
import os
import sys
import argparse
from pathlib import Path
from datetime import timedelta
from tqdm import tqdm
import time


# ──────────────────────────────────────────────
# CONFIGURACIÓN (ajusta aquí)
# ──────────────────────────────────────────────
MODELO = "medium"        # tiny | base | small | medium | large
IDIOMA = "es"            # es = español, en = inglés, None = autodetectar
DISPOSITIVO = "cpu"      # "cpu" o "cuda" si tienes GPU Nvidia
# ──────────────────────────────────────────────


def formatear_tiempo(segundos: float) -> str:
    """Convierte segundos a formato HH:MM:SS"""
    td = timedelta(seconds=int(segundos))
    horas = td.seconds // 3600
    minutos = (td.seconds % 3600) // 60
    segs = td.seconds % 60
    return f"{horas:02d}:{minutos:02d}:{segs:02d}"


def formatear_tiempo_srt(segundos: float) -> str:
    """Convierte segundos a formato SRT (HH:MM:SS,mmm)"""
    ms = int((segundos % 1) * 1000)
    td = timedelta(seconds=int(segundos))
    horas = td.seconds // 3600
    minutos = (td.seconds % 3600) // 60
    segs = td.seconds % 60
    return f"{horas:02d}:{minutos:02d}:{segs:02d},{ms:03d}"


def guardar_txt(segments, ruta_salida: Path, nombre_archivo: str):
    """Guarda transcripción con marcas de tiempo en .txt"""
    with open(ruta_salida, "w", encoding="utf-8") as f:
        f.write(f"TRANSCRIPCIÓN: {nombre_archivo}\n")
        f.write("=" * 60 + "\n\n")

        for seg in segments:
            inicio = formatear_tiempo(seg["start"])
            fin = formatear_tiempo(seg["end"])
            texto = seg["text"].strip()
            f.write(f"[{inicio} → {fin}]\n{texto}\n\n")

    print(f"  ✓ Texto guardado en: {ruta_salida}")


def guardar_srt(segments, ruta_salida: Path):
    """Guarda transcripción en formato .srt (subtítulos)"""
    with open(ruta_salida, "w", encoding="utf-8") as f:
        for i, seg in enumerate(segments, start=1):
            inicio = formatear_tiempo_srt(seg["start"])
            fin = formatear_tiempo_srt(seg["end"])
            texto = seg["text"].strip()
            f.write(f"{i}\n{inicio} --> {fin}\n{texto}\n\n")

    print(f"  ✓ Subtítulos guardados en: {ruta_salida}")


def guardar_resumen(segments, ruta_salida: Path, nombre_archivo: str, duracion_total: float):
    """Guarda transcripción limpia sin marcas de tiempo"""
    with open(ruta_salida, "w", encoding="utf-8") as f:
        f.write(f"TRANSCRIPCIÓN LIMPIA: {nombre_archivo}\n")
        f.write(f"Duración total: {formatear_tiempo(duracion_total)}\n")
        f.write("=" * 60 + "\n\n")

        texto_completo = " ".join(seg["text"].strip() for seg in segments)
        f.write(texto_completo)

    print(f"  ✓ Texto limpio guardado en: {ruta_salida}")


def transcribir(ruta_audio: str, modelo_nombre: str = MODELO, idioma: str = IDIOMA):
    ruta = Path(ruta_audio)
    if not ruta.exists():
        print(f"❌ Error: No se encuentra el archivo: {ruta_audio}")
        sys.exit(1)

    # Carpeta de salida junto al audio
    carpeta_salida = ruta.parent / "transcripciones"
    carpeta_salida.mkdir(exist_ok=True)
    nombre_base = ruta.stem  # nombre sin extensión

    print(f"\n🎙️  Archivo : {ruta.name}")
    print(f"📦  Modelo  : {modelo_nombre}")
    print(f"🌍  Idioma  : {idioma or 'autodetectar'}")
    print(f"📂  Salida  : {carpeta_salida}/\n")

    # Cargar modelo
    print("⏳ Cargando modelo (puede tardar la primera vez)...")
    t0 = time.time()
    model = whisper.load_model(modelo_nombre, device=DISPOSITIVO)
    print(f"   Modelo cargado en {time.time() - t0:.1f}s\n")

    # Transcribir
    print("🔄 Transcribiendo... (esto puede tardar varios minutos en reuniones largas)")
    opciones = {
        "language": idioma,
        "verbose": False,
        "task": "transcribe",
        # Mejoras para audio de móvil con ruido de fondo:
        "condition_on_previous_text": True,
        "compression_ratio_threshold": 2.4,
        "no_speech_threshold": 0.6,
    }

    t1 = time.time()
    resultado = model.transcribe(str(ruta), **opciones)
    duracion = time.time() - t1

    segments = resultado["segments"]
    duracion_audio = segments[-1]["end"] if segments else 0

    print(f"\n✅ Transcripción completada en {duracion:.0f}s")
    print(f"   Duración del audio: {formatear_tiempo(duracion_audio)}")
    print(f"   Segmentos detectados: {len(segments)}\n")

    # Guardar archivos
    print("💾 Guardando archivos...")
    guardar_txt(segments, carpeta_salida / f"{nombre_base}_con_tiempos.txt", ruta.name)
    guardar_srt(segments, carpeta_salida / f"{nombre_base}.srt")
    guardar_resumen(segments, carpeta_salida / f"{nombre_base}_limpio.txt", ruta.name, duracion_audio)

    print(f"\n🎉 ¡Listo! Archivos generados en: {carpeta_salida}/")
    print(f"   - {nombre_base}_con_tiempos.txt  ← transcripción con marcas de tiempo")
    print(f"   - {nombre_base}_limpio.txt       ← solo el texto")
    print(f"   - {nombre_base}.srt              ← formato subtítulos")


def transcribir_carpeta(carpeta: str):
    """Transcribe todos los .mp3/.m4a/.wav de una carpeta"""
    extensiones = {".mp3", ".m4a", ".wav", ".ogg", ".flac", ".mp4"}
    archivos = [
        f for f in Path(carpeta).iterdir()
        if f.suffix.lower() in extensiones
    ]

    if not archivos:
        print(f"❌ No se encontraron archivos de audio en: {carpeta}")
        sys.exit(1)

    print(f"\n📁 Encontrados {len(archivos)} archivos de audio en '{carpeta}'")

    for i, archivo in enumerate(archivos, 1):
        print(f"\n{'='*60}")
        print(f"Archivo {i}/{len(archivos)}")
        transcribir(str(archivo))

    print("\n✅ Todos los archivos procesados.")


# ──────────────────────────────────────────────
# PUNTO DE ENTRADA
# ──────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Transcribe reuniones de audio a texto con Whisper"
    )
    parser.add_argument(
        "ruta",
        help="Ruta al archivo .mp3 (o carpeta para procesar varios)"
    )
    parser.add_argument(
        "--modelo",
        default=MODELO,
        choices=["tiny", "base", "small", "medium", "large"],
        help="Modelo Whisper a usar (default: medium)"
    )
    parser.add_argument(
        "--idioma",
        default=IDIOMA,
        help="Código de idioma, ej: es, en, fr (default: es)"
    )
    parser.add_argument(
        "--carpeta",
        action="store_true",
        help="Procesar todos los audios de una carpeta"
    )

    args = parser.parse_args()

    MODELO = args.modelo
    IDIOMA = args.idioma

    if args.carpeta:
        transcribir_carpeta(args.ruta)
    else:
        transcribir(args.ruta)

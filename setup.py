"""
Configuración de setup para la distribución de la aplicación.
"""

from setuptools import setup, find_packages

setup(
    name="Transcriptor de Audio",
    version="0.1.0",
    description="Aplicación de escritorio para transcribir audio a texto",
    author="Tu Nombre",
    author_email="tu.email@example.com",
    url="https://github.com/turepositorio",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "SpeechRecognition>=3.10.0",
        "pydub>=0.25.1",
        "python-dotenv>=0.19.0",
        "Pillow>=9.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=3.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
            "mypy>=0.950",
            "PyInstaller>=5.0.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "transcriptor=src.main:main",
        ]
    },
    python_requires=">=3.10",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Operating System :: Microsoft :: Windows",
    ],
)

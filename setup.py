from distutils.core import setup

setup(
    name='osrmcpy',
    version='0.1',
    python_requires='>=3.5',
    url='https://github.com/GeographicaGS/libosrmc.git',
    author='Geographica',
    author_email='cayetano.benavent@geographica.gs',
    description='OSRM Python binding',
    packages=['osrmcpy'],
    install_requires=[],
)

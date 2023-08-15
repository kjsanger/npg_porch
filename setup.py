from setuptools import find_packages, setup
from distutils.util import convert_path

version_path = convert_path('server/npg/version.py')
namespace = {}
with open(version_path) as ver_file:
    exec(ver_file.read(), namespace)

setup(
    name='npg_porch',
    version=namespace['__version__'],
    package_dir={
        '': 'server',
    },
    packages=find_packages('server'),
    license='GNU General Public License v3.0',
    author='Wellcome Sanger Institute',
    author_email='npg@sanger.ac.uk',
    description='Work allocation and tracking for portable pipelines',
    install_requires=[
        'aiosqlite',
        'asyncpg',
        'fastapi',
        'httpx', # missing dep for another dep
        'pydantic<2',
        'pysqlite3',
        'psycopg2-binary',
        'sqlalchemy>=1.4.29,<2',
        'ujson',
        'uvicorn',
        'uuid'
    ],
    extras_require={
        'test': [
            'pytest',
            'pytest-asyncio',
            'requests',
            'flake8'
        ]
    }
)

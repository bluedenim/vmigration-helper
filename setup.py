import pathlib
from setuptools import setup


HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()


setup(
    name="vmigration-helper",
    version="0.0.1",
    description="Van's Migration Helper",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/bluedenim/vmigration-helper",
    author="Van Ly",
    author_email="vancly@hotmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["vmigration_helper"],
    include_package_data=False,
    install_requires=[]
)

import pathlib
from setuptools import setup


HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()


setup(
    name="vmigration-helper",
    version="1.0.0",
    description="Van's Migration Helper",
    long_description=README,
    long_description_content_type="text/markdown",
    # url="https://github.com/realpython/reader",
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

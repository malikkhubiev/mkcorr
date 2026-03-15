from setuptools import setup

setup(
    name="mkcorr",
    version="0.1.0",
    py_modules=["mkcorr"],
    install_requires=["numpy"],
    author="Malik Khubiev",
    author_email="malik.hubiev@mail.ru",
    description="MK Correlation Coefficient",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/malikkhubiev/mkcorr",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)

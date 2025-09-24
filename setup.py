from setuptools import setup, find_packages

def read_me() -> str:
    with open("README.md", "r", encoding="utf-8") as file:
        return file.read()

setup(
    name="IvalineX",
    version="1.0",
    author="Jin-Mach",
    author_email="Ji82Ma@seznam.cz",
    description="Count your code lines easily with a simple GUI.",
    long_description=read_me(),
    long_description_content_type="text/markdown",
    url="https://github.com/Jin-Mach/IvaLineX",
    packages=find_packages(),
    install_requires=[
        "PyQt6>=6.9",
        "pywin32; sys_platform=='win32'"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.12",
    entry_points={
        "console_scripts": [
            "iva_line=iva_line:create_app",
            ],
        },
    keywords="iva_line, pyqt6",
)
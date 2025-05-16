import os
from setuptools import setup, find_packages

# Get long description from README.md if it exists
this_directory = os.path.abspath(os.path.dirname(__file__))
long_description = ""
readme_path = os.path.join(this_directory, "README.md")

if os.path.exists(readme_path):
    with open(readme_path, encoding="utf-8") as f:
        long_description = f.read()

setup(
    name="energyCnV",
    version="1.0.26",
    packages=find_packages(),
    install_requires=[
        "nvidia-ml-py3",
        "pymongo",
        "bcrypt",
        "dotenv",
        "dnspython",  # Optional: Required for some MongoDB connections
    ],
    author="VIT College",
    author_email="siddhartha2706@gmail.com",
    description="Track and visualize GPU energy consumption using PyNVML, with MongoDB integration.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/siddhartha276/energyCnV",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Visualization",
    ],
    python_requires=">=3.6",
)

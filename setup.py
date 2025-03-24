from setuptools import setup, find_packages

setup(
    name="energyCnV",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "nvidia-ml-py3",
        "pymongo",
        "bcrypt",
    ],
    author="VIT College",
    author_email="siddhartha2706@gmail.com",
    description="Track and visualize GPU energy consumption using PyNVML, with MongoDB integration.",
    long_description=open("README.md", encoding="utf-8").read(),
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

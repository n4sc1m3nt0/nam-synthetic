from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="nam-synthetic",
    version="0.1.0",
    author="Rodrigo",
    author_email="rodrigo.banf@gmail.com",
    description="Generate synthetic Neural Amp Modeler profiles from text descriptions using AI, trained on a self-curated tone collection",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/n4sc1m3nt0/nam-synthetic",
    project_urls={
        "Bug Tracker": "https://github.com/n4sc1m3nt0/nam-synthetic/issues",
        "Documentation": "https://github.com/n4sc1m3nt0/nam-synthetic/blob/main/README.md",
        "Source Code": "https://github.com/n4sc1m3nt0/nam-synthetic",
    },
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=requirements,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Multimedia :: Sound/Audio",
    ],
    keywords="neural amp modeler nam guitar tone synthesis machine learning",
)

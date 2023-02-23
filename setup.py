import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="agenoria",  # Replace with your own username
    version="0.0.1",
    author="Jiuguang Wang",
    author_email="jw@robo.guru",
    description=
    "Python utility for visualizing growth data from a newborn's first year.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jiuguangw/Agenoria",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='pyups',
    version='0.1.0',
    python_requires=">=3.7",
    license= "MIT",
    packages = find_packages(),
    install_requires=[
        'pysvg-py3',
        'attributes'
    ],
    keywords = ["celestial navigation"],
    entry_points={
         'console_scripts': ['ups = pyups.ups:main'],
    },
    author = "Philip Axer",
    author_email = "philip.axer@gmail.com",
    long_description = long_description,
    long_description_content_type="text/markdown",
)
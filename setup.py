import setuptools

import csi

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="csi-tai",
    version=csi.__version__,
    author="David Tippett",
    author_email="dtaivpp@gmail.com",
    description="A connector to simplify interactions with CSI / Virtial Observer web api",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="virtual observer csi api integration",
    url="https://github.com/dtaivpp/CSI_API",
    packages=setuptools.find_packages(),
    tests_require=['unittest','sys','os', 'json'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        'Intended Audience :: Developers',
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha"
    ],
)
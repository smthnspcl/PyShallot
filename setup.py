from setuptools import setup, find_packages

setup(
    long_description_content_type="text/markdown",
    long_description=open("README.md", "r").read(),
    name="pyshallot",
    version="0.22",
    description="shallot in python",
    # author="Pascal Eberlein",
    # author_email="pascal@eberlein.io",
    url="https://github.com/nbdy/pyShallot",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
    ],
    keywords="shallot",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'pyshallot = pyshallot.__main__:main'
        ]
    },
    install_requires=open("requirements.txt").readlines()
)

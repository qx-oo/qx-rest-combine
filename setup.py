from setuptools import find_packages, setup


setup(
    name='qx-rest-combine',
    version='1.0.6',
    author='Shawn',
    author_email='q-x64@live.com',
    url='https://github.com/qx-oo/qx-rest-combine/',
    description='Django combine rest apps.',
    long_description=open("README.md").read(),
    packages=find_packages(exclude=["qx_test"]),
    install_requires=[
        'Django >= 2.2',
        'djangorestframework >= 3.10',
    ],
    python_requires='>=3.7',
    platforms='any',
)

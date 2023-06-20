import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='scispace_logger',
    version='0.0.1',
    author='scispace',
    author_email='srinath@typeset.io',
    description='Common Logger for services in Scispace',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/TypesetIO/scispace-server-logger',
    project_urls={
        "Bug Tracker": "https://github.com/TypesetIO/scispace-server-logger/issues"
    },
    license='MIT',
    packages=['scispace_logger'],
    install_requires=['boto3'],
)

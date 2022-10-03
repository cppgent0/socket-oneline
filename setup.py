from pathlib import Path

from setuptools import find_packages, setup

this_directory = Path(__file__).parent
long_desc = (this_directory / "README.md").read_text()

setup(
    name='socket-oneline',
    include_package_data=True,
    packages=find_packages(include='socket-oneline*', ),
    version='0.0.1',
    license='MIT',
    description='Client server base class over socket',
    long_description=long_desc,
    long_description_content_type='text/markdown',
    author='JA',
    author_email='cppgent0@gmail.com',
    url='https://github.com/cppgent0/socket-oneline',
    download_url='https://github.com/cppgent0/socket-one/archive/refs/tags/v_0_0_1.tar.gz',
    keywords=['socket', 'client server', 'simple'],
    install_requires=[
        'pytest',
    ],
    classifiers=[
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Development Status :: 2 - Pre-Alpha',
        'Framework :: socket',
        'Intended Audience :: Developers',
        'Topic :: Communication :: sockets :: TCPIP',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9',
    ],
)

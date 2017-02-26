from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='the_matrix',
    packages=find_packages(exclude=['tests', 'docs']),
    entry_points = {
        'console_scripts': [
            'the_matrix_identify=the_matrix.identify:command_line',
            'the_matrix_leds=the_matrix.leds:command_line',
            'the_matrix_scrolltext=the_matrix.scrolltext:command_line',
            'the_matrix_web=the_matrix.web:main',
        ]
    },
    include_package_data=True,
    zip_safe=False,

    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    install_requires=['flask'],

    description='Module to control Boldport "The Matrix"',
    long_description=long_description,
    url='https://github.cm/threebytesfull.com/the_matrix_pi',

    author='Rufus Cable',
    author_email='rufus@threebytesfull.com',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Embedded Systems',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    keywords='boldport led matrix i2c rpi as1130',
)

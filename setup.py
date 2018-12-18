from setuptools import find_packages, setup

setup(
    name='multilevel_panels',
    description='A package for set logic on hierarchical data',
    version='0.1',
    url='https://github.com/langelgjm/multilevel-panels',
    author='Gabriel J. Michael',
    author_email='gabriel.j.michael@gmail.com',
    license='MIT',
    classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.6'
      ],
    packages=['multilevel_panels'],
    package_dir={'': 'src'},
    install_requires=[
        'numpy>=1.13',
    ]
)

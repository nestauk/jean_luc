from setuptools import setup

common_kwargs = dict(
        version='0.1.0',
        license='MIT',
        install_requires=[
            'numpy==1.22.0',
            'pytest==3.9.2'
            ],
        long_description=open('README.md').read(),
        long_description_content_type='text/markdown',
        url='https://github.com/nestauk/jean_luc/',
        author='George Richardson',
        author_email='george.richardson@nesta.org.uk',
        maintainer='George Richardson',
        classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6'
        ],
        python_requires='>3.6',
        include_package_data=True,
        )

setup(name='jean_luc', packages=['jean_luc'], **common_kwargs)

import setuptools
    
with open("README.md", "r") as fh:
    long_description = fh.read()
    
setuptools.setup(
    name='distjob',
    version='0.1.0',
    author='DovaX',
    author_email='dovax.ai@gmail.com',
    description='An intermediary library used to distribute various jobs/tasks between several machines - receiving job description through API requests - sending them to available workers and allocates the capacity.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/DovaX/distjob',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
          'fastapi'
     ],
    python_requires='>=3.6',
)
    
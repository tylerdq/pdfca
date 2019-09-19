from setuptools import setup

setup(
    name='pdfca',
    version='2.3.0',
    py_modules=['pdfca'],
    install_requires=[
        'click',
        'pandas',
        'pyarrow',
        'PyPDF2'
    ],
    entry_points='''
    [console_scripts]
    pdfca=pdfca:cli
    '''
)

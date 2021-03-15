from setuptools import setup, find_packages
with open('readme.md') as readme_file:
    readme = readme_file.read()

with open('requirements.txt', 'r') as fh:
    requirements = fh.read().split('\n')
setup(
    name='Yet-Another-EfficientDet-Pytorch',
    version='0.1.0',
    py_modules=['backbone'],
    packages=find_packages(include=['efficientdet', 'efficientdet.*', 'efficientnet', 'efficientnet.*', 'backbone', 'utils', 'utils.utils.preprocess_api', 'utils.*']),
    url='https://github.com/kush-litterati/EfficientDet',
    license='',
    author='zylo117',
    author_email='',
    description='Yet-Another-EfficientDet-Pytorch',
    long_description=readme,
    install_requires=requirements,
)

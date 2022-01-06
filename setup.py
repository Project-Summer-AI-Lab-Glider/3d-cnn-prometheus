from setuptools import setup

setup(
    name='tf2 bayesian unet',
    version='1.0.1',
    install_requires=[
        'nibabel~=3.2.1',
        'tensorflow~=2.6.2',
        'matplotlib==3.1.0',
        'colorcet==2.0.1',
        'brokenaxes==0.3.1',
        'pymongo==3.8.0',
        'numpy~=1.19.5',
        'tqdm~=4.62.3',
        'scikit-image==0.17.2',
        'scipy==1.5.4',
        'glob2==0.7',
        'h5py==2.10.0'
    ],
)

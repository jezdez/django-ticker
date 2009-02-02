from setuptools import setup, find_packages

setup(
    name='django-ajax-validation',
    version='0.1.0',
    description='A simple Django app for newsticker with a row level permission based workflow.',
    author='Martin Mahner',
    author_email='martin@mahner.org',
    maintainer='Jannis Leidel',
    maintainer_email='jannis@leidel.info',
    url='http://github.com/jezdez/django-ticker/tree/master',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    # Make setuptools include all data files under version control,
    # svn and CVS by default
    include_package_data=True,
    zip_safe=False,
    # Tells setuptools to download setuptools_git before running setup.py so
    # it can find the data files under Git version control.
    setup_requires=['setuptools_git'],
)

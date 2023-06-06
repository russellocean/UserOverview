from setuptools import find_packages, setup

setup(
    name='UserOverview',
    version='0.1',
    description='A Trac plugin to display all registered users and their CC activity',
    author='Russell Welch',
    author_email='russellwelch17@gmail.com',
    url='',
    packages=find_packages(exclude=['*.tests*']),
    entry_points = {
        'trac.plugins': [
            'user_overview = user_overview.user_overview:UserOverviewMacro'
        ]
    },
)

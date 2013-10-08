from setuptools import setup, find_packages

version = '1.0a1'

setup(
    name='matem.facetedbibliography',
    version=version,
    description="Faceted bibliography",
    long_description=open('README.txt').read() + '\n' +
    open('docs/CHANGES.txt').read(),
    # Get more strings from
    #http://www.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Plone',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    platforms='Any',
    author='Alejandra Maqueda',
    author_email='',
    url='https://github.com/imatem/matem.facetedbibliography',
    license='GPL',
    namespace_packages=['matem'],
    packages=find_packages('src', exclude=['ez_setup']),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'networkx',
    ],
    extras_require={
        'test': [
            'plone.app.testing',
            'unittest2',
        ],
    },
    entry_points="""
    # -*- Entry points: -*-
    [z3c.autoinclude.plugin]
    target = plone
    """,
)

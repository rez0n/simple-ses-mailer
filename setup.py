import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setuptools.setup(
    name='simple-ses-mailer',
    version='0.0.1',
    keywords='aws, ses, mail',
    author=u'Denis Verbin <den.verbin@gmail.com',
    packages=['simple_ses_mailer'],
    url='https://github.com/rez0n/simple-ses-mailer',
    license='Apache licence, see LICENCE',
    description='',
    long_description=long_description,
    long_description_content_type="text/markdown",
    requires=[
        'boto3',
    ],
    classifiers=[
        'Topic :: Communications :: Email',
    ]
)

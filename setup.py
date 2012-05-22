from distutils.core import setup

setup(name='python-gluster',
        version='0.1',
        package_dir={'gluster': 'src'},
        packages=[
            'gluster',
            'gluster.peer',
            'gluster.volume',
            ],
        )

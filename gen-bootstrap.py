import virtualenv, textwrap
output = virtualenv.create_bootstrap_script(textwrap.dedent("""
    import os, subprocess
    def after_install(options, home_dir):
        subprocess.call([join(home_dir, 'bin', 'pip'), 
            'install', '-e',
            'git+https://github.com/shawnsi/OpenSRS-py.git#egg=OpenSRS-py'])
        subprocess.call([join(home_dir, 'bin', 'pip'), 
            'install', 'pyCLI'])
"""))
print output

import virtualenv, textwrap
output = virtualenv.create_bootstrap_script(textwrap.dedent("""
    import os, subprocess
    def after_install(options, home_dir):
        subprocess.call([join(home_dir, 'bin', 'pip'), 
            'install', 'OpenSRS'])
        subprocess.call([join(home_dir, 'bin', 'pip'), 
            'install', 'pyCLI'])
        subprocess.call([join(home_dir, 'bin', 'pip'), 
            'install', 'PyYAML'])
        subprocess.call([join(home_dir, 'bin', 'pip'), 
            'install', 'distribute'])
        subprocess.call([join(home_dir, 'bin', 'pip'), 
            'install', 'setuptools-git'])
"""))
print output

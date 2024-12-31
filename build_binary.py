import PyInstaller.__main__
import sys
import os

def build_binary():
    args = [
        'src/cli.py',
        '--onefile',
        '--name=dirtree',
        '--clean',
        '--strip',
        f'--distpath=dist/{sys.platform}',
        '--workpath=build',
    ]
    
    if sys.platform == 'win32':
        args.append('--console')
    
    PyInstaller.__main__.run(args)

if __name__ == '__main__':
    build_binary()

import os
import platform
import subprocess
from log import *
from input import *
import shutil

if os.name == 'nt' and platform.release() == '10' and platform.version() >= '10.0.14393':
    import ctypes

    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

VERSION = '1.0.0'

if __name__ == '__main__':
    print(
        f"""{COLOR_YELLOW}                                         
        
    ██╗      █████╗ ██████╗  █████╗ ██╗   ██╗███████╗██╗        
    ██║     ██╔══██╗██╔══██╗██╔══██╗██║   ██║██╔════╝██║        This tool automatically collects the files and
    ██║     ███████║██████╔╝███████║██║   ██║█████╗  ██║        runs the necessary commands so that you can
    ██║     ██╔══██║██╔══██╗██╔══██║╚██╗ ██╔╝██╔══╝  ██║        deploy your Laravel project.
    ███████╗██║  ██║██║  ██║██║  ██║ ╚████╔╝ ███████╗███████╗
    ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝  ╚═══╝  ╚══════╝╚══════╝   {COLOR_RESET}Version:{COLOR_GREEN} {VERSION} 
    {COLOR_YELLOW}                                                         
    ██████╗ ███████╗██████╗ ██╗      ██████╗ ██╗   ██╗          
    ██╔══██╗██╔════╝██╔══██╗██║     ██╔═══██╗╚██╗ ██╔╝       
    ██║  ██║█████╗  ██████╔╝██║     ██║   ██║ ╚████╔╝        
    ██║  ██║██╔══╝  ██╔═══╝ ██║     ██║   ██║  ╚██╔╝         
    ██████╔╝███████╗██║     ███████╗╚██████╔╝   ██║          
    ╚═════╝ ╚══════╝╚═╝     ╚══════╝ ╚═════╝    ╚═╝          
    
    ════════════════════════════════════════════════════════════════════════════════════════════════════════════
    {COLOR_RESET}"""
    )

    input_path = accept_path('Enter the input directory: ')
    okay(f'Input directory set to "{input_path}"')
    output_path = accept_input('Enter the output directory: ', lambda value: Validations.all())
    if not os.path.exists(output_path):
        if accept_bool('Output directory does not exist should we create it? '):
            os.mkdir(output_path)
    else:
        shutil.rmtree(output_path)
        os.mkdir(output_path)

    def run(cmd: str, ) -> int:
        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True, cwd=input_path)
        proc.communicate()
        return proc.returncode


    okay(f'Output directory set to "{output_path}"')
    good('Running `npm -i`')
    run('npm -i')
    good('Running `npm run production`')
    run('npm run production')
    if shutil.which('php') is None:
        fatal('Could not find "php" command! PHP is not installed?')
    good('Detecting Composer')
    if os.path.exists(os.path.join(input_path, 'composer.phar')):
        okay('Found composer.phar using it for install')
        if run('php composer.phar install') < 0:
            fatal('Failed to run composer install')
        if run('php composer.phar install --optimize-autoloader --no-dev') < 0:
            fatal('Failed to install optimized autoloader')
    else:
        if shutil.which('composer') is None:
            fatal('Could not find "composer" command! Composer is not installed?')
        else:
            if run('composer install') < 0:
                fatal('Failed to run composer install')
            okay('Running "composer install --optimize-autoloader --no-dev"')
            if run('composer install --optimize-autoloader --no-dev') < 0:
                fatal('Failed to install optimized autoloader')
    good('Finished composer install')
    artisan_cache = [
        'php artisan config:cache',
        'php artisan route:cache',
        'php artisan view:cache',
    ]
    good('Running php artisan optimizers')
    for command in artisan_cache:
        if run(command) < 0:
            fatal(f'Failed to execute "{command}"')
    good('Finished artisan optimizers')
    copy_paths = [
        'app',
        'bootstrap',
        'node_modules',
        'public',
        'routes',
        'resources',
        'storage',
        'vendor',
        'server.php',
        '.env'
    ]
    good('Copying files')
    for path in copy_paths:
        in_path = os.path.join(input_path, path)
        out_path = os.path.join(output_path, path)
        if not os.path.exists(in_path):
            bad(f'Missing path "{path}"')
            continue
        if os.path.isdir(in_path):
            shutil.copytree(in_path, out_path, symlinks=True)
        else:
            shutil.copy(in_path, out_path)
    good('Copied files')
    good('Done')
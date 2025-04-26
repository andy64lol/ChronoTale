import os
import sys
import venv
import subprocess
import argparse
from platform import system as platform_system

class VenvManager:
    def __init__(self, venv_dir='venv'):
        self.venv_dir = venv_dir
        self.bin_path = self._get_venv_path()

    def _get_venv_path(self):
        """Return correct binary path based on platform"""
        if platform_system() == 'Windows':
            return os.path.join(self.venv_dir, 'Scripts')
        return os.path.join(self.venv_dir, 'bin')

    def _get_python_executable(self):
        """Get path to Python executable in virtual environment"""
        if platform_system() == 'Windows':
            return os.path.join(self.bin_path, 'python.exe')
        return os.path.join(self.bin_path, 'python')

    def create(self):
        """Create virtual environment if it doesn't exist"""
        if not os.path.exists(self.venv_dir):
            print(f"Creating virtual environment in {self.venv_dir}...")
            try:
                venv.create(self.venv_dir, with_pip=True)
                print("Virtual environment created successfully.")
            except Exception as e:
                print(f"Error creating virtual environment: {str(e)}")
                sys.exit(1)
        else:
            print(f"Virtual environment already exists in {self.venv_dir}.")

    def install_packages(self, packages=None, requirements_file=None):
        """Install packages using pip"""
        if not packages and not requirements_file:
            raise ValueError("Must specify either packages or requirements file")

        python_executable = self._get_python_executable()
        if not os.path.exists(python_executable):
            raise FileNotFoundError(f"Python executable not found at {python_executable}")

        pip_args = [python_executable, '-m', 'pip', 'install', '--quiet']

        if requirements_file:
            if not os.path.exists(requirements_file):
                raise FileNotFoundError(f"Requirements file not found: {requirements_file}")
            print(f"Installing packages from {requirements_file}...")
            subprocess.check_call(pip_args + ['-r', requirements_file])
            print(f"Requirements installed from {requirements_file}")
        
        if packages:
            print(f"Installing packages: {', '.join(packages)}...")
            subprocess.check_call(pip_args + list(packages))
            print("Packages installed successfully")

def main():
    parser = argparse.ArgumentParser(description='Manage Python virtual environments')
    parser.add_argument('--venv-dir', default='venv', help='Virtual environment directory')
    parser.add_argument('--packages', nargs='+', help='List of packages to install')
    parser.add_argument('--requirements', help='Path to requirements file')
    args = parser.parse_args()

    try:
        manager = VenvManager(args.venv_dir)
        manager.create()
        manager.install_packages(args.packages, args.requirements)
        print("\nSetup completed successfully!")
        print(f"Activate your virtual environment with:")
        print(f"  Windows:  {os.path.join(manager.bin_path, 'activate')}")
        print(f"  Unix/Mac: source {os.path.join(manager.bin_path, 'activate')}")
    except Exception as e:
        print(f"\nError: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()

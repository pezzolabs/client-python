import toml
import os

def main():
    current_path = os.path.dirname(os.path.realpath(__file__))
    pyproject_path = os.path.join(current_path, "../../pyproject.toml")
    data = toml.load(pyproject_path)
    version = data["tool"]["poetry"]["version"]
    
    # save version to "version.txt file"
    version_path = os.path.join(current_path, "../version.txt")
    with open(version_path, "w") as f:
        f.write(version)
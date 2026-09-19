from pathlib import Path

from kcd2_mod_packager.lib import MakePackage


def main():
    with MakePackage(Path.cwd()) as mkpkg:
        mkpkg.make_package()


if __name__ == "__main__":
    main()

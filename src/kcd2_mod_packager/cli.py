import argparse
from pathlib import Path

from pydantic import BaseModel, ConfigDict

from kcd2_mod_packager.lib import MakePackage


class Args(BaseModel):
    model_config = ConfigDict(strict=True)

    package_path: Path


def parse_args() -> Args:
    parser = argparse.ArgumentParser()
    parser.add_argument("package_path", type=Path, help="Path to the package")
    return Args.model_validate(vars(parser.parse_args()))


def main() -> None:
    args = parse_args()
    with MakePackage(args.package_path.absolute()) as mkpkg:
        mkpkg.make_package()


if __name__ == "__main__":
    main()

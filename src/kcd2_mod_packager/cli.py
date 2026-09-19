import argparse
from pathlib import Path

from pydantic import BaseModel, ConfigDict

from kcd2_mod_packager.lib import MakePackage


class Args(BaseModel):
    model_config = ConfigDict(strict=True)

    package_path: Path
    archive: bool


def parse_args() -> Args:
    parser = argparse.ArgumentParser(
        description="Packages Kingdom Come: Deliverance II mods into .pak files",
    )
    parser.add_argument("package_path", type=Path, help="Path to the package")
    parser.add_argument(
        "-a",
        "--archive",
        action="store_true",
        help="Zip the output directory contents into out.zip instead of out/",
    )
    return Args.model_validate(vars(parser.parse_args()))


def main() -> None:
    args = parse_args()
    with MakePackage(args.package_path.absolute()) as mkpkg:
        mkpkg.make_package(archive=args.archive)


if __name__ == "__main__":
    main()

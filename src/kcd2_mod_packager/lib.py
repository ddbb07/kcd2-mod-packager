import shutil
import zipfile
from typing import TYPE_CHECKING, Self

if TYPE_CHECKING:
    from pathlib import Path
    from types import TracebackType


def is_dir_empty(target_dir: Path) -> bool:
    if not target_dir.exists():
        msg = "Target directory does not exist"
        raise ValueError(msg)
    if not target_dir.is_dir():
        msg = "Target path exists but is not a directory"
        raise ValueError(msg)

    for _ in target_dir.iterdir():
        return False
    return True


def clear_dir_contents(target_dir: Path) -> None:
    if not target_dir.exists():
        msg = "Target directory does not exist"
        raise ValueError(msg)
    if not target_dir.is_dir():
        msg = "Target path exists but is not a directory"
        raise ValueError(msg)

    for path in target_dir.iterdir():
        if path.is_symlink():
            path.unlink()
        elif path.is_dir():
            shutil.rmtree(path)
        elif path.is_file():
            path.unlink()


def ensure_empty_dir(target_dir: Path) -> None:
    if not target_dir.parent.exists():
        msg = "Target directory parent does not exist"
        raise ValueError(msg)
    if not target_dir.parent.is_dir():
        msg = "Target directory parent path exists but is not a directory"
        raise ValueError(msg)

    if not target_dir.exists():
        target_dir.mkdir()
    elif target_dir.is_dir():
        clear_dir_contents(target_dir)
    else:
        msg_0 = "Target path exists but is not a directory"
        raise ValueError(msg_0)


def copy_dir_contents(source_dir: Path, target_dir: Path) -> None:
    if not source_dir.is_dir():
        msg = "Source is not a dir"
        raise ValueError(msg)
    if not target_dir.is_dir():
        msg = "Destination is not a dir"
        raise ValueError(msg)

    for src_path in source_dir.iterdir():
        dst_path = target_dir / src_path.name
        if src_path.is_dir():
            shutil.copytree(src_path, dst_path)
        elif src_path.is_file():
            shutil.copy(src_path, dst_path)


def create_archive_file(source_dir: Path, target_file: Path) -> None:
    if not source_dir.exists():
        msg = "The archive source directory does not exist"
        raise ValueError(msg)
    if not source_dir.is_dir():
        msg = "The archive source directory path exists but is not a directory"
        raise ValueError(msg)

    if is_dir_empty(source_dir):
        return

    if not target_file.parent.exists():
        msg = "The target archive parent directory does not exist"
        raise ValueError(msg)
    if not target_file.parent.is_dir():
        msg = "The target archive parent directory path exists but is not a directory"
        raise ValueError(msg)

    with zipfile.ZipFile(target_file, "w", zipfile.ZIP_DEFLATED) as archive_file:
        for path in source_dir.rglob("*"):
            if path.is_file():
                archive_file.write(path, path.relative_to(source_dir))


class MakePackage:
    def __init__(self, root_dir: Path) -> None:
        super().__init__()
        if not root_dir.is_dir():
            msg = "Root dir is not a directory"
            raise ValueError(msg)
        self.root_dir = root_dir
        self.source_dir = self.root_dir / "src"
        self.package_dir = self.root_dir / "pkg"
        self.output_dir = self.root_dir / "out"

        if not self.source_dir.exists():
            msg = "Source directory does not exist"
            raise ValueError(msg)
        if not self.source_dir.is_dir():
            msg = "Source directory path is not a directory"
            raise ValueError(msg)

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        return None

    def ensure_empty_package_dir(self) -> None:
        ensure_empty_dir(self.package_dir)

    def ensure_empty_output_dir(self) -> None:
        ensure_empty_dir(self.output_dir)

    def ensure_empty_required_dirs(self) -> None:
        self.ensure_empty_package_dir()
        self.ensure_empty_output_dir()

    def remove_package_dir(self) -> None:
        if not self.package_dir.exists():
            msg = "The package directory does not exist"
            raise ValueError(msg)
        if not self.package_dir.is_dir():
            msg = "The package directory path exists but is not a directory"
            raise ValueError(msg)

        shutil.rmtree(self.package_dir)

    def is_package_dir_empty(self) -> bool:
        return is_dir_empty(self.package_dir)

    def is_output_dir_empty(self) -> bool:
        return is_dir_empty(self.output_dir)

    def copy_source_dir_contents_to_package_dir(self) -> None:
        if not self.is_package_dir_empty():
            clear_dir_contents(self.package_dir)

        copy_dir_contents(self.source_dir, self.package_dir)

    def copy_package_dir_contents_to_output_dir(self) -> None:
        if self.is_package_dir_empty():
            msg = "Package dir is empty"
            raise ValueError(msg)

        if not self.is_output_dir_empty():
            clear_dir_contents(self.output_dir)

        copy_dir_contents(self.package_dir, self.output_dir)

    def package_pak_files_in_directory(self, directory_path: Path) -> None:
        if self.is_package_dir_empty():
            return

        if not directory_path.exists():
            msg = "The Data directory does not exist"
            raise ValueError(msg)
        if not directory_path.is_dir():
            msg = "The Data directory path exists but is not a directory"
            raise ValueError(msg)

        for path in directory_path.iterdir():
            if path.is_dir():
                create_archive_file(path, path.with_suffix(".pak"))
                shutil.rmtree(path)

    def package_pak_files_in_data(self) -> None:
        directory_path = self.package_dir / "Data"
        if directory_path.is_dir():
            self.package_pak_files_in_directory(directory_path)

    def package_pak_files_in_localization(self) -> None:
        directory_path = self.package_dir / "Localization"
        if directory_path.is_dir():
            self.package_pak_files_in_directory(directory_path)

    def archive_output_dir_contents(self) -> None:
        create_archive_file(self.output_dir, self.output_dir.with_suffix(".zip"))

    def make_package(self, *, archive: bool = False) -> None:
        self.ensure_empty_required_dirs()
        self.copy_source_dir_contents_to_package_dir()
        self.package_pak_files_in_data()
        self.copy_package_dir_contents_to_output_dir()
        self.remove_package_dir()
        if archive:
            self.archive_output_dir_contents()
            shutil.rmtree(self.output_dir)

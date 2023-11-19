import base64
import csv
import hashlib
import pathlib
import os
from pathlib import Path

def create_dist_info_dir(container, name, version):
    dist_info = container.joinpath(f"{name}-{version}.dist-info")
    return dist_info


def _record_row_from_path(path, relative):
    file_data = path.read_bytes()
    # encoded with the urlsafe-base64-nopad encoding (base64.urlsafe_b64encode(digest) with trailing = removed) https://packaging.python.org/en/latest/specifications/recording-installed-packages/#:~:text=encoded%20with%20the%20urlsafe%2Dbase64%2Dnopad%20encoding%20(base64.urlsafe_b64encode(digest)%20with%20trailing%20%3D%20removed
    file_hash = base64.urlsafe_b64encode(hashlib.sha256(file_data).digest()).decode().rstrip('=')
    print(file_hash)
    return [relative.as_posix(), f"sha256={file_hash}", str(len(file_data))]


def iter_files(roots):
    files_list = []
    for root in roots:
        files_list.extend(list_files_recursive(root, root))
    return files_list


def list_files_recursive(original_root, root):
    all_files = []
    files_in_current_dir = sorted(os.listdir(root))
    for file_name in files_in_current_dir:
        path = Path(os.path.join(root, file_name))
        if not path.is_file():
            continue
        if path.name == 'RECORD':
            continue
        if path.suffix == ".pyc" or path.parent.name == "__pycache__":
            continue
        all_files.append((path, path.relative_to(original_root.parent)))
    subdirectories = [d for d in files_in_current_dir if os.path.isdir(os.path.join(root, d))]
    subdirectories.sort()
    for subdir in subdirectories:
        subdir_path = os.path.join(root, subdir)
        path = Path(subdir_path)
        if path.name == "__pycache__":
            continue
        all_files.extend(list_files_recursive(original_root, subdir_path))
    return all_files


def write_record(dist_info, package):
    with dist_info.joinpath("RECORD").open("w") as f:
        w = csv.writer(f, lineterminator="\n")
        for path, relative in iter_files((package, dist_info)):
            w.writerow(_record_row_from_path(path, relative))
        w.writerow([f"{dist_info.name}/RECORD", "", ""])


_NAME = "ml_metadata"
_VERSION = "1.14.0"
_PACKAGE = pathlib.Path("ml_metadata")


def main(argv=None):
    dist_info = create_dist_info_dir(Path.cwd(), _NAME, _VERSION)
    write_record(dist_info, _PACKAGE)


if __name__ == "__main__":
    main()
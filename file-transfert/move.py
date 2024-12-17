import argparse
import os
import random


class Mover:
    def __init__(self, file_src_abs_path: str, file_dst_abs_path: str, file_type: str = "pdf"):
        self.file_src_abs_path = file_src_abs_path
        self.file_dst_abs_path = file_dst_abs_path
        self.file_type = file_type.lower()
        self.files = []
        self.moved_files = []
        self.unsuccessful_files = []

    def move_files(self, src_folder: str, dest_folder: str, file_type: str):
        """
        Move files from a source directory to a destination directory.

        Parameters:
        self (Mover): The instance of the Mover class.
        destination_folder (str): The destination folder where the files will be moved.
        src_folder (str): The source folder where the files are located.
        dest_folder (str): The destination folder where the files will be moved.
        file_type (str): The file type to move.

        Returns:
        None
        """
        self.file_src_abs_path = os.path.abspath(src_folder)
        self.file_dst_abs_path = os.path.abspath(dest_folder)
        self.file_type = file_type.lower()

        if not self._validate_paths():
            return

        self._collect_files()

        self._move_collected_files()

    def _validate_paths(self):
        if not os.path.exists(self.file_src_abs_path):
            print(
                f"Source directory '{self.file_src_abs_path}' does not exist.")
            return False

        if not os.path.exists(self.file_dst_abs_path):
            print(
                f"Destination directory '{self.file_dst_abs_path}' does not exist.")
            return False

        return True

    def _collect_files(self):
        for root, _, files in os.walk(self.file_src_abs_path):
            if self.file_type == "all":
                self.files.extend([os.path.join(root, file) for file in files])
            else:
                for file in files:
                    if file.lower().endswith(f".{self.file_type}"):
                        self.files.append(os.path.join(root, file))

    def _move_collected_files(self):
        for file in self.files:
            file_name = os.path.basename(file)
            new_file_path = os.path.join(self.file_dst_abs_path, file_name)
            try:
                os.rename(file, new_file_path)
                self.moved_files.append(file)
                print(f"Moved: {file} -> {new_file_path}")
            except Exception as e:
                self.unsuccessful_files.append(file)
                print(f"Error moving {file}: {e}")

    def summary(self):
        """
        Print a summary of the move operation.

        Parameters:
        self (Mover): The instance of the Mover class.

        Returns:
        None
        """
        print("\nSummary:")
        print(f"Total files moved: {len(self.moved_files)}")
        print(f"Total files not moved: {len(self.unsuccessful_files)}")
        if self.unsuccessful_files:
            print("Unsuccessful files:")
            for file in self.unsuccessful_files:
                print(file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Move files from a source directory to a destination directory.")
    parser.add_argument("src_folder", type=str,
                        help="The source folder where the files are located.")
    parser.add_argument("dest_folder", type=str,
                        help="The destination folder where the files will be moved.")
    parser.add_argument("--file_type", type=str, default="pdf",
                        help="The file type to move. Default is 'pdf'.")
    args = parser.parse_args()

    mover = Mover("", "")
    mover.move_files(args.src_folder, args.dest_folder, args.file_type)
    mover.summary()

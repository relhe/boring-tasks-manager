import os
import argparse


class FileRenamer:
    def __init__(self, directory, extension="pdf"):
        """
        Initialize the FileRenamer class with the target directory and file extension.
        """
        self.directory = directory
        self.extension = extension

    def rename_files(self, target_word, replacement_word):
        """
        Renames files by replacing a target word with a replacement word in all files with the specified extension.
        """
        for dirpath, _, filenames in os.walk(self.directory):
            for filename in filenames:
                if filename.endswith(f'.{self.extension}') and target_word in filename:
                    new_filename = filename.replace(
                        target_word, replacement_word)
                    old_file_path = os.path.join(dirpath, filename)
                    new_file_path = os.path.join(dirpath, new_filename)
                    os.rename(old_file_path, new_file_path)
                    print(f'Renamed: {old_file_path} -> {new_file_path}')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Automate file renaming in a directory.")
    parser.add_argument("--directory", required=True,
                        help="Directory containing files to rename.")
    parser.add_argument(
        "--replace", help="Target word to replace in filenames.")
    parser.add_argument("--new", help="Replacement word for the target word.")
    parser.add_argument("--prefix", help="Prefix to add to filenames.")
    parser.add_argument("--suffix", help="Suffix to add to filenames.")
    parser.add_argument("--extension", default="pdf",
                        help="File extension to filter by (default is 'pdf').")
    parser.add_argument(
        "--change_extension", help="New file extension to replace the current extension.")

    args = parser.parse_args()

    # Initialize the FileRenamer object
    renamer = FileRenamer(args.directory, args.extension)

    # Execute the renaming operations based on provided arguments
    if args.replace and args.new:
        renamer.rename_files(args.replace, args.new)

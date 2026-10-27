import os
import zipfile
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def archive_directory(dir_path, output_zip):
    try:
        if not os.path.isdir(dir_path):
            raise ValueError(f"The provided path {dir_path} is not a directory.")

        with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(dir_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, dir_path)
                    zipf.write(file_path, arcname)
        logging.info(f"Directory {dir_path} successfully archived to {output_zip}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")


# Example usage
archive_directory("/path/to/directory", "/path/to/output.zip")

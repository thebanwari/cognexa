import os
import shutil
from pathlib import Path
from typing import Optional
import logging

logger = logging.getLogger(__name__)


def ensure_directory_exists(path: str) -> bool:
    """
    Ensure directory exists, creating it if necessary.

    Args:
        path: Directory path

    Returns:
        True if directory exists or was created successfully
    """
    try:
        Path(path).mkdir(parents=True, exist_ok=True)
        return True
    except Exception as e:
        logger.error(f"Failed to create directory {path}: {e}")
        return False


def save_file(content: str, file_path: str) -> bool:
    """
    Save content to a file.

    Args:
        content: File content
        file_path: Path where to save the file

    Returns:
        True if file was saved successfully
    """
    try:
        # Ensure directory exists
        directory = os.path.dirname(file_path)
        if directory and not ensure_directory_exists(directory):
            return False

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        logger.info(f"Successfully saved file: {file_path}")
        return True

    except Exception as e:
        logger.error(f"Failed to save file {file_path}: {e}")
        return False


def save_binary_file(content: bytes, file_path: str) -> bool:
    """
    Save binary content to a file.

    Args:
        content: Binary file content
        file_path: Path where to save the file

    Returns:
        True if file was saved successfully
    """
    try:
        # Ensure directory exists
        directory = os.path.dirname(file_path)
        if directory and not ensure_directory_exists(directory):
            return False

        with open(file_path, 'wb') as f:
            f.write(content)

        logger.info(f"Successfully saved binary file: {file_path}")
        return True

    except Exception as e:
        logger.error(f"Failed to save binary file {file_path}: {e}")
        return False


def load_file(file_path: str) -> Optional[str]:
    """
    Load content from a file.

    Args:
        file_path: Path to the file

    Returns:
        File content if successful, None otherwise
    """
    try:
        if not os.path.exists(file_path):
            logger.warning(f"File not found: {file_path}")
            return None

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        logger.info(f"Successfully loaded file: {file_path}")
        return content

    except Exception as e:
        logger.error(f"Failed to load file {file_path}: {e}")
        return None


def load_binary_file(file_path: str) -> Optional[bytes]:
    """
    Load binary content from a file.

    Args:
        file_path: Path to the file

    Returns:
        File content if successful, None otherwise
    """
    try:
        if not os.path.exists(file_path):
            logger.warning(f"File not found: {file_path}")
            return None

        with open(file_path, 'rb') as f:
            content = f.read()

        logger.info(f"Successfully loaded binary file: {file_path}")
        return content

    except Exception as e:
        logger.error(f"Failed to load binary file {file_path}: {e}")
        return None


def delete_file(file_path: str) -> bool:
    """
    Delete a file.

    Args:
        file_path: Path to the file

    Returns:
        True if file was deleted successfully
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"Successfully deleted file: {file_path}")
        return True

    except Exception as e:
        logger.error(f"Failed to delete file {file_path}: {e}")
        return False


def delete_directory(directory_path: str, recursive: bool = False) -> bool:
    """
    Delete a directory.

    Args:
        directory_path: Path to the directory
        recursive: Whether to delete recursively

    Returns:
        True if directory was deleted successfully
    """
    try:
        if not os.path.exists(directory_path):
            return True

        if recursive:
            shutil.rmtree(directory_path)
        else:
            os.rmdir(directory_path)

        logger.info(f"Successfully deleted directory: {directory_path}")
        return True

    except Exception as e:
        logger.error(f"Failed to delete directory {directory_path}: {e}")
        return False


def list_files(directory_path: str, pattern: str = "*") -> list:
    """
    List files in a directory matching a pattern.

    Args:
        directory_path: Path to the directory
        pattern: File pattern to match

    Returns:
        List of matching file paths
    """
    try:
        if not os.path.exists(directory_path):
            return []

        import glob
        pattern_path = os.path.join(directory_path, pattern)
        files = glob.glob(pattern_path)

        # Return relative paths
        return [os.path.relpath(f, directory_path) for f in files if os.path.isfile(f)]

    except Exception as e:
        logger.error(f"Failed to list files in {directory_path}: {e}")
        return []


def get_file_size(file_path: str) -> Optional[int]:
    """
    Get file size in bytes.

    Args:
        file_path: Path to the file

    Returns:
        File size in bytes if file exists, None otherwise
    """
    try:
        if not os.path.exists(file_path):
            return None

        return os.path.getsize(file_path)

    except Exception as e:
        logger.error(f"Failed to get file size for {file_path}: {e}")
        return None


def file_exists(file_path: str) -> bool:
    """
    Check if file exists.

    Args:
        file_path: Path to the file

    Returns:
        True if file exists
    """
    return os.path.exists(file_path)


def get_file_extension(file_path: str) -> str:
    """
    Get file extension.

    Args:
        file_path: Path to the file

    Returns:
        File extension (including the dot)
    """
    return os.path.splitext(file_path)[1].lower()


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename for safe filesystem usage.

    Args:
        filename: Original filename

    Returns:
        Sanitized filename
    """
    # Remove or replace invalid characters
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')

    # Remove leading/trailing spaces and dots
    filename = filename.strip(' .')

    # Ensure filename is not empty
    if not filename:
        filename = "file"

    # Limit filename length
    if len(filename) > 255:
        name, ext = os.path.splitext(filename)
        filename = name[:255-len(ext)] + ext

    return filename


def create_temp_file(suffix: str = "", prefix: str = "temp_") -> str:
    """
    Create a temporary file.

    Args:
        suffix: File suffix/extension
        prefix: File prefix

    Returns:
        Path to the temporary file
    """
    import tempfile
    temp_file = tempfile.NamedTemporaryFile(suffix=suffix, prefix=prefix, delete=False)
    temp_file.close()
    return temp_file.name


def cleanup_temp_files(directory: str, pattern: str = "temp_*") -> int:
    """
    Clean up temporary files.

    Args:
        directory: Directory to clean
        pattern: Pattern to match for temp files

    Returns:
        Number of files cleaned up
    """
    try:
        files = list_files(directory, pattern)
        cleaned_count = 0

        for file in files:
            file_path = os.path.join(directory, file)
            if delete_file(file_path):
                cleaned_count += 1

        logger.info(f"Cleaned up {cleaned_count} temporary files from {directory}")
        return cleaned_count

    except Exception as e:
        logger.error(f"Failed to cleanup temp files in {directory}: {e}")
        return 0
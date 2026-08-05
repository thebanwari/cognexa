import hashlib
import struct
from typing import List
import math


def generate_mock_embedding(text: str, dim: int = 128) -> List[float]:
    """
    Generate deterministic mock embeddings using SHA256 hash.

    Args:
        text: Input text to embed
        dim: Dimensionality of the embedding vector

    Returns:
        List of float values representing the embedding
    """
    if not text:
        return [0.0] * dim

    # Use SHA256 to generate deterministic hash
    hash_object = hashlib.sha256(text.encode('utf-8'))
    hash_bytes = hash_object.digest()

    # Convert bytes to floats using a consistent method
    embedding = []
    for i in range(dim):
        # Use multiple bytes to create each float value
        byte_index = (i * 4) % len(hash_bytes)
        # Take 4 bytes and convert to float
        value = 0
        for j in range(4):
            actual_index = (byte_index + j) % len(hash_bytes)
            value += hash_bytes[actual_index] << (8 * j)

        # Convert to float in range [-1, 1]
        float_value = ((value % 2147483647) / 2147483647.0) * 2.0 - 1.0
        embedding.append(float_value)

    # Normalize the embedding vector
    return normalize_vector(embedding)


def normalize_vector(vector: List[float]) -> List[float]:
    """
    Normalize a vector to unit length.

    Args:
        vector: Input vector

    Returns:
        Normalized vector
    """
    magnitude = math.sqrt(sum(x * x for x in vector))
    if magnitude == 0:
        return vector

    return [x / magnitude for x in vector]


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """
    Calculate cosine similarity between two vectors.

    Args:
        vec1: First vector
        vec2: Second vector

    Returns:
        Cosine similarity score
    """
    if len(vec1) != len(vec2):
        raise ValueError("Vectors must have the same dimensionality")

    if len(vec1) == 0:
        return 0.0

    # Calculate dot product
    dot_product = sum(a * b for a, b in zip(vec1, vec2))

    # Calculate magnitudes
    magnitude1 = math.sqrt(sum(x * x for x in vec1))
    magnitude2 = math.sqrt(sum(x * x for x in vec2))

    # Avoid division by zero
    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0

    return dot_product / (magnitude1 * magnitude2)


def get_text_embedding(text: str) -> List[float]:
    """
    Get embedding for text with preprocessing.

    Args:
        text: Input text

    Returns:
        Embedding vector
    """
    # Simple preprocessing
    text = text.strip().lower()

    # Use a base embedding and modify it based on text characteristics
    base_embedding = generate_mock_embedding(text)

    # Add some text-specific modifications
    if text:
        # Add position-based variation
        for i, char in enumerate(text[:10]):  # First 10 characters
            char_val = ord(char) % 256
            base_embedding[i % len(base_embedding)] += (char_val - 128) / 256.0

        # Add length-based modification
        length_factor = min(len(text) / 1000.0, 1.0)
        for i in range(len(base_embedding)):
            if i % 2 == 0:
                base_embedding[i] *= (1 + length_factor * 0.1)
            else:
                base_embedding[i] *= (1 - length_factor * 0.1)

    return normalize_vector(base_embedding)
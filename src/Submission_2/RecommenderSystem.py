"""
RecommenderSystem.py - Student Template for Image Recommendation System

This class implements the recommendation system for Phase 2 and Phase 3 of the project.
It uses CLIP embeddings to find similar images and generate transition paths.

IMPORTANT NOTES FOR STUDENTS:
- Fill in the methods below with your own implementation
- Keep the method signatures exactly as shown (parameters and return types)
- You can add helper methods if needed
- The cosine_similarity function is provided for your convenience


Phases:
- Phase 2: find_similar_images() - Find k most similar images
- Phase 3: find_transition_prompts() - Find path connecting two images
"""

import json
from datetime import datetime


class RecommenderSystem:
    """
    Recommender system for finding similar images and generating transition paths.

    Attributes:
        
        vectors_path: Path to the JSON file containing CLIP vectors
    """

    def __init__(self, vectors_path: str, image_data=None, image_id=None):
        """
        Initialize the recommender system by loading CLIP vectors.

        Args:
            vectors_path: Path to JSON file with CLIP embeddings
                         Format: {"uuid": {"image_embedding": [...], "text_embedding": [...]}, ...}
            image_data: (Optional) ImageData instance from Phase 1 for metadata access
            image_id: (Optional) ImageID instance from Phase 1 for UUID mapping
        """
        # TODO: Load vectors from JSON file
        # Structure should be: self.vectors = {uuid: {image_embedding: [...], text_embedding: [...]}}
        pass

    def preprocess(self):
        """
        Preprocess and prepare data structures for efficient queries.

        This method is called once before running Phase 2/3 queries.
        Use it to build indexes or prepare other data structures
        that will speed up similarity computations.

        """
        # TODO: Implement preprocessing
        pass


    @staticmethod
    def cosine_similarity(vec_a, vec_b):
        """
        Compute cosine similarity between two vectors.

        Cosine similarity measures the angle between vectors:
        - 1.0 = identical direction (very similar)
        - 0.0 = perpendicular (not related)
        - -1.0 = opposite direction (very different)

        Args:
            vec_a: First vector (list of floats)
            vec_b: Second vector (list of floats)

        Returns:
            float: Cosine similarity score between -1.0 and 1.0

        Formula:
            similarity = (a · b) / (||a|| * ||b||)
            where · is dot product and ||a|| is the magnitude (norm) of vector a

        Implementation tips:
        - Handle edge cases: empty vectors, zero norms
        """
        # Calculate dot product
        dot = sum(a * b for a, b in zip(vec_a, vec_b))

        # Calculate magnitudes (norms)
        norm_a = sum(a * a for a in vec_a) ** 0.5
        norm_b = sum(b * b for b in vec_b) ** 0.5

        # Return similarity (handle division by zero)
        return dot / (norm_a * norm_b) if norm_a and norm_b else 0.0

    def find_similar_images(self, query_uuid: str, k: int = 10) -> Gallery:
        """
        Find k most similar images to a query image.

        PHASE 2: This is the main evaluation method for Phase 2.

        Args:
            query_uuid: UUID of the query image
            k: Number of similar images to return (default 10)

        Returns:
            Gallery object with images field containing top-k similar UUIDs
            ordered from most to least similar

        Example:
            system = RecommenderSystem("vectors.json")
            system.preprocess()
            gallery = system.find_similar_images("uuid_123", k=10)
            print(gallery.images)  # ['uuid_45', 'uuid_67', ..., 'uuid_99']

        Evaluation:
        - Metric: Recall@100 (your top-10 vs ground truth top-100)
        - Timing: Tested on 1,000 queries
        - Scoring: 25 pts for precision + 15 pts for speed


        TODO: Implement this method
        """
        # TODO:
        # 1. Get query vector from self.vectors
        # 2. Calculate similarity to other images (use cosine_similarity)
        # 3. Sort by similarity (descending)
        # 4. Create and return Gallery with top-k images

        gallery = Gallery()
        gallery.images = []
        return gallery

    def find_transition_prompts(self, uuid_1: str, uuid_2: str) -> list:
        """
        Find a transition path of prompts connecting two images.

        PHASE 3: This is the main evaluation method for Phase 3.

        Args:
            uuid_1: Starting image UUID
            uuid_2: Destination image UUID

        Returns:
            List of prompts describing the visual transition from uuid_1 to uuid_2
            First element should be prompt of uuid_1, last should be prompt of uuid_2
            Length of list represents number of transition steps

        Example:
            prompts = system.find_transition_prompts(uuid_start, uuid_end)
            # Returns: [
            #   "a cat in the snow",          # uuid_start
            #   "an animal in the snow",      # intermediate
            #   "a creature in the snow",     # intermediate
            #   "a dragon in the snow",       # intermediate
            #   "a dragon by a mountain",     # uuid_end
            # ]

        Evaluation:
        - Metric: Word overlap (how many words match ground truth)
        - Timing: Tested on ~10 transitions
        - Scoring: 30 pts for quality + 10 pts for speed

        Algorithm overview:
        1. Get prompts for both images (use image_data if available)
        2. Extract meaningful words from prompts (stop word removal)
        3. Build a graph where nodes are images and edges connect similar images
        4. Return prompts along a path

        Key considerations:
        - Path quality: Should gradually transition from uuid_1 to uuid_2
        - Path length: Shorter paths are faster but may skip important intermediates

        TODO: Implement this method
        """
        # TODO:
        # 1. Validate that both UUIDs exist
        # 2. Get prompts using self.image_data if available
        # 3. Build set of images to explore
        # 4. Build similarity graph between candidates
        # 5. Find path 
        # 6. Extract and return prompts from path

        return []


#!/usr/bin/env python3
"""
autograder_student.py - Student Testing Autograder 

STUDENT VERSION - FOR LOCAL TESTING ONLY

This script allows you to test your implementations locally before submitting to Gradescope.

What it does:
- Phase 1: Tests ImageFiles, ImageID, ImageData, and SearchMetadata classes
- Phase 2: Tests RecommenderSystem image similarity search
- Phase 3: Tests transition path generation

How to use:
1. Place this script in your project directory
2. Run: python autograder_student.py
3. Check the output for which tests pass/fail
4. Fix any failing tests before submitting to Gradescope

================================================================================
CONFIGURATION: Modify these paths to match your local setup
================================================================================
"""

import json
import time
from pathlib import Path

# ============================================================================
# PATH CONFIGURATION - Modify these for your environment
# ============================================================================

# Set your LOCAL paths here
LOCAL_SUBMISSION_DIR = Path(__file__).parent / "submission"
LOCAL_SOURCE_DIR = Path(__file__).parent.parent / "autograder"  # Change this to your paths
LOCAL_RESULTS_DIR = Path(__file__).parent / "results_student"

# ============================================================================
# End of configuration - do not modify below this line
# ============================================================================

SUBMISSION_DIR, SOURCE_DIR, RESULTS_DIR = LOCAL_SUBMISSION_DIR, LOCAL_SOURCE_DIR, LOCAL_RESULTS_DIR

print(f"[CONFIG] Submission dir: {SUBMISSION_DIR}")
print(f"[CONFIG] Source dir: {SOURCE_DIR}\n")


def compute_precision_at_k(student_results, ground_truth_results, k=10, gt_k=100):
    """
    Compute precision@k metric.

    Returns the portion of your top-k results that match the ground truth top-gt_k.
    """
    if not student_results or not ground_truth_results:
        return 0.0

    student_top_k = set(student_results[:k])
    ground_truth_set = set(ground_truth_results[:gt_k])
    correct = len(student_top_k & ground_truth_set)

    return correct / k if k > 0 else 0.0

def evaluate_transition_quality(student_prompts, gt_word_dict):
    """
    Evaluate quality of transition prompts using word overlap metric.

    Args:
        student_prompts: List of student's transition prompts
        gt_word_dict: Ground truth word dictionary with frequencies

    Returns:
        tuple: (quality_score, student_words_dict)
            quality_score: float 0-1
            student_words_dict: dict of words extracted from student prompts
    """
    if not student_prompts or not gt_word_dict:
        return 0.0, {}

    STOP_WORDS = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'by',
        'with', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had',
        'do', 'does', 'did', 'will', 'would', 'should', 'could', 'may', 'might', 'must',
        'can', 'that', 'this', 'it', 'as', 'from', 'up', 'about', 'out', 'if', 'so',
        'than', 'no', 'not', 'only', 'own', 'such', 'too', 'very', 'just'
    }

    # Extract and count words from student prompts
    student_words = {}
    for prompt in student_prompts:
        if not prompt:
            continue
        # Lowercase and extract words
        prompt_lower = prompt.lower()
        words = re.findall(r'\b[a-z]+\b', prompt_lower)
        # Remove stop words
        words = [w for w in words if w not in STOP_WORDS]
        # Count frequencies
        for word in words:
            student_words[word] = student_words.get(word, 0) + 1

    # Compare to ground truth
    matches = 0
    for word, gt_count in gt_word_dict.items():
        student_count = student_words.get(word, 0)
        if student_count == gt_count:
            matches += 1


    # Calculate quality score
    if len(gt_word_dict) == 0:
        return 0.0, student_words

    return matches / len(gt_word_dict), student_words


def run_phase1_tests():
    """Run Phase 1 evaluation (data structures)."""
    print("\n" + "="*70)
    print("PHASE 1: Data Structure Evaluation")
    print("="*70 + "\n")

    try:
        # Find image directory
        image_dir = SOURCE_DIR / "images"
        print(f"Using image directory: {image_dir}")
        print(f"Found {len(list(image_dir.glob('*.png')))} PNG files\n")

        # Import student classes
        try:
            
            from ImageFiles import ImageFiles
            from ImageID import ImageID
            from ImageData import ImageData
            from SearchMetadata import SearchMetadata
        except ImportError as e:
            print(f"❌ ERROR: Failed to import classes: {e}")
            print("   Make sure all classes are in your submission directory.")
            return [], 0, {}

        test_results = []
        total_start = time.time()

        # Test 1: ImageFiles
        print("[1/4] Testing ImageFiles...")
        test1_start = time.time()
        try:
            image_files = ImageFiles()
            image_files.reload_fs(str(image_dir))
            added = image_files.files_added()
            num_images = len(added)
            test1_time = time.time() - test1_start

            expected_images = 10000
            status = "✅ PASS" if num_images == expected_images else "❌ FAIL"
            print(f"  {status}: Found {num_images} images (expected {expected_images})")
            print(f"  Time: {test1_time:.3f}s\n")
        except Exception as e:
            print(f"  ❌ ERROR: {e}\n")
            return [], 0, {}

        # Test 2: ImageID
        print("[2/4] Testing ImageID...")
        test2_start = time.time()
        try:
            image_id = ImageID()
            uuid_count = 0
            for file_path in added:
                uuid = image_id.generate_uuid(file_path)
                if uuid:
                    uuid_count += 1
            test2_time = time.time() - test2_start

            expected_uuids = 10000
            status = "✅ PASS" if uuid_count == expected_uuids else "❌ FAIL"
            print(f"  {status}: Generated {uuid_count} UUIDs (expected {expected_uuids})")
            print(f"  Time: {test2_time:.3f}s\n")
        except Exception as e:
            print(f"  ❌ ERROR: {e}\n")
            return [], 0, {}

        # Test 3: ImageData
        print("[3/4] Testing ImageData...")
        test3_start = time.time()
        image_data = None
        try:
            import cfg
            image_data = ImageData()
            image_id = ImageID()

            metadata_loaded = 0
            for image_file in sorted(added):
                if image_file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    try:
                        rel_path = cfg.get_canonical_pathfile(str(image_file))
                        uuid = image_id.generate_uuid(rel_path)
                        if uuid:
                            image_data.add_image(uuid, rel_path)
                            image_data.load_metadata(uuid)
                            metadata_loaded += 1
                    except:
                        pass

            test3_time = time.time() - test3_start

            expected_metadata = 10000
            status = "✅ PASS" if metadata_loaded == expected_metadata else "❌ FAIL"
            print(f"  {status}: Loaded {metadata_loaded} metadata entries (expected {expected_metadata})")
            print(f"  Time: {test3_time:.3f}s\n")
        except Exception as e:
            print(f"  ❌ ERROR: {e}\n")
            return [], 0, {}

        # Test 4: SearchMetadata
        print("[4/4] Testing SearchMetadata...")
        test4_start = time.time()
        try:
            searcher = SearchMetadata(image_data)
            # Expected result counts for each query
            expected_counts = {
                "portrait": 1111, "art": 1741, "painting": 1000, "digital": 100,  "fantasy":25
            }  

            # Test with a few sample queries
            test_queries = ["portrait", "art", "painting", "digital", "fantasy"]
                
            total_results = 0
            actual_counts = {}
            mismatches = []

            for query in test_queries:
                try:
                    results = searcher.prompt(query)
                    if results:
                        total_results += len(results)
                        actual_counts[query] = results

                    # Check against expected count
                    if query in expected_counts:
                        expected = expected_counts[query]
                        if results != expected:
                            mismatches.append(f"  '{query}': expected {expected}, got {results}")
                        print(f"INFO [Search]: prompt('{query}') found {results} results")
                    else:
                        print(f"INFO [Search]: prompt('{query}') found {results} results")
                except:
                    pass

            test4_time = time.time() - test4_start


        except Exception as e:
            print(f"  ❌ ERROR: {e}\n")
            return [], 0, {}

        total_phase1_time = time.time() - total_start
        return [], total_phase1_time, {}

    except Exception as e:
        print(f"FATAL ERROR in Phase 1: {e}")
        return [], 0, {}


def run_phase2_tests(image_data_phase1=None, searcher_phase1=None, image_id_phase1=None):
    """Run Phase 2 evaluation (image similarity)."""
    print("\n" + "="*70)
    print("PHASE 2: Image Similarity Search")
    print("="*70 + "\n")

    try:
        # Load test data
        vectors_path = SOURCE_DIR / "clip_vectors.json"
        queries_path = SOURCE_DIR / "private_test_queries.json"

        print(f"Loading CLIP vectors...")
        with open(vectors_path, 'r') as f:
            vectors_data = json.load(f)
        vectors = vectors_data.get("vectors", vectors_data)
        print(f"  Loaded {len(vectors)} vectors")

        print(f"Loading test queries...")
        with open(queries_path, 'r') as f:
            test_data = json.load(f)
        test_queries = test_data.get("queries", [])
        print(f"  Loaded {len(test_queries)} queries\n")

        # Import student's RecommenderSystem
        try:
            from RecommenderSystem import RecommenderSystem
        except ImportError as e:
            print(f"❌ ERROR: Failed to import RecommenderSystem: {e}")
            return [], 0, 0, 0.0

        print("[1/1] Testing Image Similarity (10 sample queries)...")
        try:
            system = RecommenderSystem(str(vectors_path), image_data_phase1, image_id_phase1)

            # Preprocessing
            preprocess_start = time.time()
            system.preprocess()
            preprocess_time = time.time() - preprocess_start
            print(f"  Preprocessing: {preprocess_time:.3f}s")

            # Test with 10 sample queries
            tier1_start = time.time()
            successful_queries = 0

            for query_uuid in test_queries[:10]:
                try:
                    gallery = system.find_similar_images(query_uuid, k=10)
                    if gallery and gallery.images:
                        successful_queries += 1
                except:
                    pass

            tier1_time = time.time() - tier1_start

            status = "✅ PASS" if successful_queries == 10 else "❌ FAIL"
            print(f"  {status}: {successful_queries}/10 queries returned results")
            print(f"  Query time: {tier1_time:.3f}s ({tier1_time/10 if successful_queries > 0 else 0:.4f}s/query)\n")

            return [], preprocess_time + tier1_time, preprocess_time, tier1_time

        except Exception as e:
            print(f"  ❌ ERROR: {e}\n")
            return [], 0, 0, 0

    except Exception as e:
        print(f"FATAL ERROR in Phase 2: {e}")
        return [], 0, 0, 0


def run_phase3_tests(image_data=None, image_id=None):
    """Run Phase 3 evaluation (transition paths)."""
    print("\n" + "="*70)
    print("PHASE 3: Transition Path Generation")
    print("="*70 + "\n")

    try:
        # Load test data
        vectors_path = SOURCE_DIR / "clip_vectors.json"
        gt_path = Path(__file__).parent / "transition_ground_truth.json"

        print(f"Loading CLIP vectors...")
        with open(vectors_path, 'r') as f:
            vectors_data = json.load(f)
        vectors = vectors_data.get("vectors", vectors_data)
        print(f"  Loaded {len(vectors)} vectors")

        if not gt_path.exists():
            print(f"⚠️  Warning: Ground truth file not found at {gt_path}")
            print(f"   Run generate_transition_gt.py first to create test transitions")
            return [], 0, 0.0

        print(f"Loading ground truth transitions...")
        with open(gt_path, 'r') as f:
            gt_data = json.load(f)
        transitions = gt_data.get("transitions", [])
        print(f"  Loaded {len(transitions)} transitions\n")

        # Import student's RecommenderSystem
        try:
            from RecommenderSystem import RecommenderSystem
        except ImportError as e:
            print(f"❌ ERROR: Failed to import RecommenderSystem: {e}")
            return [], 0, 0.0

        print(f"[3/3] Testing Transition Paths ({min(5, len(transitions))} sample transitions)...")
        try:
            system = RecommenderSystem(str(vectors_path), image_data, image_id)

            tier3_start = time.time()
            successful = 0

            for idx, transition in enumerate(transitions[:5]):
                uuid_1 = transition["uuid_1"]
                uuid_2 = transition["uuid_2"]
                gt_word_dict = transition["word_dict"]
                gt_path_length = transition["path_length"]

                try:
                    # Call student's find_transition_prompts
                    
                    student_prompts = system.find_transition_prompts(uuid_1, uuid_2)
                    

                    if student_prompts is None or len(student_prompts) == 0:
                        failed_transitions += 1
                        continue

                    # Evaluate quality using word overlap metric
                    quality_score, _ = evaluate_transition_quality(student_prompts, gt_word_dict)
                    total_quality += quality_score

                    # Compare path lengths
                    student_path_length = len(student_prompts)
                    path_length_diff = abs(student_path_length - gt_path_length)
                    total_path_length_diff += path_length_diff

                    successful_transitions += 1
                except Exception as e:
                    print(f"  [{idx+1}/5] ❌ Error: {str(e)[:50]}")

            tier3_time = time.time() - tier3_start

             # Calculate averages
            if successful_transitions > 0:
                avg_quality = total_quality / successful_transitions
                avg_path_diff = total_path_length_diff / successful_transitions
            else:
                avg_quality = 0.0
                avg_path_diff = 0.0


            return _, tier3_time, successful_transitions, avg_quality

        except Exception as e:
            print(f"  ❌ ERROR: {e}\n")
            return [], 0, 0.0

    except Exception as e:
        print(f"FATAL ERROR in Phase 3: {e}")
        return [], 0, 0.0


def main():
    """Main autograder entry point."""

    print("\n" + "="*70)
    print("CLIP IMAGE MANAGER - STUDENT TESTING AUTOGRADER")
    print("="*70)
    print("Local testing only - This will help you debug before submitting\n")

    # Run Phase 1
    phase1_results, phase1_time, phase1_validation = run_phase1_tests()

    # Run Phase 2
    phase2_results, phase2_time, preprocess_time, tier1_time = run_phase2_tests()

    # Run Phase 3
    phase3_results, tier3_time, tier3_quality = run_phase3_tests()

    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Phase 1 (Data Structures): ~{phase1_time:.1f}s")
    print(f"Phase 2 (Image Similarity): ~{phase2_time:.1f}s (preprocess: {preprocess_time:.1f}s, queries: {tier1_time:.1f}s)")
    print(f"Phase 3 (Transitions): ~{tier3_time:.1f}s")
    print("="*70)

    print("\n✅ Local tests completed!")
    print("   Review any failures above and fix your implementation.")
    print("   When ready, submit to Gradescope for official evaluation.\n")


if __name__ == "__main__":
    main()

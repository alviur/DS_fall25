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


def compute_precision_at_k(student_results, ground_truth_results, k=10, gt_k=100, image_id=None):
    """
    Compute precision@k: percentage of student's top-k that appear in ground truth top-gt_k.

    This is more flexible than strict Precision@10 - it allows correct results
    that may not be in the exact top-10 but are still in the top-100 of ground truth.

    Args:
        student_results: List of UUIDs returned by student (top-k items)
        ground_truth_results: List of top-gt_k UUIDs from ground truth
        k: Number of student results to evaluate (default: 10)
        gt_k: Size of ground truth set to check against (default: 100)
        image_id: Optional ImageID instance to convert UUIDs to filenames for comparison

    Returns:
        precision: float 0-1 (portion of student's top-k found in ground truth top-gt_k)
    """
    if not student_results or not ground_truth_results:
        return 0.0

    # Take only top-k from student results
    student_top_k_raw = student_results[:k]

    # Take only top-gt_k from ground truth (more flexible)
    ground_truth_raw = ground_truth_results[:gt_k]

    # If image_id is provided, convert UUIDs to filenames for comparison
    if image_id is not None:
        student_top_k = set()
        for uuid in student_top_k_raw:
            filename = image_id._file_to_uuid.get(uuid+'.png')
            if filename:
                student_top_k.add(filename)

        ground_truth_set = set()
        for uuid in ground_truth_raw:
            # Convert filename to UUID using the _file_to_uuid mapping
            filename = image_id._file_to_uuid.get(uuid+'.png')
            if filename:
                ground_truth_set.add(filename)
    else:
        # Fall back to UUID-based comparison
        student_top_k = set(student_top_k_raw)
        ground_truth_set = set(ground_truth_raw)

    
    # Count correct items (student's top-k that appear in ground truth top-gt_k)
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


        # Try to find image directory
        image_dir =  SOURCE_DIR + "images"
        image_dir = Path(image_dir)
        

       

        print(f"Using image directory: {image_dir}")
        
        print(f"Found {len(list(image_dir.glob('*.png')))} PNG files\n")
        
        
        from ImageFiles import ImageFiles
        from ImageID import ImageID
        from ImageData import ImageData
        from SearchMetadata import SearchMetadata

        # Run tests with timing
        total_start = time.time()
        test_results = []

        # Track validation status for suspension
        phase1_validation = {
            "imagefiles": False,
            "imageid": False,
            "imagedata": False,
            "searchmetadata": False
        }

        
        # Test 1: ImageFiles
        print("[1/4] Testing ImageFiles...")
        test1_start = time.time()
        try:
            
            image_files = ImageFiles()
            image_files.reload_fs(str(image_dir))
            added = image_files.files_added()
            num_images = len(added)
            test1_time = time.time() - test1_start

            # Check if matches expected count
            expected_images = 10000
            images_match = num_images == expected_images
            match_flag_1 = "PASS" if images_match else "FAIL"
            phase1_validation["imagefiles"] = images_match

            test_results.append({
                "name": "Phase 1: ImageFiles (file loading)",
                "output": f"Time: {test1_time:.3f}s\nImages loaded: {num_images}\nExpected: {expected_images}\nValidation: {match_flag_1}",
                "score": 0,
                "max_score": 0
            })
            print(f"  ✓ ImageFiles: {test1_time:.3f}s ({num_images} images) - Validation: {match_flag_1}\n")
        except Exception as e:
            test1_time = time.time() - test1_start
            test_results.append({
                "name": "Phase 1: ImageFiles (file loading)",
                "output": f"ERROR: {type(e).__name__}: {e}\nTime: {test1_time:.3f}s\nValidation: FAIL",
                "score": 0,
                "max_score": 0
            })
            print(f"  ✗ ImageFiles failed: {e}\n")

        # Test 2: ImageID
        print("[2/4] Testing ImageID...")
        test2_start = time.time()
        try:
            image_id = ImageID()
            # Generate UUIDs for all files
            uuid_count = 0
            for file_path in added:
                uuid = image_id.generate_uuid(file_path)
                if uuid:
                    uuid_count += 1
            test2_time = time.time() - test2_start

            # Check if matches expected count
            expected_uuids = 10000
            uuids_match = uuid_count == expected_uuids
            match_flag_2 = "PASS" if uuids_match else "FAIL"
            phase1_validation["imageid"] = uuids_match

            test_results.append({
                "name": "Phase 1: ImageID (UUID generation)",
                "output": f"Time: {test2_time:.3f}s\nUUIDs generated: {uuid_count}\nExpected: {expected_uuids}\nTotal images: {len(added)}\nValidation: {match_flag_2}",
                "score": 0,
                "max_score": 0
            })
            print(f"  ✓ ImageID: {test2_time:.3f}s ({uuid_count} UUIDs out of {len(added)} images) - Validation: {match_flag_2}\n")
        except Exception as e:
            test2_time = time.time() - test2_start
            test_results.append({
                "name": "Phase 1: ImageID (UUID generation)",
                "output": f"ERROR: {type(e).__name__}: {e}\nTime: {test2_time:.3f}s\nValidation: FAIL",
                "score": 0,
                "max_score": 0
            })
            print(f"  ✗ ImageID failed: {e}\n")

        # Test 3: ImageData
        print("[3/4] Testing ImageData...")
        test3_start = time.time()
        image_data = None
        try:
            # Import cfg to use read_png_metadata
            import cfg

            image_data = ImageData()
            image_id = ImageID()  # Use ImageID to properly generate UUIDs

            # Add images with UUIDs and load metadata
            metadata_loaded = 0
            for image_file in sorted(added):  # Use images found in Test 1
                if image_file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    try:
                        # Get canonical relative path
                        rel_path = cfg.get_canonical_pathfile(str(image_file))

                        # Generate UUID using ImageID
                        uuid = image_id.generate_uuid(rel_path)

                        if uuid:
                            # Add image to ImageData with UUID
                            image_data.add_image(uuid, rel_path)
                        

                            # Load metadata from PNG file
                            image_data.load_metadata(uuid)
                            
                            metadata_loaded += 1
                    except:
                        # If it fails for one image, continue with others
                        pass

            test3_time = time.time() - test3_start

            # Check if matches expected count
            expected_metadata = 10000
            metadata_match = metadata_loaded == expected_metadata
            match_flag_3 = "PASS" if metadata_match else "FAIL"
            phase1_validation["imagedata"] = metadata_match

            test_results.append({
                "name": "Phase 1: ImageData (metadata loading)",
                "output": f"Time: {test3_time:.3f}s\nMetadata from images: {metadata_loaded}\nExpected: {expected_metadata}\nTotal images in data: {len(image_data)}\nValidation: {match_flag_3}",
                "score": 0,
                "max_score": 0
            })
            print(f"  ✓ ImageData: {test3_time:.3f}s (loaded {metadata_loaded} metadata entries) - Validation: {match_flag_3}\n")
        except Exception as e:
            test3_time = time.time() - test3_start
            test_results.append({
                "name": "Phase 1: ImageData (metadata loading)",
                "output": f"ERROR: {type(e).__name__}: {e}\nTime: {test3_time:.3f}s\nValidation: FAIL",
                "score": 0,
                "max_score": 0
            })
            print(f"  ✗ ImageData failed: {e}\n")

        # Test 4: SearchMetadata
        print("[4/4] Testing SearchMetadata...")
        test4_start = time.time()
        try:
            searcher = SearchMetadata(image_data)
            # Expected result counts for each query
            expected_counts = {
                "portrait": 1111, "art": 3020, "painting": 1741, "digital": 1041,  "fantasy":765
            }  

            # Test with a few sample queries
            test_queries = ["portrait", "art", "painting", "digital", "fantasy"]
                
            total_results = 0
            actual_counts = {}
            mismatches = []

            for query in test_queries:
                try:
                    
                    results = searcher.prompt(query) if hasattr(searcher, 'prompt') else []
                    actual_count = len(results) if results else 0
                    actual_counts[query] = actual_count

                    if results:
                        total_results += actual_count

                    if query in expected_counts:
                        expected = expected_counts[query]
                        if actual_count != expected:                            
                            mismatches.append(f" Query {len(mismatches)+1}: Count mismatch!! got {actual_count}")                                                    
                    else:
                        print(f"INFO [Search]: Query prompt found {actual_count} results")
                except:
                    # If search fails for one query, continue with others
                    pass

            test4_time = time.time() - test4_start

            # Determine if search results match expected counts
            search_metadata_matches = len(mismatches) == 0
            match_flag = "PASS" if search_metadata_matches else "FAIL"
            phase1_validation["searchmetadata"] = search_metadata_matches

            output_message = f"Time: {test4_time:.3f}s\nQueries executed: {len(test_queries)}\nTotal results found: {total_results}\nSearch Result Validation: {match_flag}"

            if mismatches:
                output_message += f"\n\nMismatches ({len(mismatches)}):\n" + "\n".join(mismatches)

            test_results.append({
                "name": "Phase 1: SearchMetadata (search)",
                "output": output_message,
                "score": 0,
                "max_score": 0
            })
            print(f"  ✓ SearchMetadata: {test4_time:.3f}s (executed {len(test_queries)} queries)\n")
        except Exception as e:
            test4_time = time.time() - test4_start
            test_results.append({
                "name": "Phase 1: SearchMetadata (search)",
                "output": f"Time: {test4_time:.3f}s\nQueries executed: {len(test_queries)}\nTotal results found: {total_results}\nSearch Result Validation: FAIL\n\nDiagnostic Info:\n" + "\n".join(debug_info),
                "score": 0,
                "max_score": 0
            })
            print(f"  ✗ SearchMetadata failed: {e}\n")

        total_phase1_time = time.time() - total_start
        if mismatches:
            print("Your have mismatches!! your SearchMetadata time will be multiplied x100")
            total_phase1_time *=100

        # Return image_data, searcher, and image_id for Phase 2 filtering optimization and filename comparison
        return test_results, total_phase1_time, phase1_validation, test4_time, image_data, searcher, image_id

    except Exception as e:
        print(f"FATAL ERROR in Phase 1: {e}")
        return [{
            "name": "Phase 1: Evaluation",
            "output": f"FATAL ERROR: {type(e).__name__}: {e}",
            "score": 0,
            "max_score": 0
        }], 0, {}, 0, None, None, None



def run_phase2_tests(image_data_phase1=None, searcher_phase1=None, image_id_phase1=None):
    """
    Run Phase 2 evaluation (recommendation system).

    Args:
        image_data_phase1: ImageData instance from Phase 1 (for filtering optimization)
        searcher_phase1: SearchMetadata instance from Phase 1 (for filtering optimization)
        image_id_phase1: ImageID instance from Phase 1 (for filename-based precision comparison)
    """
    print("\n" + "="*70)
    print("PHASE 2: Recommendation System Evaluation")
    print("="*70 + "\n")

    try:
        # Load test data
        vectors_path = SOURCE_DIR+"clip_vectors_private.json"
        queries_path = SOURCE_DIR+"private_test_queries.json"

        print(f"Loading CLIP vectors from {vectors_path}...")

        with open(vectors_path, 'r') as f:
            vectors_data = json.load(f)

        if "vectors" in vectors_data:
            vectors = vectors_data["vectors"]
        else:
            vectors = vectors_data

        print(f"Loaded {len(vectors)} vectors\n")

        # Load test queries
        with open(queries_path, 'r') as f:
            test_data = json.load(f)
        test_queries = test_data.get("queries", [])

        if not test_queries:
            return [{
                "name": "Phase 2: Query Setup",
                "output": "ERROR: No test queries found",
                "score": 0,
                "max_score": 0
            }], 0, 0, 0, 0, 0, 0, 0.0, 0.0

        # Import student's solution
        try:
            from RecommenderSystem import RecommenderSystem
        except ImportError as e:
            return [{
                "name": "Phase 2: Solution Import",
                "output": f"ERROR: Failed to import RecommenderSystem from RecommenderSystem.py: {e}",
                "score": 0,
                "max_score": 0
            }], 0, 0, 0, 0, 0, 0, 0.0, 0.0

        test_results = []

        # Load precomputed ground truth from file (fast - just JSON loading)
        print("Loading precomputed ground truth from file...")
        ground_truth_path = SOURCE_DIR + "ground_truth.json"


        with open(ground_truth_path, 'r') as f:
            all_ground_truth = json.load(f)

        tier1_ground_truth = all_ground_truth

        print(f"  ✓ Loaded ground truth for {len(tier1_ground_truth)} queries\n")

        # Test Phase 2 - Tier 1 only
        print("[1/1] Testing Tier 1 (Image Similarity) - 1K queries...")
        try:
            system = RecommenderSystem(str(vectors_path), image_data_phase1, image_id_phase1)

            # Set search context for filtering optimization if available
            if image_data_phase1 is not None and searcher_phase1 is not None:
                try:
                    # Try to set the filtering context if the student's implementation supports it
                    if hasattr(system, 'set_search_context'):
                        system.set_search_context(searcher_phase1, image_data_phase1)
                        print("  ✓ Enabled metadata-based filtering optimization\n")
                except Exception as e:
                    print(f"  Note: Filtering optimization not available: {e}\n")

            # Preprocessing
            preprocess_start = time.time()
            system.preprocess()
            preprocess_time = time.time() - preprocess_start
            print(f"  Preprocessing: {preprocess_time:.3f}s\n")

            # Run Tier 1 queries (1K queries) with precision tracking
            tier1_start = time.time()
            num_queries_tier1 = 0
            tier1_precisions = []

            num_queries_try = 1000
            for query_uuid in test_queries[:num_queries_try]:  # 1K queries
                try:
                    gallery = system.find_similar_images(query_uuid, k=10)
                    num_queries_tier1 += 1

                    # Calculate precision: student's top-10 vs ground truth top-100 (relaxed)
                    if query_uuid in tier1_ground_truth:
                        precision = compute_precision_at_k(gallery.images, tier1_ground_truth[query_uuid], k=10, gt_k=100, image_id=image_id_phase1) # Compute precision here
                        tier1_precisions.append(precision)
                except Exception as e:
                    pass

            tier1_time = time.time() - tier1_start
            avg_tier1_time = tier1_time / num_queries_tier1 if num_queries_tier1 > 0 else 0
            #avg_tier1_precision = np.mean(tier1_precisions) if tier1_precisions else 0.0
            avg_tier1_precision = sum(tier1_precisions) / len(tier1_precisions) if tier1_precisions else 0.0


            test_results.append({
                "name": "Phase 2: Tier 1 (Image Similarity)",
                "output": f"Time: {tier1_time:.3f}s\nQueries: {num_queries_tier1}\nAvg per query: {avg_tier1_time:.4f}s\nRecall@100: {avg_tier1_precision:.1%} (top-10 found in GT top-100)",
                "score": 0,
                "max_score": 0
            })
            print(f"  ✓ Tier 1: {tier1_time:.3f}s ({num_queries_tier1} queries, {avg_tier1_time:.4f}s/query)")
            print(f"    → Recall@100: {avg_tier1_precision:.1%} (top-10 found in GT top-100)\n")

        except Exception as e:
            tier1_time = 0
            test_results.append({
                "name": "Phase 2: Tier 1 (Image Similarity)",
                "output": f"ERROR: {type(e).__name__}: {e}",
                "score": 0,
                "max_score": 0
            })
            print(f"  ✗ Tier 1 failed: {e}\n")

        total_phase2_time = preprocess_time + tier1_time

        return test_results, total_phase2_time, preprocess_time, tier1_time, 0, num_queries_tier1, 0, avg_tier1_precision, 0.0

    except Exception as e:
        print(f"FATAL ERROR in Phase 2: {e}")
        return [{
            "name": "Phase 2: Evaluation",
            "output": f"FATAL ERROR: {type(e).__name__}: {e}",
            "score": 0,
            "max_score": 0
        }], 0, 0, 0, 0, 0, 0, 0.0, 0.0


def run_phase3_tests(image_data=None, image_id=None):
    """
    Run Phase 3 evaluation (transition paths).

    Tests student's find_transition_prompts() method with precomputed ground truth.

    Args:
        image_data: ImageData instance from Phase 1 (for prompt retrieval)
    """
    print("\n" + "="*70)
    print("PHASE 3: Transition Paths Evaluation")
    print("="*70 + "\n")

    try:
        # Load test data
        vectors_path = SOURCE_DIR + "clip_vectors_private.json"
        gt_path = SOURCE_DIR + "transition_ground_truth.json"

        print(f"Loading CLIP vectors from {vectors_path}...")
        with open(vectors_path, 'r') as f:
            vectors_data = json.load(f)

        if "vectors" in vectors_data:
            vectors = vectors_data["vectors"]
        else:
            vectors = vectors_data

        print(f"Loaded {len(vectors)} vectors")

        # Load ground truth
        print(f"Loading transition ground truth from {gt_path}...")

        with open(gt_path, 'r') as f:
            gt_data = json.load(f)

        transitions = gt_data.get("transitions", [])
        print(f"  ✓ Loaded {len(transitions)} ground truth transitions\n")

        # Import student's solution
        try:
            from RecommenderSystem import RecommenderSystem
        except ImportError as e:
            return [{
                "name": "Phase 3: Solution Import",
                "output": f"ERROR: Failed to import RecommenderSystem: {e}",
                "score": 0,
                "max_score": 0
            }], 0, 0, 0.0

        test_results = []

        # Test Phase 3
        print(f"[3/3] Testing Tier 3 (Transition Paths) - {len(transitions)} transitions...")

        try:
            system = RecommenderSystem(str(vectors_path), image_data, image_id)

            # Set image_data if available (for prompt retrieval)
            if image_data:
                system.image_data = image_data
                print(f"Using image_data from Phase 1 for prompt retrieval")

            tier3_start = time.time()
            successful_transitions = 0
            failed_transitions = 0
            total_quality = 0.0
            total_path_length_diff = 0.0

            for idx, transition in enumerate(transitions):
                uuid_1 = transition["uuid_1"]
                uuid_2 = transition["uuid_2"]
                gt_prompts = transition["prompts"]
                gt_word_dict = transition["word_dict"]
                gt_path_length = transition["path_length"]

                try:
                    # Call student's find_transition_prompts
                    student_start = time.time()
                    student_prompts = system.find_transition_prompts(uuid_1, uuid_2)
                    student_time = time.time() - student_start

                    if student_prompts is None or len(student_prompts) == 0:
                        failed_transitions += 1
                        continue

                    # Evaluate quality using word overlap metric
                    quality_score, student_words_dict = evaluate_transition_quality(student_prompts, gt_word_dict)
                    total_quality += quality_score

                    # Compare path lengths
                    student_path_length = len(student_prompts)
                    path_length_diff = abs(student_path_length - gt_path_length)
                    total_path_length_diff += path_length_diff

                    successful_transitions += 1

                    # Debug output
                    quality_percent = quality_score * 100
                    print(f"  [{idx+1}/{len(transitions)}] Path: {student_path_length} steps | Time: {student_time:.3f}s")


                except Exception as e:
                    failed_transitions += 1
                    print(f"  [{idx+1}/{len(transitions)}] ERROR: {type(e).__name__}: {str(e)[:50]}")

            tier3_time = time.time() - tier3_start

            # Calculate averages
            if successful_transitions > 0:
                avg_quality = total_quality / successful_transitions
                avg_path_diff = total_path_length_diff / successful_transitions
            else:
                avg_quality = 0.0
                avg_path_diff = 0.0

            output_text = f"Tier 3: {tier3_time:.3f}s ({len(transitions)} queries, {tier3_time/len(transitions) if len(transitions) > 0 else 0:.3f}s/query)\n"
            output_text += f"  → Successful: {successful_transitions}/{len(transitions)}\n"
            output_text += f"  → Avg quality score: {avg_quality:.1%}\n"
            output_text += f"  → Avg path length difference: {avg_path_diff:.1f} hops"

            test_results.append({
                "name": "Phase 3: Tier 3 (Transition Paths)",
                "output": output_text,
                "score": 0,
                "max_score": 0
            })

            print(f"\n  ✓ Tier 3: {tier3_time:.3f}s ({len(transitions)} queries, {tier3_time/len(transitions) if len(transitions) > 0 else 0:.3f}s/query)")
            print(f"    → Avg quality: {avg_quality:.1%}")
            print(f"    → Avg path length difference: {avg_path_diff:.1f} hops\n")

            return test_results, tier3_time, successful_transitions, avg_quality

        except Exception as e:
            print(f"  ✗ Tier 3 failed: {e}\n")
            test_results.append({
                "name": "Phase 3: Tier 3 (Transition Paths)",
                "output": f"ERROR: {type(e).__name__}: {e}",
                "score": 0,
                "max_score": 0
            })
            return test_results, 0, 0, 0.0

    except Exception as e:
        print(f"FATAL ERROR in Phase 3: {e}")
        return [{
            "name": "Phase 3: Evaluation",
            "output": f"FATAL ERROR: {type(e).__name__}: {e}",
            "score": 0,
            "max_score": 0
        }], 0, 0, 0.0


def main():
    """Main autograder entry point."""

    print("\n" + "="*70)
    print("CLIP IMAGE MANAGER - STUDENT TESTING AUTOGRADER")
    print("="*70)
    print("Local testing only - This will help you debug before submitting\n")

    # Run Phase 1
    phase1_results, phase1_time, phase1_validation = run_phase1_tests()

    # Run Phase 2
    phase2_results = run_phase2_tests(image_data_phase1, searcher_phase1, image_id_phase1)
    phase2_tests, phase2_time, preprocess_time, tier1_time, tier2_time, num_queries_tier1, num_queries_tier2, tier1_precision, tier2_precision = phase2_results

    # Run Phase 3
    phase3_results = run_phase3_tests(image_data_phase1, image_id_phase1)
    phase3_tests, tier3_time, num_successful_tier3, tier3_quality = phase3_results

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

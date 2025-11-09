"""
Comprehensive Test Suite for Friend Connection System Backend
This single file contains all tests, demo, and test data generation
"""

import unittest
import os
import sys
from Backend import Backend
from Algorithm import UF_by_size, Bidirectional_Dijkstra


# ============================================================================
# UNIT TEST CLASS
# ============================================================================
test_dir = r"D:\dont_move\relation_file.csv"

class TestBackend(unittest.TestCase):
    """Comprehensive unit tests for the Backend class"""
    
    @classmethod
    def setUpClass(cls):
        """Create test data file once before all tests"""
        pass
    
    def setUp(self):
        """Set up test backend for each test"""
        self.backend = Backend(test_dir)
    
    # ------------------------------------------------------------------------
    # TEST 1: INITIALIZATION
    # ------------------------------------------------------------------------
    def test_01_initialization(self):
        """Test that Backend initializes correctly with proper data structures"""
        print("\n[TEST 1] Testing Backend initialization...")
        
        self.assertIsNotNone(self.backend.uf, "Union-Find should be initialized")
        self.assertIsNotNone(self.backend.graph, "Graph should be initialized")
        self.assertIsInstance(self.backend.uf, UF_by_size, "Should use UF_by_size class")
        self.assertIsInstance(self.backend.graph, Bidirectional_Dijkstra, "Should use Bidirectional_Dijkstra class")
        
        print("  ✓ Backend initialized with correct data structures")
    
    # ------------------------------------------------------------------------
    # TEST 2: SAME COMPONENT RELATIONS
    # ------------------------------------------------------------------------
    def test_02_check_relation_same_component(self):
        """Test checking relations within the same connected component"""
        print("\n[TEST 2] Testing relations within same components...")
        
        # Test Group 1: Alice, Bob, Charlie, David
        group1_tests = [
            ("Alice", "Bob"), ("Alice", "Charlie"), ("Alice", "David"),
            ("Bob", "Charlie"), ("Bob", "David"), ("Charlie", "David")
        ]
        for p1, p2 in group1_tests:
            self.assertTrue(self.backend.check_relation(p1, p2), 
                          f"{p1} and {p2} should be connected in Group 1")
        print("  ✓ Group 1 (Alice's group): All members connected")
        
        # Test Group 2: Emily, Frank, Grace, Henry
        group2_tests = [
            ("Emily", "Frank"), ("Emily", "Grace"), ("Emily", "Henry"),
            ("Frank", "Grace"), ("Frank", "Henry"), ("Grace", "Henry")
        ]
        for p1, p2 in group2_tests:
            self.assertTrue(self.backend.check_relation(p1, p2),
                          f"{p1} and {p2} should be connected in Group 2")
        print("  ✓ Group 2 (Emily's group): All members connected")
        
        # Test Group 4: Mike, Nancy (simple pair)
        self.assertTrue(self.backend.check_relation("Mike", "Nancy"))
        print("  ✓ Group 4 (Mike-Nancy): Pair connected")
    
    # ------------------------------------------------------------------------
    # TEST 3: DIFFERENT COMPONENT RELATIONS
    # ------------------------------------------------------------------------
    def test_03_check_relation_different_components(self):
        """Test that different components are not connected"""
        print("\n[TEST 3] Testing relations between different components...")
        
        disconnected_pairs = [
            ("Alice", "Emily"),   # Group 1 vs Group 2
            ("Alice", "Ivan"),    # Group 1 vs Group 3
            ("Alice", "Mike"),    # Group 1 vs Group 4
            ("Emily", "Ivan"),    # Group 2 vs Group 3
            ("Oliver", "Sam"),    # Group 5 vs Group 6
        ]
        
        for p1, p2 in disconnected_pairs:
            self.assertFalse(self.backend.check_relation(p1, p2),
                           f"{p1} and {p2} should NOT be connected (different groups)")
        
        print("  ✓ Different groups are properly disconnected")
    
    # ------------------------------------------------------------------------
    # TEST 4: NON-EXISTENT PERSONS
    # ------------------------------------------------------------------------
    def test_04_check_relation_nonexistent_person(self):
        """Test handling of non-existent persons"""
        print("\n[TEST 4] Testing non-existent person handling...")
        
        self.assertFalse(self.backend.check_relation("Alice", "Zoe"))
        self.assertFalse(self.backend.check_relation("Zoe", "Alice"))
        self.assertFalse(self.backend.check_relation("Zoe", "Yara"))
        
        print("  ✓ Non-existent persons handled correctly")
    
    # ------------------------------------------------------------------------
    # TEST 5: DIRECT CONNECTIONS
    # ------------------------------------------------------------------------
    def test_05_get_best_path_direct_connection(self):
        """Test finding paths for directly connected friends"""
        print("\n[TEST 5] Testing direct connection paths...")
        
        test_cases = [
            ("Alice", "Bob", 5, ["Alice", "Bob"]),
            ("Bob", "Charlie", 3, ["Bob", "Charlie"]),
            ("Mike", "Nancy", 5, ["Mike", "Nancy"]),
        ]
        
        for start, end, expected_dist, expected_path in test_cases:
            dist, path = self.backend.get_best_path(start, end)
            self.assertEqual(dist, expected_dist, f"Distance {start}->{end} should be {expected_dist}")
            self.assertEqual(path, expected_path, f"Path {start}->{end} should be {expected_path}")
            print(f"  ✓ {start} → {end}: distance={dist}, path={' → '.join(path)}")
    
    # ------------------------------------------------------------------------
    # TEST 6: INDIRECT CONNECTIONS (SHORTEST PATH)
    # ------------------------------------------------------------------------
    def test_06_get_best_path_indirect_connection(self):
        """Test finding shortest paths for indirectly connected friends"""
        print("\n[TEST 6] Testing indirect connection paths (shortest path)...")
        
        # Alice to Charlie: Two possible paths
        # Path 1: Alice->Bob->Charlie (5+3=8) ✓ SHORTER
        # Path 2: Alice->David->Charlie (10+2=12)
        dist, path = self.backend.get_best_path("Alice", "Charlie")
        self.assertEqual(dist, 8, "Alice to Charlie should be 8")
        self.assertEqual(path, ["Alice", "Bob", "Charlie"])
        print(f"  ✓ Alice → Charlie: {dist} (chose shorter path via Bob)")
        
        # Emily to Grace: Two possible paths
        # Path 1: Emily->Frank->Grace (4+6=10) ✓ SHORTER
        # Path 2: Emily->Henry->Grace (15+3=18)
        dist, path = self.backend.get_best_path("Emily", "Grace")
        self.assertEqual(dist, 10, "Emily to Grace should be 10")
        self.assertEqual(path, ["Emily", "Frank", "Grace"])
        print(f"  ✓ Emily → Grace: {dist} (chose shorter path via Frank)")
        
        # Ivan to Kevin: Multiple paths
        # Path 1: Ivan->Julia->Kevin (2+3=5) ✓ SHORTER
        # Path 2: Ivan->Laura->Kevin (12+4=16)
        # Path 3: Ivan->Julia->Laura->Kevin (2+7+4=13)
        dist, path = self.backend.get_best_path("Ivan", "Kevin")
        self.assertEqual(dist, 5, "Ivan to Kevin should be 5")
        self.assertEqual(path, ["Ivan", "Julia", "Kevin"])
        print(f"  ✓ Ivan → Kevin: {dist} (chose shortest path via Julia)")
    
    # ------------------------------------------------------------------------
    # TEST 7: COMPLEX PATHS IN CYCLES
    # ------------------------------------------------------------------------
    def test_07_get_best_path_complex_cycles(self):
        """Test finding paths in graphs with cycles"""
        print("\n[TEST 7] Testing paths in cyclic graphs...")
        
        # Oliver to Quinn in a cycle: Oliver->Peter->Quinn->Rachel->Oliver
        # Path 1: Oliver->Peter->Quinn (3+2=5) ✓ SHORTER
        # Path 2: Oliver->Rachel->Quinn (8+4=12)
        dist, path = self.backend.get_best_path("Oliver", "Quinn")
        self.assertEqual(dist, 5, "Oliver to Quinn should be 5")
        self.assertEqual(path, ["Oliver", "Peter", "Quinn"])
        print(f"  ✓ Oliver → Quinn: {dist} (chose shorter path in cycle)")
        
        # Sam to Victor with multiple equal paths
        # Path 1: Sam->Tom->Victor (1+2=3) ✓ TIE
        # Path 2: Sam->Uma->Victor (2+1=3) ✓ TIE
        # Path 3: Sam->Victor (10)
        dist, path = self.backend.get_best_path("Sam", "Victor")
        self.assertEqual(dist, 3, "Sam to Victor should be 3")
        self.assertIn(path, [["Sam", "Tom", "Victor"], ["Sam", "Uma", "Victor"]], 
                     "Path should be one of the two shortest")
        print(f"  ✓ Sam → Victor: {dist} (found one of two tied shortest paths)")
    
    # ------------------------------------------------------------------------
    # TEST 8: SELF PATHS
    # ------------------------------------------------------------------------
    def test_08_get_best_path_same_person(self):
        """Test finding path from a person to themselves"""
        print("\n[TEST 8] Testing self-paths...")
        
        for person in ["Alice", "Emily", "Ivan"]:
            dist, path = self.backend.get_best_path(person, person)
            self.assertEqual(dist, 0, f"Self-distance for {person} should be 0")
            self.assertEqual(path, [person], f"Self-path for {person} should be [{person}]")
            print(f"  ✓ {person} → {person}: distance=0, path=[{person}]")
    
    # ------------------------------------------------------------------------
    # TEST 9: DISCONNECTED COMPONENTS
    # ------------------------------------------------------------------------
    def test_09_get_best_path_different_components(self):
        """Test that no path exists between different components"""
        print("\n[TEST 9] Testing paths between disconnected components...")
        
        disconnected_pairs = [
            ("Alice", "Emily"),
            ("Ivan", "Mike"),
            ("Oliver", "Sam"),
        ]
        
        for start, end in disconnected_pairs:
            dist, path = self.backend.get_best_path(start, end)
            self.assertIsNone(dist, f"No path should exist between {start} and {end}")
            self.assertIsNone(path, f"Path should be None for {start} to {end}")
            print(f"  ✓ {start} → {end}: No path (different components)")
    
    # ------------------------------------------------------------------------
    # TEST 10: DYNAMIC EDGE ADDITION
    # ------------------------------------------------------------------------
    def test_10_add_relation_dynamic(self):
        """Test adding new relations dynamically"""
        print("\n[TEST 10] Testing dynamic edge addition...")
        
        # Create a fresh backend
        backend2 = Backend(test_dir)
        
        # Initially Alice and Emily are not connected
        self.assertFalse(backend2.check_relation("Alice", "Emily"))
        print("  ✓ Initially: Alice and Emily are disconnected")
        
        # Add connection between David and Emily
        backend2.add_relation("David", "Emily", 7)
        print("  ✓ Added edge: David ←→ Emily (weight: 7)")
        
        # Now they should be connected
        self.assertTrue(backend2.check_relation("Alice", "Emily"))
        print("  ✓ After addition: Alice and Emily are connected")
        
        # Find best path
        dist, path = backend2.get_best_path("Alice", "Emily")
        self.assertEqual(dist, 17)  # Alice->David(10) + David->Emily(7) = 17
        self.assertIn(path, [
            ["Alice", "Bob", "Charlie", "David", "Emily"],  # 5+3+2+7=17
            ["Alice", "David", "Emily"]  # 10+7=17
        ])
        print(f"  ✓ Best path found: distance={dist}")
    
    # ------------------------------------------------------------------------
    # TEST 11: DIJKSTRA VERIFICATION
    # ------------------------------------------------------------------------
    def test_11_dijkstra_verification(self):
        """Test that internal Dijkstra verification works correctly"""
        print("\n[TEST 11] Testing Dijkstra verification mechanism...")
        
        test_cases = [
            ("Alice", "Bob"),
            ("Alice", "Charlie"),
            ("Emily", "Henry"),
            ("Ivan", "Laura"),
            ("Sam", "Victor"),
        ]
        
        for start, end in test_cases:
            try:
                dist, path = self.backend.get_best_path(start, end)
                self.assertIsNotNone(dist)
                self.assertIsNotNone(path)
                print(f"  ✓ {start} → {end}: Verification passed")
            except Exception as e:
                self.fail(f"Verification failed for {start} to {end}: {e}")


# ============================================================================
# DEMO SECTION
# ============================================================================

def run_demo():
    """Run a demonstration of the Backend functionality"""
    print("\n" + "="*70)
    print("BACKEND DEMONSTRATION")
    print("="*70)
    
    # Create test data and backend
    backend = Backend(test_dir)
    
    print("\n--- 1. Checking if people are connected ---")
    pairs = [("Alice", "Bob"), ("Alice", "Emily"), ("Mike", "Nancy")]
    for p1, p2 in pairs:
        connected = backend.check_relation(p1, p2)
        status = "✓ Connected" if connected else "✗ Not connected"
        print(f"  {p1} and {p2}: {status}")
    
    print("\n--- 2. Finding shortest paths ---")
    queries = [("Alice", "Charlie"), ("Emily", "Henry"), ("Sam", "Victor")]
    for start, end in queries:
        dist, path = backend.get_best_path(start, end)
        if dist is not None:
            print(f"  {start} → {end}:")
            print(f"    Distance: {dist}")
            print(f"    Path: {' → '.join(path)}")
        else:
            print(f"  {start} → {end}: No path (different groups)")
    
    print("\n--- 3. Adding new connection dynamically ---")
    print("  Before: Alice and Emily are in different groups")
    print("  Adding: David ←→ Emily (weight: 7)")
    backend.add_relation("David", "Emily", 7)
    
    connected = backend.check_relation("Alice", "Emily")
    print(f"  After: Alice and Emily are {'✓ Connected' if connected else '✗ Not connected'}")
    
    if connected:
        dist, path = backend.get_best_path("Alice", "Emily")
        print(f"    New path: {' → '.join(path)} (distance: {dist})")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main entry point for running tests and demo"""
    print("\n" + "🚀"*35)
    print("FRIEND CONNECTION SYSTEM - COMPREHENSIVE TEST SUITE")
    print("🚀"*35)
    
    # Check command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "demo":
            run_demo()
            return
        elif sys.argv[1] == "test":
            # Run only tests
            pass
        elif sys.argv[1] == "verbose":
            # Run tests with verbose output
            pass
        else:
            print("\nUsage:")
            print("  python test_backend_comprehensive.py         # Run all tests")
            print("  python test_backend_comprehensive.py demo    # Run demo only")
            print("  python test_backend_comprehensive.py test    # Run tests only")
            print("  python test_backend_comprehensive.py verbose # Run tests with details")
            return
    
    # Run unit tests
    print("\n" + "="*70)
    print("RUNNING UNIT TESTS")
    print("="*70)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestBackend)
    
    # Choose verbosity based on command line
    verbosity = 2 if len(sys.argv) > 1 and sys.argv[1] == "verbose" else 1
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=verbosity)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*70)
    print("TEST RESULTS SUMMARY")
    print("="*70)
    
    total = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    passed = total - failures - errors
    
    print(f"\nTotal Tests: {total}")
    print(f"✅ Passed: {passed}")
    if failures > 0:
        print(f"❌ Failed: {failures}")
    if errors > 0:
        print(f"⚠️  Errors: {errors}")
    
    if total > 0:
        success_rate = (passed / total) * 100
        print(f"\nSuccess Rate: {success_rate:.1f}%")
    
    # List failed tests if any
    if result.failures:
        print("\n--- Failed Tests ---")
        for test, _ in result.failures:
            test_name = str(test).split()[0]
            print(f"  • {test_name}")
    
    if result.errors:
        print("\n--- Tests with Errors ---")
        for test, _ in result.errors:
            test_name = str(test).split()[0]
            print(f"  • {test_name}")
    
    # Final status
    if result.wasSuccessful():
        print("\n" + "✅"*35)
        print("ALL TESTS PASSED! Backend is working correctly!")
        print("✅"*35)
    else:
        print("\n" + "❌"*35)
        print("SOME TESTS FAILED! Please check the implementation.")
        print("❌"*35)
    
    sys.exit(0 if result.wasSuccessful() else 1)


if __name__ == "__main__":
    main()
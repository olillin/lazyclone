
import unittest
import sys
import os
import tempfile
import subprocess
import shutil

# Ensure src is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from lazyclone.git import clone

class TestIntegrationClone(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for the source repo
        self.source_dir = tempfile.mkdtemp(prefix="lazyclone_src_")
        self.dest_parent_dir = tempfile.mkdtemp(prefix="lazyclone_dest_")
        
        # Initialize a git repo in source_dir
        subprocess.run(["git", "init"], cwd=self.source_dir, check=True, stdout=subprocess.DEVNULL)
        subprocess.run(["git", "config", "user.email", "you@example.com"], cwd=self.source_dir, check=True)
        subprocess.run(["git", "config", "user.name", "Your Name"], cwd=self.source_dir, check=True)
        subprocess.run(["git", "config", "commit.gpgsign", "false"], cwd=self.source_dir, check=True)
        
        # Create a dummy file and commit it
        with open(os.path.join(self.source_dir, "test.txt"), "w") as f:
            f.write("hello world")
        subprocess.run(["git", "add", "."], cwd=self.source_dir, check=True, stdout=subprocess.DEVNULL)
        subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=self.source_dir, check=True, stdout=subprocess.DEVNULL)

    def tearDown(self):
        shutil.rmtree(self.source_dir)
        shutil.rmtree(self.dest_parent_dir)

    def test_clone_local_repo(self):
        # Clone the local repo to a new folder in dest_parent_dir
        # We pass the local path as the URL
        
        # Expected output directory name (default is the folder name of source)
        expected_name = os.path.basename(self.source_dir)
        
        # Perform clone
        clone(self.source_dir, os.path.join(self.dest_parent_dir, "cloned_repo"))
        
        # Verify it cloned
        cloned_path = os.path.join(self.dest_parent_dir, "cloned_repo")
        self.assertTrue(os.path.exists(cloned_path))
        self.assertTrue(os.path.exists(os.path.join(cloned_path, ".git")))
        self.assertTrue(os.path.exists(os.path.join(cloned_path, "test.txt")))
        
        # Verify git log
        result = subprocess.run(["git", "log", "--oneline"], cwd=cloned_path, capture_output=True, text=True)
        self.assertIn("Initial commit", result.stdout)

    def test_clone_with_custom_name(self):
        # Test cloning into a specific directory name
        custom_name = "my_custom_repo"
        target_path = os.path.join(self.dest_parent_dir, custom_name)
        
        # Perform clone
        cloned_name = clone(self.source_dir, target_path)
        
        # Verify return value (git.py logic extracts the path)
        # Note: git.py extraction might return the full path if provided, or relative.
        # Git usually echoes what you typed.
        self.assertIn(custom_name, cloned_name)
        
        # Verify existence
        self.assertTrue(os.path.exists(target_path))
        self.assertTrue(os.path.exists(os.path.join(target_path, "test.txt")))


if __name__ == "__main__":
    unittest.main()

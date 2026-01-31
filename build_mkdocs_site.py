import subprocess
import sys
import os

def run_script(script_name):
    """Run a Python script and handle errors."""
    print(f"\n{'='*60}")
    print(f"Running {script_name}...")
    print(f"{'='*60}\n")
    
    try:
        # Run the script and capture output
        result = subprocess.run(
            [sys.executable, script_name],
            check=True,
            capture_output=True,
            text=True
        )
        
        # Print the script's output
        if result.stdout:
            print(result.stdout)
        
        print(f"\n {script_name} completed successfully")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"\n Error running {script_name}")
        print(f"Error output: {e.stderr}")
        return False
    except FileNotFoundError:
        print(f"\n Script not found: {script_name}")
        return False

def main():
    """Run all build scripts in sequence."""
    print("Starting GHOSTBURN 2325 build process...")

    # List of scripts to run in order
    scripts = [
        '0_delete_folders.py',
        '1_obsidian_copy_to_docs.py',
        '2_obsidian_mkdocs_converter_nocopy_v5.py',
        '3_obsidian_fix_table_links.py',
        '4_obsidian_image_converter.py'
    ]
    
    # Run each script
    for script in scripts:
        success = run_script(script)
        
        # If any script fails, stop the process
        if not success:
            print(f"\n{'='*60}")
            print("Build process FAILED")
            print(f"{'='*60}")
            sys.exit(1)
    
    # All scripts completed successfully
    print(f"\n{'='*60}")
    print("Build process COMPLETED successfully!")
    print("Ready to run: mkdocs serve")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
    # Run mkdocs build
    print("\nBuilding mkdocs site...")
    subprocess.run(["mkdocs", "build"])
    # Run mkdocs serve
    print("\nStarting site...")
    subprocess.run(["mkdocs", "serve"])

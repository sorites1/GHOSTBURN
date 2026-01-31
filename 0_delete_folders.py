import os
import shutil

def delete_folder(folder_path, folder_name):
    """Delete a folder if it exists."""
    if os.path.exists(folder_path):
        try:
            shutil.rmtree(folder_path)
            print(f"Deleted: {folder_name}/")
            return True
        except Exception as e:
            print(f"Error deleting {folder_name}/: {e}")
            return False
    else:
        print(f"  {folder_name}/ does not exist (nothing to delete)")
        return True

def main():
    """Delete site and docs folders from the vault."""
    vault_path = r'C:\GHOSTBURN_2325'
    
    print("="*60)
    print("Cleaning build folders...")
    print("="*60)
    print(f"Vault path: {vault_path}\n")
    
    # Define folder paths
    site_path = os.path.join(vault_path, 'site')
    docs_path = os.path.join(vault_path, 'docs')
    
    # Delete folders
    site_deleted = delete_folder(site_path, 'site')
    docs_deleted = delete_folder(docs_path, 'docs')
    
    print()
    print("="*60)
    if site_deleted and docs_deleted:
        print("Clean complete! Ready for fresh build.")
    else:
        print("Clean completed with errors.")
    print("="*60)

if __name__ == "__main__":
    main()

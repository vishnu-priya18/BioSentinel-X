import os
import zipfile

def create_project_zip():
    base_dir = r"c:\Users\SHANMUGA\Desktop\medicalwaste"
    zip_path = os.path.join(base_dir, "BioSentinel-X-Complete.zip")
    
    ignore_dirs = {"node_modules", ".git", ".pytest_cache", "__pycache__", "venv", ".venv", "dist"}
    ignore_files = {"BioSentinel-X-Complete.zip", ".DS_Store"}
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(base_dir):
            dirs[:] = [d for d in dirs if d not in ignore_dirs]
            for file in files:
                if file in ignore_files or file.endswith('.db') or file.endswith('.pyc'):
                    continue
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, base_dir)
                zipf.write(full_path, rel_path)
                
    print(f"Zip created successfully at: {zip_path}")
    print(f"File size: {os.path.getsize(zip_path)} bytes")

if __name__ == "__main__":
    create_project_zip()

import os
import shutil   

#stat...blic removes public folder, creates new empty one and copies all from static to it
def static_to_public():

    source_dir = 'static'
    dest_dir = 'public'

    #crea...lder creates list of pathes of all the files inside of it based on an input path
    def create_paths_for_elements_in_folder(path):
        paths = []
        for object in os.listdir(path):
            full_path = os.path.join(path, object)
            if os.path.isfile(full_path):
                paths.append(full_path)
            else:
                subdirectory_paths = create_paths_for_elements_in_folder(full_path)
                paths.extend(subdirectory_paths)
        return paths

    if not os.path.exists(source_dir):
        raise Exception("source directory wasn't found")
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    os.mkdir(dest_dir)
    
    for source_path in create_paths_for_elements_in_folder(source_dir):
        rel_path = os.path.relpath(source_path, source_dir)
        dest_path = os.path.join(dest_dir, rel_path)
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        shutil.copy(source_path, dest_path)

    return
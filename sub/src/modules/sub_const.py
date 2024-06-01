import os
import glob

# プロジェクトの相対パス
base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
def get_tmp_dir():
    return os.path.join(base_path, 'tmp')

def tmp_file_name(ext:str):
    tmp_dir = get_tmp_dir()
    os.makedirs(tmp_dir,exist_ok=True)
    files = glob.glob(os.path.join(tmp_dir,'*'))
    return os.path.join(tmp_dir, f"{str(len(files)).zfill(8)}.{ext}")
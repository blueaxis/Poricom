# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files
from PyInstaller.utils.hooks import copy_metadata
import os, torch, glob

datas = []
datas += collect_data_files('unidic_lite')
datas += collect_data_files('manga_ocr')
datas += copy_metadata('tqdm')
datas += copy_metadata('regex')
datas += copy_metadata('sacremoses')
datas += copy_metadata('requests')
datas += copy_metadata('packaging')
datas += copy_metadata('filelock')
datas += copy_metadata('numpy')
datas += copy_metadata('tokenizers')

added_files = [
  ('../../app/assets', './assets'),
  ('../../app/bin', './bin'),
  ('../../app/components', './components')
]

block_cipher = None

a = Analysis(['../../app/main.py'],
             pathex=['../../app'],
             binaries=[],
             datas=datas+added_files,
             hiddenimports= ['stringcase'],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

excluded_binaries  = [
  'libtorch_cpu.so', 
  'libtorch_cuda_cpp.so',
  'libtorch_cuda_cu.so',
  'libtorch_cuda_linalg.so'
]
a.binaries = [x for x in a.binaries if not x[0] in excluded_binaries]

libcudnn_path = os.path.split(torch.__path__[0])[0] + '/nvidia/cudnn/lib'
libcudnn_ops_infer_path = libcudnn_path + '/libcudnn_ops_infer.so.8'
libcudnn_cnn_infer_path = libcudnn_path + '/libcudnn_cnn_infer.so.8'

included_binaries = [
  ('libcudnn_ops_infer.so.8', libcudnn_ops_infer_path,'BINARY'),
  ('libcudnn_cnn_infer.so.8', libcudnn_cnn_infer_path, 'BINARY' )
]

a.binaries = a.binaries + included_binaries

exe = EXE(pyz,
          a.scripts, 
          [],
          exclude_binaries=True,
          name='Poricom',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None,
          icon="poricom.svg")

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas, 
               strip=False,
               upx=True,
               upx_exclude=[],
               name='app')

excluded_files = [
  'libtorch_cuda_linalg.so',
  'libnccl.so.2',
  'libcufft.so.10',
  'libcusparse.so.11'
]

for binary in excluded_files:
    for filePath in glob.glob('**/'+ binary, recursive=True):
        try:
            print("Removing: {}".format(filePath))
            os.remove(filePath)
        except OSError:
            print("Error while deleting: {}".format(filePath))

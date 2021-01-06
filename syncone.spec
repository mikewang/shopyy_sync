# -*- mode: python ; coding: utf-8 -*-
# pyinstaller -D etlyy.spec  打包方法

block_cipher = None
py_files = [
    'SyncOne//Sync_Main.py',
    'SyncOne//Sync_Main.py',
    'SyncOne//Sync_Main.py',
    'SyncOne//Sync_Main.py',
    'SyncOne//global_v.py',
    'SyncOne//Sync_Request_Api.py',
    'SyncOne//Sync_Worker.py',
    'SyncOne//Sync_Write_Erp.py',
    'SyncOne//Sync_Dao.py',
    'SyncOne//Scheduler.py'
]

a = Analysis(py_files,
             pathex=['C:\\Users\\Administrator\\PycharmProjects\\shopyy_sync'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='sync_single_website',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='SyncOne')

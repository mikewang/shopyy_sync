# -*- mode: python ; coding: utf-8 -*-
# pyinstaller -D syncone.spec SyncOne  打包方法 pyinstaller -D syncone.spec SyncOne
# pyinstaller -p C:\Users\Administrator\AppData\Local\Programs\Python\Python37\Lib;C:\Users\Administrator\AppData\Local\Programs\Python\Python37\Lib\site-packages; -D syncone\syncone.spec SyncOne
# pyinstaller -p C:\Users\Administrator\PycharmProjects\untitled\venv\Lib;C:\Users\Administrator\PycharmProjects\untitled\venv\Lib\site-packages; -D syncone\syncone.spec SyncOne


block_cipher = None
py_files = [
    'Sync_Main.py',
    'Sync_Main_Form.py',
    'Spec_Form.py',
    'Dialog_Form.py',
    'global_v.py',
    'Sync_Request_Api.py',
    'Sync_Worker.py',
    'Sync_Write_Erp.py',
    'Sync_Dao.py',
    'Scheduler.py'
]

a = Analysis(py_files,
             pathex=['C:\\Users\\Administrator\\PycharmProjects\\shopyy_sync\\syncone'],
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

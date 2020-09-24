# -*- mode: python ; coding: utf-8 -*-
# pyinstaller -D etlyy.spec  打包方法

block_cipher = None


a = Analysis(['Sync_Main.py','Sync_Main_Form.py','Spec_Form.py','Dialog_Form.py','global_v.py','Sync_Request_Api.py','Sync_Worker.py','Sync_Write_Erp.py','Sync_Dao.py','Scheduler.py'],
             pathex=['C:\\Users\\wfg.langfang\\PycharmProjects\\shopyy_sync'],
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
          name='etlyy',
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
               name='etlyy')

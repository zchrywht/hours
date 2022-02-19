# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['vlc-test.py'],
             pathex=["D:\\GitHub\\hours", "C:\\Users\\zacha\\anaconda3\\envs\\hours\\Lib\\site-packages"],
             binaries=[("C:\\Program Files (x86)\\VideoLAN\\VLC\\libvlc.dll","."),
                ("C:\\Program Files (x86)\\VideoLAN\\VLC\\libvlccore.dll","."),
                ("C:\\Program Files (x86)\\VideoLAN\\VLC\\axvlc.dll","."),
                ("C:\\Program Files (x86)\\VideoLAN\\VLC\\npvlc.dll","."),
                ("C:\\Windows\\SysWOW64\\advapi32.dll","."),
                ("C:\\Windows\\SysWOW64\\kernel32.dll","."),
                ("C:\\Windows\\SysWOW64\\MSVCRT.dll","."),
                ],
             datas=[('./libvlc.dll', '.'), ('./axvlc.dll', '.'), ('./libvlccore.dll', '.'), ('./npvlc.dll', '.')],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

a.datas += Tree("C:\\Program Files (x86)\\VideoLAN\\VLC\\plugins", prefix='plugins')
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts, 
          [],
          exclude_binaries=True,
          name='vlc-test',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas, 
               strip=False,
               upx=True,
               upx_exclude=[],
               name='vlc-test')

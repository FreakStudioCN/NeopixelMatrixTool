# Python env   :               
# -*- coding: utf-8 -*-        
# @Time    : 2025/12/6 下午10:29   
# @Author  : 李清水            
# @File    : temp.py       
# @Description :

import pygame, os, glob
pkg = os.path.dirname(pygame.__file__)
print("pygame package:", pkg)
print("dlls in pygame package:")
for p in glob.glob(os.path.join(pkg, '*.dll')):
    print("  ", p)
# 也检查可能的 pygame.libs 目录
libs_dir = os.path.join(os.path.dirname(pkg), 'pygame.libs')
print("pygame.libs dir exists:", os.path.isdir(libs_dir))
if os.path.isdir(libs_dir):
    for p in glob.glob(os.path.join(libs_dir, '*.dll')):
        print("  pygame.libs:", p)

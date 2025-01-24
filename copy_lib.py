import os
import shutil

lib_path = 'lib_transcendence'
service_path = '../ft_transcendence/srcs/requirements'
services = ['auth', 'chat', 'game', 'matchmaking', 'users']

if not os.path.exists(service_path):
    exit(1)

for service in services:
    dst = f'{service_path}/{service}/django/lib_transcendence'
    if os.path.exists(dst):
        shutil.rmtree(dst)
    print('copy ->', dst)
    shutil.copytree(lib_path, dst)

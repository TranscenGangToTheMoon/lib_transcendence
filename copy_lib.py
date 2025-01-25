import filecmp
import os
import shutil

lib_path = 'lib_transcendence'
service_path = '../ft_transcendence/srcs/requirements'
services = ['auth', 'chat', 'game', 'matchmaking', 'users']

if not os.path.exists(service_path):
    exit(1)


def diff_dir(dir1, dir2):
    diff = filecmp.dircmp(dir1, dir2)

    if diff.diff_files or diff.left_only or diff.right_only:
        exit(1)

    for subdir in diff.subdirs.values():
        diff_dir(os.path.join(dir1, subdir.left), os.path.join(dir2, subdir.right))


dir_ref = f'{service_path}/{services[0]}/django/lib_transcendence'
for service in services[1:]:
    print('checking diff :', services[0], '==', service)
    diff_dir(dir_ref, f'{service_path}/{service}/django/lib_transcendence')


for service in services:
    dst = f'{service_path}/{service}/django/lib_transcendence'
    if os.path.exists(dst):
        shutil.rmtree(dst)
    print('copy ->', dst)
    shutil.copytree(lib_path, dst)

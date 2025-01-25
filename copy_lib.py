import filecmp
import os
import shutil

lib_path = 'lib_transcendence'
service_path = '../ft_transcendence/srcs/requirements'
services = ['auth', 'chat', 'game', 'matchmaking', 'users']
ignore_diff = False


def diff_dir(dir1, dir2):
    diff = filecmp.dircmp(dir1, dir2)

    if diff.diff_files:
        print('diff_files:', diff.diff_files)
        exit(1)

    if diff.left_only:
        print('left_only:', diff.left_only)
        exit(1)

    if diff.right_only:
        print('right_only:', diff.right_only)
        exit(1)

    for subdir in diff.subdirs.values():
        diff_dir(os.path.join(dir1, subdir.left), os.path.join(dir2, subdir.right))


if __name__ == '__main__':

    if not os.path.exists(service_path):
        exit(1)

    if not ignore_diff:
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

#!/usr/bin/python3

import os

def convert_assets():
    os.chdir(path_laravel)

    css_files = sorted([f for f in os.listdir('./public/static/css') if '.map' not in f])
    os.system('rm -rf ./public/static/css/main-style.css')
    os.system('rm -rf ./public/static/js/main-script.js')

    for fname in css_files:
        with open(path_laravel + './public/static/css/' + fname) as f:
            lines = f.readlines()
            lines = [l for l in lines]
            with open(path_laravel + './public/static/css/main-style.css', 'a+') as outfile:
                outfile.writelines(lines)
                outfile.write("\n")



    js_files = sorted([f for f in os.listdir('./public/static/js') if ('.map' not in f and 'runtime' not in f)])

    for fname in js_files:
        with open(path_laravel + './public/static/js/' + fname) as f:
            lines = f.readlines()
            lines = [l for l in lines]
            with open(path_laravel + './public/static/js/main-script.js', 'a+') as outfile:
                outfile.writelines(lines)
                outfile.write("\n")
    
    return True


path_react = '/var/www/html/projects/pakat-react/'
path_laravel = '/var/www/html/projects/pakat/source/'
os.chdir(path_react)

git_pull = 'git pull origin pm'
npm_install = 'npm install'
npm_build = 'npm run build'

rm_static = 'rm -rf ./public/static/ ./public/pakat-icons/ ./public/precache*.js'
cp_built_files = ('yes | cp -rf ./build/* ' + path_laravel + '/public')

git_make_branch = 'git co -b rebuild-ui master'
git_pull_branch = 'git pull origin rebuild-ui'
git_add = 'git add .'
git_commit = 'git ci -am "rebuild ui"'
git_push = 'git push origin rebuild-ui'

response = os.system(git_pull)

if response == 0:
    response = os.system(npm_install)
    response = os.system(npm_build)

    if response == 0:
        os.chdir(path_laravel)
        response = os.system(git_make_branch)
        response = os.system(rm_static)

        os.chdir(path_react)
        response = os.system(cp_built_files)

        if response == 0:
            convert_assets_result = convert_assets()
            if convert_assets_result == True:
                response = os.system(git_add)
                response = os.system(git_commit)
                response = os.system(git_pull_branch)
                response = os.system(git_push)

                print('OK')
                exit(0)

print('NOK')

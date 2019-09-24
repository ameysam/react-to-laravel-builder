#!/usr/bin/python3

import os

projects_path = '/var/www/html/projects/'

react_path = projects_path + 'pakat-react/'
laravel_path = projects_path + 'pakat/source/'

react_branch_name = 'dev'
laravel_branch_name = 'rebuild-ui'

def changeDir(directory_name):
    os.chdir(directory_name)

def push(branch_name):
    return os.system('git push origin {}' . format(branch_name))

def pull(branch_name):
    return os.system('git pull origin {}' . format(branch_name))

def gitMakeBranch(branch_name):
    return os.system('git co -b {} develop' . format(branch_name))

def gitAdd():
    return os.system('git add .')

def gitCommit(message = "rebuild ui"):
    return os.system('git ci -am "{}"' . format(message))

def gitPush(branch_name):
    return os.system('git push origin {}' . format(branch_name))

def removeStaticDir():
    return os.system('rm -rf ./public/static/ ./public/pakat-icons/ ./public/precache*.js')

def copyBuiltFiles():
    return os.system('yes | cp -rf ./build/* ' + laravel_path + '/public')

def buildReactApp():
    npm_install = 'npm install'
    npm_build = 'npm run build'
    os.system(npm_install)
    return os.system(npm_build)

def convert_assets():
    os.chdir(laravel_path)

    css_files = sorted([f for f in os.listdir('./public/static/css') if '.map' not in f])
    os.system('rm -rf ./public/static/css/main-style.css')
    os.system('rm -rf ./public/static/js/main-script.js')

    for fname in css_files:
        with open(laravel_path + './public/static/css/' + fname) as f:
            lines = f.readlines()
            lines = [l for l in lines]
            with open(laravel_path + './public/static/css/main-style.css', 'a+') as outfile:
                outfile.writelines(lines)
                outfile.write("\n")


    js_files = sorted([f for f in os.listdir('./public/static/js') if ('.map' not in f and 'runtime' not in f)])

    for fname in js_files:
        with open(laravel_path + './public/static/js/' + fname) as f:
            lines = f.readlines()
            lines = [l for l in lines]
            with open(laravel_path + './public/static/js/main-script.js', 'a+') as outfile:
                outfile.writelines(lines)
                outfile.write("\n")
    
    return True

if __name__ == "__main__":
    changeDir(react_path) #change dir to react project direction
    pull(react_branch_name) # pull from pm branch
    response = buildReactApp() # build react app

    if response == 0:
        changeDir(laravel_path)
        gitMakeBranch(laravel_branch_name)
        removeStaticDir()

        changeDir(react_path)
        response = copyBuiltFiles()

        if response == 0:
            convert_assets_result = convert_assets()
            if convert_assets_result == True:
                gitAdd()
                gitCommit()
                gitPush(laravel_branch_name)
                
                print('OK')
                exit(0)

print('NOK')



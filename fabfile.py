from fabric.api import *
import os
 
env.hosts = ['virantha@96.8.112.217']
  
def get_dep():
    # Get all the local ember.js dependencies
    js_lib_path = "site/js/lib"
    js_libs = { 'jquery.js': "http://code.jquery.com/jquery-1.9.1.js",
                #'handlebars.js': 'https://raw.github.com/wycats/handlebars.js/1.0.0/dist/handlebars.runtime.js',
                'handlebars.js': 'https://raw.github.com/wycats/handlebars.js/1.0.0/dist/handlebars.js',
                'ember.js': 'http://builds.emberjs.com.s3.amazonaws.com/ember-latest.js',
                'ember-data.js': 'http://builds.emberjs.com.s3.amazonaws.com/ember-data-latest.js',
                }
    if not os.path.exists(js_lib_path):
        os.makedirs(js_lib_path)
    
    for tgt, wgetaddr in js_libs.items():
        # Fetch all the libs
        local("wget -O %s %s" % (os.path.join(js_lib_path,tgt), wgetaddr))

def copy():
    # make sure the directory is there!
    #run('mkdir -p /home/userX/mynewfolder')
               
    # our local 'localdirectory' (it may contain files or subdirectories)
    put('site', '/home/virantha/www_kittens')
    with cd('/home/virantha/www_kittens/go/'):
        run('go get github.com/gorilla/mux')
        #run('mkdir src/github.com/virantha')
    put('go/src/github.com/virantha/server.go', '/home/virantha/www_kittens/go/src/github.com/virantha')

def build():
    with cd('/home/virantha/www_kittens/go/src/github.com/virantha'):
        run('ls')
        run('go build server.go')
        #run('nohup ./wiki >& /dev/null < /dev/null &',pty=False)

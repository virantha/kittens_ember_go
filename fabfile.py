from fabric.api import *
import os
 
env.hosts = ['virantha@96.8.112.217']
  
def get_dependencies():
    # Get all the local ember.js dependencies
    js_lib_path = "site/js/lib"
    js_libs = { 'jquery.js': "http://code.jquery.com/jquery-2.0.0.js",
                'handlebars.js': 'https://raw.github.com/wycats/handlebars.js/1.0.0-rc.4/dist/handlebars.js',
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
    put('site', '/home/virantha/www_test_wiki')
    run('cd /home/virantha/www_test_wiki/site')
    run('go build wiki.go')
    run('nohup ./wiki &')

def build():
    with cd('/home/virantha/www_test_wiki/site'):
        run('ls')
        run('go build wiki.go')
        run('nohup ./wiki >& /dev/null < /dev/null &',pty=False)

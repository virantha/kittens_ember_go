from fabric.api import *
 
env.hosts = ['virantha@96.8.112.217']
  
def get_dependencies():
    # Get all the local ember.js dependencies
    js_lib_path = "site/js/lib"
    if not os.path.exists(js_lib_path):
        os.makedirs(js_lib_path)
    local("wget -O site/js/lib/jquery.js http://code.jquery.com/jquery-2.0.0.js")
    local("wget -O site/js/lib/handlebars.js https://raw.github.com/wycats/handlebars.js/1.0.0-rc.4/dist/handlebars.js")
    local("wget -O site/js/lib/ember.js http://builds.emberjs.com.s3.amazonaws.com/ember-latest.js")
    local("wget -O site/js/lib/ember-data.js http://builds.emberjs.com.s3.amazonaws.com/ember-data-latest.js")

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

import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import sys
import subprocess

IGNORE_LIST = ["/.git/"]

class Watcher:

    def __init__(self, localdir, remotedir, ip, user, key):
        self.observer = Observer()
        self.remotedir = remotedir
        self.localdir = localdir
        self.ip = ip
        self.user = user
        self.key = key
        self.ssh_at = str(self.user)+"@"+str(self.ip)

    def run(self):
        print(" Starting watch and sync on directory - "+str(self.localdir)+" .............")
        event_handler = Handler(self.localdir, self.remotedir, self.ssh_at, self.key)
        self.observer.schedule(event_handler, self.localdir, recursive=True)
        self.observer.start()
        event_handler.handler_add_permission(self.user)
        try:
            while True:
                time.sleep(2)
        except:
            self.observer.stop()
            print ("Error")

        self.observer.join()


class Handler(FileSystemEventHandler):

    localdir = ""
    remotedir = ""
    ssh_at = ""
    key = ""
    keyfile = ""


    def __init__(self, ldir, rdir, sshat, key):
        Handler.localdir = ldir
        Handler.remotedir = rdir
        Handler.ssh_at = sshat
        Handler.key = ""
        Handler.keyfile = ""
        if key not in ["",None,0]:
            Handler.key = "-i "+str(key)
            Handler.keyfile = str(key)


    @staticmethod
    def on_any_event(event):

        if event.is_directory:
            #print ("new folder - %s" % event.src_path)
            return None

        elif event.event_type == 'created':
            # Take any action here when a file is first created.
            #print ("Received created event - %s" % event.src_path)
            Handler.handle_create_mod_event(event.src_path)

        elif event.event_type == 'modified':
            # Taken any action here when a file is modified.
            #print ("Received modified event - %s" % event.src_path)
            Handler.handle_create_mod_event(event.src_path)

        elif event.event_type == 'deleted':
            #print ("Received deleted event - %s" % event.src_path)
            Handler.handle_deleted_event(event.src_path)

    @staticmethod
    def handle_create_mod_event(src_path):
        if not Handler.is_valid_file(src_path):
            return

        remote_path_full = Handler.get_remote_path(src_path)
        bash_command = "scp "+str(Handler.key)+" "+str(src_path)+" "+str(Handler.ssh_at)+":"+str(remote_path_full)
        print ("Executing create/modify - "+bash_command)
        Handler.run_bash(bash_command)

    def handler_add_permission(self, user):
        Handler.remotedir
        Handler.ssh_at
        Handler.key
        bash_command = "/Users/shrishmarnad/Documents/workspace/test_python/folder_watcher/chown_remote.sh "+str(Handler.ssh_at)+" "+str(Handler.remotedir)+" "+str(user)+" "+str(Handler.keyfile)
        print ("Executing chown permission command - "+bash_command)
        Handler.run_bash(bash_command)

    def handle_deleted_event(src_path):
        if not Handler.is_valid_file(src_path):
            return

        remote_path_full = Handler.get_remote_path(src_path)
        bash_command = "/Users/shrishmarnad/Documents/workspace/test_python/folder_watcher/rm_remote.sh "+str(Handler.ssh_at)+" "+str(remote_path_full)+" "+str(Handler.key)
        print ("Executing delete - "+bash_command)
        Handler.run_bash(bash_command)

    @staticmethod
    def get_remote_path(src_path):
        local_path_rel = src_path.split(Handler.localdir)[1]
        remote_path_full = Handler.remotedir + str(local_path_rel)
        return remote_path_full

    @staticmethod
    def run_bash(bash_command):
        process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        if output and output != "":
            print (output)
        if error and error != "":
            print (error)
        else:
            print ("Successfully executed !!...")

    @staticmethod
    def is_valid_file(src_path):
        global IGNORE_LIST
        for filename in IGNORE_LIST:
            if filename in src_path:
                print ("Not valid file - "+str(src_path)+", contains - "+str(filename))
                return False
        return True

def print_help():
    print ("Args Error: usage : python3.6 folder_watch_scp.py <user> <ip> <localdir> <remotedir> <optional:path_to_pem_file>")

def main():
    if (len(sys.argv) < 5) or (len(sys.argv) > 6):
        print_help()
        return
    user = sys.argv[1]
    ip = sys.argv[2]
    localdir = sys.argv[3]
    remotedir = sys.argv[4]
    key = ""
    if len(sys.argv) == 6:
        key = sys.argv[5]

    w = Watcher(localdir, remotedir, ip, user, key)
    w.run()

main()

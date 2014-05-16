"""Copyright 2014 Cyrus Dasadia

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import subprocess
import time
from django.conf import settings


class RunPlugin:
    """
    Can accept a single command or a list of commands.
    Each command has to be in form of a list
    e.g. RunPlugin.execute(['/bin/ls', '--color'])
    """
    def __init__(self):
        self.current_working_dir = '/tmp'
        self.timeout = settings.PLUGIN_RUNNER_CONFIG['timeout']
        self.running_procs = dict()

    def log_error(self, msg):
        print "Error executing: %s error" % msg

    def log_success(self, msg):
        print msg

    def remove_process(self, proc):
        del self.running_procs[proc]

    def execute(self, commands):
        if commands is None:
            return False
        for cmd in commands:
            try:
                p = subprocess.Popen(cmd, cwd=self.current_working_dir,
                                     stderr=subprocess.PIPE,
                                     stdout=subprocess.PIPE)
                self.running_procs[p] = time.time()
            except BaseException, e:
                return unicode("Error: Could not execute %s, exception %s" % (cmd, e))

        while len(self.running_procs.keys()) > 0:
            for proc in self.running_procs.keys():
                process_time = self.running_procs[proc]
                return_code = proc.poll()
                if return_code is None:
                    if time.time() - process_time > self.timeout:
                        proc.kill()
                        self.remove_process(proc)
                        return unicode("Error: Process killed, exceeded timeout of %s seconds" % self.timeout)
                else:
                    if return_code == 0:
                        return_text = proc.stdout.readlines()
                    else:
                        return_text = proc.stderr.readlines()
                    self.remove_process(proc)
                    return unicode("Done: returnCode[%s], returnText[%s]" % (return_code, return_text))

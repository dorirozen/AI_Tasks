import subprocess

class Terminal(object):

    def __init__(self):
        self.responds = []

    def send(self, command):
        try:
            # Run the command and capture the output and errors
            result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    text=True)

            self.responds.append((result.stdout, result.stderr))
            return result.stdout, result.stderr
        except subprocess.CalledProcessError as e:
            # Return the error if the command fails
            return e.stdout, e.stderr

    def respond(self):
        return self.responds[-1]
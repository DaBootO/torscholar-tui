import subprocess
import sys

def torCheck():
    process = subprocess.Popen('curl --socks5 localhost:9050 --socks5-hostname localhost:9050 -s https://check.torproject.org/ | cat | grep -m 1 Congratulations | xargs', shell=True, stdout=subprocess.PIPE)
    lines = []
    # Poll process for new output until finished
    while True:
        nextline = process.stdout.readline()
        if nextline.decode() == '' and process.poll()  is not None:
            break

        lines.append(nextline.decode().rstrip())
        # sys.stdout.write(nextline.decode())
        # sys.stdout.flush()

    exitCode = process.returncode

    if (exitCode == 0):
        if "Congratulations. This browser is configured to use Tor." in lines:
            return True
        else:
            return False
    else:
        raise subprocess.CalledProcessError(exitCode)

if __name__ == '__main__':
    if torCheck():
        print("You are correctly connected to the tor network!")
    else:
        print("You are NOT connected to the tor network! Please start the tor service! e.g. sudo service tor start")
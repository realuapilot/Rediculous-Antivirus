import hashlib
import os
import datetime
import sys
import ctypes
import time
from playsound import playsound

# d41d8cd98f00b204e9800998ecf8427e  zero byte file


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        print("error on figuring out if the installer is admin!")
        return False

if is_admin():
    print ('argument list', sys.argv)
    scanpath = sys.argv[1]
    try:
        os.remove("threatsexe.txt")
        os.remove("threats.txt")
    except:
        print("Threat history files not found. No need to delete them")
    
    
    # scan history
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    history = f"[{timestamp}] Scanned in {scanpath}\n"
    with open("scanhistory.txt", 'a') as thrt:
        thrt.write(history)
        thrt.close()
    
    
    basesoutdated = 0
    if basesoutdated == 1:
        print("bases are outdated!")
        time.sleep(2)
    print("Scanning! please wait. All detected threats will show below")
    
    def load_malware_hashes(filename):
        """Loads malware hashes from a text file"""
        try:
            with open(filename, 'r') as file:
                return {line.strip() for line in file if line.strip()}
        except Exception as e:
            print(f"Error loading malware bases: {e} make sure bases are updated")
            return set()
    
    def scan_file(filepath, malware_hashes, filename):
        """Scans a file and checks if its hash is in the malware list"""
        try:
            with open(filepath, 'rb') as file:
                #print(f"Scanning {filepath}")
                with open("scanneddirs.txt", 'a') as scandirs:
                    scandirs.write(filepath)
                    scandirs.close()
                #print(filepath)
                file_data = file.read()
                file_hash = hashlib.md5(file_data).hexdigest()
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"[{timestamp}] Scanning: {filepath} (Hash: {file_hash})\n")
                if file_hash in malware_hashes:
                    with open("debug.txt", 'a') as debug:
                        debug.write(f"[{timestamp}] Threat detected: {filepath} (Hash: {file_hash})\n")
                        debug.close()
                    print(f"[{timestamp}] Threat detected: {filepath} (Hash: {file_hash})")
                    playsound('beep.wav')
                    with open("threats.txt", 'a') as thrt:
                        thrt.write(filepath + "\n")
                        thrt.close()
                    with open("threatsexe.txt", 'a') as thrtexe:
                        thrtexe.write(filename + "\n")
                        thrtexe.close()
                else:
                    clean = 1
        except Exception as e:
            print(f"Error scanning {filepath}: {e}")
    
    def scan_directory(directory, malware_hashes):
        """Scans all files in a directory"""
        for root, dirs, files in os.walk(directory):
            for file in files:
                filepath = os.path.join(root, file)
                scan_file(filepath, malware_hashes, file)
    
    
    hash_file = "bases.txt" 
    malware_hashes = load_malware_hashes(hash_file)
    directory_to_scan = scanpath
    scan_directory(directory_to_scan, malware_hashes)
    time.sleep(2)
    print("Scan finished")
    time.sleep(4)

else:
    # Didnt run as admin, Ask for admin and rerun
    print("Inorder to scan. Need admin! please accept!")
    time.sleep(3)
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
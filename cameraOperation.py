import subprocess
# sudo apt-get install gphoto2
def kill_gphoto_conflicts():
    for proc in ("gvfs-gphoto2-volume-monitor", "gvfsd-gphoto2"):
        subprocess.run(["pkill", "-f", proc], stderr=subprocess.DEVNULL)

def find_camera_port():
    # get the camera's port to be fed into capture_photo's gphoto2 command
    result = subprocess.run(
        ["gphoto2", "--auto-detect"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    #parse out useless stuff
    lines = result.stdout.strip().splitlines()
    for line in lines[2:]:
        parts = line.strip().split()
        if len(parts) >= 2:
            # Port is the last part
            print(parts[-1])
            return parts[-1]
    raise Exception("Can't find port. Either add as a constant or re-run script.")

from typing import Optional

def capture_photo(filename: str, port: Optional[str] = None):
    kill_gphoto_conflicts()
    cmd = ["gphoto2"]
    if port:
        cmd += ["--port", port]
        
    # --debug is just for now. remove once tool works perfectly
    cmd += ["--capture-image-and-download", "--filename", filename]
    
    # Sometimes get an 'I/O in progress' error. So the for loop will just keep retrying.
    # NO IDEA IF IM CURSED, BUT IF SUBJECT IS CLOSE TO THE CAMERA (0-5CM) THE CAMERA WILL THROW:
    #     *** Error ***              
    # Canon EOS Full-Press failed (0x2019: PTP Device Busy)
    # ERROR: Could not capture image.
    # ERROR: Could not capture.
    # *** Error (-110: 'I/O in progress') ***   
    # idk why
    subprocess.run(cmd, check=True)

if __name__ == "__main__":
    filename = "photo_test.jpg"
    # # explicitly pass camera’s port. Comment out the find camera `port function call if so.
    # port = "usb:003,022"
    capture_photo(filename, find_camera_port())
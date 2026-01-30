# LOLBins misuse rules for detection are used , for reference its here.

def detect_lolbins(event):
    suspicious = []

    name = event["name"].lower()
    cmd = " ".join(event["cmd"]).lower()

    if name == "powershell.exe" and ("-enc" in cmd or "-encodedcommand" in cmd):
        suspicious.append("Encoded Powershell")

    if name == "cmd.exe" and "/c" in cmd:
        suspicious.append("CMD command execution")

    if name == "certutil.exe":
        suspicious.append("Certutil abuse")

    return suspicious

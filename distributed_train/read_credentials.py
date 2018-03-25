def readCredentials(filename):
    with open(filename, 'r') as f:
        SSH = f.readline().strip()
        SCP = f.readline().strip()
        return SSH, SCP

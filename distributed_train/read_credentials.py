def readCredentials(filename):
    servers = []
    with open(filename, 'r') as f:
        for line in f:
            row = line.strip().split(',')
            server, user, passwd = row
            servers.append([server, user, passwd])
    return servers

def ssh(server, user, passwd):
    return "sshpass -p {} ssh -q -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no {}@{}".format(passwd, user, server)

def scp(server, user, passwd, local_files, dest, reverse=False, recursive=False):
    if not reverse:
        if not recursive:
            return "sshpass -p {} scp -q -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no {} {}@{}:{}".format(passwd, local_files, user, server, dest)
        return "sshpass -p {} scp -q -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -r {} {}@{}:{}".format(passwd, local_files, user, server, dest)
    else:
        if not recursive:
            return "sshpass -p {} scp -q -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no {}@{}:{} {}".format(passwd, user, server, dest, local_files)
        return "sshpass -p {} scp -q -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -r {}@{}:{} {}".format(passwd, user, server, dest, local_files)


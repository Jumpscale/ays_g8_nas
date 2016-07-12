from JumpScale import j


class Actions(ActionsBaseMgmt):

    def install(self, service):
        cuisine = service.executor.cuisine
        cuisine.package.install('samba')

        cuisine.group.ensure('sambausers')
        users = list()
        for user in service.producers.get('user', []):
            cuisine.group.user_ensure('sambausers', user.instance)
            cuisine.core.run('echo -e "{passwd}\n{passwd}" | smbpasswd -a -s {user}'.format(user=user.instance, passwd=user.hrd.get('password')))
            users.append(user.instance)

        location = service.parent.hrd.get('location')
        cuisine.core.dir_attribs(location, '775', group='sambausers')

        ### configure Samba
        cuisine.core.file_download_local('/etc/samba/smb.conf', '/tmp/smb.conf')

        smb = j.tools.inifile.open('/tmp/smb.conf')
        section = j.sal.fs.getBaseName(location)
        smb.addSection(section)
        smb.addParam(section, 'path', location)
        smb.addParam(section, 'valid users', ' '.join(users))
        smb.addParam(section, 'read only', 'no')
        smb.write('/tmp/smb.conf')

        cuisine.core.file_upload_local('/tmp/smb.conf', '/etc/samba/smb.conf')
        cuisine.core.run('service smbd restart')

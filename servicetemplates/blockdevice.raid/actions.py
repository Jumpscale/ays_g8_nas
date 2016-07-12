from JumpScale import j


class Actions(ActionsBaseMgmt):

    def install(self, service):
        disks = service.hrd.getList('disks')
        node_disks = service.parent.parent.hrd.getList('datadisks')
        node_disks = [j.data.tags.getObject(disk) for disk in node_disks]

        data_disks = list()
        for disk in disks:
            for index, d in enumerate(node_disks):
                if disk == d.tagGet('name'):
                    data_disks.append('/dev/vd' + chr(ord('b') + index))  # to get disk name

        cuisine = service.executor.cuisine
        cuisine.core.run('DEBIAN_FRONTEND=noninteractive apt-get install mdadm -y', die=False)

        # create raid array
        cuisine.core.run('mdadm --create /dev/md0 --level=raid%i --raid-devices=%s %s' % (service.hrd.getInt('raid'), len(data_disks),
                         ' '.join(data_disks)))

        # persist raid aray
        cuisine.core.run('mdadm --detail --scan >> /etc/mdadm/mdadm.conf')
        cuisine.core.run('update-initramfs -c -k `uname -r`')
        cuisine.core.run('update-grub')

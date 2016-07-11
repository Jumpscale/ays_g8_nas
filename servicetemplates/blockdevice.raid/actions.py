from JumpScale import j


class Actions(ActionsBaseMgmt):

    def install(self, service):
        disks = service.hrd.getList('disks')
        node_disks = service.parent.hrd.getList('datadisks')
        node_disks = [j.data.tags.getObject(disk) for disk in node_disks]

        data_disks = list()
        for disk in disks:
            for index, d in enumerate(node_disks):
                if disk == d.tagGet('name'):
                    data_disks.append('/dev/vd' + chr(ord('b') + index))  # to get disk name

        cuisine = service.executor.cuisine
        cuisine.core.run('apt-get install mdadm', die=False)
        cuisine.core.run('mdadm -C /dev/md0 --level=raid%i --raid-devices=4 %s' % (service.hrd.getInt('raid'), ' '.join(data_disks)))

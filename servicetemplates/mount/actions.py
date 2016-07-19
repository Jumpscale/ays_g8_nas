from JumpScale import j


class Actions(ActionsBaseMgmt):

    def install(self, service):
        target = service.hrd.getStr('location')
        filesystem = service.hrd.getStr('filesystem')
        options = service.hrd.getStr('options')
        options = '-o %s' % options if options else ''
        service.executor.cuisine.core.dir_ensure(target)
        code, _, _ = service.executor.cuisine.core.run('fsck -M /dev/md0', die=False)
        if code:
            service.executor.cuisine.core.run('mkfs.%s /dev/md0' % filesystem)
        service.executor.cuisine.core.run('mount -t %s %s /dev/md0 %s ' % (filesystem, options, target))

from JumpScale import j


class Actions(ActionsBaseMgmt):

    def install(self, service):
        target = service.hrd.getStr('location')
        filesystem = service.hrd.getStr('filesystem')
        options = service.hrd.getStr('options')
        service.executor.cuisine.core.dir_ensure(target)
        service.executor.cuisine.core.run('mount /dev/md0 %s -t %s' % (target, filesystem, options))

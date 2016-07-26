from JumpScale import j


class Actions(ActionsBaseMgmt):

    def install(self, service):
        service.executor.cuisine.user.ensure(service.instance, service.hrd.getStr('password'), encrypted_passwd=False)

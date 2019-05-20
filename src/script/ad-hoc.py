# coding=utf-8
from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from collections import namedtuple
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from options import options

"""
TaskQueueManager:
    资源资产清单：
        InventoryManager
        VariableManager

    执行选项：
        Options

    执行对象和模块：
        Play

"""


def main():

    loader = DataLoader()
    # sources 为hosts文件数组
    inv = InventoryManager(loader=loader, sources=['../../ansible_etc/hosts'])
    varivaleManager = VariableManager(loader=loader, inventory=inv)

    # {action={'module': 'shell', 'args': 'echo hello'})}
    play_source = dict(name="Ansible Play ad-hoc test", hosts='192.168.1.55', gather_facts='no',
                       tasks=[
                           dict(action=dict(module='shell', args='echo1 hello')),
                       ])

    play = Play().load(data=play_source, variable_manager=varivaleManager, loader=loader)

    password = dict()
    # inventory, variable_manager, loader, options, passwords, stdout_callback=None, run_additional_callbacks=True, run_tree=False
    tqm = TaskQueueManager(inv, varivaleManager, loader, options, password)
    # res=0 代表正常结束 res=2代表异常结束
    res = tqm.run(play)
    print res
    pass


if __name__ == '__main__':
    main()

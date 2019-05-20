# coding=utf-8
from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader
from ansible.plugins.callback import CallbackBase
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


class ModelResultCollector(CallbackBase):

    def __init__(self):
        super(ModelResultCollector, self).__init__()
        self.host_ok = {}
        self.host_unreachable = {}
        self.host_failed = {}

    def v2_runner_on_failed(self, result, ignore_errors=False):
        # result: TaskResult
        # TaskResult._result储存执行结果
        self.host_failed[result._host] = result._result

    def v2_runner_on_ok(self, result):
        self.host_ok[result._host] = result._result

    def v2_runner_on_unreachable(self, result):
        self.host_unreachable[result._host] = result._result


def main():

    callback = ModelResultCollector()

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
    tqm = TaskQueueManager(inv, varivaleManager, loader, options, password, stdout_callback=callback)
    # res=0 代表正常结束 res=2代表异常结束
    res = tqm.run(play)
    print callback.host_failed
    print callback.host_ok
    print callback.host_unreachable


if __name__ == '__main__':
    main()

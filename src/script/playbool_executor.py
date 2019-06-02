# coding=utf-8
import json

from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader
from ansible.plugins.callback import CallbackBase
from ansible.vars.manager import VariableManager
from collections import namedtuple
from ansible.executor.task_queue_manager import TaskQueueManager
from collections import OrderedDict
from src.script.options import options


# noinspection PyProtectedMember
class PlaybookCallback(CallbackBase):

    def __init__(self):
        super(PlaybookCallback, self).__init__()
        self.host_ok = {}
        self.host_unreachable = {}
        self.host_failed = {}

    def playbook_on_start(self):
        # 首先执行
        pass

    def playbook_on_stats(self, stats):
        # 结束时调用,无论成功或者失败
        print('stats', type(stats))

    def v2_runner_on_failed(self, result, ignore_errors=False):
        # 异步执行失败也调用这里
        name = result._host.get_name()
        if name not in self.host_failed:
            self.host_failed[name] = OrderedDict()
        self.host_failed[name][result.task_name] = result._result

    def v2_runner_on_ok(self, result):
        """
        result: TaskResult
            _host:
            _task: Task
            _result: dict
            _task_field
            task_name: Unicode
        1. 任务超时后不会继续往下执行，并且结果中不存在rc， 任务执行成功rc为0，超时针对的时当前步骤
        2. name只会显示步骤名称不会显示include名称
        3. 多台主机只要有一台中间执行失败就会都执行失败
        """
        name = result._host.get_name()
        if name not in self.host_ok:
            self.host_ok[name] = OrderedDict()
        self.host_ok[name][result.task_name] = result._result

    def v2_runner_on_unreachable(self, result):

        name = result._host.get_name()
        if name not in self.host_unreachable:
            self.host_unreachable[name] = OrderedDict()
        self.host_unreachable[name][result.task_name] = result._result


# noinspection PyProtectedMember
def main():
    loader = DataLoader()
    # sources 为hosts文件数组
    inv = InventoryManager(loader=loader, sources=['../../ansible_etc/hosts'])
    varivaleManager = VariableManager(loader=loader, inventory=inv)
    # playbooks, inventory, variable_manager, loader, options, passwords
    playbook = PlaybookExecutor(playbooks=['../../ansible_etc/test.yml'], inventory=inv,
                                variable_manager=varivaleManager, loader=loader, options=options, passwords=dict())
    callback = PlaybookCallback()
    playbook._tqm._stdout_callback = callback
    playbook.run()
    print(callback.host_ok)
    print(json.dumps(callback.host_ok, indent=2))


if __name__ == '__main__':
    main()

# coding=utf-8
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader
from ansible.plugins.callback import CallbackBase
from ansible.vars.manager import VariableManager
from collections import namedtuple
from ansible.executor.task_queue_manager import TaskQueueManager
from options import options


def main():
    loader = DataLoader()
    # sources 为hosts文件数组
    inv = InventoryManager(loader=loader, sources=['../../ansible_etc/hosts'])
    varivaleManager = VariableManager(loader=loader, inventory=inv)
    # playbooks, inventory, variable_manager, loader, options, passwords
    playbook = PlaybookExecutor(playbooks=['../../ansible_etc/test.yml'], inventory=inv,
                     variable_manager=varivaleManager, loader=loader, options=options,
                     passwords=dict())
    playbook.run()


if __name__ == '__main__':
    main()
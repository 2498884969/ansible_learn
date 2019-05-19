from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader


def main():
    loader = DataLoader()
    inv = InventoryManager(loader=loader, sources=['./ansible_etc/hosts'])

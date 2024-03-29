# In The Name Of God
# ========================================
# [] File Name : plugin.py
#
# [] Creation Date : 29-09-2016
#
# [] Created By : Parham Alvani (parham.alvani@gmail.com)
# =======================================
from .base import I1820Controller
from ..plugins.base import Plugins

import uuid
import threading
import asyncio
import logging

logger = logging.getLogger(__name__)


class PluginController(I1820Controller, threading.Thread):
    def __init__(self):
        super().__init__()

        self.lock = threading.Lock()
        self.chains = {}
        self.plugins = {}

        self.loop = asyncio.new_event_loop()

        self.daemon = True
        self.start()

    def run(self):
        self.loop.call_soon(logger.info, 'Event loop started :?')
        self.loop.run_forever()

    def _on_log_chain(self, log, root):
        while root is not None:
            r = root.on_log(log)
            if r:
                root = root.right
            else:
                root = root.left

    def on_log(self, log):
        with self.lock:
            for chain_id, root in self.chains.items():
                threading.Thread(name=chain_id,
                                 target=self._on_log_chain,
                                 args=(log, root, )).start()

    def new_plugin(self, name: str, chain: int, parent: str, args: dict):
        '''
        Creates new plugin

        :param parent: plugin parent that can be root or uuid:branch.
        :type parent: str
        '''

        plugin = Plugins.get(name)
        ident = uuid.uuid4()
        p = plugin(ident, **args)

        # Store newly created plugin
        with self.lock:
            self.plugins[str(ident)] = p

            if parent == 'root':
                self.chains[chain] = p
            else:
                parent, branch = parent.split(':')
                if branch == 'true':
                    self.plugins[parent].right = p
                else:
                    self.plugins[parent].left = p

        return p.ident

    def _chain_iterator(self, root):
        i = root
        if i is None:
            return []
        else:
            left = self._chain_iterator(i.left)
            right = self._chain_iterator(i.right)
            return [i] + left + right

    def list_plugin(self):
        results = {}

        with self.lock:
            for chain_id, root in self.chains.items():
                results[chain_id] = []
                for i in self._chain_iterator(root):
                    result = {}
                    result['id'] = str(i.ident)
                    result['name'] = i.name
                    result['left'] = str(i.left.ident) if i.left \
                        is not None else ''
                    result['right'] = str(i.right.ident) if i.right \
                        is not None else ''
                    results[chain_id].append(result)

        return results

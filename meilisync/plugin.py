import importlib

from loguru import logger

from meilisync.schemas import Event


class Plugin:
    is_global = False

    async def pre_event(self, event: Event): 
        logger.debug(f"pre_event: {event}, is_global: {self.is_global}")
        return event

    async def post_event(self, event: Event):
        logger.debug(f"post_event: {event}, is_global: {self.is_global}")
        return event

class SnakeToCamelCasePlugin(Plugin):
    is_global = False

    def _snake_to_camel(self, snake_str: str) -> str:
        components = snake_str.split('_')
        return components[0] + ''.join(x.title() for x in components[1:])

    async def pre_event(self, event):
        if isinstance(event, dict):
            event = {self._snake_to_camel(k): v for k, v in event.items()}
        elif hasattr(event, "__dict__"):
            for attr in list(event.__dict__):
                new_attr = self._snake_to_camel(attr)
                if new_attr != attr:
                    event.__dict__[new_attr] = event.__dict__.pop(attr)
        return event

    async def post_event(self, event):
        # No conversion needed post event
        return event   


def load_plugin(module_str: str):
    module, _, class_name = module_str.rpartition(".")
    return getattr(importlib.import_module(module), class_name)
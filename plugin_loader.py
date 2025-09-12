from __future__ import annotations

import importlib.util
import inspect
import logging
from pathlib import Path
from types import ModuleType
from typing import Any, Dict


class PluginLoader:
    """Load and execute plugins from a directory."""

    def __init__(self, path: str | Path = "plugins") -> None:
        self.path = Path(path)
        self.log = logging.getLogger(__name__)
        self.plugins: Dict[str, ModuleType] = {}
        self._load_plugins()

    def _load_plugins(self) -> None:
        """Scan the plugins directory and import plugins."""
        if not self.path.exists():
            self.log.warning("Plugin directory %s does not exist", self.path)
            return

        for file in self.path.glob("*.py"):
            if file.name == "__init__.py":
                continue
            try:
                spec = importlib.util.spec_from_file_location(file.stem, file)
                if spec is None or spec.loader is None:
                    raise ImportError(f"Could not load spec for {file}")
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                name = getattr(module, "NAME", None)
                description = getattr(module, "DESCRIPTION", None)
                execute = getattr(module, "execute", None)

                if not isinstance(name, str):
                    raise AttributeError("Plugin missing NAME")
                if not isinstance(description, str):
                    raise AttributeError("Plugin missing DESCRIPTION")
                if not inspect.iscoroutinefunction(execute):
                    raise AttributeError("Plugin missing async execute")

                self.plugins[name] = module
                self.log.info("Loaded plugin '%s' from %s", name, file)
            except Exception as exc:
                self.log.error("Failed to load plugin from %s: %s", file, exc)

    async def run(self, name: str, **kwargs: Any) -> Any:
        """Execute a previously loaded plugin by *name*."""
        module = self.plugins.get(name)
        if module is None:
            raise KeyError(f"Plugin '{name}' not found")
        try:
            self.log.info("Executing plugin '%s'", name)
            result = await module.execute(**kwargs)
            self.log.info("Plugin '%s' executed successfully", name)
            return result
        except Exception as exc:
            self.log.error("Plugin '%s' execution failed: %s", name, exc)
            raise

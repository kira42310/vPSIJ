import pytest

# Existing test scripts that are not pytest tests yet: they run at import time
# and need a real scheduler or SSH target. They are reported as skipped instead
# of being imported. Remove a file from this set once it is migrated to pytest.
LEGACY_SCRIPTS = {"test_executor.py", "test_job.py", "test_remote.py"}


class LegacyScript(pytest.Item):
    def runtest(self):
        pytest.skip("legacy script, not migrated to pytest yet")


class LegacyScriptFile(pytest.File):
    def collect(self):
        yield LegacyScript.from_parent(self, name=self.path.name)


def pytest_pycollect_makemodule(module_path, parent):
    if module_path.name in LEGACY_SCRIPTS:
        return LegacyScriptFile.from_parent(parent, path=module_path)

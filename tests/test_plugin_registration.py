from sanic import Sanic
from spf import SanicPlugin, SanicPluginsFramework
from spf.plugin import PluginRegistration, PluginAssociated


class TestPlugin(SanicPlugin):
    pass


instance = TestPlugin()


def test_legacy_registration_1():
    app = Sanic('test_legacy_registration_1')
    spf = SanicPluginsFramework(app)
    # legacy style import
    reg = TestPlugin(app)
    assert isinstance(reg, PluginAssociated)
    (plugin, reg) = reg
    assert isinstance(reg, PluginRegistration)
    assert plugin == instance

def test_legacy_registration_2():
    app = Sanic('test_legacy_registration_2')
    # legacy style import, without declaring spf first
    reg = TestPlugin(app)
    assert isinstance(reg, PluginAssociated)
    (plugin, reg) = reg
    assert isinstance(reg, PluginRegistration)
    assert plugin == instance

def test_duplicate_registration_1():
    app = Sanic('test_duplicate_registration_1')
    spf = SanicPluginsFramework(app)
    assoc1 = spf.register_plugin(instance)
    exc = None
    try:
        assoc2 = spf.register_plugin(instance)
        assert not assoc2
    except Exception as e:
        exc = e
    assert isinstance(exc, ValueError)
    assert exc.args and len(exc.args) > 1 and exc.args[1] == assoc1

def test_duplicate_legacy_registration():
    app1 = Sanic('test_duplicate_legacy_registration_1')
    app2 = Sanic('test_duplicate_legacy_registration_2')
    # legacy style import
    assoc1 = TestPlugin(app1)
    (plugin1, reg1) = assoc1
    baseline_reg_count = len(plugin1.registrations)
    assoc2 = TestPlugin(app2)
    (plugin2, reg2) = assoc2
    assert len(plugin1.registrations) == baseline_reg_count + 1
    assert plugin1 == plugin2

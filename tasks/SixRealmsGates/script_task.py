from tasks.Component.GeneralBattle.general_battle import GeneralBattle
from tasks.Component.SwitchSoul.switch_soul import SwitchSoul
from tasks.GameUi.game_ui import GameUi
from tasks.GameUi.page import page_six_gates
from tasks.SixRealmsGates.assets import SixRealmsGatesAssets


class SixRealmsGatesTask(GeneralBattle, GameUi, SwitchSoul, SixRealmsGatesAssets):
    def run(self):
        con = self.config.six_realms_gates
        self.ui_get_current_page()
        self.ui_goto(page_six_gates)

        if not self.appear(self.I_CHECK_MOON_SEA):
            self.ui_click_until_disappear(self.I_SIX_GATE_SWITCH)
            self.ui_click_until_disappear(self.I_SIX_GATE_MOON)


if __name__ == "__main__":
    from module.config.config import Config
    from module.device.device import Device
    config = Config('oas1')
    device = Device(config)
    t = SixRealmsGatesTask(config, device)

    t.run()

    # print(t.find_one())
    # target, order = t.find_one()
    # print(t.check_medal_is_frog(True, target, order))

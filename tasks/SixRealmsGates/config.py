# This Python file uses the following encoding: utf-8
# @author runhey
# github https://github.com/runhey
from pydantic import BaseModel, Field
from tasks.Component.SwitchSoul.switch_soul_config import SwitchSoulConfig

from tasks.Component.config_base import ConfigBase
from tasks.TrueOrochi.config import TrueOrochiScheduler, TrueOrochiConfig

class SixRealmsGatesConfig(BaseModel):
    share_collect: bool = Field(default=True, description='share_collect_help')
    share_area_boss: bool = Field(default=True, description='share_area_boss_help')
    share_secret: bool = Field(default=True, description='share_secret_help')
    broken_amulet: int = Field(title='Broken Amulet', default=100, description='trifles_broken_amulet_help')


class SixRealmsGatesRaid(ConfigBase):
    scheduler: TrueOrochiScheduler = Field(default_factory=TrueOrochiScheduler)
    switch_soul: SwitchSoulConfig = Field(default_factory=SwitchSoulConfig)
    universal: SixRealmsGatesConfig = Field(default_factory=SixRealmsGatesConfig)
    pass

from module.atom.image import RuleImage
from module.atom.click import RuleClick
from module.atom.long_click import RuleLongClick
from module.atom.swipe import RuleSwipe
from module.atom.ocr import RuleOcr
from module.atom.list import RuleList

# This file was automatically generated by ./dev_tools/assets_extract.py.
# Don't modify it manually.
class TalismanPassAssets: 


	# Image Rule Assets
	# 领取全部 
	I_TP_GET_ALL = RuleImage(roi_front=(903,599,70,71), roi_back=(903,599,70,71), threshold=0.8, method="Template matching", file="./tasks/TalismanPass/tp/tp_tp_get_all.png")
	# 任务 的右上方红点 
	I_RED_POINT_TASK = RuleImage(roi_front=(1226,312,23,24), roi_back=(1226,312,23,24), threshold=0.8, method="Template matching", file="./tasks/TalismanPass/tp/tp_red_point_task.png")
	# 今日 的右上方红点 
	I_RED_POINT_DAY = RuleImage(roi_front=(632,157,23,26), roi_back=(632,157,23,26), threshold=0.8, method="Template matching", file="./tasks/TalismanPass/tp/tp_red_point_day.png")
	# 本周 的右上方红点 
	I_RED_POINT_WEEK = RuleImage(roi_front=(795,156,24,25), roi_back=(795,156,24,25), threshold=0.8, method="Template matching", file="./tasks/TalismanPass/tp/tp_red_point_week.png")
	# 等级奖励 
	I_RED_POINT_LEVEL = RuleImage(roi_front=(1222,174,21,22), roi_back=(1214,165,40,43), threshold=0.8, method="Template matching", file="./tasks/TalismanPass/tp/tp_red_point_level.png")
	# 选择一号奖励 
	I_TP_LEVEL_1 = RuleImage(roi_front=(203,435,122,59), roi_back=(203,435,122,59), threshold=0.8, method="Template matching", file="./tasks/TalismanPass/tp/tp_tp_level_1.png")
	# 选择二号奖励 
	I_TP_LEVEL_2 = RuleImage(roi_front=(577,435,122,55), roi_back=(577,435,122,55), threshold=0.8, method="Template matching", file="./tasks/TalismanPass/tp/tp_tp_level_2.png")
	# 选择三号奖励 
	I_TP_LEVEL_3 = RuleImage(roi_front=(967,433,109,61), roi_back=(967,433,109,61), threshold=0.8, method="Template matching", file="./tasks/TalismanPass/tp/tp_tp_level_3.png")
	# 前往 
	I_TP_GOTO = RuleImage(roi_front=(995,254,85,34), roi_back=(928,219,206,315), threshold=0.8, method="Template matching", file="./tasks/TalismanPass/tp/tp_tp_goto.png")
	# 经验的 
	I_TP_EXP = RuleImage(roi_front=(922,254,32,36), roi_back=(884,215,100,331), threshold=0.8, method="Template matching", file="./tasks/TalismanPass/tp/tp_tp_exp.png")
	# 溢出确认 
	I_OVERFLOW_CONFIRME = RuleImage(roi_front=(585,410,116,44), roi_back=(585,410,116,44), threshold=0.8, method="Template matching", file="./tasks/TalismanPass/tp/tp_overflow_confirme.png")



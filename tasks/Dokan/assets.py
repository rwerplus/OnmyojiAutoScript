from module.atom.image import RuleImage
from module.atom.click import RuleClick
from module.atom.long_click import RuleLongClick
from module.atom.swipe import RuleSwipe
from module.atom.ocr import RuleOcr
from module.atom.list import RuleList

# This file was automatically generated by ./dev_tools/assets_extract.py.
# Don't modify it manually.
class DokanAssets: 


	# Click Rule Assets
	# 道馆随机点击安全区域 
	C_DOKAN_RANDOM_CLICK_AREA = RuleClick(roi_front=(142,294,107,150), roi_back=(142,294,107,150), name="dokan_random_click_area")
	# 道馆随机点击安全区域1：竂友突破信息 
	C_DOKAN_RANDOM_CLICK_AREA1 = RuleClick(roi_front=(42,594,10,30), roi_back=(42,594,10,30), name="dokan_random_click_area1")
	# 道馆随机点击安全区域2：切换查看队伍模式。初步测试下来这个地方最安全，除了庭院、町中、逢魔外其他各场景都可用。 
	C_DOKAN_RANDOM_CLICK_AREA2 = RuleClick(roi_front=(1122,360,10,40), roi_back=(1122,360,10,40), name="dokan_random_click_area2")
	# 道馆随机点击安全区域3 
	C_DOKAN_RANDOM_CLICK_AREA3 = RuleClick(roi_front=(333,44,107,20), roi_back=(333,44,107,20), name="dokan_random_click_area3")
	# 道馆突破排名弹出时,点击此区域关闭 
	C_DOKAN_TOPPA_RANK_CLOSE_AREA = RuleClick(roi_front=(1150,380,100,150), roi_back=(1150,380,100,150), name="dokan_toppa_rank_close_area")
	# 准备战斗 
	C_DOKAN_READY_FOR_BATTLE = RuleClick(roi_front=(42,94,1207,543), roi_back=(42,94,1207,543), name="dokan_ready_for_battle")
	# 查找道馆时 点击此区域 隐藏道馆详情(显示防守人数,馆主等级等的卡片) 
	C_DOKAN_CANCEL_SELECT_DOKAN = RuleClick(roi_front=(1070,610,30,90), roi_back=(1070,610,30,90), name="dokan_cancel_select_dokan")
	# ruleanimate 用作检测选择道馆时,确定地图区域稳定无动作 
	C_DOKAN_CANCEL_SELECT_DOKAN_CHECK_ANIMATE = RuleClick(roi_front=(600,330,80,60), roi_back=(600,330,80,60), name="dokan_cancel_select_dokan_check_animate")
	# 查找道馆时 刷新道馆列表 
	C_DOKAN_REFRESH = RuleClick(roi_front=(1140,630,40,30), roi_back=(1140,630,40,30), name="dokan_refresh")
	# 道馆战斗时,左上角 退出按钮区域 
	C_DOKAN_BATTLE_QUIT_AREA = RuleClick(roi_front=(10,36,50,14), roi_back=(10,36,50,14), name="dokan_battle_quit_area")


	# Image Rule Assets
	# 阴阳寮->神社的按钮 
	I_RYOU_SHENSHE = RuleImage(roi_front=(850,660,100,60), roi_back=(850,660,100,60), threshold=0.8, method="Template matching", file="./tasks/Dokan/res/res_ryou_shenshe.png")
	# 神社->道馆 
	I_RYOU_DOKAN = RuleImage(roi_front=(465,160,100,50), roi_back=(465,160,100,50), threshold=0.8, method="Template matching", file="./tasks/Dokan/res/res_ryou_dokan.png")
	# 阴阳寮卡通人界面,左侧已开启的活动 列表 
	I_RYOU_DOKAN_ACTIVATED = RuleImage(roi_front=(0,150,200,400), roi_back=(0,150,200,400), threshold=0.8, method="Template matching", file="./tasks/Dokan/res/res_ryou_dokan_activated.png")
	# 是否已经成功进入道馆，上面中间的“道馆突破”文字 
	I_RYOU_DOKAN_CHECK = RuleImage(roi_front=(567,15,144,42), roi_back=(567,15,144,42), threshold=0.8, method="Template matching", file="./tasks/Dokan/res/res_ryou_dokan_check.png")
	# 道馆内式神录 
	I_RYOU_DOKAN_SHIKIGAMI = RuleImage(roi_front=(960,580,140,120), roi_back=(960,580,140,120), threshold=0.8, method="Template matching", file="./tasks/Dokan/res/res_ryou_dokan_shikigami.png")
	# 优先攻击选项 
	I_RYOU_DOKAN_ATTACK_PRIORITY = RuleImage(roi_front=(666,672,58,25), roi_back=(666,672,58,25), threshold=0.8, method="Template matching", file="./tasks/Dokan/res/res_ryou_dokan_priority.png")
	# 优先攻击: 见习 
	I_RYOU_DOKAN_ATTACK_PRIORITY_0 = RuleImage(roi_front=(98,170,94,43), roi_back=(98,170,94,43), threshold=0.8, method="Template matching", file="./tasks/Dokan/res/res_ryou_dokan_priority_0.png")
	# 优先攻击: 初级 
	I_RYOU_DOKAN_ATTACK_PRIORITY_1 = RuleImage(roi_front=(342,175,96,42), roi_back=(342,175,96,42), threshold=0.8, method="Template matching", file="./tasks/Dokan/res/res_ryou_dokan_priority_1.png")
	# 优先攻击: 中级 
	I_RYOU_DOKAN_ATTACK_PRIORITY_2 = RuleImage(roi_front=(585,175,89,35), roi_back=(585,175,89,35), threshold=0.8, method="Template matching", file="./tasks/Dokan/res/res_ryou_dokan_priority_2.png")
	# 优先攻击: 高级 
	I_RYOU_DOKAN_ATTACK_PRIORITY_3 = RuleImage(roi_front=(830,175,88,41), roi_back=(830,175,88,41), threshold=0.8, method="Template matching", file="./tasks/Dokan/res/res_ryou_dokan_priority_3.png")
	# 优先攻击: 黑脸 
	I_RYOU_DOKAN_ATTACK_PRIORITY_4 = RuleImage(roi_front=(1072,178,94,39), roi_back=(1072,178,94,39), threshold=0.8, method="Template matching", file="./tasks/Dokan/res/res_ryou_dokan_priority_4.png")
	# 正在查找道馆,还未选择 
	I_RYOU_DOKAN_FINDING_DOKAN = RuleImage(roi_front=(980,60,100,160), roi_back=(980,60,100,160), threshold=0.8, method="Template matching", file="./tasks/Dokan/res/res_ryou_dokan_finding_dokan.png")
	# 已选择道馆 
	I_RYOU_DOKAN_FOUND_DOKAN = RuleImage(roi_front=(440,580,360,140), roi_back=(440,580,360,140), threshold=0.8, method="Template matching", file="./tasks/Dokan/res/res_ryou_dokan_found_dokan.png")
	# 状态：集结等待中。检查右下角的挑战是不是灰色的。FIXME 黄色和灰色的挑战截图总是傻傻分不清，先改用OCR 
	I_RYOU_DOKAN_GATHERING = RuleImage(roi_front=(653,76,46,26), roi_back=(653,76,46,26), threshold=0.85, method="Template matching", file="./tasks/Dokan/res/res_ryou_dokan_gathering.png")
	# 状态：检查右下角有没有挑战？通常是失败了，并退出来到集结界面，可重新开始点击右下角挑战进入战斗 
	I_RYOU_DOKAN_START_CHALLENGE = RuleImage(roi_front=(1100,550,180,80), roi_back=(1100,550,180,80), threshold=0.8, method="Template matching", file="./tasks/Dokan/res/res_ryou_dokan_start_challenge.png")
	# 状态：达到失败次数，CD中。挑战次数恢复倒数 
	I_RYOU_DOKAN_CD1 = RuleImage(roi_front=(1068,500,146,27), roi_back=(1068,500,146,27), threshold=0.8, method="Template matching", file="./tasks/Dokan/res/res_ryou_dokan_cd1.png")
	# 状态：达到失败次数，CD中。观战按钮 
	I_RYOU_DOKAN_CD = RuleImage(roi_front=(1122,566,117,74), roi_back=(1122,566,117,74), threshold=0.8, method="Template matching", file="./tasks/Dokan/res/res_ryou_dokan_cd.png")
	# 状态：进入战斗，待开始，右下角图标。 
	I_RYOU_DOKAN_IN_FIELD = RuleImage(roi_front=(1128,536,100,100), roi_back=(1128,536,100,100), threshold=0.8, method="Template matching", file="./tasks/Dokan/res/res_ryou_dokan_in_field.png")
	# 馆主战等待中 
	I_DOKAN_BOSS_WAITING = RuleImage(roi_front=(460,140,370,80), roi_back=(460,140,370,80), threshold=0.8, method="Template matching", file="./tasks/Dokan/res/res_dokan_boss_waiting.png")
	# 馆主战 等待 或 进行中时 在寮境中出现的馆主图标 
	I_RYOU_DOKAN_MASTER_BATTLE = RuleImage(roi_front=(640,0,640,360), roi_back=(640,0,640,360), threshold=0.8, method="Template matching", file="./tasks/Dokan/res/res_ryou_dokan_master_battle.png")
	# 放弃突破 
	I_DOKAN_ABANDONED_TOPPA = RuleImage(roi_front=(0,550,180,170), roi_back=(0,550,180,170), threshold=0.8, method="Template matching", file="./tasks/Dokan/res/res_ryou_dokan_abandoned_toppa.png")
	# 放弃突破 确认按钮 
	I_DOKAN_ABANDONED_TOPPA_ENSURE = RuleImage(roi_front=(0,0,1280,720), roi_back=(0,0,1280,720), threshold=0.8, method="Template matching", file="./tasks/Dokan/res/res_ryou_dokan_abandoned_toppa_ensure.png")
	# 放弃突破 
	I_DOKAN_ABANDONED_TOPPA_TITLE = RuleImage(roi_front=(1020,160,260,80), roi_back=(1020,160,260,80), threshold=0.8, method="Template matching", file="./tasks/Dokan/res/res_ryou_dokan_abandoned_toppa_title.png")
	# 状态：道馆胜利 
	I_RYOU_DOKAN_WIN = RuleImage(roi_front=(620,50,100,80), roi_back=(620,50,100,80), threshold=0.8, method="Template matching", file="./tasks/Dokan/res/res_ryou_dokan_win.png")
	# 状态：进入战斗，待开始，右下角图标。 
	I_RYOU_DOKAN_IN_FIELD2 = RuleImage(roi_front=(1131,562,88,48), roi_back=(1131,562,88,48), threshold=0.8, method="Template matching", file="./tasks/Dokan/res/res_ryou_dokan_in_field2.png")
	# 馆主战,第一阵容 
	I_RYOU_DOKAN_BATTLE_MASTER_FIRST = RuleImage(roi_front=(1080,180,160,70), roi_back=(1080,180,160,70), threshold=0.8, method="Template matching", file="./tasks/Dokan/res/res_ryou_dokan_battle_master_first.png")
	# 馆主战,第二阵容 # TODO 截图 
	I_RYOU_DOKAN_BATTLE_MASTER_SECOND = RuleImage(roi_front=(1080,180,160,70), roi_back=(1080,180,160,70), threshold=0.8, method="Template matching", file="./tasks/Dokan/res/res_ryou_dokan_battle_master_second.png")
	# 状态：战斗结算，可能是打完小朋友了，也可能是失败了。 
	I_RYOU_DOKAN_BATTLE_OVER = RuleImage(roi_front=(571,503,106,49), roi_back=(571,503,106,49), threshold=0.8, method="Template matching", file="./tasks/Dokan/res/res_ryou_dokan_battle_over.png")
	# 状态：战斗中，左上角的加油图标 
	I_RYOU_DOKAN_FIGHTING = RuleImage(roi_front=(232,36,42,19), roi_back=(232,36,42,19), threshold=0.8, method="Template matching", file="./tasks/Dokan/res/res_ryou_dokan_fighting.png")
	# 状态：道馆已经结束 
	I_RYOU_DOKAN_FINISHED = RuleImage(roi_front=(658,649,91,27), roi_back=(658,649,91,27), threshold=0.8, method="Template matching", file="./tasks/Dokan/res/res_ryou_dokan_finished.png")
	# 道馆失败/成功 出现的突破排名 弹窗 
	I_RYOU_DOKAN_TOPPA_RANK = RuleImage(roi_front=(110,80,170,70), roi_back=(110,80,170,70), threshold=0.8, method="Template matching", file="./tasks/Dokan/res/res_ryou_dokan_toppa_rank.png")
	# 状态：道馆挑战失败，投票 保留赏金 
	I_RYOU_DOKAN_FAILED_VOTE_KEEP_BOUNTY = RuleImage(roi_front=(1020,220,260,120), roi_back=(1020,220,260,120), threshold=0.8, method="Template matching", file="./tasks/Dokan/res/res_ryou_dokan_failed_vote_keep_bounty.png")
	# 状态：道馆挑战失败，投票 再战道馆 
	I_RYOU_DOKAN_FAILED_VOTE_BATTLE_AGAIN = RuleImage(roi_front=(1020,220,260,120), roi_back=(1020,220,260,120), threshold=0.8, method="Template matching", file="./tasks/Dokan/res/res_ryou_dokan_failed_vote_battle_again.png")
	# 状态：道馆投票 放弃突破 
	I_RYOU_DOKAN_ABANDONED_TOPPA_ABANDONED = RuleImage(roi_front=(1020,220,260,120), roi_back=(1020,220,260,120), threshold=0.8, method="Template matching", file="./tasks/Dokan/res/res_ryou_dokan_abandoned_toppa_abandoned.png")
	# 状态：道馆投票 继续突破 
	I_RYOU_DOKAN_ABANDONED_TOPPA_CONTINUE = RuleImage(roi_front=(1020,220,260,120), roi_back=(1020,220,260,120), threshold=0.8, method="Template matching", file="./tasks/Dokan/res/res_ryou_dokan_abandoned_toppa_continue.png")
	# 道馆战斗界面 点击退出按钮后 弹出的确认按钮 
	I_RYOU_DOKAN_QUIT_BATTLE_ENSURE = RuleImage(roi_front=(0,0,1280,720), roi_back=(0,0,1280,720), threshold=0.8, method="Template matching", file="./tasks/Dokan/res/res_ryou_dokan_quit_battle_ensure.png")
	# 道馆退出确认 
	I_RYOU_DOKAN_EXIT_ENSURE = RuleImage(roi_front=(678,395,125,56), roi_back=(678,395,125,56), threshold=0.8, method="Template matching", file="./tasks/Dokan/res/res_ryou_dokan_exit_ensure.png")
	# 进入加油相关：道馆战报按钮 
	I_RYOU_DOKAN_CHEERING_SCORES = RuleImage(roi_front=(157,100,35,39), roi_back=(157,100,35,39), threshold=0.8, method="Template matching", file="./tasks/Dokan/res/res_ryou_dokan_cheering_scores.png")
	# 进入加油相关：前往战斗中的竂友 
	I_RYOU_DOKAN_CHEERING_ATTACKING_SAMA = RuleImage(roi_front=(948,182,56,295), roi_back=(948,182,56,295), threshold=0.8, method="Template matching", file="./tasks/Dokan/res/res_ryou_dokan_cheering_attacking_sama.png")
	# 场景检测：阴阳竂 
	I_SCENE_RYOU = RuleImage(roi_front=(1161,674,75,31), roi_back=(1161,674,75,31), threshold=0.8, method="Template matching", file="./tasks/Dokan/res/scene_ryou.png")
	# 场景检测：神社 
	I_SCENE_SHENSHE = RuleImage(roi_front=(0,100,600,600), roi_back=(0,100,600,600), threshold=0.8, method="Template matching", file="./tasks/Dokan/res/scene_shenshe.png")
	# 道馆 地图界面 建立道馆按钮 
	I_RYOU_DOKAN_CREATE_DOKAN = RuleImage(roi_front=(230,580,130,120), roi_back=(230,580,130,120), threshold=0.8, method="Template matching", file="./tasks/Dokan/res/res_ryou_dokan_create_dokan.png")
	# 道馆 地图界面 点击建立道馆按钮后弹窗中的 确认按钮 
	I_RYOU_DOKAN_CREATE_DOKAN_ENSURE = RuleImage(roi_front=(0,0,1280,720), roi_back=(0,0,1280,720), threshold=0.8, method="Template matching", file="./tasks/Dokan/res/res_ryou_dokan_create_dokan_ensure.png")
	# 道馆信息 右上角关闭按钮 
	I_RYOU_DOKAN_DOKAN_INFO_CLOSE = RuleImage(roi_front=(1150,80,100,90), roi_back=(1150,80,100,90), threshold=0.8, method="Template matching", file="./tasks/Dokan/res/res_ryou_dokan_dokan_info_close.png")
	# 寮境界面,道馆打完后 出现在底部的'今日可挑战机会'字样 
	I_RYOU_DOKAN_TODAY_ATTACK_COUNT = RuleImage(roi_front=(500,630,250,50), roi_back=(500,630,250,50), threshold=0.8, method="Template matching", file="./tasks/Dokan/res/res_ryou_dokan_today_attack_count.png")
	# 今日道馆已挑战成功 
	I_RYOU_DOKAN_REMAIN_ATTACK_COUNT_DONE = RuleImage(roi_front=(550,610,220,80), roi_back=(550,610,220,80), threshold=0.9, method="Template matching", file="./tasks/Dokan/res/res_ryou_dokan_remain_attack_count_done.png")
	# 今日可挑战次数:0次 
	I_RYOU_DOKAN_REMAIN_ATTACK_COUNT_ZERO = RuleImage(roi_front=(650,610,110,80), roi_back=(650,610,110,80), threshold=0.9, method="Template matching", file="./tasks/Dokan/res/res_ryou_dokan_remain_attack_count_zero.png")
	# 今日可挑战次数:1次 
	I_RYOU_DOKAN_REMAIN_ATTACK_COUNT_ONE = RuleImage(roi_front=(650,610,110,80), roi_back=(650,610,110,80), threshold=0.9, method="Template matching", file="./tasks/Dokan/res/res_ryou_dokan_remain_attack_count_one.png")
	# 今日可挑战次数:2次 
	I_RYOU_DOKAN_REMAIN_ATTACK_COUNT_TWO = RuleImage(roi_front=(650,610,110,80), roi_back=(650,610,110,80), threshold=0.9, method="Template matching", file="./tasks/Dokan/res/res_ryou_dokan_remain_attack_count_two.png")
	# 查找道馆时,中间信息卡片 馆主等级-修习 
	I_CENTER_GUANZHU_XIUXI = RuleImage(roi_front=(0,0,1280,720), roi_back=(0,0,1280,720), threshold=0.8, method="Template matching", file="./tasks/Dokan/res/res_ryou_dokan_center_guanzhu_xiuxi.png")
	# 查找道馆时,中间防守人数字样,为了定位该图下方的 防守人数数字 
	I_CENTER_POINT_PEOPLE_NUMBER = RuleImage(roi_front=(0,0,1280,720), roi_back=(0,0,1280,720), threshold=0.8, method="Template matching", file="./tasks/Dokan/res/res_ryou_dokan_center_point_people_number.png")
	# 查找道馆时,挑战按钮 
	I_CENTER_CHALLENGE = RuleImage(roi_front=(0,0,1280,720), roi_back=(0,0,1280,720), threshold=0.8, method="Template matching", file="./tasks/Dokan/res/res_ryou_dokan_center_challenge.png")
	# 查找道馆时,确认挑战按钮 
	I_CHALLENGE_ENSURE = RuleImage(roi_front=(0,0,1280,720), roi_back=(0,0,1280,720), threshold=0.8, method="Template matching", file="./tasks/Dokan/res/res_ryou_dokan_challenge_ensure.png")
	# 查找道馆时,确认刷新道馆列表按钮 
	I_REFRESH_ENSURE = RuleImage(roi_front=(0,0,1280,720), roi_back=(0,0,1280,720), threshold=0.8, method="Template matching", file="./tasks/Dokan/res/res_ryou_dokan_refresh_ensure.png")
	# 查找道馆时,右侧道馆赏金图标,为了定位该图右侧的 赏金金额 
	I_RIGHTPAD_POINT_BOUNTY = RuleImage(roi_front=(1050,0,230,0), roi_back=(1050,0,230,50), threshold=0.8, method="Template matching", file="./tasks/Dokan/res/res_ryou_dokan_rightpad_point_bounty.png")
	# 寮境中上部的标志 
	I_RYOU_DOKAN_CENTER_TOP = RuleImage(roi_front=(500,20,300,70), roi_back=(500,20,300,70), threshold=0.8, method="Template matching", file="./tasks/Dokan/res/res_ryou_dokan_center_top.png")
	# 左上角退出按钮- 
	I_RYOU_DOKAN_DOKAN_QUIT = RuleImage(roi_front=(0,2,80,80), roi_back=(0,2,80,80), threshold=0.8, method="Template matching", file="./tasks/Dokan/res/res_ryou_dokan_dokan_quit.png")
	# 道馆攻破后夺得资金界面 
	I_RYOU_DOKAN_SPOILS_OF_DOKAN = RuleImage(roi_front=(480,400,400,100), roi_back=(480,400,400,100), threshold=0.8, method="Template matching", file="./tasks/Dokan/res/res_ryou_dokan_spoils_of_dokan.png")


	# List Rule Assets
	# 这个是当前活跃的竂活动列表界面 
	L_RYOU_ACTIVITY_LIST = RuleList(folder="./tasks/Dokan/res", direction="vertical", mode="ocr", roi_back=(20,150,170,400), size=(42, 27), 
					 array=["道馆", "首领", "狭间"])


	# Ocr Rule Assets
	# 道馆地图里找文字：万 
	O_DOKAN_MAP = RuleOcr(roi=(270,130,740,460), area=(270,130,740,460), mode="Full", method="Default", keyword="万", name="dokan_map")
	# 道馆里找文字：后开战 
	O_DOKAN_GATHERING = RuleOcr(roi=(535,75,211,29), area=(535,75,211,29), mode="Single", method="Default", keyword="开战", name="dokan_gathering")
	# 道馆里找文字：剩余突破时间 
	O_DOKAN_ATTACKING = RuleOcr(roi=(1122,546,92,51), area=(1122,546,92,51), mode="Single", method="Default", keyword="剩余", name="dokan_attacking")
	# 道馆里找文字：后挑战馆主 
	O_DOKAN_BOSS_WAITING = RuleOcr(roi=(603,148,130,32), area=(603,148,130,32), mode="Single", method="Default", keyword="馆主", name="dokan_boss_waiting")
	# 查找道馆时,右侧边栏中的赏金 
	O_DOKAN_RIGHTPAD_BOUNTY = RuleOcr(roi=(0,0,0,0), area=(0,0,0,0), mode="Single", method="Default", keyword="", name="dokan_rightpad_bounty")
	# 查找道馆时,中间卡片上防守人数 
	O_DOKAN_CENTER_PEOPLE_NUMBER = RuleOcr(roi=(0,0,0,0), area=(0,0,0,0), mode="Full", method="Default", keyword="", name="dokan_center_people_number")


	# Swipe Rule Assets
	# 道馆选择界面 右侧侧边栏 手指向上滑动 
	S_DOKAN_LIST_UP = RuleSwipe(roi_front=(1100,420,30,21), roi_back=(1240,240,30,21), mode="default", name="dokan_list_up")



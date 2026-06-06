import sys, os
sys.path.insert(0, r'D:\Develop\Git_repository\make-something\NarutoScript')

from module.config.config import AzurLaneConfig

config = AzurLaneConfig(config_name='1-日周活')

print("=== 可用任务模块 ===")
task_dir = r'D:\Develop\Git_repository\make-something\NarutoScript\tasks'
modules = [d for d in os.listdir(task_dir) if os.path.isdir(os.path.join(task_dir, d)) and not d.startswith('__') and not d.startswith('.')]
for m in sorted(modules):
    print(f"  {m}")

print(f"\n=== 当前配置的任务 ===")
print(f"  调度器: {'开启' if config.Scheduler_Enable else '关闭'}")
print(f"  下次运行: {config.Scheduler_NextRun}")

# 查看 pending_task
print(f"\n  等待中任务: {config.pending_task}")

# 尝试获取下一个任务
try:
    next_task = config.get_next_task()
    print(f"  下一个任务: {next_task}")
except Exception as e:
    print(f"  get_next_task error: {e}")

# 查看各任务开关
print(f"\n=== 日常任务开关 ===")
tasks_to_check = ['SquadRaid_SquadRaidFight', 'Duel_DuelDaily', 'Freebies_MailRewardClaim', 
                  'ZhaoCai_ZhaoCaiFree', 'Freebies_ActivityReward', 'Mission_MissionAccept',
                  'Recruit_Recruit', 'Freebies_OrganizationPray',
                  'Freebies_MonthlySignIn', 'Freebies_DailyShareStart',
                  'TiLiPurchase_TiLiPurchaseTimes', 'CultivationRoad_CultivationFinish',
                  'SurvivalTrail_SurvivalTrialResetTimes']
for t in tasks_to_check:
    try:
        val = getattr(config, t, 'NOT_FOUND')
        print(f"  {t}: {val}")
    except:
        print(f"  {t}: error")

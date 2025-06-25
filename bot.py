import discord
from discord.ext import commands
import json
import os

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

TASK_FILE = "tasks.json"

def load_tasks():
    if os.path.exists(TASK_FILE):
        with open(TASK_FILE, "r") as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(TASK_FILE, "w") as f:
        json.dump(tasks, f, indent=2)

@bot.event
async def on_ready():
    print(f"Bot đang hoạt động với tên: {bot.user}")

@bot.command()
async def addtask(ctx, *, task_info):
    """Thêm task: !addtask Tên task - @user - deadline"""
    parts = task_info.split(" - ")
    if len(parts) != 3:
        await ctx.send("❌ Định dạng sai. Ví dụ: `!addtask Viết báo cáo - @Tuấn - 30/06`")
        return
    task_name, assigned_to, deadline = parts
    task = {
        "task": task_name.strip(),
        "assigned": assigned_to.strip(),
        "deadline": deadline.strip()
    }
    tasks = load_tasks()
    tasks.append(task)
    save_tasks(tasks)
    await ctx.send(f"✅ Đã thêm task: **{task_name}** cho {assigned_to} (Deadline: {deadline})")

@bot.command()
async def listtasks(ctx):
    """Hiển thị tất cả task"""
    tasks = load_tasks()
    if not tasks:
        await ctx.send("📭 Không có task nào.")
        return
    msg = "**📋 Danh sách task:**\n"
    for i, t in enumerate(tasks, 1):
        msg += f"{i}. **{t['task']}** - {t['assigned']} - Deadline: {t['deadline']}\n"
    await ctx.send(msg)

bot.run("TOKEN")
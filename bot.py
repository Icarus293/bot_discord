import discord
from discord.ext import commands
import json
import os
from dotenv import load_dotenv

load_dotenv()

ALLOWED_CHANNEL_ID = 1387478463480332429

intents = discord.Intents.default()
intents.message_content = True
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

def is_allowed_channel(ctx):
    return ctx.channel.id == ALLOWED_CHANNEL_ID

@bot.event
async def on_ready():
    print(f"✅ Bot đang hoạt động với tên: {bot.user}")

@bot.command()
@commands.check(is_allowed_channel)
async def addtask(ctx, *, task_info):
    parts = task_info.split(" - ")
    if len(parts) != 3:
        await ctx.send("❌ Định dạng sai. Ví dụ: `!addtask Viết báo cáo - @Tuấn - 30/06`")
        return
    task_name, assigned_to, deadline = parts
    task = {
        "task": task_name.strip(),
        "assigned": assigned_to.strip(),
        "deadline": deadline.strip(),
        "done": False
    }
    tasks = load_tasks()
    tasks.append(task)
    save_tasks(tasks)
    await ctx.send(f"✅ Đã thêm task: **{task_name}** cho {assigned_to} (Deadline: {deadline})")

@bot.command()
@commands.check(is_allowed_channel)
async def listtasks(ctx):
    tasks = load_tasks()
    if not tasks:
        await ctx.send("📭 Không có task nào.")
        return
    msg = "**📋 Danh sách task:**\n"
    for i, t in enumerate(tasks, 1):
        status = "✅" if t.get("done") else "❌"
        msg += f"{i}. {status} **{t['task']}** - {t['assigned']} - Deadline: {t['deadline']}\n"
    await ctx.send(msg)

@bot.command()
@commands.check(is_allowed_channel)
async def removetask(ctx, index: int):
    tasks = load_tasks()
    if 1 <= index <= len(tasks):
        removed = tasks.pop(index - 1)
        save_tasks(tasks)
        await ctx.send(f"🗑️ Đã xoá task: **{removed['task']}**")
    else:
        await ctx.send("❌ Số thứ tự không hợp lệ.")

@bot.command()
@commands.check(is_allowed_channel)
async def done(ctx, index: int):
    tasks = load_tasks()
    if 1 <= index <= len(tasks):
        tasks[index - 1]['done'] = True
        save_tasks(tasks)
        await ctx.send(f"✅ Task **{tasks[index - 1]['task']}** đã được đánh dấu là hoàn thành.")
    else:
        await ctx.send("❌ Số thứ tự không hợp lệ.")

@bot.command()
@commands.check(is_allowed_channel)
async def cleartasks(ctx):
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    await ctx.send("⚠️ Bạn có chắc muốn xoá toàn bộ task không? Nhập `yes` để xác nhận.")
    try:
        msg = await bot.wait_for("message", timeout=15.0, check=check)
        if msg.content.lower() == "yes":
            save_tasks([])
            await ctx.send("🧹 Tất cả task đã được xoá.")
        else:
            await ctx.send("❌ Huỷ lệnh xoá.")
    except:
        await ctx.send("⏰ Hết thời gian xác nhận. Huỷ lệnh.")

@bot.command()
@commands.check(is_allowed_channel)
async def helptask(ctx):
    help_msg = """
🛠 **Hướng dẫn sử dụng Task Bot:**

📌 `!addtask Tên - @người - deadline` → Thêm task mới  
📌 `!listtasks` → Hiển thị danh sách task  
📌 `!removetask số` → Xóa task theo số thứ tự  
📌 `!done số` → Đánh dấu task đã hoàn thành  
📌 `!cleartasks` → Xóa toàn bộ task (có xác nhận)  
📌 `!helptask` → Xem hướng dẫn này
"""
    await ctx.send(help_msg)

# Lấy token từ biến môi trường
bot.run(os.getenv("TOKEN"))

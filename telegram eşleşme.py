from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters, CallbackQueryHandler
import os

# Kullanıcı profilleri
users = {}
photos = {}
pending_requests = {}
user_queue = []

# Başlangıç komutu
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Merhaba! Şehir, semt ve yaşınızı göndererek kaydolun (örn: İstanbul Kadıköy 30). Fotoğrafınızı daha sonra yükleyebilirsiniz."
    )

# Kullanıcı kaydetme
async def register_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = update.message.text.split()
    
    if len(user_data) == 3:
        city, district, age_str = user_data
        if age_str.isdigit():
            age = int(age_str)
            user_id = update.message.from_user.id

            if user_id not in users:
                users[user_id] = {"city": city, "district": district, "age": age}
                await update.message.reply_text("Kaydınız alındı! Şimdi fotoğrafınızı yükleyin.")
                user_queue.append(user_id)  # Kullanıcıyı kuyruga ekle
            else:
                await update.message.reply_text("Zaten kayıtlısınız. Fotoğrafınızı yükleyebilirsiniz.")
        else:
            await update.message.reply_text("Yaşınızı sayısal olarak girin (örn: 30).")
    else:
        await update.message.reply_text("Geçersiz format. Lütfen şehir, semt ve yaşınızı doğru formatta girin.")

# Fotoğraf yükleme
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    if user_id in users:
        photo_file = await update.message.photo[-1].get_file()
        photo_path = f"{user_id}_photo.jpg"
        await photo_file.download_to_drive(photo_path)
        photos[user_id] = photo_path
        await update.message.reply_text("Fotoğrafınız alındı! Şimdi diğer kullanıcıları görebilirsiniz.")
        await show_next_user(update, context)  # Kuyruğun başındaki kullanıcıyı göster
    else:
        await update.message.reply_text("Lütfen önce şehir, semt ve yaş bilgilerinizi girin.")

# Kullanıcıyı gösterme
async def show_next_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_queue:
        other_id = user_queue.pop(0)  # Kuyruğun başındaki kullanıcıyı al
        if other_id != user_id:
            other_user = users.get(other_id)
            photo_path = photos.get(other_id)
            keyboard = [
                [InlineKeyboardButton("Beğen", callback_data=f"like_{other_id}")],
                [InlineKeyboardButton("Geç", callback_data=f"pass_{other_id}")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            if photo_path and os.path.exists(photo_path):
                await update.message.reply_photo(photo=open(photo_path, 'rb'), caption=f"Kullanıcı: {other_user['city']}, {other_user['district']}, Yaş: {other_user['age']}", reply_markup=reply_markup)
            else:
                await update.message.reply_text(f"Kullanıcı: {other_user['city']}, {other_user['district']}, Yaş: {other_user['age']}", reply_markup=reply_markup)
        else:
            await update.message.reply_text("Kuyrukta başka kullanıcı kalmadı.")
    else:
        await update.message.reply_text("Kuyrukta başka kullanıcı bulunmuyor.")

# Inline butonlara tıklama
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    user_id = query.from_user.id

    print(f"Button clicked by user {user_id}. Data: {data}")  # Debug mesajı

    if data.startswith('like_'):
        other_user_id = int(data.split('_')[1])
        await handle_reaction(user_id, other_user_id, 'beğen', context)
    elif data.startswith('pass_'):
        other_user_id = int(data.split('_')[1])
        await handle_reaction(user_id, other_user_id, 'geç', context)

# Beğeni gönderme
async def handle_reaction(user_id: int, other_user_id: int, reaction: str, context: ContextTypes.DEFAULT_TYPE):
    print(f"Handling reaction: {reaction} for user {user_id} and other user {other_user_id}")  # Debug mesajı
    if reaction == "beğen":
        pending_requests[user_id] = other_user_id
        await check_matches(user_id, other_user_id, context)
    elif reaction == "geç":
        if user_id in user_queue:
            user_queue.remove(user_id)  # Kullanıcıyı kuyruktan çıkar
        await show_next_user(await context.bot.get_chat(user_id), context)

# Eşleşme kontrolü
async def check_matches(user_id: int, other_user_id: int, context: ContextTypes.DEFAULT_TYPE):
    print(f"Checking matches for user {user_id} and other user {other_user_id}")  # Debug mesajı
    if other_user_id in pending_requests and pending_requests[other_user_id] == user_id:
        print(f"Match found between user {user_id} and user {other_user_id}")  # Debug mesajı
        await notify_match(user_id, other_user_id, context)

# Eşleşme bildirimi
async def notify_match(user1_id: int, user2_id: int, context: ContextTypes.DEFAULT_TYPE):
    print(f"Notifying match between user {user1_id} and user {user2_id}")  # Debug mesajı
    if user1_id in users and user2_id in users:
        user1_photo_path = photos.get(user1_id)
        user2_photo_path = photos.get(user2_id)

        if user1_photo_path and os.path.exists(user1_photo_path):
            await context.bot.send_photo(chat_id=user2_id, photo=open(user1_photo_path, 'rb'), caption="Eşleştiniz! Diğer kullanıcı sizinle eşleşti.")
            print(f"Photo sent to user {user2_id}")  # Debug mesajı
        if user2_photo_path and os.path.exists(user2_photo_path):
            await context.bot.send_photo(chat_id=user1_id, photo=open(user2_photo_path, 'rb'), caption="Eşleştiniz! Diğer kullanıcı sizinle eşleşti.")
            print(f"Photo sent to user {user1_id}")  # Debug mesajı

def main():
    app = ApplicationBuilder().token("telegram tokeninizi buraya girin").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, register_user))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(CallbackQueryHandler(button_click))

    app.run_polling()

if __name__ == '__main__':
    main()

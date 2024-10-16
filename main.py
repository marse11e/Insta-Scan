import instaloader
from src.parsers.insta_parser import InstaParser, PostHandler
import configparser

def load_or_login_session(loader, username, password):
    """Функция для загрузки сессии или логина в аккаунт Instagram"""
    try:
        loader.load_session_from_file(username)
        print(f"Сессия для пользователя {username} загружена.")
    except FileNotFoundError:
        print(f"Файл сессии не найден, выполняем вход для {username}.")
        loader.login(username, password)
        loader.save_session_to_file()
        print("Сессия сохранена.")

def main():
    config = configparser.ConfigParser()
    config.read("src/configs/config.ini")
    username = config.get("Instagram", "username")
    password = config.get("Instagram", "password")

    L = instaloader.Instaloader()
    load_or_login_session(L, username, password)

    parser = InstaParser(loader=L)
    post_parser = PostHandler(loader=L)

    
        
    choice = input("\n1. Профиль пользователя\n2. Пост по URL\nВведите номер (1-2): ")

    if choice == "1":
        instagram_username = input("Введите имя пользователя: ")
        choice_2 = input("\n1. Посты (изображения)\n2. Посты (видео)\n3. Рилсы\n4. Сторис\n5. Все\nВведите номер (1-5): ")
        actions = {
            "1": parser.download_posts_as_images,
            "2": parser.download_posts_as_videos,
            "3": parser.download_reels,
            "4": parser.download_stories,
            "5": parser.download_profile_data
        }
        actions.get(choice_2, lambda x: print("Неверный выбор"))(instagram_username)

    elif choice == "2":
        post_url = input("Введите URL поста: ")
        choice_2 = input("\n1. Скачать пост\n2. Информация в JSON\n3. Комментарии в JSON\nВведите номер (1-3): ")
        actions = {
            "1": post_parser.download_post_by_url,
            "2": post_parser.save_post_info_to_json,
            "3": post_parser.save_comments_to_json
        }
        actions.get(choice_2, lambda x: print("Неверный выбор"))(post_url=post_url, save_path='data/raw')

    else:
        print("Неверный выбор. Пожалуйста, введите номер от 1 до 2.")


if __name__ == "__main__":
    main()

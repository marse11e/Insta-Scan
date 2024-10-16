import instaloader
import os
import shutil
import json


class InstaParser:
    def __init__(self, loader):
        self.loader: instaloader.Instaloader = loader

    def move_files(self, source_path, destination_path):
        """Перемещает файлы из source_path в destination_path"""
        if os.path.exists(source_path):
            shutil.move(source_path, destination_path)
            print(f"Загрузка завершена! Медиа сохранены в {destination_path}")
        else:
            print(f"Ошибка: Папка {source_path} не найдена.")

    def download_posts_as_images(self, username: str):
        """Скачивает посты как изображения"""
        print(f"Скачивание изображений из профиля {username}...")
        self.loader.download_profile(
            username, profile_pic=False, post_filter=lambda post: post.is_video == False)
        self.move_files(username, os.path.join("data/raw/", username))

    def download_posts_as_videos(self, username: str):
        """Скачивает посты как видео"""
        print(f"Скачивание видео из профиля {username}...")
        self.loader.download_profile(
            username, profile_pic=False, post_filter=lambda post: post.is_video == True)
        self.move_files(username, os.path.join("data/raw/", username))

    def download_reels(self, username: str):
        """Скачивает рилсы"""
        print(f"Скачивание рилсов из профиля {username}...")
        self.loader.download_profile(
            username, profile_pic=False, post_filter=lambda post: post.typename == 'Reel')
        self.move_files(username, os.path.join("data/raw/", username))

    def download_stories(self, username: str):
        """Метод для скачивания историй пользователя Instagram."""
        try:
            profile = instaloader.Profile.from_username(
                self.loader.context, username)

            stories = self.loader.get_stories(userids=[profile.userid])

            for story in stories:
                for item in story.get_items():
                    print(f"Скачиваем историю: {item.mediaid} от {item.date}")
                    self.loader.download_storyitem(item, target=f"{username}")
            self.move_files(username, os.path.join("data/raw/", username))

        except instaloader.exceptions.ProfileNotExistsException:
            print(f"Профиль {username} не найден.")
        except instaloader.exceptions.InstaloaderException as e:
            print(f"Ошибка при загрузке историй: {str(e)}")

    def download_profile_data(self, username: str, ):
        """Метод для парсинга данных профиля Instagram и загрузки его медиа"""
        try:
            profile = instaloader.Profile.from_username(
                self.loader.context, username)

            print(f"Парсим профиль: {profile.username}")
            print(f"Полное имя: {profile.full_name}")
            print(f"Биография: {profile.biography}")
            print(f"Количество постов: {profile.mediacount}")
            print(f"Количество подписчиков: {profile.followers}")
            print(f"Количество подписок: {profile.followees}\n")
            print(
                f"Ссылка на профиль: https://instagram.com/{profile.username}\n\n")

            self.download_posts_as_images(username)
            self.download_posts_as_videos(username)
            self.download_reels(username)
            self.download_stories(username)

        except instaloader.exceptions.ProfileNotExistsException:
            print(f"Профиль {username} не найден.")

        except instaloader.exceptions.InstaloaderException as e:
            print(f"Ошибка при парсинге: {str(e)}")


class PostHandler:
    def __init__(self, loader):
        self.loader: instaloader.Instaloader = loader

    def download_post_by_url(self, post_url: str, save_path: str):
        try:
            post = instaloader.Post.from_shortcode(
                self.loader.context, self._get_shortcode_from_url(post_url))
            self.loader.download_post(post, target=save_path)
            print(f"Пост {post.shortcode} скачан и сохранен в {save_path}")

        except instaloader.exceptions.InstaloaderException as e:
            print(f"Ошибка при скачивании поста: {str(e)}")

    def save_post_info_to_json(self, post_url: str, save_path: str):
        try:
            post = instaloader.Post.from_mediaid(
                self.loader.context, self._get_shortcode_from_url(post_url))

            post_info = {
                "shortcode": post.shortcode,
                "likes": post.likes,
                "comments": post.comments,
                "caption": post.caption,
                "owner_username": post.owner_username,
                "owner_id": post.owner_id,
                "post_url": f"https://www.instagram.com/p/{post.shortcode}/",
            }

            with open(os.path.join(save_path, f"{post.shortcode}_info.json"), "w", encoding="utf-8") as json_file:
                json.dump(post_info, json_file, ensure_ascii=False, indent=4)

            print(f"Информация о посте {post.shortcode} записана в {save_path}")

        except instaloader.exceptions.InstaloaderException as e:
            print(f"Ошибка при сохранении информации о посте: {str(e)}")

    def save_comments_to_json(self, post_url: str, save_path: str):
        try:
            post = instaloader.Post.from_shortcode(
                self.loader.context, self._get_shortcode_from_url(post_url))

            comments_list = []
            for comment in post.get_comments():
                comments_list.append({
                    "username": comment.owner.username,
                    "comment_text": comment.text,
                    "comment_date": comment.created_at_utc.isoformat(),
                })

            with open(os.path.join(save_path, f"{post.shortcode}_comments.json"), "w", encoding="utf-8") as json_file:
                json.dump(comments_list, json_file,
                          ensure_ascii=False, indent=4)

            print(f"Комментарии к посту {post.shortcode} записаны в {save_path}")

        except instaloader.exceptions.InstaloaderException as e:
            print(f"Ошибка при сохранении комментариев: {str(e)}")

    def _get_shortcode_from_url(self, url: str) -> str:
        return url.split('/')[-2]

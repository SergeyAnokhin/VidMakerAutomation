from moviepy.editor import VideoFileClip, CompositeVideoClip, vfx

def create_video_with_gifsOK(background_path, gif_path, duration=5):
    """
    Создает видео с фоном и двумя анимированными GIF-файлами.
    
    Args:
        background_path (str): Путь к фоновому видео
        gif_path (str): Путь к GIF-файлу
        duration (int): Длительность итогового видео в секундах
        
    Returns:
        VideoFileClip: Итоговый видеоклип
    """
    # Читаем основной фоновый клип
    background_clip = VideoFileClip(background_path).set_duration(duration)

    # Загружаем первый GIF и делаем чёрный цвет прозрачным
    gif1 = VideoFileClip(gif_path).set_duration(duration).fx(vfx.mask_color, color=[0, 0, 0], threshold=100, stiffness=5)
    gif1 = gif1.set_position(("center", "top"))  # Позиционируем первый GIF в нужном месте

    # Загружаем второй GIF и также делаем чёрный цвет прозрачным
    gif2 = VideoFileClip(gif_path).set_duration(duration).fx(vfx.mask_color, color=[0, 0, 0], threshold=100, stiffness=5)
    gif2 = gif2.set_position(("center", "bottom"))  # Позиционируем второй GIF в другом месте

    # Комбинируем клипы
    final_clip = CompositeVideoClip([background_clip, gif1, gif2])

    return final_clip

def create_video_with_gifsKO(background_path, gif_path, duration=5):
    """
    Создает видео с фоном и двумя анимированными GIF-файлами с последовательным наложением.
    
    Args:
        background_path (str): Путь к фоновому видео
        gif_path (str): Путь к GIF-файлу
        duration (int): Длительность итогового видео в секундах
        
    Returns:
        VideoFileClip: Итоговый видеоклип
    """
    # Читаем основной фоновый клип
    background_clip = VideoFileClip(background_path).set_duration(duration)

    # Загружаем первый GIF и делаем чёрный цвет прозрачным
    gif1 = VideoFileClip(gif_path).set_duration(duration).fx(vfx.mask_color, color=[0, 0, 0], thr=100, s=5)
    gif1 = gif1.set_position(("center", "top"))

    # Создаём первый композитный клип с фоном и первым GIF
    first_layer = CompositeVideoClip([background_clip, gif1])

    # Загружаем второй GIF и делаем чёрный цвет прозрачным
    gif2 = VideoFileClip(gif_path).set_duration(duration).fx(vfx.mask_color, color=[0, 0, 0], thr=100, s=5)
    gif2 = gif2.set_position(("center", "bottom"))

    # Создаём финальный композитный клип, накладывая второй GIF поверх первого слоя
    final_clip = CompositeVideoClip([first_layer, gif2])

    return final_clip

if __name__ == "__main__":
    final_clip = create_video_with_gifsKO("Clip1/background_video.mp4", "static/animated2.gif")
    final_clip.write_videofile("output_with_two_gifs.mp4", codec="libx264") 



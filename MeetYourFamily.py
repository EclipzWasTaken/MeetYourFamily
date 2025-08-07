from moviepy import VideoFileClip, ImageClip, TextClip, CompositeVideoClip, concatenate_videoclips, AudioFileClip
import random

# Base video path
base_video_path = "Base Video.mp4"

Dad = ['Von', 'Rogan', 'Reynolds', 'Gillis', 'Downey', 'Diesel']
Mom = ['Sweeney', 'Robbie', 'Olsen', 'Lawrence', 'Johansson', 'Hathaway']
Little_Sis = ['Rodrigo', 'Ortega', 'Grande', 'Carpenter']
Aunt = ['Trump', 'Putin', 'Musk', 'Kim', 'Biden']
Big_sis = ['Mcrae', 'Eilish', 'Charli', 'Beer']
Friend = ['Tate', 'Speed', 'Ross', 'NLE', 'Hart', 'Druski', 'Cenat', 'Black']
Aunty_Daughter = ['SZA', 'Stallion', 'Spice', 'Minaj']


list_of_titles = [['DAD', Dad], ['MOM', Mom], ['AUNT', Aunt], ['LITTLE SIS', Little_Sis], ['BIG SIS', Big_sis], ['FRIEND', Friend], ["Mi Prima", Aunty_Daughter]]

# Load base video
base_clip = VideoFileClip(base_video_path)

# take the first 13 seconds of the base video
base_clip = base_clip.with_duration(13).resized(height=1920, width=1080).without_audio()

# Add text to the base video
base_text = TextClip(text="Meet Your Family", font_size=90, color='blue', font= 'font.ttf', size = (340, 500)).with_duration(13).with_position(("center", 500))
base_clip = CompositeVideoClip([base_clip, base_text])

clips = [base_clip]

# Create text clip for the member's name
for title in list_of_titles:
    text_clip = TextClip(text = title[0], font_size=50, color='blue', font= 'font.ttf', size = (340, 500)).with_duration(5)
    text_clip = text_clip.with_position(('center', 200))
    person_name = random.choice(title[1])
    person_clip = ImageClip(f"images/{title[0].lower()}/{person_name.lower()}.jpg").with_duration(5).with_position("center").resized(height=800)
    person_clip = person_clip.with_position(("center", "center"))
    # Add the text and person clip to the base video
    final_clip = CompositeVideoClip([person_clip, text_clip])
    final_clip = final_clip.resized(height=1920, width=1080)
    #base_clip = concatenate_videoclips([base_clip, person_clip, text_clip])
    clips.append(final_clip)

audio = AudioFileClip('Brother.mp3')


# Concatenate all clips into a final video
final_video = concatenate_videoclips(clips, method="compose")
final_video = final_video.with_audio(audio) # Add audio to the final video
# Save the final video
final_video.write_videofile("MeetYourFamily.mp4", fps=24)
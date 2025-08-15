from moviepy import VideoFileClip, ImageClip, TextClip, CompositeVideoClip, concatenate_videoclips, AudioFileClip, clips_array
import random
from youtube import upload_video


# Initialize Fields
base_length = 7
person_length = 3
video_length = base_length + person_length * 7

def createSubClip():
    sub_clip = VideoFileClip(f'rot_clips/{random.choice(rot_clips)}.mp4').without_audio().with_duration(video_length)
    sub_clip = sub_clip.resized(height=1920, width=1080)
    return sub_clip


def upload():
    upload_video("MeetYourFamily.mp4", "Say Hello to Your New Celebrity Family 😎✨ (You’ve Been Adopted)", 
                 "Ever wonder what it’s like to have famous parents, iconic siblings, and a drama-packed group chat? Well, " 
                 "guess what... you’re in the family now. Let’s meet your celebrity relatives — and yes, one of them definitely cries at award shows."
                 "#YourFamousFamily #CelebrityDNA #WelcomeToTheClique #Israel", privacy_status="public")

Dad = ['Von', 'Rogan', 'Reynolds', 'Gillis', 'Downey', 'Diesel']
Mom = ['Sweeney', 'Robbie', 'Olsen', 'Lawrence', 'Johansson', 'Hathaway']
Little_Sis = ['Rodrigo', 'Ortega', 'Grande', 'Carpenter']
Aunt = ['Trump', 'Putin', 'Musk', 'Kim', 'Biden']
Big_sis = ['Mcrae', 'Eilish', 'Charli', 'Beer']
Friend = ['Tate', 'Speed', 'Ross', 'NLE', 'Hart', 'Druski', 'Cenat', 'Black']
Aunty_Daughter = ['SZA', 'Stallion', 'Spice', 'Minaj']
song = ['Brother', 'grr', 'NLU', 'sus', 'TD']
base_clips = ['Base Video', 'beach', 'beer', 'diva', 'lava', 'water', 'waterfall']
rot_clips = ['bed', 'car', 'hydro', 'mine', 'sub', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10']

list_of_titles = [['DAD', Dad], ['MOM', Mom], ['AUNT', Aunt], ['LITTLE SIS', Little_Sis], ['BIG SIS', Big_sis], ['FRIEND', Friend], ["Mi Prima", Aunty_Daughter]]

# Load base video
base_clip = VideoFileClip(f'base_clips/{random.choice(base_clips)}.mp4')

# take the first 16 seconds of the base video
base_clip = base_clip.with_duration(base_length).resized(height=1920, width=1080).without_audio()

# Add text to the base video
base_text = TextClip(text="Meet Your Family", font_size=160, color='blue', font= 'font.ttf', size = (1400, 900)).with_duration(base_length).with_position(("center", 500))
base_clip = CompositeVideoClip([base_clip, base_text])

clips = [base_clip]

text_clip_final = []

# Create text clip for the member's name
for title in list_of_titles:
    text_clip = TextClip(text = title[0], font_size=200, color='pink', font= 'font.ttf', size = (1000, 700)).with_duration(person_length)
    text_clip = text_clip.with_position(('center', 200))

    # Make new text clip so it can be attached to center of the video
    text_clip_final.append(text_clip)

    person_name = random.choice(title[1])
    person_clip = ImageClip(f"images/{title[0].lower()}/{person_name.lower()}.jpg").with_duration(person_length).with_position("center").resized(height = 1920, width=1080)
    person_clip = person_clip.with_position(("center", "center"))
    clips.append(person_clip)

audio = AudioFileClip(f'songs/{random.choice(song)}.mp3').with_duration(video_length)

# Concatenate all clips into a final video
final_video = concatenate_videoclips(clips, method="compose") # Add audio to the final video

sub_clip = createSubClip()

h = min(final_video.h, sub_clip.h)
sub_clip = sub_clip.resized(height=h)
final_video = final_video.resized(height=h)

num = 1#random.randint(0, 2)
if num == 0:
    final_video = clips_array([[final_video], [sub_clip]])
    print('double')
elif num == 1:
    final_video = clips_array([[final_video, sub_clip], [createSubClip(), createSubClip()]])
    print('quad')
else:
    print('single')

text_clips = concatenate_videoclips(text_clip_final, method="compose").with_position(("center", "center")).with_start(base_length)

final_video = final_video.with_audio(audio)
final_video = CompositeVideoClip([final_video, text_clips])
final_video.write_videofile("MeetYourFamily.mp4", fps=24)

upload()
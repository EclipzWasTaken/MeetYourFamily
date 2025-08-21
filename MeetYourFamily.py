from moviepy import VideoFileClip, ImageClip, TextClip, CompositeVideoClip, concatenate_videoclips, AudioFileClip, clips_array
import random
from youtube import upload_video


# Initialize Fields
base_length = 5
person_length = 3
video_length = base_length + person_length * 7

Dad = ['Von', 'Rogan', 'Reynolds', 'Gillis', 'Downey', 'Diesel']
Mom = ['Sweeney', 'Robbie', 'Olsen', 'Lawrence', 'Johansson', 'Hathaway']
Little_Sis = ['Rodrigo', 'Ortega', 'Grande', 'Carpenter']
Aunt = ['Trump', 'Putin', 'Musk', 'Kim', 'Biden']
Big_sis = ['Mcrae', 'Eilish', 'Charli', 'Beer']
Friend = ['Tate', 'Speed', 'Ross', 'NLE', 'Hart', 'Druski', 'Cenat', 'Black']
Aunty_Daughter = ['SZA', 'Stallion', 'Spice', 'Minaj']
song = ['Brother', 'grr', 'NLU', 'sus', 'TD', 'bar', 'said', 'confidence', 'bryan', 'rock']
base_clips = ['Base Video', 'beach', 'beer', 'diva', 'lava', 'water', 'waterfall']
rot_clips = ['bed', 'car', 'hydro', 'mine', 'sub', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'fish', 'workout', 'tsa', 'phone', 'faces', 'airport', 'soccer', 'familyguy', 'college', 'bath']

list_of_titles = [['DAD', Dad], ['MOM', Mom], ['AUNT', Aunt], ['LITTLE SIS', Little_Sis], ['BIG SIS', Big_sis], ['FRIEND', Friend], ["Mi Prima", Aunty_Daughter]]

def createSubClip() -> VideoFileClip:
    rot_choice = random.randint(0, len(rot_clips) - 1)
    sub_clip = VideoFileClip(f'rot_clips/{rot_clips.pop(rot_choice)}.mp4').without_audio().with_duration(6)
    sub_clip = sub_clip.resized(height=720)
    while len(rot_clips) > 0 and sub_clip.duration < video_length:
        rot_choice = random.randint(0, len(rot_clips) - 1)
        sub_clip = concatenate_videoclips([sub_clip, VideoFileClip(f'rot_clips/{rot_clips.pop(rot_choice)}.mp4').resized(height=720).with_duration(random.randint(6, 12))], method="chain")
    sub_clip = sub_clip.with_duration(video_length)
    return sub_clip

def upload():
    upload_video("MeetYourFamily.mp4", "Say Hello to Your New Celebrity Family 😎✨ (You’ve Been Adopted)", 
                 "Ever wonder what it’s like to have famous parents, iconic siblings, and a drama-packed group chat? Well, " 
                 "guess what... you’re in the family now. Let’s meet your celebrity relatives — and yes, one of them definitely cries at award shows."
                 "#YourFamousFamily #CelebrityDNA #WelcomeToTheClique #Israel #Shorts", privacy_status="public")

# Load base video
base_clip = VideoFileClip(f'base_clips/{random.choice(base_clips)}.mp4')

# take the first 16 seconds of the base video
base_clip = base_clip.with_duration(base_length).resized(height=720).without_audio()

# Add text to the base video
base_text = TextClip(text="Meet Your Family", font_size=160, color='blue', font= 'font.ttf', size = (1400, 900)).with_duration(base_length).with_position(("center", 500))
base_clip = CompositeVideoClip([base_clip, base_text])

clips = [base_clip]

text_clips = [ImageClip('title_images/Meet Your Family.png').with_duration(base_length).with_position(("center", 'center'))]

# Create text clip for the member's name
for title in list_of_titles:
    text_clip = ImageClip(f'title_images/{title[0]}.png').with_duration(person_length).with_position(("center", 'center'))
    text_clips.append(text_clip)

    person_name = random.choice(title[1])
    person_clip = ImageClip(f"images/{title[0].lower()}/{person_name.lower()}.jpg").with_duration(person_length).with_position("center").resized(height = 720)
    person_clip = person_clip.with_position(("center", "center"))
    clips.append(person_clip)

audio = AudioFileClip(f'songs/{random.choice(song)}.mp3').with_duration(video_length)

# Concatenate all clips into a final video
final_video = concatenate_videoclips(clips, method="chain") # Add audio to the final video

sub_clip = createSubClip()

h = min(final_video.h, sub_clip.h)
sub_clip = sub_clip.resized(height=h)
final_video = final_video.resized(height=h)

text_clips = concatenate_videoclips(text_clips, method="chain").with_position(("center", "center"))

final_video = CompositeVideoClip([final_video, text_clips])

TARGET_W, TARGET_H = 1440, 2560
num = 2#random.randint(0, 3)

if num == 0:
    # Double stack (vertical)
    final_video = clips_array([
        [final_video],
        [sub_clip]
    ])
    final_video = final_video.resized((TARGET_W, TARGET_H))
    print('double')

elif num == 1:
    # Quad layout (2x2 grid)
    sub_w, sub_h = TARGET_W // 2, TARGET_H // 2  

    final_resized = final_video.resized((sub_w, sub_h))
    sub_resized = sub_clip.resized((sub_w, sub_h))

    quad = clips_array([
        [final_resized, sub_resized],
        [createSubClip().resized((sub_w, sub_h)), createSubClip().resized((sub_w, sub_h))]
    ])

    final_video = quad.resized((TARGET_W, TARGET_H))
    print('quad')

elif num == 2:
    # Hexa layout (3 rows, 2 columns)
    sub_w, sub_h = TARGET_W // 2, TARGET_H // 3  

    final_resized = final_video.resized((sub_w, sub_h))
    sub_resized = sub_clip.resized((sub_w, sub_h))

    hexa = clips_array([
        [final_resized, sub_resized],
        [createSubClip().resized((sub_w, sub_h)), createSubClip().resized((sub_w, sub_h))],
        [createSubClip().resized((sub_w, sub_h)), createSubClip().resized((sub_w, sub_h))]
    ])

    final_video = hexa.resized((TARGET_W, TARGET_H))
    print('hexa')

else:
    # Single — just resize to Shorts format
    final_video = final_video.resized((TARGET_W, TARGET_H))
    print('single')



final_video = final_video.with_audio(audio)

final_video.write_videofile("MeetYourFamily.mp4", fps=24, preset = 'ultrafast', threads=4)

upload()
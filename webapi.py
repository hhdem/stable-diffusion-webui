# python3 -m venv "venv"
# . venv/bin/activate
# python3 webapi.py
from webui import initialize
initialize()

from modules.script_callbacks import before_ui_callback
before_ui_callback()

from modules.txt2img import txt2img
import json
from flask import Flask
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import hmac

def generateImage():
    id_task = "my-task"
    prompt = "a cat"
    negative_prompt = ""
    prompt_styles = []
    steps = 11
    sampler_index = 0
    restore_faces = False
    tiling = False
    n_iter = 1
    batch_size = 1
    cfg_scale = 7
    seed = -1
    subseed = -1
    subseed_strength = 0
    seed_resize_from_h = 0
    seed_resize_from_w = 0
    seed_enable_extras = False
    height = 512
    width = 512
    enable_hr = False
    denoising_strength = 0.7
    hr_scale = 2.0
    hr_upscaler = "Latent"
    hr_second_pass_steps = 0
    hr_resize_x = 0
    hr_resize_y = 0
    override_settings_texts = []
    # 1 girl  [] 11 0 False False 1 1 7 -1.0 -1.0 0 0 0 False 512 512 False 0.7 2 Latent 0 0 0 []
    images, info_str, _ , _ = txt2img(id_task, prompt, negative_prompt, prompt_styles, steps, sampler_index,
                        restore_faces, tiling, n_iter, batch_size, cfg_scale, seed, subseed,
                        subseed_strength, seed_resize_from_h, seed_resize_from_w, seed_enable_extras,
                        height, width, enable_hr, denoising_strength, hr_scale, hr_upscaler,
                        hr_second_pass_steps, hr_resize_x, hr_resize_y, override_settings_texts, 0)
    # print output parameters
    info = json.loads(info_str)
    print(json.dumps(info, indent=4))

    # save images
    for i, image in enumerate(images):
        filename = f"{id_task}-{i}.png"
        image.save(filename)
        return f"Saved {filename} ({image.size[0]}x{image.size[1]} pixels"

def safe_str_cmp(a: str, b: str) -> bool:
    """This function compares strings in somewhat constant time. This
    requires that the length of at least one string is known in advance.

    Returns `True` if the two strings are equal, or `False` if they are not.
    """

    if isinstance(a, str):
        a = a.encode("utf-8")  # type: ignore

    if isinstance(b, str):
        b = b.encode("utf-8")  # type: ignore

    return hmac.compare_digest(a, b)

class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __str__(self):
        return "User(id='%s')" % self.id

users = [
    User(1, 'user1', 'abcxyz'),
    User(2, 'user2', 'abcxyz'),
]

username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}

def authenticate(username, password):
    user = username_table.get(username, None)
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user

def identity(payload):
    user_id = payload['identity']
    return userid_table.get(user_id, None)

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'super-secret'

jwt = JWT(app, authenticate, identity)

@app.route("/generate")
@jwt_required()
def generate():
    # result = generateImage()
    return f"<p>Hello, World!</p>"

if __name__ == '__main__':
    app.run()
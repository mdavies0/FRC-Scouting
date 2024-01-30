# FRC Scouting Template
---
This repository serves as a template for making data input fields for scouting in FRC competitions. It is scripted using python and uses the pygame GUI module.

Data from the QR codes can be handled however it is needed, but we are working on an android app solution to do this for you, putting the data in a .csv file. It can be found [here](https://github.com/PIPIPIG233666/scouting_app).

The data will come out in this order: match number, team color, team number, start position, auton top cones, auton middle cones, auton bottom cones, auton top cubes, auton middle cubes, auton bottom cubes, auton charging station status, auton left community, teleop top cones, teleop middle cones, teleop bottom cones, teleop top cubes, teleop middle cubes, teleop bottom cubes, links scored, endgame charging station/community status, penalties, breakdown, tipping, defense, comments/defense description

## Installation and Running
Python is required for running. If it is not already installed, you can download and install it from [here](https://www.python.org/downloads/). When installing, make sure to select "Add Python 3.xx to PATH" when prompted.
Running the scouting app requires the modules pygame, qrcode, and Pillow to be installed. Running "teamfinder.py" requires the modules tbapy and pyperclip. You can install all of them with this command, from your command line:
`pip install pygame qrcode Pillow tbapy pyperclip`

When these modules are installed, clone this repository and run "main.py". Every time a QR Code is generated, it will be saved to the "QR Codes" folder with the date, match number, and team number selected.

If git is installed, you can copy and paste this command to clone this repository and install required packages at the same time: `git clone https://github.com/TotsIsTots/573_Scouting_2023 && pip install pygame qrcode Pillow tbapy pyperclip`

## Settings
The settings are stored in the "main_config.ini" file. It looks like this inside:
```ini
[Matches]
# list of event matches
match_list = 
default_alliance_color = red
default_alliance_number = 1

[Scrolling]
# Scrolling speed per scroll increment (in pixels)
scroll_speed = 20

# scrollable height in pixels
display_height = 1400  

[Window]
# window size in pixels
screen_w = 900 
screen_h = 600

window_caption = FRC Scouting
window_icon_path = Assets/icon.png
background_path = Assets/background.png

[ActionButtons]
# position of "Generate" and "Reset" buttons in pixels
action_buttons_pos = 20, 1350

# size of "Generate" and "Reset" buttons in pixels
action_buttons_size = 40

# rgb values for the "Generate" and "Reset" buttons
generate_button_color = 0, 200, 0
generate_text_color = 255, 255, 255
reset_button_color = 0, 0, 200
reset_text_color = 255, 255, 255

[QRCodes]
# size of the qr code in pixels
display_size = 512

#save location for qr codes
save_path = QR Codes
```
To change any values, open the file in a text editor and replace the default values with the new ones you want.

To have multiple scouting apps (for example, pit scouting and match scouting), make a copy of "main.py" and name it soemthing else. Then, copy the "main_config.ini" file and rename it to "filename_config.ini". For example, the config file for "pit_scouting.py" would be "pit_scouting_config.ini".
## Auto Team Number Selection
The team numbers for the event matches can be set manually or automatically. To set them manually, open the config file and change "match_list". When running the program with auto team number selection, the team will be the color and number specified in the config file by default. In the config file, the default alliance color is "red" and the default alliance number is "1". This means that the default team number will be the first team in the red alliance.
### Manually
To automattically present the team numbers for the current match in your event, set match_list to be a list of dictionaries with the following format in the example below:
```matches = [{'red': ['1596', '4715', '7782'], 'blue': ['6079', '7823', '5505']}, {'red': ['5216', '4827', '6112'], 'blue': ['6345', '4391', '5230']}, ...]```
This is would it would look like for the 2022 Michigan Escanaba event, shown [here](https://www.thebluealliance.com/event/2022miesc).

### Automatically
Alternitively, you can run "teamfinder.py" with an internet connection. When running, it will prompt you for an event code. This is the code that is used in the URL for the event on The Blue Alliance. For example, the event code for the 2022 Michigan Escanaba event is "2022miesc". You can find the event code by going to the event on The Blue Alliance and copying the last part of the URL. It will look something like this: "https://www.thebluealliance.com/event/2022miesc". The event code is the part after the last "/". In this case, it is "2022miesc". It will then copy the formatted qualification matches to your clipboard, so you can paste it into the config file.


## Input/Display Fields
Every input field has values that can be changed at and/or after initialization. They are listed here with their variable types. if there is an "=" after a value, it is optional and a default value is listed. Obviously, a value defined at initialization is already defined for after initialization. Each has methods, most include an update(), draw(self), and handleInput() methods which are already handled in the code and will not be listed here. The TextField object has a special method listed below.

### Header
**At initialization:**
- y: float
- title: str
- size: int
- thickness: float = 2
- color: tuple = (180, 180, 180)
- bold: bool = True

**After Initialization:**
- y: float
- size: int
- thickness: float = 2
- color: tuple = (180, 180, 180)
- title_font: [pygame.font.SysFont](https://www.pygame.org/docs/ref/font.html#pygame.font.SysFont) = pg.font.SysFont('arial', size (from init), bold (from init))

### Counter
**At initialization:**
- x: float
- y: float
- size: int
- value: int = 0

**After Initialization:**
- x: float
- y: float
- value: int = 0 

### Dropdown
**At initialization:**
- x: float
- y: float
- width: float
- height: float
- options: list (of strings)
- title: str = ""
- title_size: int = 14
- title_placement: str = "u" (u and r are accepted)

**After initialization:**
- x: float
- y: float
- width: float
- height: float
- selected_num = -1
- opened: bool = 0
- border_thickness: float = 4
- inner_border_thickness: float = 2
- border_color: tuple = (180, 180, 180)
- background_color: tuple = (20, 20, 20)

### Checkmark
**At initialization:**
- x: float
- y: float
- title: str
- size: int
- check_placement: str = 'l' (u, d, l, and r are accepted)

**After initialization:**
- y: float
- title: str
- title_color: tuple = (180, 180, 180)
- title_font: [pygame.font.SysFont](https://www.pygame.org/docs/ref/font.html#pygame.font.SysFont) = pg.font.SysFont('arial', size)
- box_thickness: float = 4
- box_color: tuple = (20, 20, 20)
- box_border_color: tuple = (180, 180, 180)
- value: bool = False

### MultiCheckmark
**At initialization:**
- checkmarks: list (of [Checkmark](#checkmark) objects)


### TextField
**At initialization:**
- x: float
- y: float
- width: float
- height: float
- text_size: int
- border_thickness: float = 4
- title: str = ''
- title_size: str = 14

**After initialization:**
- y: float
- height: float
- font_color: tuple = (180, 180, 180)
- font: [pygame.font.SysFont](https://www.pygame.org/docs/ref/font.html#pygame.font.SysFont) = pg.font.SysFont('arial', text_size)
- content: list (of str) = ['']
- color: tuple = (20, 20, 20)
- unselected_color: tuple = (128, 128, 128)
- selected_color: tuple = (180, 180, 180)
- selected: bool = False
- cursor_color: tuple = (180, 180, 180)

**Methods:**
> get_string(self) -> str

When called on a TextField object, it will return a single string of the compiled content in the object with "\n" used for new lines. 

### TeamColorToggle
**At initialization:**
- x: float
- y: float
- title: str
- size: int
- box_placement: str = 'l' (u, d, l, and r are accepted)

**After initialization:**
- y: float
- box_thickness: float = 4
- box_color: tuple = (255, 0, 0)
- box_border_color: tuple = (180, 180, 180)
- value: str = 'red'

### ImageArray
**At initialization:**
- x: float
- y: float
- width: int
- height: int
- image_path_list: list (of str)
- title: str = ''
- title_size: int = 14
- default_image: int = 0
- linked_object: [TeamColorToggle](#teamcolortoggle) or [Dropdown](#dropdown) = None

**After initialization:**
- y: float
- image_path_list: list (of str)

## Field Initialization
Initialization of the fields we use can be found in the main function.
```python
[...]
    # Initialize data input objects and headers here, QR code lists data in order of initialization
    prematch_header = UI_Elements.Header(32, 'Prematch', 24)
    
    start_position_image = UI_Elements.ImageArray(550, 70, 164, 183, ['assets/red side.png', 'assets/blue side.png'], title='Starting Position', title_size=24, linked_object=team_color)
    start_positions = UI_Elements.MultiCheckmark([UI_Elements.Checkmark(625, 80, '', 32), UI_Elements.Checkmark(625, 145, '', 32), UI_Elements.Checkmark(625, 210, '', 32)])

    auton_header = UI_Elements.Header(270, 'Autonomous', 24)

    a_top_cone = UI_Elements.Counter(20, 300, 48, 0, 'Top cones', 24, 'r')
    a_mid_cone = UI_Elements.Counter(20, 350, 48, 0, 'Mid cones', 24, 'r')
    a_bot_cone = UI_Elements.Counter(20, 400, 48, 0, 'Bot cones', 24, 'r')

    a_top_cube = UI_Elements.Counter(300, 300, 48, 0, 'Top cubes', 24, 'r')
    a_mid_cube = UI_Elements.Counter(300, 350, 48, 0, 'Mid cubes', 24, 'r')
    a_bot_cube = UI_Elements.Counter(300, 400, 48, 0, 'Bot cubes', 24, 'r')

    a_charging_station = UI_Elements.Dropdown(
        590, 305, 100, 32, ['No', 'Docked', 'Engaged'], 'Charging Station', 20)
    a_charging_station_example = UI_Elements.ImageArray(700, 305, 120, 120, ['assets/empty.png', 'assets/docked.png', 'assets/engaged.png'], linked_object=a_charging_station)
    a_left_community = UI_Elements.Checkmark(590, 450, 'Left Community', 32)

    teleop_header = UI_Elements.Header(500, 'Teleop', 24)

    t_top_cone = UI_Elements.Counter(20, 530, 48, 0, 'Top cones', 24, 'r')
    t_mid_cone = UI_Elements.Counter(20, 580, 48, 0, 'Mid cones', 24, 'r')
    t_bot_cone = UI_Elements.Counter(20, 630, 48, 0, 'Bot cones', 24, 'r')

    t_top_cube = UI_Elements.Counter(300, 530, 48, 0, 'Top cubes', 24, 'r')
    t_mid_cube = UI_Elements.Counter(300, 580, 48, 0, 'Mid cubes', 24, 'r')
    t_bot_cube = UI_Elements.Counter(300, 630, 48, 0, 'Bot cubes', 24, 'r')

    links_scored = UI_Elements.Counter(590, 550, 48, 0, 'Links Scored', 24)

    endgame_header = UI_Elements.Header(730, 'Endgame', 24)

    e_charging_station = UI_Elements.Dropdown(20, 770, 150, 32, [
                                              'No', 'Parked', 'Docked', 'Engaged'], 'Charging Station/Community', 24)
    e_charging_station_example = UI_Elements.ImageArray(180, 770, 150, 150, ['assets/empty.png', 'assets/parked.png', 'assets/docked.png', 'assets/engaged.png'], linked_object=e_charging_station)

    postmatch_header = UI_Elements.Header(960, 'Postmatch', 24)

    penalties = UI_Elements.Checkmark(20, 1000, 'Penalties?', 32)

    breakdown = UI_Elements.Checkmark(20, 1050, 'Robot Breakdown?', 32)

    defense = UI_Elements.Dropdown(20, 1130, 380, 40, [
                                   "Didn't Play", "Played Poorly", "Played Some Well", "Completely Played Very Well"], 'Defense', 24)

    comments = UI_Elements.TextField(
        420, 1000, 330, 300, 24, title='Comments/Breakdown Details', title_size=24)
[...]
```
Indents under examples are just formatting and are not required, it can all be on one line.

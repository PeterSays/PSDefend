import copy
import os
import signal
import random
import pygame
from pygame.locals import *

from Unit import Unit
from Tile import Tile
from Team import Team
from Material import Material
from Skill import Skill
from Interface import Interface, Option, Counter, Die, SplashCounter
from Animated import Animated
import petools

pygame.init()
# pygame.mixer.init()
pygame.font.init()
fps = 60
fpsClock = pygame.time.Clock()
frame = -1
tilesize = 32
moves_left = 0
col_num = 20
row_num = 15
scr_width = tilesize * col_num
guibar_size = (scr_width, 35)
scr_height = (tilesize * row_num) + guibar_size[1]
screen = pygame.display.set_mode((scr_width, scr_height))
bg_color = pygame.Color(0, 0, 0)
selected_object = None
select_phase = None
routine_list = []
unit_list = []
team_list = []
tile_array = []
tile_list = []
interface_list = []
animinterf_list = []
option_list = []
splashcounter_list = []

displaying = [
    [],  # tiles
    [],  # units
    []  # text/interface/effects
]

if True:
    tilesets = ['grass']
    punch = Skill('Punch', 'attack', 90, 110, move_cost=1, hp_cost=5, bash=2, user_anim='punch', target_anim='bash_3delay')
    chop = Skill('Chop', 'attack', 90, 110, move_cost=1, hp_cost=5, cut=2, target_anim='slash')
    wood_mat = Material('wood', 'wood', (150, 75, 0), (130, 90, 0), bash_resist=1.2, cut_resist=0.8, temp_conduct=0.5)
    stone_mat = Material('stone', 'stone', (75, 75, 75), (65, 50, 50), bash_resist=0.8, cut_resist=1.2, temp_conduct=0.7, heat_dam=300)
    metal_mat = Material('metal', 'metal', (170, 170, 170), (120, 120, 135), bash_resist=0.8, cut_resist=1.2, temp_conduct=2.0, cold_dam=-200, heat_dam=250)
    base_attr = {
        'control_point': {
            'stats': {'hp': 100, 'mp': 10, 'strength': 0, 'toughness': 5, 'agility': 0, 'intelligence': 5},
            'material': metal_mat
        },
        'infotower': {
            'stats': {'hp': 20, 'mp': 0, 'strength': 0, 'toughness': 5, 'agility': 0, 'intelligence': 3},
            'material': metal_mat
        },
        'rune_pillar': {
            'stats': {'hp': 20, 'mp': 15, 'strength': 0, 'toughness': 4, 'agility': 0, 'intelligence': 0},
            'material': stone_mat
        }
    }
    build_attr = {
        'wood_wall': {
            'stats': {'hp': 20, 'mp': 0, 'strength': 0, 'toughness': 4, 'agility': 0, 'intelligence': 0},
            'material': wood_mat
        }
    }
    unit_attr = {
        'peter_says': {
            'stats': {'hp': 10, 'mp': 10, 'strength': 3, 'toughness': 3, 'agility': 3, 'intelligence': 3},
            'skills': [punch, chop],
            'material': None
        },
        'joe': {
            'stats': {'hp': 10, 'mp': 10, 'strength': 3, 'toughness': 3, 'agility': 3, 'intelligence': 3},
            'skills': [punch, chop],
            'material': None
        }
    }


def is_clicked(has_rect_list, mark=False):
    mouse_pos = pygame.mouse.get_pos()
    for has_rect in has_rect_list:
        if has_rect.rect.x <= mouse_pos[0] <= has_rect.rect.x + has_rect.rect.width and has_rect.rect.y <= mouse_pos[1] <= has_rect.rect.y + has_rect.rect.height:
            return has_rect
    return False


# These functions are for constructing objects within the context of the game!
# This way I don't have to worry about what the class-defining scripts have access to.
def generate_unit_options(selected_unit: Unit):
    new_options = []

    xoffset = round(selected_unit.rect.width * 1.5)
    yoffset = -30
    yoffset_incr = 30

    if selected_unit.x + xoffset > scr_width-24:
        xoffset = xoffset * -1
    if selected_unit.y + yoffset > scr_height-20:
        yoffset_incr += 30
        yoffset_incr = yoffset_incr * -1

    if selected_unit.movement_cost and len(selected_unit.open_adjacents()):
        if selected_unit.team.movepoints >= selected_unit.movement_cost:
            move_option = Option('Move Option', selected_unit.x + xoffset, selected_unit.y, text_val='Move')
            new_options.append(move_option)

    for skil in selected_unit.skill_list:
        if len(selected_unit.in_range(skil)) and selected_unit.team.movepoints >= skil.move_cost and selected_unit.hp >= skil.hp_cost and selected_unit.mp >= skil.mp_cost:
            skill_option = Option(f'{skil.name} Option', selected_unit.x + xoffset, selected_unit.y, text_val=skil.name, skill=skil)
            new_options.append(skill_option)

    opt_ind = 0
    for optio in new_options:
        opt_ind += 1
        optio.y += yoffset*opt_ind
        optio.rect.y = optio.y-2
        yoffset += yoffset_incr

    return new_options


def make_base(name, spritename, starttile):
    base_unit = Unit(name, spritename, starttile, base_attr[spritename]['stats'], is_base=True)
    routine_list.append(base_unit)
    displaying[1].append(base_unit)
    return base_unit


def make_team(name, base_spritename, base_starttile, teamcolor, computer=False):
    new_base = make_base(f'{name} Base', base_spritename, base_starttile)
    new_team = Team(name, new_base, comp=computer, color=teamcolor)
    new_base.team = new_team
    routine_list.append(new_team)
    team_list.append(new_team)
    return new_team


def make_unit(name, spritename, team_, specific_spawntile=None):
    empt_list = team_.base.on_tile.nearby_empty()
    if not specific_spawntile and len(empt_list):
        specific_spawntile = random.choice(empt_list)
        new_unit = Unit(name, spritename, specific_spawntile, unit_attr[spritename]['stats'], skill_list=unit_attr[spritename]['skills'])
        new_unit.team = team_
        team_.members.append(new_unit)
        routine_list.append(new_unit)
        unit_list.append(new_unit)
        displaying[1].insert(0, new_unit)
        return new_unit
    else:
        print(empt_list)
        return False


def make_animinterf(foldername, x, y, frametime=3, loop=0):
    # for reference: base animations
    anim_seq = []
    folder_path = f'{os.curdir}/interface/{foldername}'
    file_list = os.listdir(folder_path)
    file_list = sorted(file_list)
    for filename in file_list:
        frame_img = pygame.image.load(f'{folder_path}/{filename}')
        anim_seq.append(frame_img)
    this_anim = Animated(foldername, anim_seq, x=x, y=y, loop=loop, frametime=frametime)
    animinterf_list.append(this_anim)
    return this_anim


def make_splashcounter(name, x, y, num_val, fontname='ubuntumono', fontsize=24, fontcolor=(0, 0, 0)):
    new_scounter = SplashCounter(name, x, y, num_val, fontname=fontname, fontsize=fontsize, fontcolor=fontcolor)

    return new_scounter

def calc_damage(user, target, skill):
    if not skill.magic:
        base_dmg = user.strength
    else:
        base_dmg = user.
    skill_power = random.randint(skill.power_minimum, skill.power_maximum)


def use_skill(user, target, skill):
    if skill.user_anim:
        user_anim = make_animinterf(skill.user_anim, going_unit.x, going_unit.y, loop=1)
        user_anim.x = user.x + user.x_offset
        user_anim.y = user.y + user.y_offset

        # ua_wid = user_anim.sprite.get_rect().width
        # ua_hig = user_anim.sprite.get_rect().height
        # if ua_wid < 32:
        #    user_anim.x_offset = 32 - ua_wid
        # elif ua_wid > 32:
        #    user_anim.x_offset = ua_wid - 32

        # if ua_hig < 32:
        #    user_anim.y_offset = 32 - ua_hig
        # elif ua_hig > 32:
        #    user_anim.y_offset = ua_hig - 32

    for r in range(skill.repeats):
        for aoe_offset in skill.aoe:
            aoe_xoffset = aoe_offset[0]
            aoe_yoffset = aoe_offset[1]
            this_target =
            if col_num-1 >= aoe_xoffset and row_num-1 >= aoe_yoffset:

            if skill.target_anim:
                target_anim = make_animinterf(skill.target_anim, going_unit.x, going_unit.y, loop=1)
                target_anim.x = target.x + target.x_offset
                target_anim.y = target.y + target.y_offset

                dam_scounter = SplashCounter('Damage', target.x, target.y, 10)
                splashcounter_list.append(dam_scounter)

                #ta_wid = target_anim.sprite.get_rect().width
                #ta_hig = target_anim.sprite.get_rect().height
                #if ta_wid < 32:
                #    target_anim.x_offset = 32 - ta_wid
                #elif ta_wid > 32:
                #    target_anim.x_offset = ta_wid - 32

                #if ta_hig < 32:
                #    target_anim.y_offset = 32 - ta_hig
                #elif ta_hig > 32:
                #    target_anim.y_offset = ta_hig - 32




def initialize_map(thismap, tile_name):
    mapsiz = (row_num, col_num)
    for row_no in range(row_num):
        new_row = []
        for col_no in range(col_num):
            tn_suffix = '_'
            if (row_no % 2 == 1 and col_no % 2 == 0) or (row_no % 2 == 0 and col_no % 2 == 1):  # alternate between color variants
                tn_suffix += 'a'
            else:
                tn_suffix += 'b'
            new_col = Tile(row_no, col_no, tile_name+tn_suffix, mapsiz, guibar_size[1])
            tile_list.append(new_col)
            displaying[0].append(new_col)
            new_row.append(new_col)
        thismap.append(new_row)

    for nr in thismap:
        for nc in nr:
            nc.initialize(thismap)


def initialize_teams(players_no, teams_no=4):
    players_unassigned = players_no
    neutral_made = False
    for t in range(teams_no+1):
        is_comp = True
        teamname = f'Team {t+1}'
        team_basename = random.choice(list(base_attr.keys()))
        team_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        spawn_col = random.randint(0, col_num - 1)
        spawn_row = random.randint(0, row_num - 1)
        teamspawn = tile_array[spawn_row][spawn_col]

        if players_unassigned > 0:
            is_comp = False
            players_unassigned -= 1
        elif not neutral_made:
            teamname = 'Neutral'
            team_basename = 'control_point'
            team_color = (111, 111, 111)
            teamspawn = tile_array[round(row_num/2)-1][round(col_num/2)-1]
            neutral_made = True

        while not teamspawn or teamspawn.unit_here:
            teamspawn = random.choice(teamspawn.surround_list())

        thisteam = make_team(teamname, team_basename, teamspawn, team_color, computer=is_comp)
        for interf in thisteam.interfaces:
            interface_list.append(interf)
            displaying[2].append(interf)


# starts here
initialize_map(tile_array, random.choice(tilesets))
initialize_teams(1, teams_no=2)

for team in team_list:
    for sd in range(5):
        chos = random.choice(list(unit_attr.keys()))
        unit_name = chos
        unit_sprite = chos
        nu = make_unit(unit_name, unit_sprite, team)

turn_index = random.randint(0, len(team_list)-1)
going_unit = None
going_skill = None
frame_num = -1
while True:
    going_team = team_list[turn_index]
    frame_num += 1
    screen.fill(bg_color)
    pressed_keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == QUIT:
            os.kill(os.getpid(), signal.SIGKILL)

        elif event.type == KEYDOWN:
            if event.key == pygame.K_SPACE:
                print(f'Selected Phase: {select_phase}')
                print(f'Selected Object: {selected_object}')
                print(f'Going Unit: {going_unit}')
            
        elif event.type == MOUSEBUTTONDOWN:  # and not going_team.comp
            if select_phase == 'option':
                # if option clicked, set selected_object to that
                # otherwise exit menu
                option_clicked = is_clicked(option_list)
                if option_clicked:
                    selected_object = option_clicked
                    option_clicked = None
                    option_list = []
                    if selected_object.name == 'Move Option':
                        going_team.movepoints -= going_unit.movement_cost
                        select_phase = 'nearby tile'
                        selected_object = None

                    elif selected_object.skill:
                        going_team.movepoints -= selected_object.skill.move_cost
                        going_skill = selected_object.skill
                        select_phase = f'target'
                        selected_object = None

                elif is_clicked(tile_list):
                    option_list = []
                    for m in going_team.members:
                        m.clicked = False
                        m.going = False
                    select_phase = 'unit'
                    selected_object = None

            elif select_phase == 'nearby tile':
                clicked_obj = is_clicked(going_unit.open_adjacents())
                if clicked_obj:
                    selected_object = clicked_obj

            elif select_phase == 'unit':
                clicked_obj = is_clicked(unit_list)
                if clicked_obj and clicked_obj in going_team.members:
                    new_option_list = generate_unit_options(clicked_obj)
                    if len(new_option_list):
                        selected_object = clicked_obj

            elif select_phase == 'target':
                clicked_obj = is_clicked(going_unit.in_range(going_skill))
                if clicked_obj:
                    selected_object = clicked_obj

            if selected_object:
                selected_object.clicked = True

    if not going_team.going:
        for inter in going_team.interfaces:
            if inter not in displaying[2]:
                displaying[2].append(inter)
        selected_object = None
        select_phase = 'unit'
        going_team.turn_start()

    elif going_team.done:
        going_team.turn_end()
        turn_index += 1
        if turn_index >= len(team_list):
            turn_index = 0

    elif select_phase == 'unit' and selected_object:
        going_unit = selected_object
        going_unit.going = True
        selected_object = None
        select_phase = 'option'
        option_list = generate_unit_options(going_unit)

    elif select_phase == 'nearby tile' and selected_object:
        going_unit.on_tile.unit_here = None
        going_unit.on_tile = selected_object
        selected_object.unit_here = going_unit
        going_unit.dest_x = selected_object.x
        going_unit.dest_y = selected_object.y
        going_unit.going = False
        going_unit = None
        if going_team.movepoints <= 0:
            going_team.done = True
        else:
            select_phase = 'unit'
            selected_object = None

    elif select_phase == 'target' and selected_object:
        use_skill(going_unit, selected_object, going_skill)

        going_unit.going = False
        going_unit = None
        if going_team.movepoints <= 0:
            going_team.done = True
        else:
            select_phase = 'unit'
            selected_object = None

    for routine_haver in routine_list:
        routine_haver.routine()
    for option in option_list:
        option.routine()

    destscounter_list = []
    for scounter in splashcounter_list:
        scounter.routine()
        if scounter.destroy:
            destscounter_list.append(scounter)

    for destscounter in destscounter_list:
        if destscounter in splashcounter_list:
            splashcounter_list.remove(destscounter)

    # Rendering
    for dl_index in range(len(displaying)):

        if dl_index == 1:  # team markers
            for t in team_list:
                team_units = copy.copy(t.members)
                team_units.append(t.base)
                for m in team_units:
                    x_shake = 0
                    y_shake = 0
                    if t.going:
                        x_shake = 1
                    if m.going:
                        x_shake += 7
                        y_shake = 1
                    outline_rect = pygame.Rect(m.on_tile.rect.x + random.randint(-1 * x_shake, x_shake), m.on_tile.rect.y + random.randint(-1 * y_shake, y_shake), 32, 32)
                    pygame.draw.rect(screen, m.team.color, outline_rect, width=2, border_radius=1)

        dl = displaying[dl_index]
        for displayed_obj in dl:
            if displayed_obj.visible:
                screen.blit(displayed_obj.sprite, (displayed_obj.x+displayed_obj.x_offset, displayed_obj.y+displayed_obj.y_offset))

    for scounter in splashcounter_list:  # routine called above
        if scounter.visible:
            screen.blit(scounter.sprite, (scounter.x, scounter.y))

    destaniminterf_list = []
    for animterf in animinterf_list:
        if animterf.visible:
            screen.blit(animterf.sprite, (animterf.x+animterf.x_offset, animterf.y+animterf.y_offset))
        animterf.advance()
        if animterf.destroy:
            destaniminterf_list.append(animterf)

    for destaniminterf in destaniminterf_list:
        if destaniminterf in animinterf_list:
            animinterf_list.remove(destaniminterf)
    destaniminterf_list = []

    for opt in option_list:
        bg_rect = pygame.Rect(opt.rect.x, opt.rect.y, opt.rect.width, opt.rect.height)
        pygame.draw.rect(screen, opt.bg_color, bg_rect, width=0)

        outline_rect = pygame.Rect(opt.rect.x, opt.rect.y, opt.rect.width, opt.rect.height)
        pygame.draw.rect(screen, opt.outline_color, outline_rect, width=2, border_radius=1)

        screen.blit(opt.sprite, (opt.x, opt.y))

    pygame.display.flip()
    fpsClock.tick(fps)

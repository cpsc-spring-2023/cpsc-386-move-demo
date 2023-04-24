

import os
import pygame

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, "data")

asset_dict = {
  'suck1': 'zapsplat_foley_balloon_pump_suck_in_water_bubbles_gurgle_squelch_003_46240.mp3',
  'suck2': 'food_drink_straw_suck_air_dregs_soda.mp3',
  'suck3': 'zapsplat_foley_balloon_pump_in_water_single_suck_hiss_gurgle_46237.mp3',
  'explosion': 'jessey_drake_oldschool_DEATH_EXPLOSION_2_video_retro_game_chip_set_8BIT_XPO_JD.mp3',
}

def get(key):
  x = asset_dict.get(key, None)
  if x:
    x = os.path.join(data_dir, x)
  return x



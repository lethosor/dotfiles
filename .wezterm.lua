local wezterm = require 'wezterm'
local config = wezterm.config_builder()

-- Window
config.initial_cols = 96
config.initial_rows = 25

config.enable_scroll_bar = true
config.use_resize_increments = true
config.window_padding = {
  left = 1,
  right = 10,  -- scroll bar
  top = 1,
  bottom = 1,
}

config.window_frame = {
  font = wezterm.font{family='Ubuntu', weight='Bold'},
}

-- Cursor
config.default_cursor_style = 'BlinkingBar'
config.cursor_blink_ease_in = 'Constant'
config.cursor_blink_ease_out = 'Constant'

-- Colors
-- config.color_scheme = 'Monokai (light) (terminal.sexy)'
-- config.color_scheme = 'Material Lighter (base16)'
-- config.color_scheme = 'Github Light (Gogh)'
-- config.color_scheme = 'Google (light) (terminal.sexy)'
-- config.color_scheme = 'Atelier Forest Light (base16)'
local TAB_BG_INACTIVE = '#DCD8D4'
local TAB_FG = '#333'
config.colors = {
  foreground = '#2e3436',
  background = '#ffffff',

  scrollbar_thumb = '#aaa',

  ansi = {
    'rgb(46,52,54)',
    'rgb(204,0,0)',
    'rgb(71,140,6)',
    'rgb(196,106,0)',
    'rgb(52,101,164)',
    'rgb(117,80,123)',
    'rgb(6,152,154)',
    'rgb(170,170,170)',
  },
  brights = {
    'rgb(85,87,83)',
    'rgb(239,41,41)',
    'rgb(122,202,45)',
    'rgb(252,172,79)',
    'rgb(114,159,207)',
    'rgb(173,127,168)',
    'rgb(63,205,205)',
    'rgb(255,255,255)',
  },

  tab_bar = {
    active_tab = {
      bg_color = '#F6F5F4',
      fg_color = TAB_FG,
    },
    inactive_tab = {
      bg_color = TAB_BG_INACTIVE,
      fg_color = TAB_FG,
      strikethrough=true,
    },
    inactive_tab_hover = {
      bg_color = '#E6E3E0',
      fg_color = TAB_FG,
    },
  },
}
config.colors.tab_bar.new_tab = config.colors.tab_bar.inactive_tab
config.colors.tab_bar.new_tab_hover = config.colors.tab_bar.inactive_tab_hover
config.bold_brightens_ansi_colors = false

config.window_frame.inactive_titlebar_bg = TAB_BG_INACTIVE
config.window_frame.active_titlebar_bg = TAB_BG_INACTIVE

-- Font
config.font = wezterm.font('DejaVu Sans Mono')
config.font_size = 11
config.freetype_load_target = 'Light'

return config

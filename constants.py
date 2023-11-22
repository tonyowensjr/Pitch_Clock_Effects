################################################################################
# The url for the Baseball Savant data
SAVANT_URL = 'https://baseballsavant.mlb.com/leaderboard/pitch-tempo?game_type={game_type}&n=q&season_end={year}&season_start={year}&split=no&team=&type=Pit&with_team_only=1'

################################################################################
# The columns of the timing data dataframe
TIMING_COLS = ['pitches_empty','tempo_empty','timer_equiv_empty',
              'fast_empty','slow_empty','pitches_on_base','tempo_on_base',
              'timer_on_base','fast_on_base','slow_on_base']
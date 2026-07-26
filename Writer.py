from OklchPlotter import OklchPlotter


# quick and dirty, has to fit with get_stats_csv_line()
def get_stats_csv_header():
    thread_id = 'id'
    # lightness
    median_lightness = 'L med'
    ref_lightness = 'L ref'
    stdev_lightness = 'L std'
    mean_diff_lightness = 'L mean-med'
    mode_val_lightness = 'L max'
    # chroma
    median_chroma = 'C med'
    ref_chroma = 'C ref'
    stdev_chroma = 'C std'
    mean_diff_chroma = 'C mean-med'
    mode_val_chroma = 'C max'
    # hue
    median_hue = 'H med'
    ref_hue = 'H ref'
    stdev_hue = 'H std'
    mean_diff_hue = 'H mean-med'
    mode_val_hue = 'H max'
    stats = [median_lightness, ref_lightness, stdev_lightness, mean_diff_lightness, mode_val_lightness,
             median_chroma, ref_chroma, stdev_chroma, mean_diff_chroma, mode_val_chroma,
             median_hue, ref_hue, stdev_hue, mean_diff_hue, mode_val_hue]
    header = thread_id
    for stat in stats:
        header += ', ' + stat
    header += '\n'
    return header

# quick and dirty, has to fit with get_stats_csv_header()
def get_stats_csv_line(thread: OklchPlotter):
    thread_id = '\"' + thread.thread_pic.thread_id + '\"'
    # lightness
    median_lightness = thread.lightness_stats.median # 'L med'
    ref_lightness = thread.ref_lightness # 'L ref'
    stdev_lightness = int(round(thread.lightness_stats.stdev)) # 'L std'
    mean_diff_lightness = thread.lightness_stats.mean - median_lightness# 'L mean-med'
    mode_val_lightness = thread.lightness_stats.mode_val # 'L max'
    # chroma
    median_chroma = thread.chroma_stats.median # 'C med'
    ref_chroma = thread.ref_chroma # 'C ref'
    stdev_chroma = int(round(thread.chroma_stats.stdev)) # 'C std'
    mean_diff_chroma = thread.chroma_stats.mean - median_chroma # 'C mean-med'
    mode_val_chroma = thread.chroma_stats.mode_val # 'C max'
    # hue
    median_hue = thread.hue_stats.median # 'H med'
    ref_hue = thread.ref_hue # 'H ref'
    stdev_hue = int(round(thread.hue_stats.stdev)) # 'H std'
    mean_diff_hue = thread.hue_stats.mean - median_hue # 'H mean-med'
    mode_val_hue = thread.hue_stats.mode_val # 'H max'
    stats = [median_lightness, ref_lightness, stdev_lightness, mean_diff_lightness, mode_val_lightness,
             median_chroma, ref_chroma, stdev_chroma, mean_diff_chroma, mode_val_chroma,
             median_hue, ref_hue, stdev_hue, mean_diff_hue, mode_val_hue]
    line = thread_id
    for stat in stats:
        line += ', ' + str(stat)
    line += '\n'
    return line

def save_stats_csv(csv_lines: list[str], filename: str):
    with open('./tables/' + filename, 'w') as file:
        file.writelines(csv_lines)



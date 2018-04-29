import glob
import os
import re
import sys


trackers_section_exp = re.compile('trackersll(\d+:.*)ee\d+:')
tracker_len_exp = re.compile('(el)?(\d+):')

print 'Simple tool to replace tracker info in *.fastresume files v0.1'

if len(sys.argv) != 3:
    print 'Usage: ' + sys.argv[0] + ' <old tracker> <new tracker> '
    print '*.fastresume files must be in BT_backup folder beside the script'
    sys.exit(1)

old_text = sys.argv[1]
new_text = sys.argv[2]

os.chdir('BT_backup')

for file in glob.glob('*.fastresume'):
    with open(file, 'rb') as f:
        data = f.read()

    if old_text not in data:
        print 'Skippping ' + file
        continue

    print 'Found item in ' + file
    trackers_section = re.search(trackers_section_exp, data)
    if not trackers_section:
        continue
    trackers = trackers_section.group(1)

    tracker_list = []
    i = 0
    while i < len(trackers):
        len_found = re.search(tracker_len_exp, trackers[i:])
        tracker_len = int(len_found.group(2))
        i += len_found.end()
        tracker = trackers[i:i+tracker_len]
        if tracker.find(old_text) != -1:
            new_tracker = tracker.replace(old_text, new_text)
            print ' Replacing ' + tracker + ' with ' + new_tracker
            tracker = new_tracker
        tracker_list.append(str(len(tracker)) + ':' + tracker)
        i += tracker_len

    data = data.replace(trackers, 'el'.join(tracker_list))
    with open(file, 'wb') as f:
        f.write(data)

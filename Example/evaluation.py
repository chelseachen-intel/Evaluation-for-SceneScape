import json
import matplotlib.pyplot as plt
import numpy as np


class Vividict(dict):
    def __missing__(self, key):
        value = self[key] = type(self)()
        return value


predicted = Vividict()
label = Vividict()

scale = 1
dis_8w = 0  # distance error for Player-8w
dis_2m = 0
frame_8w = 0  # count for paired num of frames
frame_2m = 0
ids_2m = [2]
ids_8w = [1]

with open('outfile.json') as f:
    for line in f:
        jdata = json.loads(line)
        for item in jdata['objects']:

            if not predicted[item['id']]['x']:
                predicted[item['id']]['x'] = [item['position']['x'] * scale]
            else:
                predicted[item['id']]['x'].append(item['position']['x'] * scale)

            if not predicted[item['id']]['y']:
                predicted[item['id']]['y'] = [item['position']['y'] * scale]
            else:
                predicted[item['id']]['y'].append(item['position']['y'] * scale)

            curframe = jdata['frame'] - 1
            gt_name = 'frames/L3FrontCam_' + str(curframe) + '.json'
            with open(gt_name, 'r') as load_f:
                gt = json.load(load_f)

                for obj in gt['objects']:

                    if not label[obj['objectName']]['x']:
                        label[obj['objectName']]['x'] = [obj['wposition']['z']]
                    else:
                        label[obj['objectName']]['x'].append(obj['wposition']['z'])

                    if not label[obj['objectName']]['y']:
                        label[obj['objectName']]['y'] = [obj['wposition']['x']]
                    else:
                        label[obj['objectName']]['y'].append(obj['wposition']['x'])

                    if obj['objectName'] == 'Player8-W' and item['id'] in ids_8w:
                        dis_8w += (np.sqrt((item['position']['x'] * scale - obj['wposition']['z']) ** 2 + (
                                item['position']['y'] * scale - obj['wposition']['x']) ** 2))
                        frame_8w += 1
                    elif obj['objectName'] == 'Player2-M' and item['id'] in ids_2m:
                        dis_2m += (np.sqrt((item['position']['x'] * scale - obj['wposition']['z']) ** 2 + (
                                item['position']['y'] * scale - obj['wposition']['x']) ** 2))
                        frame_2m += 1

mean_dis8 = dis_8w / frame_8w
print('8w', mean_dis8)

mean_dis2 = dis_2m / frame_2m
print('2M', mean_dis2)

plt.figure()
for id, v in label.items():
    plt.plot(label[id]['x'], label[id]['y'], label=id, linewidth=3)
for key, v in predicted.items():
    plt.plot(predicted[key]['x'], predicted[key]['y'], label=key, linewidth=1.5, linestyle=':')

plt.legend()

mess = 'Player_8W:    ' + str(round(mean_dis8, 2)) + '\n' + 'Player_2M :   ' + str(round(mean_dis2, 2))
plt.text(0.5, 12.5, mess, bbox={'facecolor': '#74C476',
                                'edgecolor': 'b',
                                'alpha': 0.5,
                                'pad': 8,
                                })
plt.xlim((0, 22))
plt.ylim((0, 14))
plt.show()
print(1)

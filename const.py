# UUID
CORE_INDICATE_UUID = ('72c90005-57a9-4d40-b746-534e22ec9f9e')
CORE_NOTIFY_UUID = ('72c90003-57a9-4d40-b746-534e22ec9f9e')
CORE_WRITE_UUID = ('72c90004-57a9-4d40-b746-534e22ec9f9e')

# INDEX & ID
MESSAGE_TYPE_INDEX = 0
EVENT_TYPE_INDEX = 1
STATE_INDEX = 2
MESSAGE_TYPE_ID = 1
EVENT_TYPE_ID = 0

INPUT_NUM = [2, 1, 3, 1, 1]     # それぞれのセンサの状態が格納されているインデックス
INPUT_PRINT = [['','Single Pressed.', 'Long Pressed.', 'Double Pressed.'],
              ['Tap Event Detected', 'Shake Event Detected', 'Flip Event Detected', 'Orientation Event Detected'],
              ['Activating', 'Someone was detected', 'Nobody was Detected'],
              ['Value Changed'],
              ['Value of Temperature Sensor Was Changed']]
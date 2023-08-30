from bleak import BleakClient, BleakScanner
from struct import pack
import asyncio
import const
import csv

class Mesh:
    device_num = 0

# Notifyを有効化 ---------------------------------------
def on_receive_notify(sender, data: bytearray):
    if data[const.MESSAGE_TYPE_INDEX] != const.MESSAGE_TYPE_ID and data[const.EVENT_TYPE_INDEX] != const.EVENT_TYPE_ID:
        return
    else:
        num = data[const.INPUT_NUM[Mesh.device_num]]
        print(const.INPUT_PRINT[Mesh.device_num][num])
        # print('[notify] ', int(str(data[6]), 16))
        return

# Indicateを有効化 ---------------------------------------
def on_receive_indicate(sender, data: bytearray):
    data = bytes(data)
    print('[indicate] ',data)
    try: print(f'[Battery Level] {data[10]*10}%')
    except: pass

# 非同期で送信 --------------------------------------------
async def send_command(client: BleakClient, format: str, contents: list, duration: int):
    
    command = pack(format, *contents)
    checksum = 0
    for x in command:
        checksum += x
    command = command + pack('B', checksum & 0xFF) # チェックサムをバイト配列に追加
    print('command ',command)
    
    try:
        # Write command
        await client.write_gatt_char(const.CORE_WRITE_UUID, command, response=True)
    except Exception as e:
        print('error', e)
        return
    
    await asyncio.sleep(duration / 1000)
    

# スキャン -------------------------------------------------
async def scan(prefix='MESH-100'):
    while True:
        print(f'scanning {prefix}')
        try: return next(d for d in await BleakScanner.discover() if d.name and d.name.startswith(prefix))
        except StopIteration: continue

# csvファイルから読み込み ------------------------------------
def read_csv(file_name):
    data: list = []
    with open(file_name, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader: data.append(row)
    return data


# メイン ---------------------------------------------------
async def main():
    # csvファイルから読み込み
    csv_data: list = read_csv('mesh-allocation.csv')

    # ブロックをスキャン
    device = await scan(csv_data[Mesh.device_num][1])
    print('found', device.name, device.address)

    # スキャンで見つかったブロックと接続します。キャラクタリスティックの Notify と Indicate を有効化
    # その後、ブロック機能の有効化
    async with BleakClient(device, timeout=None) as client:
        # 初期化
        await client.start_notify(const.CORE_NOTIFY_UUID, on_receive_notify)
        await client.start_notify(const.CORE_INDICATE_UUID, on_receive_indicate)
        await client.write_gatt_char(const.CORE_WRITE_UUID, pack('<BBBB', 0, 2, 1, 3), response=True)
        print('connected')

        # button & move
        if(Mesh.device_num == 0 or Mesh.device_num == 1):
            await asyncio.sleep(30)

        else:
            time = 30 * 1000
            format: str = ''
            contents: list = []

            # motion
            if(Mesh.device_num == 2):
                format = '<BBBBHH'
                contents = [1, 0, 1, 1, 750, 500]

            # brightness
            elif(Mesh.device_num == 3):
                mode = 12   # 4: proximity(近接センサ), 8: ambient light(環境光センサ)
                format = '<BBBBBB'
                contents = [1, 0, 1, 0, 2, mode]
            
            # temperature
            elif(Mesh.device_num == 4):
                mode = 4    # 4: temperature(温度センサ), 8: humidity(湿度センサ)
                format = '<BBBHHHHBBB'
                contents = [1, 0, 1, 40, 10, 100, 50, 0, 0, mode]

            # LED
            elif(Mesh.device_num == 5):
                time = 5 * 1000

                messagetype = 1
                red = 2
                green = 8
                blue = 32
                duration = 5 * 1000 # [ms]
                on = 1 * 1000 # [ms]
                off = 500 # [ms]
                pattern = 1 # 1:点滅する, 2:ふわっと光る

                format = '<BBBBBBBHHHB'
                contents = [messagetype, 0, red, 0, green, 0, blue, duration, on, off, pattern]

            await send_command(client, format, contents, time)
            
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
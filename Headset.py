import sys
import time

from cortex2 import EmotivCortex2Client

# Headset Data
_USER = 'ahmad11'  # TODO: update
if _USER.lower() == 'felix':
    _CLIENT_ID = 'XaV809JWyQJtIzYKSS8VzCQdlKsh7jLpxs1qePL6'
    _CLIENT_SECRET = '97edNd8wo7AeoEJ7S64oLqnadcMKSVVNDB8kZWHVsHI2VHWbq93A1NHbM5IVE70SjH1L3NKJlfcPtSJA9gOVNe1brMtgK2jpltKlAJ7VdjrACqyOuiUD55SdGLtGu5aV'
    _PROFILE_NAME = 'profile1'
elif _USER.lower() == 'ahmad11':
    _CLIENT_ID = 'C8Ug1hGFiTlGlezJijYZhrhWH8wsFREdVW0iU0dr'
    _CLIENT_SECRET = 'SYeM47wmrMaTzsTCnw5Aad4DopCCJ7b4Xels24exFiLXc1GmiL1S7p4bk0f5C7aHHvnid4y1sR507rKnGd2OyFSxaoFR1B6yPxKcKIGF1WMywZcdiltdNgLZYKdVMxOV'
    _PROFILE_NAME = 'Traning07'

_URL = "wss://localhost:6868"

_COMMAND_POWER_THRESHOLD = 0.3


class Headset:
    def __init__(self):
        # Remember to start the Emotiv App before you start!
        # Start client with authentication
        self._client = EmotivCortex2Client(_URL,
                                           client_id=_CLIENT_ID,
                                           client_secret=_CLIENT_SECRET,
                                           check_response=True,
                                           authenticate=True,
                                           debug=False)

        # Test API connection by using the request access method
        self._client.request_access()

        # Explicit call to Authenticate (approve and get Cortex Token)
        self._client.authenticate()

        # Connect to headset, connect to the first one found, and start a session for it
        # client.query_headsets()
        headsets = str(self._client.query_headsets())
        print('Detected Headsets: ' + headsets)
        if headsets == '[]':
            print('No Headset present!')
            self.is_present = False
            return
        self.is_present = True

        self._client.connect_headset(0)
        self.session = self._client.create_session(0)
        print('session response: ' + str(self.session))

        # Subscribe to the motion and mental command streams
        # Spins up a separate subscription thread
        # client.subscribe(streams=["mot", "com"])
        sub_res = self._client.subscribe(streams=["com"])
        print('subscription response: ' + str(sub_res))

        # Test message handling speed
        a = self._client.subscriber_messages_handled
        time.sleep(5)
        b = self._client.subscriber_messages_handled
        print('Message handling speed: ' + str((b - a) / 5))

        print('profiles: ' + str(self._client.query_profiles()))
        self._client.load_profile(_PROFILE_NAME)
        print('loaded profile: ' + str(self._client.get_current_profile()))

        # Grab a single instance of data
        print('Single instance of data: ' + str(self._client.receive_data()))
        print('data: ' + str(self._client.data_streams))

        # debug output
        print('get_detection_info("mentalCommand"):\t' + str(self._client.get_detection_info('mentalCommand')))
        # print('setting level: ' + str(self.client.mental_command_action_level('set', level=1)))
        # print('get_mental_command_action_level:\t' + str(self.client.mental_command_action_level('get', PROFILE_NAME)))
        # self.client.data_deque_size = 1     # only store newest data sample. Only relevent when data read via data_streams
        # print('dequeue size: ' + str(self.client.data_deque_size))
        print('newest data: ' + str(self._client.data_streams))

    def get_commands(self, approach: str) -> (float, float, float):
        left, right, push = 0.0, 0.0, 0.0
        ex_msg = 'Progress before error:\n'
        t = time.time()

        try:
            # get command and it's power using the given approach
            if approach == "stream":
                # data_streams[0]['com'][0] entry looks like this: {'data': ['neutral', 0.0], 'time': 1605721182.8614}
                datas = self._client.data_streams
                ex_msg += '\tmanaged to get data_stream\n'
                print('data_streams: ' + str(datas))
                newest_command = list(datas.values())[0]['com'][0]     # sucks because it returns empty command dequeue for virtual headsets
                print('newest_command: ' + str(newest_command))
                ex_msg += '\talso managed to get newest_command\n'
                com, pow = newest_command['data']
                ex_msg += '\talso managed to unpack com and pow from newest_command["data"]\n'
                t_data = newest_command['time']
                ex_msg += '\talso managed to extract time from newest_command["time"]\n'
            elif approach == "receive":
                # receive_data()'s response looks like this: {'com': ['left', 0.7], 'sid': 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx', 'time': 1605738564.002}
                data = self._client.receive_data()     # also sucks because it does not reliably get the newest command
                ex_msg += '\tmanaged to call receive_data()\n'
                com, pow = data['com']
                ex_msg += '\talso managed to unpack com and pow from data\n'
                t_data = data['time']
                ex_msg += '\talso managed to extract time from data\n'
            else:
                raise ValueError
            # output result for debugging purposes
            print('received command: {} {}\tit took {}ms.'.format(str(com), str(pow), str(int((time.time() - t) * 1000))), end=' ')
            print('It is {}ms old'.format(str(int((time.time() - t_data) * 1000))))

            if pow >= _COMMAND_POWER_THRESHOLD:
                if com == 'left':
                    left = pow
                elif com == 'right':
                    right = pow
                elif com == 'push':
                    push = pow
                else:
                    print('not implemented command received!')
        except:
            print('failed to get new headset data sample')
            print(f'exception: {sys.exc_info()[0]}')
            print(ex_msg)
            pass

        print(f'left power: \t{left}\nright power: \t{right}\npush power: \t{push}\n')
        return left, right, push

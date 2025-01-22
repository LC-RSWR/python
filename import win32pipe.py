import win32pipe
import win32file
import pywintypes

def create_named_pipe():
    pipe_name = r'\\.\pipe\TreatmentPlanGeneratePdf_pipe_name'
    pipe = win32pipe.CreateNamedPipe(
        pipe_name,
        win32pipe.PIPE_ACCESS_DUPLEX,
        win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_READMODE_MESSAGE | win32pipe.PIPE_WAIT,
        win32pipe.PIPE_UNLIMITED_INSTANCES,
        65536,
        65536,
        0,
        None
    )
    return pipe

def start_server():
    pipe = create_named_pipe()
    win32pipe.ConnectNamedPipe(pipe, None)
    while True:
        data = read_from_pipe(pipe)
        print(f'Received data: {data}')
        if data == 'exit':
            break
    win32file.CloseHandle(pipe)

def read_from_pipe(pipe):
    buffer_size = 1024
    data = win32file.ReadFile(pipe, buffer_size)[1].decode('utf-8')
    return data

start_server()


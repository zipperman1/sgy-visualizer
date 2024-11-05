import argparse
import numpy as np
import matplotlib.pyplot as plt


TEXT_HEADER_SIZE = 3200
BINARY_HEADER_SIZE = 400
TRACE_SIZE = 240

DATA_FORMATS = {1: "4-byte IBM floating-point",
                2: "4-byte, two's complement integer",
                3: "2-byte, two's complement integer",
                4: "4-byte fixed-point with gain (obsolete)",
                5: "4-byte IEEE floating-point",
                8: "1-byte, two's complement integer"}

TRACE_SORTING_CODES = {-1: "Other",
                      0: "Unknown",
                      1: "As recorded",
                      2: "CDP ensemble",
                      3: "Single fold continuous profile",
                      4: "Horizontally stacked",
                      5: "Common source point",
                      6: "Common reciever point",
                      7: "Common offset point",
                      8: "Common mid-point",
                      9: "Common conversion point"}

parser = argparse.ArgumentParser()
parser.add_argument('-i', dest='file_path', required=True)

args = parser.parse_args()

with open(args.file_path, "rb") as f:
    # Text Header
    text_header = f.read(TEXT_HEADER_SIZE)
    print("Textual File Header:\n", text_header.decode("ascii"))
    
    # Binary Header
    binary_header_current = f.read(4)
    print("Job identification number: ", int.from_bytes(binary_header_current, byteorder="big"))
    
    binary_header_current = f.read(4)
    print("Line number: ", int.from_bytes(binary_header_current, byteorder="big"))
    
    binary_header_current = f.read(4)
    print("Reel number: ", int.from_bytes(binary_header_current, byteorder="big"))
    
    binary_header_current = f.read(2)
    num_traces = int.from_bytes(binary_header_current, byteorder="big")
    print("Number of data traces per ensemble: ", num_traces)
    
    binary_header_current = f.read(2)
    print("Number of auxiliary traces per ensemble: ", int.from_bytes(binary_header_current, byteorder="big"))
    
    binary_header_current = f.read(2)
    print("Sample interval in microseconds (μs): ", int.from_bytes(binary_header_current, byteorder="big"))
    
    binary_header_current = f.read(2)
    print("Sample interval in microseconds (μs) of original field recording: ", int.from_bytes(binary_header_current, byteorder="big"))
    
    binary_header_current = f.read(2)
    samples_num = int.from_bytes(binary_header_current, byteorder="big")
    print("Number of samples per data trace: ", samples_num)
    
    binary_header_current = f.read(2)
    print("Number of samples per data trace for original field recording: ", int.from_bytes(binary_header_current, byteorder="big"))
    
    binary_header_current = f.read(2)
    data_format = int.from_bytes(binary_header_current, byteorder="big")
    print("Data sample format code: ", DATA_FORMATS[data_format])
    
    binary_header_current = f.read(2)
    print("The expected number of data traces per trace ensemble: ", int.from_bytes(binary_header_current, byteorder="big"))
    
    binary_header_current = f.read(2)
    trace_sorting_code = int.from_bytes(binary_header_current, byteorder="big")
    print("Trace sorting code: ", TRACE_SORTING_CODES[trace_sorting_code])
    
    binary_header_current = f.read(2)
    print("Vertical sum code: ", int.from_bytes(binary_header_current, byteorder="big"))
    
    binary_header_current = f.read(2)
    print("Sweep frequency at start (Hz): ", int.from_bytes(binary_header_current, byteorder="big"))
    
    binary_header_current = f.read(2)
    print("Sweep frequency at end (Hz): ", int.from_bytes(binary_header_current, byteorder="big"))
    
    binary_header_current = f.read(2)
    print("Sweep length (ms): ", int.from_bytes(binary_header_current, byteorder="big"))
    
    binary_header_current = f.read(2)
    print("Sweep type code: ", int.from_bytes(binary_header_current, byteorder="big"))
    
    binary_header_current = f.read(2)
    print("Trace number of sweep channel: ", int.from_bytes(binary_header_current, byteorder="big"))
    
    binary_header_current = f.read(2)
    print("Sweep trace taper length in milliseconds at start if tapered: ", int.from_bytes(binary_header_current, byteorder="big"))
    
    binary_header_current = f.read(2)
    print("Sweep trace taper length in milliseconds at end: ", int.from_bytes(binary_header_current, byteorder="big"))
    
    binary_header_current = f.read(2)
    print("Taper type: ", int.from_bytes(binary_header_current, byteorder="big"))
    
    binary_header_current = f.read(2)
    print("Correlated data traces: ", int.from_bytes(binary_header_current, byteorder="big"))
    
    binary_header_current = f.read(2)
    print("Binary gain recovered: ", int.from_bytes(binary_header_current, byteorder="big"))
    
    binary_header_current = f.read(2)
    print("Amplitude recovery method: ", int.from_bytes(binary_header_current, byteorder="big"))
    
    binary_header_current = f.read(2)
    print("Measurement system: ", int.from_bytes(binary_header_current, byteorder="big"))
    
    binary_header_current = f.read(2)
    print("Impulse signal polarity: ", int.from_bytes(binary_header_current, byteorder="big"))
    
    binary_header_current = f.read(2)
    print("Vibratory polarity code: ", int.from_bytes(binary_header_current, byteorder="big"))
    
    f.seek(240, 1)
    
    ver1, ver2 = f.read(1), f.read(1)
    print("SEG Y Format Revision Number:  ", int.from_bytes(ver1, byteorder="big"), ".", int.from_bytes(ver2, byteorder="big"), sep='')
    
    binary_header_current = f.read(2)
    print("Fixed length trace flag: ", int.from_bytes(binary_header_current, byteorder="big"))
    
    binary_header_current = f.read(2)
    print("The expected number of data traces per trace ensemble: ", int.from_bytes(binary_header_current, byteorder="big"))
    
    binary_header_current = f.read(2)
    print("The expected number of data traces per trace ensemble: ", int.from_bytes(binary_header_current, byteorder="big"))
    
    binary_header_current = f.read(2)
    print("The expected number of data traces per trace ensemble: ", int.from_bytes(binary_header_current, byteorder="big"))
    
    binary_header_current = f.read(2)
    optional_text_header_num = int.from_bytes(binary_header_current, byteorder="big")
    print("Number of 3200-byte, Extended Textual File Header records following the Binary Header: ", optional_text_header_num)
    
    # Traces
    f.seek(3840, 0)
    traces = bytearray()
    while (trace := f.read(4 * samples_num)):
        f.seek(240, 1)
        traces += trace
    
    dt = np.dtype(np.float32)
    dt = dt.newbyteorder('>')
    traces_array = np.frombuffer(traces, dtype=dt).reshape(num_traces, samples_num).T
    plt.imshow(traces_array)
    plt.show()
    
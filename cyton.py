import time
import math
import random
import argparse
import serial

START = 0xA0
END_C0 = 0xC0
END_C1 = 0xC1

def int24_to_bytes_le(v: int) -> bytes:
    # clamp signed 24-bit
    if v > 0x7FFFFF:
        v = 0x7FFFFF
    if v < -0x800000:
        v = -0x800000
    # two's complement for negative
    if v < 0:
        v = (1 << 24) + v
    # little-endian: LSB first (per OpenBCI_GUI InterfaceSerial.pde comment)
    return bytes([v & 0xFF, (v >> 8) & 0xFF, (v >> 16) & 0xFF])

def make_packet(sample_id: int, t: float, end_byte: int = END_C0) -> bytes:
    # 8 EEG channels, 24-bit signed counts (ADS1299 raw-ish)
    chans = []
    for ch in range(8):
        freq = 10.0 + 0.7 * ch
        phase = 0.4 * ch
        amp = 200_000
        noise = random.gauss(0, 2000)
        v = int(amp * math.sin(2 * math.pi * freq * t + phase) + noise)
        chans.append(v)

    aux6 = bytes([0, 0, 0, 0, 0, 0])  # 6 bytes (3 axes * int16), keep zero for now

    pkt = bytearray()
    pkt.append(START)
    pkt.append(sample_id & 0xFF)
    for v in chans:
        pkt.extend(int24_to_bytes_le(v))
    pkt.extend(aux6)
    pkt.append(end_byte)
    return bytes(pkt)  # 33 bytes

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", required=True, help="e.g. /dev/tnt0 or COM9")
    ap.add_argument("--baud", type=int, default=115200)
    ap.add_argument("--fs", type=float, default=250.0)
    ap.add_argument("--autostart", action="store_true")
    ap.add_argument("--endbyte", choices=["c0", "c1"], default="c0")
    args = ap.parse_args()

    endb = END_C0 if args.endbyte == "c0" else END_C1

    ser = serial.Serial(
        port=args.port,
        baudrate=args.baud,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        timeout=0.01,
        write_timeout=1.0,
    )

    streaming = args.autostart
    sample_id = 0
    t0 = time.perf_counter()
    next_time = time.perf_counter()

    print(f"Opened {args.port} @ {args.baud}, fs={args.fs}, end={args.endbyte}, autostart={args.autostart}")
    print("Commands understood: 'b' start streaming, 's' stop streaming")

    try:
        while True:
            cmd = ser.read(64)
            if cmd:
                for b in cmd:
                    if b == ord('b'):
                        streaming = True
                        print("START")
                    if b == ord('v'):
                        streaming = False
                        sample_id = 0
                        ser.write(b"OpenBCI V3 Simulator\n$$$")
                    elif b == ord('s'):
                        streaming = False
                        print("STOP")
                        
            if cmd:
              print(f"Received command: {cmd}")                        

            if not streaming:
                time.sleep(0.01)
                continue

            now = time.perf_counter()
            if now < next_time:
                time.sleep(next_time - now)

            t = time.perf_counter() - t0
            pkt = make_packet(sample_id, t, end_byte=endb)
            if len(pkt) != 33:
                raise RuntimeError(f"packet length != 33: {len(pkt)}")

            ser.write(pkt)
            sample_id = (sample_id + 1) & 0xFF
            next_time += 1.0 / args.fs

    except KeyboardInterrupt:
        pass
    finally:
        ser.close()

if __name__ == "__main__":
    main()
